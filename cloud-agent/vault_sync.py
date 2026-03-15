#!/usr/bin/env python3
"""
Vault Sync System - Platinum Tier
Syncs vault between Cloud and Local using Git
SECURITY: Only syncs markdown/state, NEVER secrets
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VaultSync:
    """
    Git-based vault synchronization.

    SECURITY RULES:
    - .env files NEVER synced (.gitignore)
    - credentials.json NEVER synced
    - WhatsApp sessions NEVER synced
    - Only markdown files and state
    """

    def __init__(self, vault_path: str, sync_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.sync_interval = sync_interval
        self.is_cloud = os.getenv('CLOUD_MODE', '') == 'true'

        # Verify git repo
        if not (self.vault_path / '.git').exists():
            logger.error(f"❌ {vault_path} is not a git repository!")
            raise ValueError("Vault must be a git repository")

        # Verify .gitignore protects secrets
        self._verify_gitignore()

    def _verify_gitignore(self):
        """Ensure .gitignore protects sensitive files"""
        gitignore_path = self.vault_path / '.gitignore'

        if not gitignore_path.exists():
            logger.error("❌ .gitignore not found!")
            raise ValueError(".gitignore required for security")

        gitignore_content = gitignore_path.read_text()

        required_patterns = [
            '.env',
            'credentials.json',
            'token.json',
            '.whatsapp_session'
        ]

        for pattern in required_patterns:
            if pattern not in gitignore_content:
                logger.error(f"❌ .gitignore missing: {pattern}")
                raise ValueError(f"Security risk: {pattern} not ignored")

        logger.info("✅ .gitignore verified - secrets protected")

    def pull(self) -> bool:
        """Pull changes from remote"""
        try:
            os.chdir(self.vault_path)

            # Stash any local changes first
            subprocess.run(['git', 'stash'], capture_output=True)

            # Pull from remote
            result = subprocess.run(
                ['git', 'pull', '--rebase'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info("📥 Pulled changes from remote")
                return True
            else:
                logger.warning(f"⚠️  Pull failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error during pull: {e}")
            return False

    def push(self) -> bool:
        """Push local changes to remote"""
        try:
            os.chdir(self.vault_path)

            # Check for changes
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True
            )

            if not status_result.stdout.strip():
                # No changes
                return True

            # Add markdown files only
            subprocess.run(['git', 'add', '*.md'], capture_output=True)
            subprocess.run(['git', 'add', 'Needs_Action/'], capture_output=True)
            subprocess.run(['git', 'add', 'Plans/'], capture_output=True)
            subprocess.run(['git', 'add', 'Pending_Approval/'], capture_output=True)
            subprocess.run(['git', 'add', 'Approved/'], capture_output=True)
            subprocess.run(['git', 'add', 'Done/'], capture_output=True)
            subprocess.run(['git', 'add', 'Updates/'], capture_output=True)

            # Commit
            agent_name = 'cloud-agent' if self.is_cloud else 'local-agent'
            commit_msg = f"[{agent_name}] Sync at {datetime.now().isoformat()}"

            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                capture_output=True,
                text=True
            )

            if commit_result.returncode != 0 and 'nothing to commit' not in commit_result.stdout:
                logger.warning(f"⚠️  Commit failed: {commit_result.stderr}")
                return False

            # Push
            push_result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True
            )

            if push_result.returncode == 0:
                logger.info("📤 Pushed changes to remote")
                return True
            else:
                logger.warning(f"⚠️  Push failed: {push_result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error during push: {e}")
            return False

    def sync_loop(self):
        """Continuous sync loop"""
        agent_name = '🌩️  CLOUD' if self.is_cloud else '🏠 LOCAL'
        logger.info(f"{agent_name} Vault Sync started")
        logger.info(f"   Sync interval: {self.sync_interval}s")
        logger.info(f"   Vault path: {self.vault_path}")

        while True:
            try:
                # Pull first (get remote changes)
                self.pull()

                # Small delay
                time.sleep(2)

                # Push our changes
                self.push()

                # Wait for next sync
                time.sleep(self.sync_interval)

            except KeyboardInterrupt:
                logger.info("Vault sync stopped")
                break
            except Exception as e:
                logger.error(f"Sync error: {e}")
                time.sleep(self.sync_interval)


def main():
    """Main entry point"""
    vault_path = os.getenv('VAULT_PATH', '/opt/ai-employee-vault')
    sync_interval = int(os.getenv('SYNC_INTERVAL', '60'))

    syncer = VaultSync(vault_path, sync_interval)
    syncer.sync_loop()


if __name__ == '__main__':
    main()
