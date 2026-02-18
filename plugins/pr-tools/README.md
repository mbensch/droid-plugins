# PR Tools

A plugin that prevents a common pitfall: pushing commits to branches that already have merged or closed PRs.

## Installation

### Factory (Droid)

```bash
droid plugin marketplace add https://github.com/mbensch/mb-ai-tools
droid plugin install pr-tools@mb-ai-tools
```

### Claude Code

```bash
/plugin marketplace add https://github.com/mbensch/mb-ai-tools
/plugin install pr-tools@mb-ai-tools
```

## Skills

### `safe-pr-workflow`

Automatically invoked before git push and PR creation operations. Checks whether the current branch already has a merged or closed PR, and if so, creates a new branch to avoid silently pushing to a dead PR.

**What it prevents:**
- Pushing commits to a branch whose PR was already merged
- Creating PRs on branches that already have closed/merged PRs
- Silent loss of work when pushes succeed but no visible PR exists

## Plugin Structure

```
pr-tools/
├── .factory-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── safe-pr-workflow/
│       └── SKILL.md
└── README.md
```

## License

MIT
