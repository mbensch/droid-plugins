#!/bin/bash
# Example: Update JIRA ticket description with acli

TICKET_KEY="PROJ-123"

# Method 1: Update with inline text (short descriptions)
acli jira workitem edit \
  --key "$TICKET_KEY" \
  --description "This is the updated description" \
  --yes

# Method 2: Update from a file (recommended for large descriptions)
cat > /tmp/jira-description.md << 'EOF'
## Overview
This is a comprehensive description with markdown formatting.

## Implementation Details
- Step 1: Do this
- Step 2: Do that
- Step 3: Complete

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
EOF

acli jira workitem edit \
  --key "$TICKET_KEY" \
  --description-file "/tmp/jira-description.md" \
  --yes

# Method 3: Update multiple fields at once
acli jira workitem edit \
  --key "$TICKET_KEY" \
  --summary "New summary for the ticket" \
  --description "Updated description" \
  --assignee "@me" \
  --labels "updated,in-progress" \
  --yes

# Verify the update
echo "Verifying update..."
acli jira workitem view "$TICKET_KEY" --fields "key,summary,description,assignee,labels"

# Clean up
rm /tmp/jira-description.md
