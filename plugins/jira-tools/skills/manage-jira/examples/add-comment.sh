#!/bin/bash
# Example: Add comments to JIRA tickets with acli

TICKET_KEY="PROJ-123"

# Method 1: Simple inline comment
acli jira workitem comment create \
  --key "$TICKET_KEY" \
  --body "This is a simple comment"

# Method 2: Comment from a file
cat > /tmp/jira-comment.txt << 'EOF'
## Update

I've completed the implementation. Here are the key changes:

1. Added new feature X
2. Fixed bug Y
3. Updated documentation

Next steps:
- Review the PR
- Run tests in staging
- Deploy to production

Please review and provide feedback.
EOF

acli jira workitem comment create \
  --key "$TICKET_KEY" \
  --body-file "/tmp/jira-comment.txt"

# Method 3: Mention users in comment (using @ mentions)
acli jira workitem comment create \
  --key "$TICKET_KEY" \
  --body "[@user@example.com|~accountId] Please review this ticket."

# Method 4: Add comment to multiple tickets via JQL
acli jira workitem comment create \
  --jql "project = PROJ AND status = 'In Review'" \
  --body "Reminder: Please complete your reviews by EOD"

# Method 5: Add comment and view all comments
acli jira workitem comment create \
  --key "$TICKET_KEY" \
  --body "Added new comment"

echo "All comments for $TICKET_KEY:"
acli jira workitem comment list --key "$TICKET_KEY"

# Clean up
rm /tmp/jira-comment.txt
