#!/bin/bash
#
# Ralph Wiggum Stop Hook - Gold Tier Component
# Keeps Claude working autonomously until task is complete
#
# This hook intercepts Claude Code's exit and checks if the task is complete.
# If not complete, it re-injects the prompt to continue working.
#

VAULT_PATH="${VAULT_PATH:-/mnt/e/all-d-files/Ai_Employee_Vault}"
LOOP_STATE_FILE="$VAULT_PATH/.ralph_wiggum_state.json"
MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-10}"

# Check if we're in a Ralph loop
if [ ! -f "$LOOP_STATE_FILE" ]; then
    # Not in a loop, allow normal exit
    exit 0
fi

# Read loop state
TASK_FILE=$(jq -r '.task_file' "$LOOP_STATE_FILE" 2>/dev/null)
COMPLETION_PROMISE=$(jq -r '.completion_promise' "$LOOP_STATE_FILE" 2>/dev/null)
CURRENT_ITERATION=$(jq -r '.current_iteration' "$LOOP_STATE_FILE" 2>/dev/null)
ORIGINAL_PROMPT=$(jq -r '.original_prompt' "$LOOP_STATE_FILE" 2>/dev/null)

# Validate state
if [ -z "$TASK_FILE" ] || [ "$TASK_FILE" = "null" ]; then
    echo "[Ralph Wiggum] Invalid state file, exiting loop"
    rm -f "$LOOP_STATE_FILE"
    exit 0
fi

# Check max iterations
if [ "$CURRENT_ITERATION" -ge "$MAX_ITERATIONS" ]; then
    echo "[Ralph Wiggum] Max iterations ($MAX_ITERATIONS) reached"
    echo "[Ralph Wiggum] Task may be incomplete. Manual intervention required."
    rm -f "$LOOP_STATE_FILE"
    exit 0
fi

# Strategy 1: Check for completion promise in output
if [ -n "$COMPLETION_PROMISE" ] && [ "$COMPLETION_PROMISE" != "null" ]; then
    # Check if Claude output contains the promise
    if grep -q "<promise>$COMPLETION_PROMISE</promise>" "$CLAUDE_OUTPUT" 2>/dev/null; then
        echo "[Ralph Wiggum] Completion promise found: $COMPLETION_PROMISE"
        echo "[Ralph Wiggum] Task complete after $CURRENT_ITERATION iterations"
        rm -f "$LOOP_STATE_FILE"
        exit 0
    fi
fi

# Strategy 2: Check if task file moved to Done/ folder (more reliable)
TASK_FILENAME=$(basename "$TASK_FILE")
DONE_PATH="$VAULT_PATH/Done/$TASK_FILENAME"

if [ -f "$DONE_PATH" ]; then
    echo "[Ralph Wiggum] Task file found in Done/ folder"
    echo "[Ralph Wiggum] Task complete after $CURRENT_ITERATION iterations"
    rm -f "$LOOP_STATE_FILE"
    exit 0
fi

# Task not complete - increment iteration and continue
NEXT_ITERATION=$((CURRENT_ITERATION + 1))

echo "[Ralph Wiggum] Task not complete (iteration $CURRENT_ITERATION/$MAX_ITERATIONS)"
echo "[Ralph Wiggum] Continuing autonomous loop..."

# Update state
jq ".current_iteration = $NEXT_ITERATION" "$LOOP_STATE_FILE" > "$LOOP_STATE_FILE.tmp"
mv "$LOOP_STATE_FILE.tmp" "$LOOP_STATE_FILE"

# Log iteration
echo "$(date -Iseconds) - Iteration $NEXT_ITERATION - Task: $TASK_FILE" >> "$VAULT_PATH/Logs/ralph_wiggum.log"

# Re-inject the prompt with context
CONTINUE_PROMPT="Continue working on the task. This is iteration $NEXT_ITERATION of $MAX_ITERATIONS.

Previous attempt did not complete the task. Review your previous output and continue.

Original task: $ORIGINAL_PROMPT

The task will be considered complete when the file is moved to the Done/ folder.

Continue working autonomously."

# Block the exit and re-run Claude with continuation prompt
echo "$CONTINUE_PROMPT"

# Exit with code 77 signals to Claude Code to continue with new prompt
exit 77
