# Weekly Business and Accounting Auditor Skill

**Purpose:** Automatically generate comprehensive weekly business and accounting audits with CEO briefing.

## When to Use This Skill

Use this skill to:
- Generate Monday morning CEO briefings
- Perform weekly business health checks
- Audit accounting data from Odoo
- Analyze completed tasks and productivity
- Review subscription costs and optimizations
- Generate actionable insights and recommendations

## Core Capabilities

1. **Financial Analysis** - Revenue, expenses, profit margins from Odoo
2. **Task Analysis** - Completed tasks, bottlenecks, time tracking
3. **Subscription Audit** - Cost analysis and optimization recommendations
4. **Goal Progress** - Track progress against Business_Goals.md
5. **Proactive Suggestions** - AI-generated recommendations
6. **Social Media Performance** - Engagement metrics from recent posts

## Workflow

### Step 1: Collect Data

Gather data from multiple sources:

1. **Odoo Accounting Data** (via Odoo MCP):
   - Get revenue summary for past week
   - Get expense summary for past week
   - Get outstanding invoices
   - Get account balances

2. **Task Completion Data**:
   - Read all files in /Done/ from past week
   - Count tasks by type and priority
   - Calculate average completion time

3. **Business Goals**:
   - Read Business_Goals.md
   - Extract current metrics and targets

4. **Social Media Performance**:
   - Read recent LinkedIn/Facebook/Twitter posts
   - Calculate engagement metrics
   - Identify top-performing content

5. **Subscription Data**:
   - Read Business_Goals.md subscription list
   - Flag subscriptions meeting audit criteria

### Step 2: Analyze Data

Perform comprehensive analysis:

1. **Financial Health**:
   ```
   - Total Revenue (week)
   - Total Expenses (week)
   - Net Profit
   - Profit Margin %
   - Outstanding Receivables
   - Cash Position
   ```

2. **Productivity Metrics**:
   ```
   - Tasks Completed
   - Average Time per Task
   - Task Completion Rate
   - Bottlenecks (tasks > 3 days)
   - Priority Distribution
   ```

3. **Goal Progress**:
   ```
   - Revenue vs Target
   - Monthly progress %
   - Quarterly projection
   - Goal achievement likelihood
   ```

4. **Cost Optimization**:
   ```
   - Subscription costs
   - Unused services
   - Cost per task/feature
   - Optimization opportunities
   ```

### Step 3: Generate Insights

Create AI-powered insights:

1. **Trend Analysis**:
   - Week-over-week comparisons
   - Identify positive and negative trends
   - Predict next week's performance

2. **Anomaly Detection**:
   - Unusual expenses
   - Revenue spikes or drops
   - Task completion anomalies

3. **Risk Identification**:
   - Overdue invoices
   - Budget overruns
   - Missed deadlines
   - Goal misalignment

4. **Opportunity Identification**:
   - Revenue expansion opportunities
   - Cost reduction opportunities
   - Productivity improvements
   - Automation candidates

### Step 4: Generate Briefing

Create formatted CEO briefing:

