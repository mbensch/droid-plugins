# Droid Marketplace - Agent Guide

This guide explains how to use Droid to work with the `mb-ai-tools` marketplace repository.

## Working with This Repository

Droid can help you with:

**Creating new plugins:**
- Generate plugin structure with proper files (.factory-plugin, hooks.json, plugin.json)
- Create hook scripts in Python or other languages
- Write skills documentation in Markdown format
- Test plugin functionality

**Managing the marketplace:**
- Add new plugins to marketplace.json
- Update plugin versions and descriptions
- Validate plugin manifests
- Test plugin installation

**Troubleshooting plugins:**
- Debug hook execution failures
- Check marketplace.json syntax
- Verify plugin structure matches specification
- Test hooks with sample data

**Documentation tasks:**
- Write plugin README files
- Create usage examples
- Document hook interfaces
- Maintain developer guides

## Repository Structure

This repo serves as a marketplace for both Factory (Droid) and Claude Code. The `.factory-plugin/` directories are for Droid, and `.claude-plugin/` directories are for Claude Code. Plugins using only `skills/` and `commands/` work on both platforms. Hook-based plugins (`droid-receipts`, `auto-worktrees`) are Droid-only.

```
mb-ai-tools/
├── .factory-plugin/
│   └── marketplace.json    # Factory marketplace manifest (all plugins)
├── .claude-plugin/
│   └── marketplace.json    # Claude Code marketplace manifest (compatible plugins only)
├── plugins/
│   ├── droid-receipts/     # Session receipt generator (Droid-only)
│   │   ├── .factory-plugin/
│   │   │   └── plugin.json
│   │   ├── hooks/
│   │   │   └── generate-receipt.py
│   │   ├── hooks.json
│   │   └── README.md
│   ├── auto-worktrees/     # Automatic worktree management (Droid-only)
│   │   ├── .factory-plugin/
│   │   │   └── plugin.json
│   │   ├── hooks/
│   │   ├── hooks.json
│   │   └── README.md
│   ├── manual-worktrees/   # On-demand worktree commands
│   │   ├── .factory-plugin/
│   │   │   └── plugin.json
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   └── worktree.md
│   │   └── README.md
│   ├── worktrees-skill/     # Worktree management skill
│   │   ├── .factory-plugin/
│   │   │   └── plugin.json
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   └── using-worktrees/
│   │   │       └── SKILL.md
│   │   └── README.md
│   ├── jira-tools/          # Jira ticket management skills
│   │   ├── .factory-plugin/
│   │   │   └── plugin.json
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   ├── manage-jira/
│   │   │   ├── create-jira-story/
│   │   │   └── create-jira-bug/
│   │   └── README.md
│   └── pr-tools/            # Safe PR workflow
│       ├── .factory-plugin/
│       │   └── plugin.json
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── safe-pr-workflow/
│       └── README.md
└── README.md               # Marketplace docs
```

## Available Tasks

Ask Droid to:

1. **"Add a plugin called X that does Y"** - Creates new plugin structure
2. **"Update the marketplace.json for my new plugin"** - Registers plugin
3. **"Debug why my SessionEnd hook isn't firing"** - Troubleshoots issues
4. **"Create a README for the droid-receipts plugin"** - Writes documentation
5. **"Check if my plugin.json is valid"** - Validates manifest syntax
6. **"Write test data for my hook"** - Generates sample JSON for testing
7. **"Refactor generate-receipt.py to use functions"** - Code improvements

## Plugin Types

1. **Hooks** - Executed on events (SessionEnd, PreCommit, etc.)
   - Defined in `hooks.json`
   - Scripts in `hooks/` directory

2. **Skills** - On-demand capabilities invoked via slash commands
   - Defined in `SKILL.md` files
   - Can be simple text-based or complex AI-driven

3. **Droids** - Custom autonomous agents for specific use cases
   - Reusable configurations with specialized tools and behaviors

## Quick Start

To create a new plugin:

```
Use Droid to:
1. Create the directory structure under plugins/
2. Set up .factory-plugin/plugin.json with name, version, description
3. Add hooks.json or skills directory as needed
4. Create hook scripts or skill definitions
5. Add plugin to marketplace.json
6. Write plugin README.md in the plugin directory
7. Update the root README.md with the new plugin
8. Test by installing locally
9. Commit and push
```

**IMPORTANT: Always keep README.md updated.** When adding, removing, or renaming plugins, you MUST update:
- The plugin's own `plugins/{name}/README.md`
- The root `README.md` Available Plugins section and Platform Compatibility table
- The `.factory-plugin/marketplace.json` entries
- The `.claude-plugin/marketplace.json` entries (if the plugin is Claude Code compatible)
- Add `.claude-plugin/plugin.json` to the plugin directory (if Claude Code compatible)

## Testing Plugins

Locally test plugin before pushing:

```bash
# Add as local marketplace
droid plugin marketplace add /path/to/this/repo

# Install plugin
droid plugin install your-plugin@mb-ai-tools

# Test functionality
# Verify hooks fire
# Check logs in ~/.factory/logs/
```

## Common Issues

**Hook not executing:**
- Check file permissions (chmod +x)
- Verify hooks.json path references
- Check Factory logs for errors
- Test with sample JSON input

**Plugin not appearing:**
- Verify marketplace.json syntax
- Check source path is correct
- Reload marketplace list with `/plugins`

**Marketplace install fails:**
- Verify git history contains plugin.json
- Check commit hash is correct
- Ensure README.md exists in plugin directory
