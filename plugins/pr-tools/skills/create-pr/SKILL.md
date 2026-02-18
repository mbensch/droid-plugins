---
name: create-pr
version: 1.0.0
description: |
  Create a pull request with consistent formatting, branch naming, and Jira integration.
  Use when the user asks to create a PR, push and open a PR, or submit their changes for review.
  Handles branch naming, PR title, description, and respects repo-specific templates.
---

# Create Pull Request

## Priority Order

1. **Repo PR template** -- if `.github/pull_request_template.md` (or variants) exists, use it as the description structure. Fill in every section meaningfully or remove sections that don't apply. Never leave template placeholder text.
2. **AGENTS.md / repo rules** -- if the repo has an AGENTS.md or other guideline files mentioning PR conventions, branch naming, or commit style, follow those.
3. **This skill's defaults** -- use the format below when no repo-specific guidance exists.

## Before Starting

### Ask for Jira Ticket

Use AskUser to ask:

> "Do you have a Jira ticket for this PR? If so, provide the ticket key (e.g. PROJ-1234). Leave blank if none."

Do NOT skip this question. The answer drives branch naming and PR title.

### Check for Repo-Specific Templates

Before creating the PR, check for templates and conventions:

```bash
# Check for PR templates
ls .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null

# Check for AGENTS.md
ls AGENTS.md 2>/dev/null
```

If a template exists, read it and use it as the description structure.

## Branch Naming

If a Jira ticket was provided:
```
PROJ-1234/short-description-of-change
```

If no Jira ticket:
```
type/short-description-of-change
```

Where `type` is one of: `feat`, `fix`, `refactor`, `chore`, `ci`, `docs`, `test`.

Rules:
- Lowercase, hyphen-separated
- Keep the slug under 5 words
- The Jira ticket prefix comes first when present

## PR Title

If a Jira ticket was provided:
```
type: short description [PROJ-1234]
```

If no Jira ticket:
```
type: short description
```

Conventional commit prefixes: `feat`, `fix`, `refactor`, `chore`, `ci`, `docs`, `test`. Use optional scope in parentheses when it adds clarity (e.g. `feat(inventory): add incomplete listings query [CARS-31271]`).

Rules:
- Lowercase after the prefix
- No period at the end
- The Jira ticket goes in square brackets at the end of the title
- Be specific: "add customer platform API client" not "add new feature"

## Default PR Description Format

Use this format when the repo has no PR template:

```markdown
## Summary

[One paragraph. What this PR does and why. Reference the Jira ticket naturally if one exists.]

## Changes

[Grouped by logical category. Use sub-headers for large PRs. Be specific about what was added, changed, or removed. Mention new files/modules by path when it helps the reviewer navigate.]

## Testing

[How the changes were verified. Include test results, commands run, and manual verification steps. Example:]

- All tests pass (`mix test` / `npm test` / `pytest` etc.)
- Linter/formatter clean
- Manual verification: [describe what was checked]
```

Optional sections -- include only when relevant:
- `## Jira` -- link to the ticket (e.g. `https://yourorg.atlassian.net/browse/PROJ-1234`)
- `## Migration / Deployment Notes` -- if there are env var changes, feature flags, or ordering concerns
- `## Screenshots` -- for UI changes

### What NOT to include

- File-by-file changelogs (the diff shows that)
- Tables listing every file changed (unless the PR is a broad refactor and it genuinely helps)
- Empty template sections with placeholder text
- Implementation details that are obvious from the code

## Filling In Repo Templates

When a repo template exists, follow these rules:

- **Fill every section** with real content or remove the section entirely
- **Never leave placeholder/instruction text** like "Describe what this PR does" or "What needs to be done locally to validate this change?"
- **Be concise** -- a section with one good sentence beats three paragraphs of filler
- **Jira section** -- provide the full URL: `https://yourorg.atlassian.net/browse/PROJ-1234`

## Workflow

1. **Ask for Jira ticket** via AskUser
2. **Check for repo template and AGENTS.md** -- read them if they exist
3. **Check branch state** -- use the `safe-pr-workflow` skill to verify the branch is safe to push
4. **Create branch** if not already on a feature branch (use the naming convention above)
5. **Stage and commit** changes if uncommitted work exists
6. **Push** the branch
7. **Create the PR** with `gh pr create`
8. **Report** the PR URL to the user

## Using gh pr create

When the repo has a PR template, use `--fill` or `--body` to provide the filled-in template. Do not use `--fill` alone as it only uses the commit messages.

```bash
gh pr create --base main --title "feat: description [PROJ-1234]" --body "filled description"
```

If the default branch is not `main`, detect it:
```bash
gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'
```
