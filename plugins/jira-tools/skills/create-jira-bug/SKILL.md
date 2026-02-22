---
name: create-jira-bug
version: 1.3.0
user-invocable: false
description: |
  Create a well-structured Jira Bug with consistent formatting optimized for both human readers and AI agents.
  Invoked internally by the /jira-create command. Handles clarifying questions, optional codebase investigation, and MCP-based ticket creation.
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
- **Always use Markdown formatting.** The MCP tools convert Markdown to ADF internally. Never use Jira wiki markup (`h2.`, `{{code}}`, `{code}`, `#` for numbered lists). Use `## Heading`, `` `code` ``, triple-backtick fenced code blocks, and `1.` for numbered lists.

### Summary Line

- Concise phrase describing the defect.
- Not a commit message -- no `fix:` prefix.
- Describe the symptom, not the fix: "GraphQL endpoint returns 500 on empty input" not "Add nil check for input parameter".

## Workflow

### 1. Parse the Request

Extract from the user's message:
- What is broken (for Description)
- How to trigger it (for Steps to Reproduce)
- Environment, logs, screenshots (for Additional Information)
- Parent ticket / epic (if mentioned)
- Assignment preference
- Team preference (if mentioned)

### 2. Ask Clarifying Questions

Use AskUser when genuinely ambiguous. Common questions:

- **Missing parent**: "Which epic or parent ticket should this bug live under?"
- **Unclear reproduction**: "Can you walk me through the exact steps to trigger this?"
- **Missing environment**: "Which environment did you observe this in -- prod, staging, or dev?"
- **Assignment**: "Should this be assigned to you or left unassigned?"
- **Missing team**: "Which team should own this bug?" (only if team cannot be inferred from the parent -- see step 6)

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

### 6. Set Team

Every ticket **must** have a team assigned to appear on the board. Follow the team assignment instructions from the active project skill (e.g. `cars-project`), which contains the correct custom field ID and team UUID resolution steps for the current org.

If no project skill is active:
1. **If a parent ticket was provided**, fetch it with `atlassian___getJiraIssue` and check if it has a team field set.
   - If yes, use **AskUser** to offer using the parent's team or specifying a different one.
   - If no, ask the user which team should own this bug.
2. **If no parent was provided**, ask the user which team should own this bug.
3. Set the team via `atlassian___editJiraIssue` using the field ID and value format appropriate for the org (see `manage-jira` skill for discovery steps).

## What This Skill Does NOT Cover

- Other issue types (Story, Chore, Task, Epic) -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
- Sprint or other custom field assignment -- use `manage-jira` skill.
