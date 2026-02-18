# Jira Tools

A Factory plugin that bundles three Jira skills for managing tickets, creating stories, and filing bugs via Atlassian MCP tools.

## Installation

### From Marketplace (Recommended)

```bash
# Add the marketplace
droid plugin marketplace add https://github.com/mbensch/mbensch-droid-plugins

# Install the plugin
droid plugin install jira-tools@mbensch-droid-plugins
```

Or use the interactive UI: `/plugins` → Marketplaces → Add marketplace → enter URL

### From Local Directory (Development)

```bash
droid plugin marketplace add /path/to/mbensch-droid-plugins
droid plugin install jira-tools@mbensch-droid-plugins
```

## Prerequisites

Requires the [Atlassian MCP integration](https://app.factory.ai/settings/integrations) to be configured in Factory settings. The `acli` CLI is supported as a fallback for basic operations.

## Skills

### `manage-jira`

General-purpose Jira ticket management. Droid will automatically use this skill when you ask to:

- View, edit, or transition tickets
- Search with JQL
- Add comments
- Set custom fields (team, sprint, story points)
- Bulk operations

Includes a full acli command reference and troubleshooting guide.

### `create-jira-story`

Structured Jira Story creation with a consistent format optimized for both human readers and AI agents. Triggered when you ask to create a story or write a ticket.

**Format:** Background, Acceptance Criteria, Out of Scope (optional), Additional Information/Links.

### `create-jira-bug`

Structured Jira Bug creation with a consistent diagnostic format. Triggered when you ask to file a bug or report a defect.

**Format:** Description, Steps to Reproduce, Additional Information/Links.

## Plugin Structure

```
jira-tools/
├── .factory-plugin/
│   └── plugin.json
├── skills/
│   ├── manage-jira/
│   │   ├── SKILL.md
│   │   ├── references.md
│   │   └── examples/
│   │       ├── view-ticket.sh
│   │       ├── search-tickets.sh
│   │       ├── add-comment.sh
│   │       └── update-description.sh
│   ├── create-jira-story/
│   │   └── SKILL.md
│   └── create-jira-bug/
│       └── SKILL.md
└── README.md
```

## License

MIT
