# Droid Plugins

My personal Factory plugin marketplace - a collection of plugins and tools I've built for Droid.

## Overview

This is my personal marketplace for distributing Droid plugins I've created. Built as a [Factory Enterprise Plugin Registry](https://docs.factory.ai/enterprise/enterprise-plugin-registry), it follows the Git-based marketplace format that Factory uses for plugin distribution.

## Installation

Add this marketplace to Factory:

```bash
droid plugin marketplace add https://github.com/mbensch/mbensch-droid-plugins
```

Install plugins:

```bash
# Core plugins
droid plugin install droid-receipts@mbensch-droid-plugins

# Choose ONE worktree approach (see Author's Notes below)
droid plugin install manual-worktrees@mbensch-droid-plugins  # or auto-worktrees

# Optional: enhances worktree handling
droid plugin install worktrees-skill@mbensch-droid-plugins
```

Or browse available plugins via the UI:

```bash
/plugins
```

## Available Plugins

### droid-receipts

Generate visual receipts for Droid sessions showing token usage and costs.

**Features:**
- Automatic receipt generation when sessions end (via SessionEnd hook)
- HTML and SVG output formats
- Factory Token Usage calculation with model multipliers
- Cache token discounting (billed at 1/10 rate)
- Star Wars-style droid cashier names
- Cost breakdown by token type

### auto-worktrees

Automatically create and manage git worktrees for Droid sessions, isolating each session on its own branch.

**Features:**
- Creates isolated worktree for each session on `droid/{session_id}` branch
- Worktrees created at `../droid-worktrees/{repo}-{session_id}/`
- Automatic cleanup of worktrees older than 14 days
- Prevents conflicts between concurrent Droid sessions
- Works on macOS and Linux

### manual-worktrees

On-demand git worktree creation via a slash command.

**Features:**
- `/worktree` - Create a worktree for the current session on demand
- Session isolation with dedicated branches
- Flexible: use alongside or instead of automatic worktree creation

### worktrees-skill

A skill for systematic git worktree management with smart directory selection and safety verification.

**Features:**
- Droid-invocable skill for creating isolated worktrees
- Smart directory selection (`.worktrees/`, `worktrees/`, or `../droid-worktrees/`)
- Safety verification to ensure directories are gitignored
- Auto-detection of project setup commands (npm, cargo, pip, go mod)
- Baseline test verification before starting work

### jira-tools

Jira skills for managing tickets, creating stories, and filing bugs via Atlassian MCP tools.

**Skills:**
- `manage-jira` - General-purpose ticket management (view, edit, search, transition, custom fields)
- `create-jira-story` - Structured Story creation with consistent formatting
- `create-jira-bug` - Structured Bug creation with diagnostic formatting

**Requires:** [Atlassian MCP integration](https://app.factory.ai/settings/integrations) configured in Factory settings.

## Author's Notes

### Choosing a Worktree Plugin

**Do not install both `auto-worktrees` and `manual-worktrees`.** They serve the same purpose with different approaches - pick one based on your workflow:

- **auto-worktrees** - Best if you want every Droid session to automatically get its own isolated worktree. Great for "set it and forget it" workflows where you always want session isolation.

- **manual-worktrees** - Best if you prefer control over when worktrees are created. Use `/worktree` when you need isolation. Start here if you're unsure.

### Recommended Setup

```bash
# Option A: Automatic worktrees + skill
droid plugin install auto-worktrees@mbensch-droid-plugins
droid plugin install worktrees-skill@mbensch-droid-plugins

# Option B: Manual worktrees + skill (recommended if unsure)
droid plugin install manual-worktrees@mbensch-droid-plugins
droid plugin install worktrees-skill@mbensch-droid-plugins
```

The `worktrees-skill` plugin complements either choice by giving Droid a deeper understanding of worktree best practices for complex implementation tasks.

## Adding New Plugins

To add a new plugin to this marketplace:

1. Create a new directory under `plugins/your-plugin-name/`
2. Add a `.factory-plugin/plugin.json` manifest
3. Add your plugin files (hooks.json, skills/, hooks/, etc.)
4. Update `.factory-plugin/marketplace.json` to register the plugin
5. Commit and push

**Example structure:**
```
plugins/
└── your-plugin/
    ├── .factory-plugin/
    │   └── plugin.json
    ├── hooks.json
    ├── hooks/
    └── README.md
```

**Update marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "your-plugin",
      "description": "Plugin description",
      "source": "./plugins/your-plugin",
      "category": "productivity"
    }
  ]
}
```

## Contributing

Contributions welcome! To contribute:

1. Fork this repository
2. Add your plugin under `plugins/`
3. Update the marketplace.json
4. Submit a pull request

## License

Plugins in this marketplace are available under the MIT License.
