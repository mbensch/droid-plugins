# Jira Tools

A Factory plugin for Jira issue creation and management via Atlassian MCP tools. Use `/jira-create` to create Initiatives, Epics, Stories, and Bugs with guided intake and optional codebase analysis.

## Installation

### From Marketplace (Recommended)

```bash
# Add the marketplace
droid plugin marketplace add https://github.com/mbensch/mb-ai-tools

# Install the plugin
droid plugin install jira-tools@mb-ai-tools
```

Or use the interactive UI: `/plugins` → Marketplaces → Add marketplace → enter URL

### From Local Directory (Development)

```bash
droid plugin marketplace add /path/to/mb-ai-tools
droid plugin install jira-tools@mb-ai-tools
```

## Prerequisites

Requires the [Atlassian MCP integration](https://app.factory.ai/settings/integrations) to be configured in Factory settings. The `acli` CLI is supported as a fallback for basic operations.

## Commands

### `/jira-create`

The primary entry point for creating any Jira issue type. The command:

1. Detects whether you are inside a git repository
2. Asks what type of issue you want to create (Initiative, Epic, Story, Bug)
3. Gathers your initial description
4. Optionally analyzes the codebase to produce a more accurate ticket (for technical requests in a repo)
5. Delegates to the appropriate create skill, which handles clarifying questions, description formatting, ticket creation, and team assignment

## Skills

### `manage-jira`

General-purpose Jira ticket management. Droid will automatically use this skill when you ask to:

- View, edit, or transition tickets
- Search with JQL
- Add comments
- Set custom fields (team, sprint, story points)
- Bulk operations

Includes a full acli command reference and troubleshooting guide.

### `create-jira-objective` *(internal)*

Structured Jira Objective creation. Invoked by `/jira-create`. Objectives are the highest level of the work hierarchy (Objective → Initiative → Epic → Story/Bug).

**Format:** Description (S.M.A.R.T), Key Results (1-3), Milestones / Phases (each maps to an Initiative).

### `create-jira-initiative` *(internal)*

Structured Jira Initiative creation. Invoked by `/jira-create`.

**Format:** Background, Objectives, Key Results / Success Metrics, Out of Scope (optional), Additional Information/Links.

### `create-jira-epic` *(internal)*

Structured Jira Epic creation. Invoked by `/jira-create`.

**Format:** Background, Goals, Acceptance Criteria, Out of Scope (optional), Additional Information/Links.

### `create-jira-story` *(internal)*

Structured Jira Story creation. Invoked by `/jira-create`.

**Format:** Background, Acceptance Criteria, Out of Scope (optional), Additional Information/Links.

### `create-jira-bug` *(internal)*

Structured Jira Bug creation. Invoked by `/jira-create`.

**Format:** Description, Steps to Reproduce, Additional Information/Links.

### `human-writing` *(internal)*

Applies human-writing guidelines to all ticket content drafted by `/jira-create`. Removes AI-sounding patterns (inflated significance, promotional language, em dash overuse, rule of three, AI vocabulary words) and ensures descriptions read like a person wrote them. Based on Wikipedia's "Signs of AI writing" guide.

Originally authored by [Factory-AI/factory-plugins](https://github.com/Factory-AI/factory-plugins/blob/master/plugins/droid-evolved/skills/human-writing/SKILL.md).

### `cars-project` *(internal)*

CARS project-specific configuration for the `carscommerce.atlassian.net` org. Activated automatically by `/jira-create` when the user is authenticated to carscommerce and selects the CARS project. Provides team field ID and UUID resolution instructions so create skills do not hardcode org-specific values.

## Plugin Structure

```
jira-tools/
├── .factory-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── jira-create.md
├── skills/
│   ├── manage-jira/
│   │   ├── SKILL.md
│   │   ├── references.md
│   │   └── examples/
│   │       ├── view-ticket.sh
│   │       ├── search-tickets.sh
│   │       ├── add-comment.sh
│   │       └── update-description.sh
│   ├── create-jira-objective/
│   │   └── SKILL.md
│   ├── create-jira-initiative/
│   │   └── SKILL.md
│   ├── create-jira-epic/
│   │   └── SKILL.md
│   ├── create-jira-story/
│   │   └── SKILL.md
│   ├── create-jira-bug/
│   │   └── SKILL.md
│   ├── human-writing/
│   │   └── SKILL.md
│   └── cars-project/
│       └── SKILL.md
└── README.md
```

## License

MIT
