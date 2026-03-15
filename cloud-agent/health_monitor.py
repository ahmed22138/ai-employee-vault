#!/usr/bin/env python3
"""
Cloud Health Monitor - Platinum Tier
Monitors all cloud processes and restarts on failure
"""

import os
import sys
import time
import logging
import subprocess
import psutil
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthMonitor:
    """
    Monitors cloud agent health and auto-restarts failed processes.

    **MONITORING**:
    - Process health (PIDs)
    - Memory usage
    - Disk space
    - Network connectivity
    - Last sync time
    """

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.check_interval = 60  # Check every minute
        self.max_memory_percent = 80  # Alert if > 80% memory
        self.max_disk_percent = 90   # Alert if > 90% disk

        # Process tracking
        self.processes = {
            'email_triage': {
                'command': 'python3 cloud-agent/watchers/cloud_email_triage.py',
                'pid': None,
                'last_restart': None,
                'restart_count': 0
            },
            'vault_sync': {
                'command': 'python3 cloud-agent/vault_sync.py',
                'pid': None,
                'last_restart': None,
                'restart_count': 0
            }
        }

        # Health metrics
        self.health_log = self.vault_path / 'Logs' / 'health_monitor.log'
        self.health_log.parent.mkdir(parents=True, exist_ok=True)

    def is_process_running(self, process_name: str) -> bool:
        """Check if process is running"""
        process_info = self.processes.get(process_name)
        if not process_info:
            return False

        pid = process_info.get('pid')
        if not pid:
            return False

        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def start_process(self, process_name: str) -> bool:
        """Start a process"""
        process_info = self.processes.get(process_name)
        if not process_info:
            logger.error(f"❌ Unknown process: {process_name}")
            return False

        try:
            # Start process in background
            cmd = process_info['command'].split()
            process = subprocess.Popen(
                cmd,
                cwd=str(self.vault_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            process_info['pid'] = process.pid
            process_info['last_restart'] = datetime.now()
            process_info['restart_count'] += 1

            logger.info(f"✅ Started {process_name} (PID: {process.pid})")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start {process_name}: {e}")
            return False

    def restart_process(self, process_name: str) -> bool:
        """Restart a process"""
        logger.warning(f"🔄 Restarting {process_name}...")

        # Kill if still running
        process_info = self.processes.get(process_name)
        if process_info and process_info.get('pid'):
            try:
                process = psutil.Process(process_info['pid'])
                process.terminate()
                process.wait(timeout=5)
            except Exception:
                pass

        # Start fresh
        return self.start_process(process_name)

    def check_system_resources(self) -> Dict[str, any]:
        """Check system resource usage"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk
        disk = psutil.disk_usage(str(self.vault_path))
        disk_percent = disk.percent

        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'memory_available_gb': memory.available / (1024**3),
            'disk_available_gb': disk.free / (1024**3)
        }

    def check_network(self) -> bool:
        """Check network connectivity"""
        try:
            # Try to reach GitHub (where vault is hosted)
            response = requests.get('https://api.github.com', timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def check_vault_sync(self) -> bool:
        """Check if vault has synced recently"""
        try:
            # Check last git commit time
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ct'],
                cwd=str(self.vault_path),
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False

            last_commit_time = datetime.fromtimestamp(int(result.stdout.strip()))
            time_since_sync = datetime.now() - last_commit_time

            # Alert if no sync in 10 minutes
            return time_since_sync < timedelta(minutes=10)

        except Exception:
            return False

    def log_health_metrics(self, metrics: Dict):
        """Log health metrics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }

        # Append to log
        with open(self.health_log, 'a') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')

    def send_alert(self, alert_type: str, message: str):
        """Send alert (write to Updates folder for local agent)"""
        alert_file = self.vault_path / 'Updates' / f'ALERT_{alert_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        alert_content = f"""---
type: health_alert
severity: high
created_by: cloud_health_monitor
timestamp: {datetime.now().isoformat()}
---

## {alert_type.upper()} ALERT

{message}

**Action Required**: Review cloud agent health.

Check logs: `/Logs/health_monitor.log`
"""
        alert_file.write_text(alert_content)
        logger.warning(f"🚨 ALERT: {alert_type} - {message}")

    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info("🌩️  Cloud Health Monitor started")
        logger.info(f"   Check interval: {self.check_interval}s")

        while True:
            try:
                # Check all processes
                for process_name in self.processes.keys():
                    if not self.is_process_running(process_name):
                        logger.warning(f"⚠️  Process down: {process_name}")
                        self.restart_process(process_name)

                # Check system resources
                resources = self.check_system_resources()

                if resources['memory_percent'] > self.max_memory_percent:
                    self.send_alert('HIGH_MEMORY', f"Memory usage: {resources['memory_percent']:.1f}%")

                if resources['disk_percent'] > self.max_disk_percent:
                    self.send_alert('HIGH_DISK', f"Disk usage: {resources['disk_percent']:.1f}%")

                # Check network
                if not self.check_network():
                    logger.warning("⚠️  Network connectivity issues")
                    self.send_alert('NETWORK_DOWN', "Cannot reach GitHub")

                # Check vault sync
                if not self.check_vault_sync():
                    logger.warning("⚠️  Vault sync delayed")
                    self.send_alert('SYNC_DELAYED', "No vault sync in 10+ minutes")

                # Log metrics
                self.log_health_metrics(resources)

                # Status update
                logger.info(f"✅ Health check passed | CPU: {resources['cpu_percent']:.1f}% | "
                           f"MEM: {resources['memory_percent']:.1f}% | "
                           f"DISK: {resources['disk_percent']:.1f}%")

                # Wait for next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Health monitor stopped")
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(self.check_interval)


def main():
    """Main entry point"""
    logger.info("🌩️  Starting Cloud Health Monitor (Platinum Tier)")

    vault_path = os.getenv('VAULT_PATH', '/opt/ai-employee-vault')

    monitor = HealthMonitor(vault_path)
    monitor.monitor_loop()


if __name__ == '__main__':
    main()
