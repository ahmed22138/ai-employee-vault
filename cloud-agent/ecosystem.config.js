/**
 * PM2 Ecosystem Configuration - Platinum Tier Cloud Agent
 * Manages all cloud processes with auto-restart and monitoring
 */

module.exports = {
  apps: [
    {
      name: 'cloud-email-triage',
      script: 'cloud-agent/watchers/cloud_email_triage.py',
      interpreter: 'python3',
      cwd: '/opt/ai-employee-vault',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        VAULT_PATH: '/opt/ai-employee-vault',
        CLOUD_MODE: 'true',
        GMAIL_CHECK_INTERVAL: '120'
      },
      error_file: '/var/log/ai-employee/cloud-email-triage-error.log',
      out_file: '/var/log/ai-employee/cloud-email-triage-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true
    },
    {
      name: 'vault-sync',
      script: 'cloud-agent/vault_sync.py',
      interpreter: 'python3',
      cwd: '/opt/ai-employee-vault',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: {
        VAULT_PATH: '/opt/ai-employee-vault',
        CLOUD_MODE: 'true',
        SYNC_INTERVAL: '60'
      },
      error_file: '/var/log/ai-employee/vault-sync-error.log',
      out_file: '/var/log/ai-employee/vault-sync-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true
    },
    {
      name: 'health-monitor',
      script: 'cloud-agent/health_monitor.py',
      interpreter: 'python3',
      cwd: '/opt/ai-employee-vault',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        VAULT_PATH: '/opt/ai-employee-vault',
        CLOUD_MODE: 'true'
      },
      error_file: '/var/log/ai-employee/health-monitor-error.log',
      out_file: '/var/log/ai-employee/health-monitor-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true
    }
  ]
};
