"""
File System Watcher
Monitors the Inbox folder for new files and creates action items.
"""

import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from base_watcher import BaseWatcher


class InboxFileHandler(FileSystemEventHandler):
    """Handler for file system events in the Inbox folder."""

    def __init__(self, watcher):
        self.watcher = watcher

    def on_created(self, event):
        """Called when a file is created in the monitored directory."""
        if event.is_directory:
            return

        source = Path(event.src_path)
        self.watcher.logger.info(f'New file detected: {source.name}')

        try:
            # Create action file
            self.watcher.process_new_file(source)
        except Exception as e:
            self.watcher.logger.error(f'Error processing file {source.name}: {e}', exc_info=True)


class FilesystemWatcher(BaseWatcher):
    """Watches the Inbox folder for new files."""

    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=5)  # 5 second check interval
        self.inbox = self.vault_path / 'Inbox'
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.processed_files = set()

        # Set up watchdog observer
        self.observer = Observer()
        self.event_handler = InboxFileHandler(self)

    def check_for_updates(self) -> list:
        """
        Check for new files in the Inbox folder.

        Returns:
            List of new file paths
        """
        new_files = []

        for file_path in self.inbox.iterdir():
            if file_path.is_file() and file_path not in self.processed_files:
                new_files.append(file_path)

        return new_files

    def process_new_file(self, file_path: Path):
        """
        Process a new file dropped in the Inbox.

        Args:
            file_path: Path to the new file
        """
        # Create action file
        action_file = self.create_action_file(file_path)

        # Mark as processed
        self.processed_files.add(file_path)

        # Update dashboard
        self.update_dashboard(f'New file detected: {file_path.name}')

        self.logger.info(f'Processed file: {file_path.name} -> {action_file.name}')

    def create_action_file(self, file_path: Path) -> Path:
        """
        Create an action file for the dropped file.

        Args:
            file_path: Path to the file

        Returns:
            Path to the created action file
        """
        # Get file metadata
        stats = file_path.stat()
        file_size = stats.st_size
        file_type = file_path.suffix
        created_time = datetime.fromtimestamp(stats.st_ctime).isoformat()

        # Create action file content
        content = f'''---
type: file_drop
source_file: {file_path.name}
file_type: {file_type}
file_size: {file_size} bytes
detected_at: {datetime.now().isoformat()}
created_at: {created_time}
status: pending
priority: medium
---

## New File Detected

A new file has been dropped in the Inbox folder and requires processing.

### File Details
- **Filename**: {file_path.name}
- **Type**: {file_type or "unknown"}
- **Size**: {file_size:,} bytes ({file_size / 1024:.2f} KB)
- **Created**: {created_time}

### Suggested Actions
- [ ] Review file contents
- [ ] Categorize file (document/image/data/other)
- [ ] Determine appropriate storage location
- [ ] Extract relevant metadata if applicable
- [ ] Move to appropriate folder or archive
- [ ] Update Dashboard with processing result

### Processing Notes
Add processing notes here when reviewing this file.

---
*Action created by: File System Watcher*
*Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
'''

        # Create action file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f'FILE_{timestamp}_{file_path.stem}.md'
        action_path = self.needs_action / action_filename

        action_path.write_text(content)

        return action_path

    def run_with_watchdog(self):
        """Run the watcher using watchdog for real-time monitoring."""
        self.logger.info('Starting File System Watcher with real-time monitoring')
        self.logger.info(f'Monitoring folder: {self.inbox}')

        # Schedule the observer
        self.observer.schedule(self.event_handler, str(self.inbox), recursive=False)
        self.observer.start()

        try:
            # Also check for any existing files
            existing_files = self.check_for_updates()
            if existing_files:
                self.logger.info(f'Found {len(existing_files)} existing file(s) in Inbox')
                for file_path in existing_files:
                    self.process_new_file(file_path)

            # Keep the watcher running
            import time
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info('Stopping File System Watcher...')
            self.observer.stop()

        self.observer.join()


def main():
    """Main entry point for the file system watcher."""
    import sys
    import os

    # Get vault path from environment or use current directory
    vault_path = os.getenv('VAULT_PATH', os.getcwd())

    print('=== File System Watcher ===')
    print(f'Vault Path: {vault_path}')
    print(f'Inbox Folder: {Path(vault_path) / "Inbox"}')
    print('Drop files into the Inbox folder to trigger processing.')
    print('Press Ctrl+C to stop.')
    print('=' * 40)

    watcher = FilesystemWatcher(vault_path)

    try:
        watcher.run_with_watchdog()
    except KeyboardInterrupt:
        print('\nWatcher stopped by user.')
        sys.exit(0)


if __name__ == '__main__':
    main()
