# Droid Worktrees

A Factory plugin that automatically creates and manages git worktrees for Droid sessions, isolating each session on its own branch.

## Installation

### From Marketplace (Recommended)

```bash
# Add the marketplace
droid plugin marketplace add https://github.com/mbensch/mbensch-droid-plugins

# Install the plugin
droid plugin install droid-worktrees@mbensch-droid-plugins
```

Or use the interactive UI: `/plugins` → Marketplaces → Add marketplace → enter URL

### From Local Directory (Development)

```bash
droid plugin marketplace add /path/to/mbensch-droid-plugins
droid plugin install droid-worktrees@mbensch-droid-plugins
```

## How It Works

1. **SessionStart Hook**: When a Droid session starts, two hooks fire in sequence:
   - **cleanup-worktrees.sh**: Removes worktrees older than 14 days and deletes their `droid/*` branches
   - **create-worktree.sh**: Creates a new git worktree for the current session

2. **Worktree Location**: Worktrees are created at:
   ```
   {project}/../droid-worktrees/{repo-name}-{session-id}/
   ```

3. **Branch Naming**: Each session gets its own branch:
   ```
   droid/{session-id}
   ```

## Benefits

- **Isolation**: Each session works in its own worktree, preventing conflicts between concurrent sessions
- **Clean History**: Each session's changes are on a dedicated branch
- **Automatic Cleanup**: Stale worktrees (>14 days old) are automatically removed
- **Safe**: Skips non-git directories gracefully

## Configuration

The cleanup threshold (14 days) can be modified by editing the `cleanup-worktrees.sh` script. Future versions may support environment variable configuration.

## Plugin Structure

```
droid-worktrees/
├── .factory-plugin/
│   └── plugin.json       # Plugin manifest
├── hooks/
│   ├── create-worktree.sh
│   └── cleanup-worktrees.sh
├── hooks.json            # Hook configuration
└── README.md
```

## Requirements

- Git 2.5+ (for worktree support)
- `jq` for JSON parsing
- Works on macOS and Linux

## Troubleshooting

**Worktree not created:**
- Ensure the project directory is a git repository
- Check that `jq` is installed
- Verify the `droid-worktrees` directory is writable

**Old worktrees not being cleaned:**
- Cleanup runs on SessionStart, so stale worktrees are removed when a new session begins
- Manual cleanup: `git worktree prune`

## License

MIT
