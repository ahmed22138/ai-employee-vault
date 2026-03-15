#!/usr/bin/env python3
"""
Configuration Loader for AI Employee System

Loads environment variables from .env file and provides easy access.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for AI Employee system."""

    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration.

        Args:
            env_file: Path to .env file (default: .env)
        """
        self.vault_path = Path(__file__).parent
        self.env_file = self.vault_path / env_file
        self.config: Dict[str, Any] = {}

        # Load environment variables
        self.load_env()

    def load_env(self) -> None:
        """Load environment variables from .env file."""
        if not self.env_file.exists():
            logger.warning(f".env file not found at {self.env_file}")
            logger.warning("Using .env.example as template - please create .env file")

            # Try to load from .env.example if .env doesn't exist
            example_file = self.vault_path / ".env.example"
            if example_file.exists():
                logger.info("Loading defaults from .env.example")
                self._parse_env_file(example_file, use_defaults=True)
            return

        logger.info(f"Loading configuration from {self.env_file}")
        self._parse_env_file(self.env_file)

        # Also load from system environment (overrides .env)
        self._load_system_env()

    def _parse_env_file(self, file_path: Path, use_defaults: bool = False) -> None:
        """
        Parse .env file and load variables.

        Args:
            file_path: Path to env file
            use_defaults: If True, only load example values (not real credentials)
        """
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Skip example/placeholder values if not using defaults
                        if not use_defaults and ('your-' in value or 'example' in value.lower()):
                            logger.debug(f"Skipping placeholder value for {key}")
                            continue

                        # Set environment variable and store in config
                        os.environ[key] = value
                        self.config[key] = value

        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")

    def _load_system_env(self) -> None:
        """Load variables from system environment (overrides .env)."""
        # List of expected environment variables
        expected_vars = [
            'SMTP_USER', 'SMTP_PASSWORD', 'SMTP_HOST', 'SMTP_PORT',
            'ODOO_URL', 'ODOO_DB', 'ODOO_USERNAME', 'ODOO_PASSWORD',
            'FACEBOOK_PAGE_ACCESS_TOKEN', 'FACEBOOK_PAGE_ID',
            'INSTAGRAM_ACCOUNT_ID',
            'TWITTER_API_KEY', 'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_SECRET',
            'VAULT_PATH', 'DRY_RUN', 'BROWSER_HEADLESS'
        ]

        for var in expected_vars:
            value = os.getenv(var)
            if value:
                self.config[var] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key) or os.getenv(key) or default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get boolean configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Boolean value
        """
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get integer configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Integer value
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Invalid integer value for {key}: {value}, using default {default}")
            return default

    def validate(self) -> Dict[str, bool]:
        """
        Validate configuration and check required values.

        Returns:
            Dictionary with validation results for each tier
        """
        results = {
            'bronze': True,  # Bronze tier needs no credentials
            'silver': True,
            'gold': True
        }

        # Silver tier validation
        smtp_user = self.get('SMTP_USER')
        smtp_pass = self.get('SMTP_PASSWORD')

        if not smtp_user or not smtp_pass or 'your-' in smtp_user:
            logger.warning("⚠️  SMTP credentials not configured - Email sending won't work")
            results['silver'] = False

        # Check Gmail credentials file
        creds_path = self.vault_path / self.get('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        if not creds_path.exists():
            logger.warning("⚠️  Gmail credentials.json not found - Gmail watcher won't work")
            results['silver'] = False

        # Gold tier validation (optional services)
        odoo_url = self.get('ODOO_URL')
        if not odoo_url or 'your-' in odoo_url:
            logger.info("📝 Odoo not configured - will use dry run mode")

        fb_token = self.get('FACEBOOK_PAGE_ACCESS_TOKEN')
        if not fb_token or 'your-' in fb_token:
            logger.info("📝 Facebook not configured - will use dry run mode")

        twitter_key = self.get('TWITTER_API_KEY')
        if not twitter_key or 'your-' in twitter_key:
            logger.info("📝 Twitter not configured - will use dry run mode")

        return results

    def print_status(self) -> None:
        """Print configuration status."""
        print("\n" + "="*60)
        print("AI EMPLOYEE CONFIGURATION STATUS")
        print("="*60)

        validation = self.validate()

        print("\n🥉 BRONZE TIER:")
        print(f"   Status: {'✅ Ready' if validation['bronze'] else '❌ Not Ready'}")

        print("\n🥈 SILVER TIER:")
        print(f"   Status: {'✅ Ready' if validation['silver'] else '⚠️  Needs Configuration'}")
        print(f"   SMTP Email: {'✅' if self.get('SMTP_USER') and 'your-' not in self.get('SMTP_USER', '') else '❌'}")
        print(f"   Gmail Creds: {'✅' if (self.vault_path / 'credentials.json').exists() else '❌'}")

        print("\n🏆 GOLD TIER:")
        print(f"   Status: {'✅ Ready' if validation['gold'] else '⚠️  Needs Configuration'}")
        print(f"   WhatsApp: {'✅' if Path(self.get('WHATSAPP_SESSION_PATH', '~/.whatsapp_session')).expanduser().exists() else '📝 Need QR scan'}")
        print(f"   Odoo: {'✅' if self.get('ODOO_URL') and 'your-' not in self.get('ODOO_URL', '') else '📝 Optional'}")
        print(f"   Facebook: {'✅' if self.get('FACEBOOK_PAGE_ACCESS_TOKEN') and 'your-' not in self.get('FACEBOOK_PAGE_ACCESS_TOKEN', '') else '📝 Optional'}")
        print(f"   Twitter: {'✅' if self.get('TWITTER_API_KEY') and 'your-' not in self.get('TWITTER_API_KEY', '') else '📝 Optional'}")

        print("\n" + "="*60)

        # Recommendations
        if not validation['silver']:
            print("\n💡 NEXT STEPS:")
            print("   1. Copy .env.example to .env")
            print("   2. Edit .env with your credentials")
            print("   3. Run: python config_loader.py")

        print()


# Singleton instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get singleton configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


# Convenience functions
def get(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get configuration value."""
    return get_config().get(key, default)


def get_bool(key: str, default: bool = False) -> bool:
    """Get boolean configuration value."""
    return get_config().get_bool(key, default)


def get_int(key: str, default: int = 0) -> int:
    """Get integer configuration value."""
    return get_config().get_int(key, default)


if __name__ == "__main__":
    # When run directly, show configuration status
    config = Config()
    config.print_status()
