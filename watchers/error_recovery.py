#!/usr/bin/env python3
"""
Error Recovery System - Gold Tier Component
Provides error recovery and graceful degradation for AI Employee system
"""

import os
import json
import logging
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ErrorRecovery')


class ErrorRecoverySystem:
    """
    Manages error recovery and graceful degradation
    Monitors watchers, restarts failed processes, and maintains system health
    """

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.state_file = self.vault_path / '.error_recovery_state.json'
        self.error_log = self.vault_path / 'Logs' / 'error_recovery.log'
        self.error_log.parent.mkdir(parents=True, exist_ok=True)

        # Recovery configuration
        self.max_retries = 3
        self.backoff_base = 2  # Exponential backoff base (seconds)
        self.max_backoff = 300  # Max 5 minutes backoff

        # Process definitions
        self.processes = {
            'filesystem_watcher': {
                'command': 'python3 watchers/filesystem_watcher.py',
                'critical': True,
                'restart_on_failure': True
            },
            'gmail_watcher': {
                'command': 'python3 watchers/gmail_watcher.py',
                'critical': True,
                'restart_on_failure': True
            },
            'whatsapp_watcher': {
                'command': 'python3 watchers/whatsapp_watcher.py',
                'critical': False,
                'restart_on_failure': True
            },
            'orchestrator': {
                'command': 'python3 watchers/orchestrator.py',
                'critical': True,
                'restart_on_failure': True
            }
        }

        # Load or initialize state
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load error recovery state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Initialize state
        return {
            'process_failures': {},
            'last_health_check': None,
            'degraded_services': [],
            'error_count': 0
        }

    def _save_state(self):
        """Save error recovery state"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _log_error(self, message: str, severity='ERROR'):
        """Log error to error recovery log"""
        try:
            timestamp = datetime.now().isoformat()
            with open(self.error_log, 'a') as f:
                f.write(f"{timestamp} [{severity}] {message}\n")
        except Exception as e:
            logger.error(f"Failed to write error log: {e}")

    def exponential_backoff(self, retry_count: int) -> int:
        """Calculate exponential backoff delay"""
        delay = min(self.backoff_base ** retry_count, self.max_backoff)
        return delay

    def with_retry(self, max_retries=None):
        """Decorator for automatic retry with exponential backoff"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = max_retries or self.max_retries

                for attempt in range(retries):
                    try:
                        return func(*args, **kwargs)

                    except Exception as e:
                        if attempt < retries - 1:
                            delay = self.exponential_backoff(attempt)
                            logger.warning(
                                f"{func.__name__} failed (attempt {attempt + 1}/{retries}): {e}. "
                                f"Retrying in {delay}s..."
                            )
                            time.sleep(delay)
                        else:
                            logger.error(f"{func.__name__} failed after {retries} attempts: {e}")
                            raise

            return wrapper
        return decorator

    def check_process_health(self, process_name: str) -> bool:
        """Check if a process is running"""
        try:
            # Check via ps command
            result = subprocess.run(
                ['pgrep', '-f', process_name],
                capture_output=True,
                text=True
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to check process health for {process_name}: {e}")
            return False

    def restart_process(self, process_name: str) -> bool:
        """Restart a failed process"""
        try:
            process_config = self.processes.get(process_name)

            if not process_config:
                logger.error(f"Unknown process: {process_name}")
                return False

            logger.info(f"Restarting process: {process_name}")

            # Start process in background
            subprocess.Popen(
                process_config['command'].split(),
                cwd=str(self.vault_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Wait a bit and check if it started
            time.sleep(2)

            if self.check_process_health(process_name):
                logger.info(f"Process {process_name} restarted successfully")
                self._log_error(f"Process {process_name} restarted", 'INFO')

                # Reset failure count
                if process_name in self.state['process_failures']:
                    del self.state['process_failures'][process_name]
                self._save_state()

                return True
            else:
                logger.error(f"Process {process_name} failed to start")
                return False

        except Exception as e:
            logger.error(f"Failed to restart {process_name}: {e}")
            self._log_error(f"Failed to restart {process_name}: {e}")
            return False

    def handle_process_failure(self, process_name: str):
        """Handle a process failure"""
        process_config = self.processes.get(process_name)

        if not process_config:
            return

        # Track failure
        if process_name not in self.state['process_failures']:
            self.state['process_failures'][process_name] = {
                'count': 0,
                'first_failure': datetime.now().isoformat(),
                'last_failure': None
            }

        self.state['process_failures'][process_name]['count'] += 1
        self.state['process_failures'][process_name]['last_failure'] = datetime.now().isoformat()
        self.state['error_count'] += 1

        failure_count = self.state['process_failures'][process_name]['count']

        logger.warning(f"Process {process_name} failed (failure #{failure_count})")
        self._log_error(f"Process {process_name} failed (#{failure_count})", 'WARNING')

        # Attempt restart if configured
        if process_config['restart_on_failure'] and failure_count <= self.max_retries:
            delay = self.exponential_backoff(failure_count - 1)
            logger.info(f"Waiting {delay}s before restart attempt...")
            time.sleep(delay)

            if self.restart_process(process_name):
                return

        # Graceful degradation for non-critical services
        if not process_config['critical']:
            logger.warning(f"{process_name} is degraded but system continues (non-critical service)")
            if process_name not in self.state['degraded_services']:
                self.state['degraded_services'].append(process_name)
        else:
            logger.error(f"CRITICAL: {process_name} has failed and is critical to system operation")
            self._log_error(f"CRITICAL: {process_name} failure", 'CRITICAL')

        self._save_state()

    def health_check(self) -> Dict:
        """Perform system health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': 'healthy',
            'processes': {},
            'degraded_services': self.state['degraded_services'],
            'total_errors': self.state['error_count']
        }

        # Check each process
        all_critical_healthy = True
        for process_name, config in self.processes.items():
            is_healthy = self.check_process_health(process_name)

            health_status['processes'][process_name] = {
                'status': 'running' if is_healthy else 'down',
                'critical': config['critical'],
                'failure_count': self.state['process_failures'].get(process_name, {}).get('count', 0)
            }

            if not is_healthy:
                if config['critical']:
                    all_critical_healthy = False
                    health_status['overall_health'] = 'critical'

                self.handle_process_failure(process_name)

        # Determine overall health
        if health_status['overall_health'] != 'critical':
            if len(self.state['degraded_services']) > 0:
                health_status['overall_health'] = 'degraded'
            else:
                health_status['overall_health'] = 'healthy'

        self.state['last_health_check'] = health_status['timestamp']
        self._save_state()

        return health_status

    def run_monitoring(self, interval=60):
        """Run continuous health monitoring"""
        logger.info("Error Recovery System started - monitoring system health")

        try:
            while True:
                logger.info("Running health check...")
                health = self.health_check()

                logger.info(f"System health: {health['overall_health'].upper()}")

                for process_name, status in health['processes'].items():
                    logger.info(f"  {process_name}: {status['status']}")

                if health['overall_health'] == 'critical':
                    logger.error("SYSTEM IN CRITICAL STATE - Manual intervention may be required")

                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Error Recovery System stopped by user")


def main():
    """Main entry point for error recovery system"""
    import argparse

    parser = argparse.ArgumentParser(description='Error Recovery System')
    parser.add_argument('--interval', type=int, default=60,
                       help='Health check interval in seconds (default: 60)')
    parser.add_argument('--vault-path', default='/mnt/e/all-d-files/Ai_Employee_Vault',
                       help='Vault path')

    args = parser.parse_args()

    system = ErrorRecoverySystem(args.vault_path)
    system.run_monitoring(interval=args.interval)


if __name__ == '__main__':
    main()
