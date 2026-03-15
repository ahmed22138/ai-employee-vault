# LinkedIn Poster Skill

**Purpose:** Automatically generate and post LinkedIn content about business activities to generate sales leads.

## When to Use This Skill

Use this skill when:
- User requests to post on LinkedIn
- Weekly business summary needs to be shared
- New product/service announcement
- Sharing accomplishments or milestones
- Generating sales leads through thought leadership

## Core Capabilities

1. **Content Generation** - Create engaging LinkedIn posts based on business activities
2. **Post Drafting** - Generate posts in /Plans/LinkedIn/ folder
3. **Approval Workflow** - All posts require human approval before posting
4. **Scheduling** - Queue posts for optimal posting times

## Workflow

### Step 1: Identify Content Opportunities

Monitor these sources for post-worthy content:
- Completed tasks in /Done/ folder (project milestones)
- Business metrics from Dashboard.md
- New client wins or successful deliveries
- Industry insights or lessons learned

### Step 2: Generate Post Draft

When content opportunity is identified:

1. Read Business_Goals.md to understand:
   - Target audience
   - Business value proposition
   - Key messaging themes

2. Create post draft in /Plans/LinkedIn/DRAFT_YYYY-MM-DD_topic.md with structure:
   ```markdown
   ---
   type: linkedin_post
   created: YYYY-MM-DDTHH:MM:SSZ
   status: draft
   target_audience: [executives|developers|business owners]
   goal: [awareness|leads|engagement]
   ---

   ## Post Content

   [Main post text - 1-3 short paragraphs]
   [Include hook, value, and call-to-action]

   ## Hashtags

   #hashtag1 #hashtag2 #hashtag3

   ## Image Suggestion

   [Description of image that would accompany post]
   ```

3. Follow LinkedIn best practices:
   - Start with attention-grabbing hook
   - Keep paragraphs short (1-2 sentences)
   - Include personal story or specific example
   - End with question or call-to-action
   - Use 3-5 relevant hashtags
   - Aim for 1,300-2,000 characters

### Step 3: Request Approval

1. Move draft to /Pending_Approval/LINKEDIN_POST_[topic]_[date].md
2. Update Dashboard with "LinkedIn post ready for review"
3. Wait for human to review and either:
   - Move to /Approved/ → Schedule for posting
   - Move to /Rejected/ → Archive
   - Edit and move to /Approved/ → Schedule edited version

### Step 4: Post to LinkedIn

**IMPORTANT:** This requires a LinkedIn MCP server or API integration.

For Bronze/Silver tier without API:
- Create final post text file in /Approved/
- User manually posts to LinkedIn
- Log activity in Logs/

For Gold+ tier with LinkedIn API:
- Use LinkedIn API to programmatically post
- Log activity with post URL
- Move to /Done/

## Content Types

### 1. Project Milestone Post
```
🎯 Just completed [project name] for [client/industry]

[Brief description of challenge]

Here's what made this project successful:
→ [Key insight 1]
→ [Key insight 2]
→ [Key insight 3]

[Lesson learned or takeaway]

[Question to audience]

#projectmanagement #[industry] #success
```

### 2. Weekly Wins Post
```
Week in review: 3 wins that matter

✅ [Accomplishment 1]
✅ [Accomplishment 2]
✅ [Accomplishment 3]

[Brief reflection on what enabled these wins]

What's your biggest win this week?

#productivity #business #growth
```

### 3. Value/Insight Post
```
[Contrarian or interesting statement]

After [X years/projects] in [industry], here's what I've learned:

[3-5 specific, actionable insights]

[Closing thought]

What's your experience been?

#[industry] #insights #[topic]
```

## Posting Schedule

Optimal LinkedIn posting times (based on engagement data):
- Tuesday-Thursday: 8-10 AM, 12 PM, 5-6 PM
- Avoid: Weekends, late nights, Monday mornings

Target frequency:
- Minimum: 1 post per week (every Monday morning)
- Optimal: 3 posts per week (Mon/Wed/Fri)
- Maximum: 1 post per day (avoid spam)

## Safety Rules

1. **Always Require Approval** - Never post to LinkedIn without explicit human approval
2. **No Controversial Topics** - Avoid politics, religion, or divisive subjects
3. **Professional Tone** - Maintain business-appropriate language
4. **Fact-Check** - Verify all claims and statistics before posting
5. **Privacy** - Never share client names without permission
6. **Authenticity** - Posts should reflect genuine experiences and insights

## Company Handbook Integration

Follow these rules from Company_Handbook.md:
- Get approval for all social media posts
- Maintain professional brand voice
- Protect client confidentiality
- Represent business values accurately

## Examples

### Good Post (Engaging, Value-Driven)
```
Most businesses fail at client communication.

Not because they're bad at their work.
But because they don't set clear expectations upfront.

Here's the simple framework I use:

1. Define success metrics before starting
2. Set weekly check-in cadence
3. Document decisions in writing
4. Over-communicate on blockers

Result? 100% client satisfaction rate this quarter.

What's your secret to great client relationships?

#clientsuccess #businesstips #communication
```

### Bad Post (Too Salesy, No Value)
```
🚨 SALE ALERT 🚨

Get 50% off our services this week only!

Limited time offer! DM me now!

#sale #discount #hireme
```

## Integration with Other Systems

- **Dashboard.md**: Check for accomplishments to post about
- **Done/ folder**: Find completed projects worth highlighting
- **Business_Goals.md**: Align posts with business objectives
- **Accounting/** folder: Share revenue milestones (if appropriate)

## Metrics to Track

Log these metrics in /Logs/ for each post:
- Post date and time
- Engagement (likes, comments, shares) - manual entry after 24-48 hours
- Lead inquiries generated
- Post topic/type
- Audience response sentiment

## Prompts to Use This Skill

- "Create a LinkedIn post about [topic]"
- "Draft a post celebrating [accomplishment]"
- "Generate this week's LinkedIn content"
- "What should I post on LinkedIn about [project]?"

## Technical Implementation

### Bronze/Silver Tier (Manual Posting)
1. Generate post drafts as markdown files
2. Request approval via file movement
3. User copies approved text and posts manually
4. Log activity

### Gold+ Tier (Automated Posting)
1. Integrate LinkedIn API via MCP server
2. Generate posts programmatically
3. Schedule posts using orchestrator
4. Auto-post after approval
5. Track engagement via API

---

*This skill is part of the Silver Tier AI Employee system*
*Requires: Business_Goals.md, Company_Handbook.md, HITL approval workflow*
