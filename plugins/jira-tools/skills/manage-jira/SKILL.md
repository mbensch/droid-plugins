---
name: manage-jira
version: 2.0.0
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
atlassian___search(query: "dealer domain docker build")
```

Use this for broad searches. Use `searchJiraIssuesUsingJql` when you need precise JQL filtering.

## Setting Custom Fields

This is where MCP shines over acli. The acli `edit` command does not support custom fields at all (no `--custom` flag, and `--from-json` cannot be combined with `--key`).

### Discovering Custom Field IDs

To find custom field IDs and their expected formats, view an existing ticket with all fields:

```
atlassian___getJiraIssue(cloudId, issueIdOrKey: "PROJ-123")
```

Then look through the `fields` object for non-null custom fields. Common ones:

| Field | Typical ID | Notes |
|-------|-----------|-------|
| Sprint | `customfield_10007` | Varies by instance |
| Team | `customfield_11100` | Varies by instance |
| Story Points | `customfield_10004` | Varies by instance |

### Setting Team

The team field value format depends on how it was configured. Try a plain string ID first:

```
atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: {
  "customfield_11100": "51869d83-db7d-4d45-bed0-131a61dd5c9a"
})
```

**What works:** Pass the team UUID as a plain string.

**What does NOT work:** Wrapping it in `{"id": "..."}` returns a 400 Bad Request.

To find the team ID, look at an existing ticket that already has the team set.

### Setting Sprint

```
atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-123", fields: {
  "customfield_10007": 22725
})
```

**What works:** Pass the sprint ID as a plain integer.

**What does NOT work:** Wrapping it in `{"id": 22725}` returns a 400 Bad Request.

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
2. **Find field values** by viewing an existing ticket in the target project/sprint/team:
   ```
   atlassian___getJiraIssue(cloudId, issueIdOrKey: "EXISTING-123")
   ```
   Extract sprint ID from `customfield_10007[0].id` and team ID from `customfield_11100.id`.
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
   atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-456", fields: {"customfield_11100": "team-uuid"})
   atlassian___editJiraIssue(cloudId, issueIdOrKey: "PROJ-456", fields: {"customfield_10007": 22725})
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
