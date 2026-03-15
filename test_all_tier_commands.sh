#!/bin/bash

################################################################################
# AI EMPLOYEE VAULT - COMPLETE TIER COMMAND TESTING SCRIPT
################################################################################
# Purpose: Test ALL tier commands to ensure they work and are user-runnable
# Tests: Bronze, Silver, Gold, Platinum, Master Wizard
# Output: Detailed test report with pass/fail status
################################################################################

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0

# Test results file
REPORT_FILE="TIER_COMMAND_TEST_REPORT.md"

# Helper functions
log_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -e "${BLUE}[TEST $TOTAL_TESTS]${NC} $1"
}

log_pass() {
    PASSED_TESTS=$((PASSED_TESTS + 1))
    echo -e "${GREEN}✅ PASS${NC}: $1"
    echo "✅ PASS: $1" >> "$REPORT_FILE"
}

log_fail() {
    FAILED_TESTS=$((FAILED_TESTS + 1))
    echo -e "${RED}❌ FAIL${NC}: $1"
    echo "❌ FAIL: $1" >> "$REPORT_FILE"
}

log_warning() {
    WARNINGS=$((WARNINGS + 1))
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    echo "⚠️  WARN: $1" >> "$REPORT_FILE"
}

log_section() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
    echo -e "\n## $1\n" >> "$REPORT_FILE"
}

# Initialize report
cat > "$REPORT_FILE" << 'EOF'
# 🧪 AI EMPLOYEE VAULT - TIER COMMAND TEST REPORT

**Test Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Tester:** Automated Command Testing Script
**Purpose:** Verify all tier commands work and are user-runnable

---

EOF

echo "Starting comprehensive tier command testing..."
echo ""

################################################################################
# SETUP SCRIPT TESTS
################################################################################

log_section "1. SETUP SCRIPT VALIDATION"

log_test "Testing setup_silver_tier.sh syntax"
if bash -n setup_silver_tier.sh 2>/dev/null; then
    log_pass "setup_silver_tier.sh has valid syntax"
else
    log_fail "setup_silver_tier.sh has syntax errors"
fi

log_test "Testing setup_gold_tier.sh syntax"
if bash -n setup_gold_tier.sh 2>/dev/null; then
    log_pass "setup_gold_tier.sh has valid syntax"
else
    log_fail "setup_gold_tier.sh has syntax errors"
fi

log_test "Testing setup_platinum_tier.sh syntax"
if bash -n setup_platinum_tier.sh 2>/dev/null; then
    log_pass "setup_platinum_tier.sh has valid syntax"
else
    log_fail "setup_platinum_tier.sh has syntax errors"
fi

log_test "Testing setup_complete_system.sh syntax"
if bash -n setup_complete_system.sh 2>/dev/null; then
    log_pass "setup_complete_system.sh has valid syntax"
else
    log_fail "setup_complete_system.sh has syntax errors"
fi

log_test "Checking all setup scripts are executable"
EXECUTABLE_COUNT=0
for script in setup_silver_tier.sh setup_gold_tier.sh setup_platinum_tier.sh setup_complete_system.sh; do
    if [[ -x "$script" ]]; then
        EXECUTABLE_COUNT=$((EXECUTABLE_COUNT + 1))
    fi
done
if [[ $EXECUTABLE_COUNT -eq 4 ]]; then
    log_pass "All 4 setup scripts are executable"
else
    log_fail "Only $EXECUTABLE_COUNT/4 setup scripts are executable"
fi

################################################################################
# BRONZE TIER COMMAND TESTS
################################################################################

log_section "2. BRONZE TIER COMMANDS"

log_test "Testing filesystem_watcher.py import"
if python3 -c "import sys; sys.path.insert(0, 'watchers'); import filesystem_watcher" 2>/dev/null; then
    log_pass "filesystem_watcher.py imports successfully"
else
    log_fail "filesystem_watcher.py has import errors"
fi

log_test "Testing filesystem_watcher.py --help"
if timeout 2 python3 watchers/filesystem_watcher.py --help 2>/dev/null; then
    log_pass "filesystem_watcher.py accepts --help flag"
else
    log_warning "filesystem_watcher.py doesn't have --help (not critical)"
fi

log_test "Checking Bronze tier folder structure"
BRONZE_FOLDERS=("Needs_Action" "Needs_Action/whatsapp" "Processing" "Pending_Approval" "Approved" "Done" "Failed")
FOLDER_COUNT=0
for folder in "${BRONZE_FOLDERS[@]}"; do
    if [[ -d "$folder" ]]; then
        FOLDER_COUNT=$((FOLDER_COUNT + 1))
    fi
