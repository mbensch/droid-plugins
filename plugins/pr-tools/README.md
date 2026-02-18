# PR Tools

Skills for safe and consistent pull request workflows: branch naming, PR creation with Jira integration, and protection against pushing to merged PRs.

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

### `create-pr`

Creates pull requests with consistent formatting, branch naming, and Jira integration. Respects repo-specific PR templates and AGENTS.md conventions when they exist.

**Features:**
- Asks for Jira ticket and uses it in branch name (`PROJ-1234/description`) and PR title (`feat: description [PROJ-1234]`)
- Detects and fills repo PR templates (`.github/pull_request_template.md`)
- Falls back to a default Summary/Changes/Testing format when no template exists
- Conventional commit prefixes in PR titles
- Integrates with `safe-pr-workflow` to verify branch state before pushing

## Plugin Structure

```
pr-tools/
├── .factory-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── safe-pr-workflow/
│   │   └── SKILL.md
│   └── create-pr/
│       └── SKILL.md
└── README.md
```

## License

MIT
