#!/usr/bin/env python3
"""
Ralph Wiggum Loop Manager - Gold Tier Component
Initiates and manages autonomous Claude loops for multi-step tasks
"""

import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('RalphWiggum')


class RalphWiggumLoop:
    """
    Manages Ralph Wiggum autonomous loops
    Keeps Claude Code working until task is complete
    """

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.state_file = self.vault_path / '.ralph_wiggum_state.json'
        self.log_file = self.vault_path / 'Logs' / 'ralph_wiggum.log'
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def start_loop(
        self,
        prompt: str,
        task_file: str,
        completion_promise: Optional[str] = None,
        max_iterations: int = 10
    ) -> bool:
        """
        Start a Ralph Wiggum autonomous loop

        Args:
            prompt: The task prompt for Claude
            task_file: Path to task file (relative to vault)
            completion_promise: Optional promise string to detect completion
            max_iterations: Maximum iterations before giving up

        Returns:
            bool: True if loop started successfully
        """
        try:
            # Create state file
            state = {
                'task_file': task_file,
                'completion_promise': completion_promise or 'TASK_COMPLETE',
                'original_prompt': prompt,
                'current_iteration': 0,
                'max_iterations': max_iterations,
                'started_at': datetime.now().isoformat()
            }

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)

            logger.info(f"Ralph Wiggum loop started for: {task_file}")
            logger.info(f"Max iterations: {max_iterations}")

            # Log the start
            self._log(f"Loop started - Task: {task_file}, Max iterations: {max_iterations}")

            # Execute Claude Code with the prompt
            # The stop hook will manage the loop
            result = subprocess.run(
                ['claude', 'code'],
                input=prompt,
                text=True,
                capture_output=True
            )

            # Check if loop completed successfully
            if not self.state_file.exists():
                logger.info("Ralph Wiggum loop completed successfully")
                return True
            else:
                logger.warning("Ralph Wiggum loop may not have completed")
                return False

        except Exception as e:
            logger.error(f"Error starting Ralph Wiggum loop: {e}")
            return False

    def check_status(self) -> dict:
        """Check current loop status"""
        if not self.state_file.exists():
            return {'active': False, 'message': 'No active loop'}

        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)

            return {
                'active': True,
                'task_file': state.get('task_file'),
                'current_iteration': state.get('current_iteration'),
                'max_iterations': state.get('max_iterations'),
                'started_at': state.get('started_at')
            }

        except Exception as e:
            logger.error(f"Error reading loop status: {e}")
            return {'active': False, 'error': str(e)}

    def cancel_loop(self) -> bool:
        """Cancel current loop"""
        if self.state_file.exists():
            self.state_file.unlink()
            logger.info("Ralph Wiggum loop cancelled")
            self._log("Loop cancelled by user")
            return True
        return False

    def _log(self, message: str):
        """Log to ralph_wiggum.log"""
        try:
            timestamp = datetime.now().isoformat()
            with open(self.log_file, 'a') as f:
                f.write(f"{timestamp} - {message}\n")
        except Exception as e:
            logger.error(f"Error writing to log: {e}")


def main():
    """CLI interface for Ralph Wiggum loop manager"""
    import argparse

    parser = argparse.ArgumentParser(description='Ralph Wiggum Autonomous Loop Manager')
    parser.add_argument('command', choices=['start', 'status', 'cancel'],
                       help='Command to execute')
    parser.add_argument('--prompt', '-p', help='Task prompt for Claude')
    parser.add_argument('--task-file', '-f', help='Task file to monitor')
    parser.add_argument('--promise', help='Completion promise string')
    parser.add_argument('--max-iterations', '-i', type=int, default=10,
                       help='Maximum iterations (default: 10)')
    parser.add_argument('--vault-path', default='/mnt/e/all-d-files/Ai_Employee_Vault',
                       help='Vault path')

    args = parser.parse_args()

    loop = RalphWiggumLoop(args.vault_path)

    if args.command == 'start':
        if not args.prompt or not args.task_file:
            print("Error: --prompt and --task-file required for start command")
            return 1

        print(f"Starting Ralph Wiggum loop...")
        print(f"Task: {args.task_file}")
        print(f"Max iterations: {args.max_iterations}")

        success = loop.start_loop(
            prompt=args.prompt,
            task_file=args.task_file,
            completion_promise=args.promise,
            max_iterations=args.max_iterations
        )

        if success:
            print("Loop completed successfully!")
            return 0
        else:
            print("Loop did not complete successfully")
            return 1

    elif args.command == 'status':
        status = loop.check_status()
        print(json.dumps(status, indent=2))
        return 0

    elif args.command == 'cancel':
        if loop.cancel_loop():
            print("Loop cancelled")
            return 0
        else:
            print("No active loop to cancel")
            return 1


if __name__ == '__main__':
    exit(main())
