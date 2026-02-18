#!/bin/bash
# Example: View JIRA ticket with acli

# View ticket with default fields
acli jira workitem view PROJ-123

# View with specific fields
acli jira workitem view PROJ-123 --fields "key,summary,status,assignee,description,labels"

# View all fields
acli jira workitem view PROJ-123 --fields "*all"

# View as JSON (for parsing)
acli jira workitem view PROJ-123 --json

# Open ticket in web browser
acli jira workitem view PROJ-123 --web

# View multiple tickets
for key in PROJ-123 PROJ-124 PROJ-125; do
  echo "=== $key ==="
  acli jira workitem view "$key" --fields "key,summary,status"
  echo ""
done

# View ticket and parse JSON with jq
acli jira workitem view PROJ-123 --json | jq '.fields | {key, summary, status: .status.name}'
