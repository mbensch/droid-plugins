---
name: create-jira-story
version: 1.1.0
description: |
  Create a well-structured Jira Story with consistent formatting optimized for both human readers and AI agents.
  Use when the user asks to create a Jira story, write a ticket, or capture work as a story.
  Handles clarifying questions, optional codebase investigation, and MCP-based ticket creation.
---

# Create Jira Story

## Story Description Format

Every story MUST use this exact structure. Do not deviate.

```markdown
## Background
[One paragraph. Context, business need, or user motivation. Short as possible.]

## Acceptance Criteria
* [Concrete, testable, outcome-oriented requirement]
* [Another requirement]

## Out of Scope
[Only if the user explicitly calls out exclusions. Omit this section entirely otherwise.]

## Additional Information / Links
* [Designs, documentation, dependencies, related tickets]
```

### Rules

- **Background**: One paragraph. Resist expanding. Reference specific systems, endpoints, or files only when it helps the reader understand scope without reading the codebase.
- **Acceptance Criteria**: 2-6 bullet points. Outcome-oriented ("Healthcheck requests no longer appear in application logs"), never implementation-oriented ("Add Plug.Logger with log level filter"). If you need more than 6, the story should be split.
- **Out of Scope**: Only present when the user explicitly provides exclusions. Never add this section speculatively.
- **Additional Information / Links**: Only include when there is genuinely useful context to link. Never duplicate information already present in other Jira fields (Reporter, Product Owner, assignee, parent, etc.). Omit if empty.
- If any section lacks information, use AskUser to prompt the user rather than leaving placeholders.
- Clear, concise, professional tone throughout.
- **Always use Markdown formatting.** The MCP tools convert Markdown to ADF internally. Never use Jira wiki markup (`h2.`, `{{code}}`, `{code}`, `#` for numbered lists). Use `## Heading`, `` `code` ``, triple-backtick fenced code blocks, and `1.` for numbered lists.

### Summary Line

- Concise action phrase describing the deliverable.
- Not a commit message -- no `feat:` / `fix:` prefix.
- Not a fragment like "add dialyzer" -- write "Add Dialyzer static analysis to CI pipeline".

## Workflow

### 1. Parse the Request

Extract from the user's message:
- The problem or need (for Background)
- Desired outcomes (for Acceptance Criteria)
- Parent ticket / epic (if mentioned)
- Explicit exclusions (for Out of Scope)
- Assignment preference
- Any links or references

### 2. Ask Clarifying Questions

Use AskUser when genuinely ambiguous. Common questions:

- **Missing parent**: "Which epic or parent ticket should this story live under?"
- **Scope ambiguity**: "This sounds like it could be multiple stories. Should we split it?"
- **Assignment**: "Should this be assigned to you or left unassigned?"
- **Vague criteria**: "Can you clarify what 'improved logging' means specifically? What should be logged?"

Do NOT ask about format -- the format is fixed. Do NOT ask questions you can answer by investigating the codebase.

### 3. Investigate the Codebase (When Applicable)

When the story involves technical changes in the current repo:

- Search relevant source files, config, router, endpoints to understand current state.
- Use findings to write an accurate Background paragraph.
- Add relevant file paths or technical details to Additional Information if they would save the implementer discovery time.

Skip this step for non-technical stories or stories targeting a different repo.

### 4. Draft the Description

Write the description following the mandatory format. Before creating, review:

- Is Background one paragraph?
- Are Acceptance Criteria testable outcomes?
- Is Out of Scope only present if the user said something is excluded?
- Is Additional Information free of field duplication?

### 5. Create the Ticket

Use `atlassian___createJiraIssue` via the `manage-jira` skill for API mechanics:

- `issueTypeName`: Always `"Story"`
- `parent`: Set when provided by the user
- `assignee_account_id`: Set when the user requests assignment (look up from an existing ticket if needed)
- `projectKey`: Derive from the parent ticket's project, or ask the user

## What This Skill Does NOT Cover

- Other issue types (Bug, Chore, Task, Epic) -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
- Sprint, team, or custom field assignment -- use `manage-jira` skill.
