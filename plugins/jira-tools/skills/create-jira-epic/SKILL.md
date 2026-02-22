---
name: create-jira-epic
version: 1.1.0
user-invocable: false
description: |
  Create a well-structured Jira Epic with consistent formatting optimized for both human readers and AI agents.
  Invoked internally by the /jira-create command. Handles clarifying questions, optional codebase investigation, and MCP-based ticket creation.
---

# Create Jira Epic

## Epic Description Format

Every epic MUST use this exact structure. Do not deviate.

```markdown
## Background
[1-3 paragraphs. Business context, strategic driver, or user need that motivates this body of work.]

## Goals
* [Concrete goal or outcome this epic aims to achieve]
* [Another goal]

## Acceptance Criteria
* [High-level, testable condition that signals the epic is complete]
* [Another condition]

## Additional Information / Links
* [Designs, documentation, dependencies, related tickets or initiatives, out-of-scope items]
```

### Rules

- **Background**: 1-3 paragraphs. Describe the business or product context. Reference specific systems or domains when it helps scope the work. Do not summarise the goals here -- that is what the Goals section is for. Use the extra paragraphs to give implementers enough context to make good decisions without having to read the codebase.
- **Goals**: 2-5 bullet points. Each goal describes an intended outcome, not a task ("Reduce p99 checkout latency below 300ms", not "Optimise checkout service"). If there is only one goal, use a single bullet.
- **Acceptance Criteria**: 2-6 high-level, testable conditions that signal the epic is complete. These are coarser than story-level criteria -- they describe the epic's delivered state, not individual story outcomes.
- **Additional Information / Links**: Include designs, documentation, dependencies, related tickets, and any out-of-scope items the user has mentioned. Never duplicate information already present in other Jira fields. Omit if empty.
- If any section lacks information, use AskUser to prompt the user rather than leaving placeholders.
- Clear, concise, professional tone throughout.
- **Always use Markdown formatting.** The MCP tools convert Markdown to ADF internally. Never use Jira wiki markup (`h2.`, `{{code}}`, `{code}`, `#` for numbered lists). Use `## Heading`, `` `code` ``, triple-backtick fenced code blocks, and `1.` for numbered lists.

### Summary Line

- Concise noun phrase or action phrase describing the body of work.
- Not a commit message -- no `feat:` prefix.
- Examples: "Checkout performance optimisation", "Migrate authentication service to OAuth 2.0"

## Workflow

### 1. Parse the Request

Extract from the user's message or the context passed from `/jira-create`:
- The strategic or product driver (for Background)
- Desired outcomes (for Goals)
- High-level completion conditions (for Acceptance Criteria)
- Parent initiative (if mentioned)
- Out-of-scope items (for Additional Information)
- Team preference (if mentioned)
- Any links or references

### 2. Ask Clarifying Questions

Use AskUser when genuinely ambiguous. Common questions:

- **Missing goals**: "What specific outcomes should this epic achieve?"
- **Scope ambiguity**: "This sounds like it spans multiple epics. Should we scope it down, or keep it broad?"
- **Missing parent**: "Should this epic live under a specific initiative, or stand alone?"
- **Vague criteria**: "How will we know this epic is done? What is the measurable outcome?"
- **Missing team**: "Which team should own this epic?" (only if team cannot be inferred from the parent -- see step 6)

Do NOT ask about format -- the format is fixed. Do NOT ask questions you can answer by investigating the codebase.

### 3. Investigate the Codebase

If codebase analysis was requested during `/jira-create`, always investigate:

- Search relevant source files, services, config, and architectural boundaries to understand current state.
- Use findings to write an accurate Background and Goals.
- Add relevant file paths, service names, or architecture notes to Additional Information if they would help the implementer.

### 4. Draft the Description

Write the description following the mandatory format. Before creating, review:

- Is Background 1-3 paragraphs focused on context and driver?
- Are Goals outcome-oriented, not task-oriented?
- Are Acceptance Criteria high-level and testable?
- Are out-of-scope items in Additional Information (not a separate section)?

### 5. Create the Ticket

Use `atlassian___createJiraIssue` via the `manage-jira` skill for API mechanics:

- `issueTypeName`: Always `"Epic"`
- `parent`: Set when the user provides a parent initiative
- `projectKey`: Derive from the parent ticket's project, or ask the user

### 6. Post-Creation Steps

After creating the ticket, follow any post-creation steps defined by the active project skill (e.g. `cars-project`). These may include setting required custom fields such as team. If no project skill is active, skip this step.

## What This Skill Does NOT Cover

- Other issue types (Initiative, Story, Bug) -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
- Sprint or other custom field assignment -- use `manage-jira` skill.
