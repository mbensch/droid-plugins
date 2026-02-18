#!/bin/bash
# Example: Search JIRA tickets with acli

# Basic search - my open tickets
acli jira workitem search --jql "assignee = currentUser() AND status != Done"

# Search with specific fields
acli jira workitem search \
  --jql "project = PROJ AND status = 'In Progress'" \
  --fields "key,summary,status,assignee,priority"

# Search and output as JSON
acli jira workitem search \
  --jql "project = PROJ AND created >= -7d" \
  --json > recent-tickets.json

# Search and output as CSV (for spreadsheets)
acli jira workitem search \
  --jql "project = PROJ AND status = 'To Do'" \
  --csv > todo-tickets.csv

# Get count of matching tickets
COUNT=$(acli jira workitem search \
  --jql "project = PROJ AND status = 'In Progress'" \
  --count)
echo "Found $COUNT tickets in progress"

# Search with limit
acli jira workitem search \
  --jql "project = PROJ ORDER BY created DESC" \
  --limit 10

# Complex search with multiple conditions
acli jira workitem search \
  --jql "project = PROJ AND (status = 'To Do' OR status = 'In Progress') AND priority IN (High, Highest) AND assignee = currentUser()"

# Search by text
acli jira workitem search \
  --jql "text ~ 'bug' AND project = PROJ"

# Search tickets created this week
acli jira workitem search \
  --jql "project = PROJ AND created >= startOfWeek()"

# Search tickets updated today
acli jira workitem search \
  --jql "project = PROJ AND updated >= startOfDay()"

# Search unassigned tickets
acli jira workitem search \
  --jql "project = PROJ AND assignee is EMPTY AND status != Done"

# Search by labels
acli jira workitem search \
  --jql "project = PROJ AND labels IN (bug, critical)"

# Open search results in web browser
acli jira workitem search \
  --jql "project = PROJ AND status = 'In Progress'" \
  --web

# Parse JSON output with jq
echo "Ticket keys from search:"
acli jira workitem search \
  --jql "project = PROJ AND status = 'To Do'" \
  --json | jq -r '.issues[].key'

# Clean up
rm -f recent-tickets.json todo-tickets.csv
