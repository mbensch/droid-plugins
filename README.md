# Droid Plugins

My personal Factory plugin marketplace - a collection of plugins and tools I've built for Droid.

## Overview

This is my personal marketplace for distributing Droid plugins I've created. Built as a [Factory Enterprise Plugin Registry](https://docs.factory.ai/enterprise/enterprise-plugin-registry), it follows the Git-based marketplace format that Factory uses for plugin distribution.

## Installation

Add this marketplace to Factory:

```bash
droid plugin marketplace add https://github.com/mbensch/mbensch-droid-plugins
```

Then install plugins:

```bash
droid plugin install droid-receipts@mbensch-droid-plugins
droid plugin install droid-worktrees@mbensch-droid-plugins
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

### droid-worktrees

Automatically create and manage git worktrees for Droid sessions, isolating each session on its own branch.

**Features:**
- Creates isolated worktree for each session on `droid/{session_id}` branch
- Worktrees created at `../droid-worktrees/{repo}-{session_id}/`
- Automatic cleanup of worktrees older than 14 days
- Prevents conflicts between concurrent Droid sessions
- Works on macOS and Linux

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