```markdown
# Weekly Business Audit & CEO Briefing

**Week of:** [Date Range]
**Generated:** [Timestamp]
**Status:** [Red/Yellow/Green Flag]

---

## Executive Summary

[2-3 sentence overview of week's performance]

**Key Highlights:**
- [Top achievement]
- [Major concern]
- [Critical action needed]

---

## Financial Performance

### Revenue
- **This Week:** $X,XXX
- **Target:** $X,XXX (XX% of target)
- **Last Week:** $X,XXX (X% change)

### Expenses
- **This Week:** $X,XXX
- **Breakdown:**
  - Software/Tools: $XXX
  - Services: $XXX
  - Other: $XXX

### Profitability
- **Net Profit:** $X,XXX
- **Profit Margin:** XX%
- **Runway:** X months (at current burn rate)

---

## Productivity Analysis

### Tasks Completed
- **Total:** X tasks
- **High Priority:** X
- **Medium Priority:** X
- **Low Priority:** X

### Performance Metrics
- **Average Completion Time:** X days
- **Completion Rate:** XX%
- **Bottlenecks:** X tasks > 3 days

### Top Achievements
1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

---

## Goal Progress

### Monthly Revenue Goal ($XX,XXX)
- **Current MTD:** $X,XXX (XX%)
- **Weekly Average:** $X,XXX
- **Projected End-of-Month:** $X,XXX
- **Status:** [On Track / Behind / Ahead]

### Other Goals
- [Goal 1]: XX% complete
- [Goal 2]: XX% complete

---

## Cost Optimization Opportunities

### Subscription Audit
[List subscriptions flagged for review]

1. **[Service Name]** - $XX/month
   - Issue: No login in XX days
   - Recommendation: Cancel and save $XX/month

2. **[Service Name]** - $XX/month
   - Issue: Duplicate functionality
   - Recommendation: Consolidate

**Potential Monthly Savings:** $XXX

---

## Social Media Performance

### This Week's Activity
- **Posts Published:** X
- **Total Engagement:** X (likes + comments + shares)
- **Avg Engagement per Post:** X
- **Best Performing:** [Post title/topic]

### Recommendations
- Post more about: [Topic]
- Best posting time: [Day/Time]
- Content format: [Type]

---

## Risks & Alerts

### 🔴 Critical Issues
- [Critical issue requiring immediate attention]

### 🟡 Warnings
- [Warning that needs attention this week]

### 🟢 Positive Trends
- [Positive trend to maintain/amplify]

---

## Proactive Recommendations

### This Week's Action Items
1. **[Action 1]** - [Rationale]
2. **[Action 2]** - [Rationale]
3. **[Action 3]** - [Rationale]

### Strategic Initiatives
- [Long-term recommendation]
- [Investment suggestion]
- [Process improvement]

---

## Next Week's Focus

**Priorities:**
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

**Deadlines:**
- [Upcoming deadline 1]
- [Upcoming deadline 2]

---

*Audit generated by AI Employee Weekly Auditor*
*Data sources: Odoo, Task Logs, Business Goals, Social Media*
```

### Step 5: Save and Notify

1. Save briefing to `/Briefings/YYYY-MM-DD_Weekly_Audit.md`
2. Update Dashboard.md with audit completion
3. Create notification in Needs_Action if critical issues found
4. Log audit completion to audit log

## Integration Points

### Odoo MCP Server
```
Use Odoo MCP to:
- get_revenue_summary (date_from, date_to)
- get_expense_summary (date_from, date_to)
- get_invoices (state='posted', limit=100)
- get_account_balances ()
```

### Social Media MCP Server
```
Use Social Media MCP to:
- generate_summary (platform='linkedin', limit=10)
- generate_summary (platform='facebook', limit=10)
- generate_summary (platform='twitter', limit=10)
```

### File System
```
Read from:
- /Done/*.md (past 7 days)
- Business_Goals.md
- /Logs/*.json (past 7 days)
```

## Scheduling

This skill should run automatically:
- **When:** Every Monday at 7:00 AM
- **Trigger:** Orchestrator scheduled task
- **Duration:** ~2-5 minutes

Manual trigger command:
```
Use the weekly-auditor skill to generate this week's business audit and CEO briefing
```

## Data Requirements

### Minimum Required:
- Business_Goals.md exists and is up to date
- At least one task in /Done/ folder
- Odoo MCP server configured (optional but recommended)

### Optimal:
- Odoo accounting data available
- Social media MCP configured
- Complete task history in /Done/
- Accurate subscription data in Business_Goals.md

## Error Handling

If data source unavailable:
- **Odoo offline**: Skip financial section, note in briefing
- **No tasks in Done/**: Note zero productivity, flag for review
- **Social media MCP offline**: Skip social section
- **Business Goals missing**: Create template and warn user

## Output Location

Briefing saved to:
```
/Briefings/YYYY-MM-DD_Weekly_Audit.md
```

## Security Considerations

1. **Financial Data**: Odoo credentials via environment variables only
2. **Sensitive Metrics**: Briefing may contain sensitive data - keep local
3. **Audit Log**: All audit runs logged with timestamp
4. **Data Privacy**: No external API calls except configured MCPs

## Example Prompts

### Basic Usage
```
Generate this week's business audit and CEO briefing
```

### Specific Date Range
```
Use the weekly-auditor skill to generate an audit for January 1-7, 2026
```

### Focus Area
```
Generate weekly audit with focus on financial performance and cost optimization
```

### Quick Summary
```
Create a quick weekly summary (skip detailed analysis)
```

## Metrics to Track

Log these metrics for each audit:
- Audit generation time
- Data sources accessed
- Issues detected (count by severity)
- Recommendations generated (count)
- User actions taken on previous recommendations

---

*This skill is part of the Gold Tier AI Employee system*
*Requires: Odoo MCP (optional), Social Media MCP (optional), Business_Goals.md, Task history*
