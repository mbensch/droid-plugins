---
name: create-jira-bug
version: 1.0.0
description: |
  Create a well-structured Jira Bug with consistent formatting optimized for both human readers and AI agents.
  Use when the user asks to file a bug, report a defect, or log an issue they encountered.
  Handles clarifying questions, optional codebase investigation, and MCP-based ticket creation.
---

# Create Jira Bug

## Bug Description Format

Every bug MUST use this exact structure. Do not deviate.

```markdown
## Description
[One paragraph. What is broken and what is the impact. Short as possible.]

## Steps to Reproduce
1. [Step one]
2. [Step two]
3. [Observe: what happens vs what should happen]

## Additional Information / Links
* [Logs, screenshots, environment, related tickets]
```

### Rules

- **Description**: One paragraph. State what is broken and what the impact is. Reference specific systems, endpoints, or error messages when it helps the reader understand the problem without investigating.
- **Steps to Reproduce**: Numbered steps ending with an "Observe" step that contrasts actual vs expected behavior. If the bug is intermittent or environment-specific and steps cannot be provided, replace this section with **Observed Behavior** containing environment details, timestamps, and relevant log snippets.
- **Additional Information / Links**: Always include for bugs -- at minimum state the environment (prod/staging/dev). Add logs, screenshots, error messages, related tickets, or Datadog/Splunk links when available. Never duplicate information already present in other Jira fields (Reporter, assignee, parent, etc.).
- If any section lacks information, use AskUser to prompt the user rather than leaving placeholders.
- Clear, concise, diagnostic tone throughout.

### Summary Line

- Concise phrase describing the defect.
- Not a commit message -- no `fix:` prefix.
- Describe the symptom, not the fix: "GraphQL endpoint returns 500 on empty dealer ID" not "Add nil check for dealer ID".

## Workflow

### 1. Parse the Request

Extract from the user's message:
- What is broken (for Description)
- How to trigger it (for Steps to Reproduce)
- Environment, logs, screenshots (for Additional Information)
- Parent ticket / epic (if mentioned)
- Assignment preference

### 2. Ask Clarifying Questions

Use AskUser when genuinely ambiguous. Common questions:

- **Missing parent**: "Which epic or parent ticket should this bug live under?"
- **Unclear reproduction**: "Can you walk me through the exact steps to trigger this?"
- **Missing environment**: "Which environment did you observe this in -- prod, staging, or dev?"
- **Assignment**: "Should this be assigned to you or left unassigned?"

Do NOT ask about format -- the format is fixed. Do NOT ask questions you can answer by investigating the codebase.

### 3. Investigate the Codebase (When Applicable)

When the bug involves code in the current repo:

- Search relevant source files to understand the likely area of failure.
- Use findings to write an accurate Description paragraph.
- Add relevant file paths, error handlers, or config details to Additional Information if they would save the investigator discovery time.

Skip this step for bugs in external systems or a different repo.

### 4. Draft the Description

Write the description following the mandatory format. Before creating, review:

- Is Description one paragraph focused on the symptom and impact?
- Are Steps to Reproduce concrete and numbered?
- Does Additional Information include at least the environment?

### 5. Create the Ticket

Use `atlassian___createJiraIssue` via the `manage-jira` skill for API mechanics:

- `issueTypeName`: Always `"Bug"`
- `parent`: Set when provided by the user
- `assignee_account_id`: Set when the user requests assignment (look up from an existing ticket if needed)
- `projectKey`: Derive from the parent ticket's project, or ask the user

## What This Skill Does NOT Cover

- Other issue types (Story, Chore, Task, Epic) -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
- Sprint, team, or custom field assignment -- use `manage-jira` skill.
