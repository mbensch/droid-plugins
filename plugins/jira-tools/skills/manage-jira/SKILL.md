---
name: manage-jira
version: 2.1.0
description: |
  Manage JIRA tickets using the Atlassian MCP tools (preferred) or Atlassian CLI (acli) as fallback.
  Use when the user asks to view, edit, comment on, create, search, or transition JIRA tickets.
  Handles authentication, field discovery, custom fields (team, sprint), and output formatting.
---

# Manage JIRA Tickets

## Tool Priority

1. **Atlassian MCP tools** (preferred) -- direct API access, handles custom fields, no CLI parsing
2. **acli CLI** (fallback) -- good for basic operations, but cannot set custom fields

Use the MCP tools for anything involving custom fields (team, sprint, story points, etc.). Fall back to acli only when MCP is unavailable or for operations MCP doesn't cover (like opening a ticket in the browser).

## Formatting: Always Use Markdown

The MCP tools (`createJiraIssue`, `editJiraIssue`, `addCommentToJiraIssue`) accept **Markdown only**. They internally convert Markdown to Atlassian Document Format (ADF). Never use Jira wiki markup with these tools -- it will be stored as raw text and won't render.

| What you want | Correct (Markdown) | Wrong (Wiki markup) |
|---------------|-------------------|-------------------|
| Heading | `## Heading` | `h2. Heading` |
| Bold | `**bold**` | `*bold*` |
| Inline code | `` `code` `` | `{{code}}` |
| Code block | ` ```lang ` | `{code:lang}` |
| Bullet list | `* item` or `- item` | `* item` (same, but context matters) |
| Numbered list | `1. item` | `# item` |
| Link | `[text](url)` | `[text\|url]` |

This applies to the `description` parameter in `createJiraIssue`, the `fields` object in `editJiraIssue`, and the `commentBody` in `addCommentToJiraIssue`.

## Getting Started with Atlassian MCP

### 1. Get the Cloud ID

Every MCP call needs a `cloudId`. Fetch it once per session:

```
atlassian___getAccessibleAtlassianResources()
```

This returns a list of sites. Pick the one matching the user's org. The `id` field is the cloudId.

### 2. Common Operations

#### View a Ticket

```
atlassian___getJiraIssue(cloudId, issueIdOrKey: "PROJ-123")
```

To get specific fields only, pass a `fields` array:

```
atlassian___getJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: ["summary", "status", "assignee"])
```

#### Create a Ticket

```
atlassian___createJiraIssue(
  cloudId,
  projectKey: "PROJ",
  issueTypeName: "Task",
  summary: "Title here",
  description: "Description in markdown"
)
```

Note: `createJiraIssue` only supports standard fields (summary, description, assignee, issueType, parent). For custom fields like team and sprint, create the ticket first, then use `editJiraIssue` to set them.

#### Edit a Ticket

```
atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: {...})
```

#### Search with JQL

```
atlassian___searchJiraIssuesUsingJql(cloudId, jql: "project = PROJ AND status = 'In Progress'")
```

#### Transition (Change Status)

First get available transitions:
```
atlassian___getTransitionsForJiraIssue(cloudId, issueIdOrKey: "PROJ-123")
```

Then transition:
```
atlassian___transitionJiraIssue(cloudId, issueIdOrKey: "PROJ-123", transition: {"id": "31"})
```

#### Add a Comment

```
atlassian___addCommentToJiraIssue(cloudId, issueIdOrKey: "PROJ-123", commentBody: "Comment in markdown")
```

#### Search (Rovo -- general search across Jira and Confluence)

```
atlassian___search(query: "authentication service deployment")
```

Use this for broad searches. Use `searchJiraIssuesUsingJql` when you need precise JQL filtering.

## Setting Custom Fields

This is where MCP shines over acli. The acli `edit` command does not support custom fields at all (no `--custom` flag, and `--from-json` cannot be combined with `--key`).

### Discovering Custom Field IDs

Custom field IDs vary between Jira instances. Never assume a field ID -- always discover it first by viewing an existing ticket that has the field set:

```
atlassian___getJiraIssue(cloudId, issueIdOrKey: "PROJ-123")
```

Scan the `fields` object for non-null entries with keys like `customfield_XXXXX`. Common fields and how to recognise them:

| Field | How to identify | Typical format |
|-------|----------------|----------------|
| Sprint | Array of sprint objects with `id`, `name`, `state` | `customfield_XXXXX` |
| Team | String UUID or object with team name | `customfield_XXXXX` |
| Story Points | Numeric value | `customfield_XXXXX` |

If the active project skill (e.g. `cars-project`) provides field IDs for the current org, use those instead of discovering them manually.

### Setting Team

