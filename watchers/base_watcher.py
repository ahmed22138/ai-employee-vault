"""
Base Watcher Template
All watchers inherit from this base class for consistent behavior.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """Base class for all watcher scripts."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self):
        """Set up logging for this watcher."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f'{self.__class__.__name__}_{datetime.now().strftime("%Y-%m-%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items that need processing.

        Returns:
            List of new items to process
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md file in Needs_Action folder for the item.

        Args:
            item: The item to create an action file for

        Returns:
            Path to the created file
        """
        pass

    def run(self):
        """Main loop - continuously check for updates."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring vault at: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()

                if items:
                    self.logger.info(f'Found {len(items)} new item(s) to process')

                for item in items:
                    try:
                        action_file = self.create_action_file(item)
                        self.logger.info(f'Created action file: {action_file.name}')
                    except Exception as e:
                        self.logger.error(f'Error creating action file: {e}', exc_info=True)

            except Exception as e:
                self.logger.error(f'Error in main loop: {e}', exc_info=True)

            time.sleep(self.check_interval)

    def update_dashboard(self, message: str):
        """
        Add an entry to the Dashboard.

        Args:
            message: The message to add to recent activity
        """
        dashboard_path = self.vault_path / 'Dashboard.md'

        try:
            if dashboard_path.exists():
                content = dashboard_path.read_text()

                # Find the Recent Activity section and add new entry
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                new_entry = f'- [{timestamp}] {message}\n'

                # Insert after "## Recent Activity"
                if '## Recent Activity' in content:
                    parts = content.split('## Recent Activity')
                    # Find the end of the Recent Activity section
                    after_header = parts[1].split('\n', 1)
                    updated_content = (
                        parts[0] +
                        '## Recent Activity\n' +
                        new_entry +
                        after_header[1] if len(after_header) > 1 else ''
                    )
                    dashboard_path.write_text(updated_content)
                    self.logger.debug(f'Updated dashboard with: {message}')
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')


if __name__ == '__main__':
    print('This is a base class. Please use a specific watcher implementation.')
