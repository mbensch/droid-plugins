# acli JIRA Command Reference

## Quick Command Syntax

### View Commands
```bash
acli jira workitem view <KEY>                    # View ticket
acli jira workitem view <KEY> --json             # JSON output
acli jira workitem view <KEY> --web              # Open in browser
acli jira workitem view <KEY> --fields "f1,f2"   # Specific fields
```

### Edit Commands
```bash
acli jira workitem edit --key "<KEY>" --summary "text" --yes
acli jira workitem edit --key "<KEY>" --description "text" --yes
acli jira workitem edit --key "<KEY>" --description-file "file.md" --yes
acli jira workitem edit --key "<KEY>" --assignee "email" --yes
acli jira workitem edit --key "<KEY>" --assignee "@me" --yes
acli jira workitem edit --key "<KEY>" --labels "label1,label2" --yes
acli jira workitem edit --jql "query" --assignee "email" --yes
```

### Comment Commands
```bash
acli jira workitem comment create --key "<KEY>" --body "text"
acli jira workitem comment create --key "<KEY>" --body-file "file.txt"
acli jira workitem comment create --jql "query" --body "text"
```

### Create Commands
```bash
acli jira workitem create --project "KEY" --type "Type" --summary "text"
acli jira workitem create --project "KEY" --type "Type" --summary "text" --description "text"
acli jira workitem create --project "KEY" --type "Type" --summary "text" --assignee "email"
```

### Search Commands
```bash
acli jira workitem search --jql "query"
acli jira workitem search --jql "query" --json
acli jira workitem search --jql "query" --csv
acli jira workitem search --jql "query" --count
acli jira workitem search --jql "query" --limit 50
acli jira workitem search --jql "query" --fields "key,summary,status"
```

### Transition Commands
```bash
acli jira workitem transition --key "<KEY>" --status "Status Name" --yes
acli jira workitem transition --jql "query" --status "Status Name" --yes
```

### Assign Commands
```bash
acli jira workitem assign --key "<KEY>" --assignee "email"
acli jira workitem assign --key "<KEY>" --assignee "@me"
acli jira workitem assign --jql "query" --assignee "email"
```

## Common Field Names

Standard fields for `--fields` flag:

- `key` - Ticket key (e.g., PROJ-123)
- `summary` - Ticket title
- `description` - Full description
- `status` - Current status
- `assignee` - Assigned user
- `reporter` - User who created ticket
- `creator` - User who created ticket
- `priority` - Priority level
- `type` or `issuetype` - Issue type (Bug, Task, Story, etc.)
- `created` - Creation timestamp
- `updated` - Last update timestamp
- `project` - Project key
- `labels` - Labels/tags
- `comment` - Comments

Special values:
- `*all` - All fields
- `*navigable` - All navigable fields
- `-fieldname` - Exclude a field

## Common JQL Patterns

### By User
```
assignee = currentUser()
assignee = "user@example.com"
reporter = currentUser()
```

### By Status
```
status = "To Do"
status = "In Progress"
status = Done
status IN ("To Do", "In Progress")
status != Done
```

### By Date
```
created >= -7d              # Last 7 days
created >= startOfWeek()    # This week
updated >= startOfDay()     # Today
updated >= "2024-01-01"     # Specific date
```

### By Project
```
project = PROJKEY
project IN (PROJ1, PROJ2)
```

### By Text
```
text ~ "search term"
summary ~ "bug"
description ~ "error"
```

### By Priority/Labels
```
priority = High
priority IN (High, Highest)
labels = urgent
labels IN (bug, critical)
```

### Compound Queries
```
project = MYPROJ AND status = "In Progress" AND assignee = currentUser()
project = MYPROJ AND (status = "To Do" OR status = "In Progress")
project = MYPROJ AND created >= -7d ORDER BY created DESC
assignee = currentUser() AND status != Done AND priority = High
```

## Issue Types

Common issue types (may vary by project):
- `Task`
- `Bug`
- `Story`
- `Epic`
- `Subtask`

## Common Status Names

Typical workflow statuses (vary by project):
- `To Do`
- `In Progress`
- `In Review`
- `Done`
- `Closed`
- `Blocked`

**Tip**: Use `acli jira workitem view <KEY>` to see available transitions for a specific ticket.

## Flags Reference

### Common Flags
- `--yes` or `-y` - Skip confirmation prompts (required for automation)
- `--json` - JSON output format
- `--csv` - CSV output format
- `--web` or `-w` - Open in web browser
- `--help` or `-h` - Show help

### Targeting Flags
- `--key` or `-k` - Ticket key(s), comma-separated
- `--jql` or `-j` - JQL query
- `--filter` - Saved filter ID

### Content Flags
- `--body` or `-b` - Inline text content
- `--body-file` or `-F` - Read content from file
- `--description` or `-d` - Inline description
- `--description-file` - Read description from file
- `--summary` or `-s` - Ticket summary/title
- `--assignee` or `-a` - Assignee email or "@me"
- `--labels` or `-l` - Comma-separated labels
- `--type` or `-t` - Issue type
- `--status` or `-s` - Status name for transitions
- `--project` or `-p` - Project key
- `--fields` or `-f` - Fields to display

### Search Flags
- `--limit` or `-l` - Maximum results
- `--count` - Show count only
- `--paginate` - Fetch all results

### Other Flags
- `--ignore-errors` - Continue on errors (bulk operations)
- `--edit-last` - Edit last comment from same author

## Tips

1. **Always use `--yes` for automation** - Prevents interactive prompts
2. **Test JQL queries first** - Use `--count` to verify scope before bulk operations
3. **Use files for large content** - `--description-file` for content > 1000 chars
4. **JSON for parsing** - Use `--json` when processing output programmatically
5. **Multiple keys** - Can specify multiple tickets: `--key "KEY-1,KEY-2,KEY-3"`
6. **Special assignee values**:
   - `@me` - Assign to current user
   - `default` - Assign to project default assignee