The team field ID and value format vary by instance. Discover the field ID by inspecting an existing ticket, then set it:

```
atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: {
  "<team-field-id>": "<team-uuid>"
})
```

**What works:** Pass the team UUID as a plain string.

**What does NOT work:** Wrapping it in `{"id": "..."}` returns a 400 Bad Request.

To find the team UUID, look at an existing ticket that already has the team set and read the value from the relevant `customfield_XXXXX` key.

### Setting Sprint

The sprint field ID varies by instance. Discover it from an existing ticket, then set it:

```
atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: {
  "<sprint-field-id>": <sprint-id-integer>
})
```

**What works:** Pass the sprint ID as a plain integer.

**What does NOT work:** Wrapping it in `{"id": ...}` returns a 400 Bad Request.

To find the sprint ID, look at an existing ticket in the target sprint. The sprint field contains an array of sprint objects with `id`, `name`, `state`, `startDate`, `endDate`.

### Setting Multiple Custom Fields at Once

Be careful -- some custom field combinations fail together even if each works individually. If a multi-field edit returns 400, try setting them one at a time.

## acli Fallback

Use acli when MCP tools are not available or for these specific operations:

### When acli is better

- **Opening in browser**: `acli jira workitem view PROJ-123 --web`
- **Bulk operations with JQL**: `acli jira workitem edit --jql "..." --assignee "email" --yes`
- **CSV export**: `acli jira workitem search --jql "..." --csv`
- **Sprint management**: `acli jira sprint list-workitems`, `acli jira sprint view`

### acli Basics

acli uses `workitem` instead of `issue`.

```bash
# Check if available
which acli && acli --version

# Auth (if needed)
acli jira auth

# View
acli jira workitem view PROJ-123 --json

# Create
acli jira workitem create --project "PROJ" --type "Task" --summary "Title"

# Edit (standard fields only)
acli jira workitem edit --key "PROJ-123" --summary "New title" --yes

# Search
acli jira workitem search --jql "project = PROJ" --json --limit 10

# Transition
acli jira workitem transition --key "PROJ-123" --status "In Progress" --yes
```

**Always use `--yes`** for non-interactive operation.

### acli Limitations

- **No custom field support** in edit commands. No `--custom` flag exists. The `--from-json` flag cannot be combined with `--key`.
- **`--fields` in search** is limited. Some field names (like `sprint`) are rejected.
- **JQL team filter** does not accept quoted team names with spaces. `team = 'Name With Spaces'` fails with "option does not exist."
- **Sprint view** may fail silently with `command execution failed` and no useful error.
- **JSON output from view** works well for parsing field values and discovering custom field IDs.

## Workflow: Create a Fully Configured Ticket

This is the pattern that works reliably end-to-end, using MCP for every step:

1. **Get cloudId** via `getAccessibleAtlassianResources`
2. **Discover custom field IDs** by viewing an existing ticket in the target project that already has team and sprint set:
   ```
   atlassian___getJiraIssue(cloudId, issueIdOrKey: "EXISTING-123")
   ```
   Identify the sprint field key (look for an array of sprint objects), the team field key (look for a UUID string or team name object), and any other needed custom fields. If the active project skill provides these IDs, skip this step.
3. **Create the ticket** via MCP:
   ```
   atlassian___createJiraIssue(
     cloudId,
     projectKey: "PROJ",
     issueTypeName: "Task",
     summary: "Title here",
     description: "Description in markdown"
   )
   ```
   The response includes the new ticket's `key` (e.g. `PROJ-456`).
4. **Set custom fields** via MCP (one call per field if batching fails):
   ```
   atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-456", fields: {"<team-field-id>": "<team-uuid>"})
   atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-456", fields: {"<sprint-field-id>": <sprint-id-integer>})
   ```
5. **Verify** by viewing the ticket:
   ```
   atlassian___getJiraIssue(cloudId, issueIdOrKey: "PROJ-456")
   ```

## Common JQL Patterns

```
assignee = currentUser()
project = PROJ AND status = "In Progress"
project = PROJ AND sprint in openSprints()
created >= -7d ORDER BY created DESC
text ~ "search term"
priority IN (High, Highest) AND status != Done
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| MCP edit returns 400 | Wrong field value format | Check an existing ticket for the exact format. Try plain value vs wrapped in `{"id": ...}` |
| acli `--custom` flag | Flag doesn't exist | Use MCP `editJiraIssue` instead |
| acli `--from-json` with `--key` | Mutually exclusive flags | Use MCP or only `--from-json` with `issues` array in JSON |
| JQL team filter fails | Team names with spaces | Use MCP search or filter by other criteria |
| Sprint field rejected in `--fields` | acli doesn't support sprint as a field name | Use `--fields "*all"` and parse JSON, or use MCP |