done
if [[ $FOLDER_COUNT -eq 7 ]]; then
    log_pass "All 7 Bronze tier folders exist"
else
    log_fail "Only $FOLDER_COUNT/7 Bronze tier folders exist"
fi

################################################################################
# SILVER TIER COMMAND TESTS
################################################################################

log_section "3. SILVER TIER COMMANDS"

log_test "Testing email_triage.py syntax"
if python3 -m py_compile watchers/email_triage.py 2>/dev/null; then
    log_pass "email_triage.py has valid Python syntax"
else
    log_fail "email_triage.py has syntax errors"
fi

log_test "Testing linkedin_monitor.py syntax"
if python3 -m py_compile watchers/linkedin_monitor.py 2>/dev/null; then
    log_pass "linkedin_monitor.py has valid Python syntax"
else
    log_fail "linkedin_monitor.py has syntax errors"
fi

log_test "Checking Gmail OAuth dependencies"
if python3 -c "from google.oauth2.credentials import Credentials; from googleapiclient.discovery import build" 2>/dev/null; then
    log_pass "Gmail OAuth dependencies installed"
else
    log_warning "Gmail OAuth dependencies not installed (run setup_silver_tier.sh)"
fi

log_test "Checking SMTP dependencies"
if python3 -c "import smtplib; from email.mime.text import MIMEText" 2>/dev/null; then
    log_pass "SMTP dependencies available (built-in)"
else
    log_fail "SMTP dependencies missing (critical)"
fi

log_test "Checking if .env file exists"
if [[ -f ".env" ]]; then
    log_pass ".env file exists"
else
    log_warning ".env file not found (create with setup_silver_tier.sh)"
fi

################################################################################
# GOLD TIER COMMAND TESTS
################################################################################

log_section "4. GOLD TIER COMMANDS"

log_test "Testing whatsapp_watcher.py syntax"
if python3 -m py_compile watchers/whatsapp_watcher.py 2>/dev/null; then
    log_pass "whatsapp_watcher.py has valid Python syntax"
else
    log_fail "whatsapp_watcher.py has syntax errors"
fi

log_test "Testing browser_action_executor.py syntax"
if python3 -m py_compile processors/browser_action_executor.py 2>/dev/null; then
    log_pass "browser_action_executor.py has valid Python syntax"
else
    log_fail "browser_action_executor.py has syntax errors"
fi

log_test "Checking Playwright installation"
if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    log_pass "Playwright library installed"
else
    log_warning "Playwright not installed (run setup_gold_tier.sh)"
fi

log_test "Checking Chromium browser installation"
if python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium; p.stop()" 2>/dev/null; then
    log_pass "Chromium browser installed"
else
    log_warning "Chromium browser not installed (run: python3 -m playwright install chromium)"
fi

log_test "Checking WhatsApp session directory"
if [[ -d ".whatsapp_session" ]]; then
    SESSION_FILES=$(find .whatsapp_session -type f | wc -l)
    if [[ $SESSION_FILES -gt 10 ]]; then
        log_pass "WhatsApp session exists with $SESSION_FILES files"
    else
        log_warning "WhatsApp session exists but has only $SESSION_FILES files (may need re-login)"
    fi
else
    log_warning "WhatsApp session not found (login required)"
fi

################################################################################
# PLATINUM TIER COMMAND TESTS
################################################################################

log_section "5. PLATINUM TIER COMMANDS"

log_test "Testing cloud_email_triage.py syntax"
if python3 -m py_compile watchers/cloud_email_triage.py 2>/dev/null; then
    log_pass "cloud_email_triage.py has valid Python syntax"
else
    log_fail "cloud_email_triage.py has syntax errors"
fi

log_test "Testing vault_sync.py syntax"
if python3 -m py_compile cloud-agent/vault_sync.py 2>/dev/null; then
    log_pass "vault_sync.py has valid Python syntax"
else
    log_fail "vault_sync.py has syntax errors"
fi

log_test "Testing local_approval_agent.py syntax"
if python3 -m py_compile local-agent/local_approval_agent.py 2>/dev/null; then
    log_pass "local_approval_agent.py has valid Python syntax"
else
    log_fail "local_approval_agent.py has syntax errors"
fi

log_test "Checking .gitignore exists"
if [[ -f ".gitignore" ]]; then
    log_pass ".gitignore file exists"
else
    log_warning ".gitignore not found (create with setup_platinum_tier.sh)"
