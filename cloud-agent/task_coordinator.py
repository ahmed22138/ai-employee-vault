#!/usr/bin/env python3
"""
Task Coordinator - Platinum Tier
Implements claim-by-move rule to prevent double-work between agents
"""

import os
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskCoordinator:
    """
    Coordinates task ownership between Cloud and Local agents.

    **CLAIM-BY-MOVE RULE**:
    - First agent to move task from /Needs_Action to /In_Progress/<agent>/
      owns it
    - Other agents MUST ignore claimed tasks
    - If task in /In_Progress/cloud/, Local must not touch it
    - If task in /In_Progress/local/, Cloud must not touch it
    """

    def __init__(self, vault_path: str, agent_name: str):
        self.vault_path = Path(vault_path)
        self.agent_name = agent_name  # 'cloud' or 'local'

        # Folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.my_in_progress = self.in_progress / agent_name
        self.other_agent = 'local' if agent_name == 'cloud' else 'cloud'
        self.other_in_progress = self.in_progress / self.other_agent

        # Create folders
        for folder in [self.needs_action, self.my_in_progress, self.other_in_progress]:
            folder.mkdir(parents=True, exist_ok=True)

    def can_claim(self, task_path: Path) -> bool:
        """
        Check if this agent can claim a task.

        Returns True if:
        - Task is in /Needs_Action
        - Task is NOT already claimed by other agent
        """
        # If already in our In_Progress, we own it
        if str(task_path).startswith(str(self.my_in_progress)):
            return True

        # If in other agent's In_Progress, we can't touch it
        if str(task_path).startswith(str(self.other_in_progress)):
            logger.debug(f"⛔ Task claimed by {self.other_agent}: {task_path.name}")
            return False

        # If in Needs_Action, we can claim it
        if str(task_path).startswith(str(self.needs_action)):
            return True

        return False

    def claim_task(self, task_path: Path) -> Optional[Path]:
        """
        Claim a task by moving it to /In_Progress/<agent>/.

        Returns new path if successful, None if already claimed.
        """
        if not task_path.exists():
            logger.warning(f"⚠️  Task not found: {task_path}")
            return None

        # Check if we can claim
        if not self.can_claim(task_path):
            return None

        # Already in our In_Progress?
        if str(task_path).startswith(str(self.my_in_progress)):
            return task_path

        try:
            # Determine destination based on domain
            # e.g., Needs_Action/email/task.md -> In_Progress/cloud/email/task.md
            relative_path = task_path.relative_to(self.needs_action)
            dest_path = self.my_in_progress / relative_path

            # Create parent directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Atomic move (claim)
            shutil.move(str(task_path), str(dest_path))

            logger.info(f"✅ Claimed task: {task_path.name}")
            logger.info(f"   Moved to: {dest_path.relative_to(self.vault_path)}")

            return dest_path

        except FileNotFoundError:
            # Another agent claimed it first!
            logger.debug(f"⚠️  Task already claimed by {self.other_agent}: {task_path.name}")
            return None
        except Exception as e:
            logger.error(f"Error claiming task: {e}")
            return None

    def release_task(self, task_path: Path, destination: str = 'Done') -> bool:
        """
        Release a task (move to Done or other folder).

        Args:
            task_path: Current task path
            destination: Where to move ('Done', 'Pending_Approval', etc.)
        """
        try:
            dest_folder = self.vault_path / destination
            dest_folder.mkdir(parents=True, exist_ok=True)

            # Preserve relative path structure
            if str(task_path).startswith(str(self.my_in_progress)):
                relative_path = task_path.relative_to(self.my_in_progress)
            else:
                relative_path = task_path.name

            dest_path = dest_folder / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(task_path), str(dest_path))

            logger.info(f"✅ Released task to {destination}: {task_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error releasing task: {e}")
            return False

    def get_available_tasks(self, domain: Optional[str] = None) -> List[Path]:
        """
        Get tasks available for this agent to claim.

        Args:
            domain: Optional domain filter (e.g., 'email', 'social')

        Returns:
            List of task paths in /Needs_Action that can be claimed
        """
        tasks = []

        if domain:
            search_path = self.needs_action / domain
        else:
            search_path = self.needs_action

        if not search_path.exists():
            return tasks

        # Find all .md files
        for task_path in search_path.rglob('*.md'):
            if self.can_claim(task_path):
                tasks.append(task_path)

        return tasks

    def get_my_tasks(self) -> List[Path]:
        """Get tasks currently claimed by this agent"""
        if not self.my_in_progress.exists():
            return []

        return list(self.my_in_progress.rglob('*.md'))


class CloudTaskCoordinator(TaskCoordinator):
    """
    Cloud agent task coordinator.

    **CLOUD OWNERSHIP**:
    - Email triage (drafts only)
    - Social media post drafts
    - Research tasks
    - Data analysis
    """

    def __init__(self, vault_path: str):
        super().__init__(vault_path, 'cloud')

    def can_claim(self, task_path: Path) -> bool:
        """Cloud-specific claim rules"""
        if not super().can_claim(task_path):
            return False

        # Cloud can claim email and social tasks
        path_str = str(task_path)
        if '/email/' in path_str or '/social/' in path_str:
            return True

        # Cloud CANNOT claim payment or WhatsApp tasks (Local only)
        if '/payments/' in path_str or 'WHATSAPP' in task_path.name:
            logger.debug(f"⛔ {task_path.name} is LOCAL-only (payments/WhatsApp)")
            return False

        return True


class LocalTaskCoordinator(TaskCoordinator):
    """
    Local agent task coordinator.

    **LOCAL OWNERSHIP**:
    - All approvals (HITL)
    - Payments/banking
    - WhatsApp (has session)
    - Final send/post actions
    """

    def __init__(self, vault_path: str):
        super().__init__(vault_path, 'local')

    def can_claim(self, task_path: Path) -> bool:
        """Local-specific claim rules"""
        if not super().can_claim(task_path):
            return False

        # Local can claim ANY task (has all permissions)
        return True


def main():
    """Demo/test"""
    vault_path = os.getenv('VAULT_PATH', '/mnt/e/all-d-files/Ai_Employee_Vault')
    is_cloud = os.getenv('CLOUD_MODE', '') == 'true'

    if is_cloud:
        coordinator = CloudTaskCoordinator(vault_path)
        logger.info("🌩️  Cloud Task Coordinator initialized")
    else:
        coordinator = LocalTaskCoordinator(vault_path)
        logger.info("🏠 Local Task Coordinator initialized")

    # List available tasks
    tasks = coordinator.get_available_tasks()
    logger.info(f"Available tasks: {len(tasks)}")
    for task in tasks:
        logger.info(f"  - {task.name}")


if __name__ == '__main__':
    main()