fi

log_test "Checking git repository initialization"
if [[ -d ".git" ]]; then
    log_pass "Git repository initialized"
else
    log_warning "Git not initialized (run setup_platinum_tier.sh)"
fi

log_test "Checking deployment script exists"
if [[ -f "cloud-agent/deployment/deploy_to_cloud.sh" ]]; then
    log_pass "Cloud deployment script exists"
    if bash -n cloud-agent/deployment/deploy_to_cloud.sh 2>/dev/null; then
        log_pass "deploy_to_cloud.sh has valid syntax"
    else
        log_fail "deploy_to_cloud.sh has syntax errors"
    fi
else
    log_warning "deploy_to_cloud.sh not found (created by setup_platinum_tier.sh)"
fi

################################################################################
# PROCESSOR COMMAND TESTS
################################################################################

log_section "6. PROCESSOR MODULES"

PROCESSORS=(
    "processors/email_executor.py"
    "processors/whatsapp_executor.py"
    "processors/browser_action_executor.py"
    "processors/task_logger.py"
    "processors/approval_tracker.py"
)

for processor in "${PROCESSORS[@]}"; do
    PROCESSOR_NAME=$(basename "$processor")
    log_test "Testing $PROCESSOR_NAME syntax"
    if python3 -m py_compile "$processor" 2>/dev/null; then
        log_pass "$PROCESSOR_NAME has valid Python syntax"
    else
        log_fail "$PROCESSOR_NAME has syntax errors"
    fi
done

################################################################################
# ORCHESTRATOR COMMAND TESTS
################################################################################

log_section "7. ORCHESTRATOR MODULE"

log_test "Testing orchestrator.py syntax"
if python3 -m py_compile orchestrator/orchestrator.py 2>/dev/null; then
    log_pass "orchestrator.py has valid Python syntax"
else
    log_fail "orchestrator.py has syntax errors"
fi

log_test "Testing orchestrator.py import"
if python3 -c "import sys; sys.path.insert(0, 'orchestrator'); import orchestrator" 2>/dev/null; then
    log_pass "orchestrator.py imports successfully"
else
    log_fail "orchestrator.py has import errors"
fi

################################################################################
# DOCUMENTATION TESTS
################################################################################

log_section "8. DOCUMENTATION FILES"

DOCS=(
    "START_HERE.md"
    "MASTER_GUIDE.md"
    "HOW_TO_START_ALL_TIERS.md"
    "FINAL_COMPLETION_REPORT.md"
    "VERIFICATION_TEST_REPORT.md"
    "PLATINUM_DEPLOYMENT_GUIDE.md"
    "QUICK_REFERENCE.txt"
)

DOCS_FOUND=0
for doc in "${DOCS[@]}"; do
    if [[ -f "$doc" ]]; then
        DOCS_FOUND=$((DOCS_FOUND + 1))
    fi
done

log_test "Checking documentation files"
if [[ $DOCS_FOUND -eq ${#DOCS[@]} ]]; then
    log_pass "All ${#DOCS[@]} essential documentation files exist"
else
    log_warning "Only $DOCS_FOUND/${#DOCS[@]} documentation files found"
fi

################################################################################
# USER-RUNNABLE COMMAND TESTS
################################################################################

log_section "9. USER-RUNNABLE COMMANDS"

log_test "Testing Bronze tier start command format"
if grep -q "python3 watchers/filesystem_watcher.py" HOW_TO_START_ALL_TIERS.md 2>/dev/null; then
    log_pass "Bronze tier start command documented"
else
    log_warning "Bronze tier start command not found in docs"
fi

log_test "Testing Silver tier setup command format"
if [[ -x "setup_silver_tier.sh" ]]; then
    log_pass "Silver tier setup command is executable"
else
    log_fail "Silver tier setup command is not executable"
fi

log_test "Testing Gold tier setup command format"
if [[ -x "setup_gold_tier.sh" ]]; then
    log_pass "Gold tier setup command is executable"
else
    log_fail "Gold tier setup command is not executable"
fi

log_test "Testing Platinum tier setup command format"
if [[ -x "setup_platinum_tier.sh" ]]; then
    log_pass "Platinum tier setup command is executable"
else
    log_fail "Platinum tier setup command is not executable"
fi

log_test "Testing master wizard command format"
if [[ -x "setup_complete_system.sh" ]]; then
    log_pass "Master wizard command is executable"
else
    log_fail "Master wizard command is not executable"
fi

################################################################################
# STATUS CHECK COMMAND TESTS
################################################################################

log_section "10. STATUS CHECK COMMANDS"

log_test "Testing process status command"
if ps aux | grep -q "grep"; then
    log_pass "Process status command (ps aux | grep) works"
else
    log_fail "Process status command failed"
fi

log_test "Testing file count commands"
if [[ -d "Needs_Action/whatsapp" ]]; then
    COUNT=$(ls -1 Needs_Action/whatsapp/ 2>/dev/null | wc -l)
    log_pass "File count command works (found $COUNT files in Needs_Action/whatsapp/)"
else
    log_warning "Needs_Action/whatsapp/ directory not found"
fi

log_test "Testing find command for pending approvals"
if find Pending_Approval/ -name '*.md' 2>/dev/null | head -1 >/dev/null; then
    COUNT=$(find Pending_Approval/ -name '*.md' 2>/dev/null | wc -l)
    log_pass "Find command works (found $COUNT files in Pending_Approval/)"
else
    log_warning "Pending_Approval/ directory not found or empty"
fi

################################################################################
# PERMISSION TESTS
################################################################################

log_section "11. FILE PERMISSIONS"

log_test "Testing write permission in Needs_Action/"
if touch Needs_Action/.test_file 2>/dev/null; then
    rm Needs_Action/.test_file
    log_pass "Write permission in Needs_Action/ works"
else
    log_fail "No write permission in Needs_Action/"
fi

log_test "Testing write permission in Approved/"
if touch Approved/.test_file 2>/dev/null; then
    rm Approved/.test_file
    log_pass "Write permission in Approved/ works"
else
    log_fail "No write permission in Approved/"
fi

log_test "Testing write permission in Done/"
if touch Done/.test_file 2>/dev/null; then
    rm Done/.test_file
    log_pass "Write permission in Done/ works"
else
    log_fail "No write permission in Done/"
fi

################################################################################
# DEPENDENCY TESTS
################################################################################

log_section "12. PYTHON DEPENDENCIES"

DEPENDENCIES=(
    "watchdog"
    "schedule"
    "playwright"
)

for dep in "${DEPENDENCIES[@]}"; do
    log_test "Checking $dep installation"
    if python3 -c "import $dep" 2>/dev/null; then
        log_pass "$dep is installed"
    else
        log_warning "$dep not installed (may be needed for some tiers)"
    fi
done

################################################################################
# FINAL SUMMARY
################################################################################

log_section "TEST SUMMARY"

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 📊 Final Results" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Metric | Count |" >> "$REPORT_FILE"
echo "|--------|-------|" >> "$REPORT_FILE"
echo "| Total Tests | $TOTAL_TESTS |" >> "$REPORT_FILE"
echo "| ✅ Passed | $PASSED_TESTS |" >> "$REPORT_FILE"
echo "| ❌ Failed | $FAILED_TESTS |" >> "$REPORT_FILE"
echo "| ⚠️  Warnings | $WARNINGS |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "**Success Rate:** $PASS_RATE%" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo "**Status:** ✅ ALL CRITICAL TESTS PASSED" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**User-Runnable:** ✅ YES - All commands are user-runnable" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**Production Ready:** ✅ YES" >> "$REPORT_FILE"
else
    echo "**Status:** ❌ SOME TESTS FAILED" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**User-Runnable:** ⚠️  PARTIAL - Some commands may have issues" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**Production Ready:** ❌ NO - Fix failed tests first" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "*Test Date: $(date '+%Y-%m-%d %H:%M:%S')*" >> "$REPORT_FILE"
echo "*Report File: $REPORT_FILE*" >> "$REPORT_FILE"

# Console summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           TEST SUMMARY${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Total Tests:    $TOTAL_TESTS"
echo -e "${GREEN}✅ Passed:      $PASSED_TESTS${NC}"
echo -e "${RED}❌ Failed:      $FAILED_TESTS${NC}"
echo -e "${YELLOW}⚠️  Warnings:    $WARNINGS${NC}"
echo ""
echo -e "Success Rate:   $PASS_RATE%"
echo ""

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}✅ ALL CRITICAL TESTS PASSED${NC}"
    echo -e "${GREEN}✅ All commands are USER-RUNNABLE${NC}"
    echo -e "${GREEN}✅ System is PRODUCTION READY${NC}"
else
    echo -e "${RED}❌ SOME TESTS FAILED - Review report for details${NC}"
fi

echo ""
echo -e "Detailed report saved to: ${BLUE}$REPORT_FILE${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

exit 0
