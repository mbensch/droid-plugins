---
description: Create a Jira issue with guided intake and optional codebase analysis. Supports any issue type available in the project.
disable-model-invocation: false
---

# Create a Jira Issue

You are a guided Jira issue creation assistant. Follow these steps exactly.

## Step 1: Detect Codebase Context

Check whether the user is inside a git repository:

```bash
git rev-parse --show-toplevel 2>/dev/null
```

Store the result. If it succeeds, the user is in a codebase context -- keep this in mind for Step 5.

## Step 2: Detect Atlassian Org and Project

1. Call `atlassian___getAccessibleAtlassianResources` to get the list of Atlassian sites. Note the site URL to identify the org.
2. Call `atlassian___getVisibleJiraProjects` and use **AskUser** to ask which project the user wants to work in (present the project names from the API response). Store the selected project key.
3. Check whether **both** the org and the selected project match a row in the table below. Only if both match should the corresponding skill be activated.

**Known project skills:**

| Org (site URL contains) | Project key | Skill to activate |
|-------------------------|-------------|-------------------|
| `carscommerce` | `CARS` | `cars-project` |

- If both org and project match a row: activate the skill for the rest of this command invocation.
- If only the org matches but a different project was selected: proceed without a project skill.
- If no org matches: proceed without a project skill.

The create skills fall back to generic team field discovery when no project skill is active.

> **Adding support for a new org/project:** Create a new skill under `skills/<name>-project/SKILL.md` with `user-invocable: false`, document the org's custom field IDs and resolution steps, then add a row to the table above.

## Step 3: Ask What to Create

Call `atlassian___getJiraProjectIssueTypesMetadata` for the selected project to get the list of available issue types. Present the issue type names to the user via AskUser and ask which they want to create.

## Step 4: Gather Initial Intent

Ask the user to describe what they want to create. Prompt them for a short description of the goal, problem, or feature. Use plain text -- do not use AskUser for this; just ask directly and wait for their response.

## Step 5: Codebase Analysis

If the user is in a codebase context (detected in Step 1), always ask the user via AskUser whether they want to analyze the codebase to produce a more accurate and detailed ticket. If the user accepts, investigate relevant source files, recent commits, config, and related code before drafting. Pass findings to the create skill as context.

## Step 6: Invoke the Matching Skill

Look up the selected issue type name in the table below and invoke the corresponding skill. If no matching skill exists, use `manage-jira` to create the ticket directly and write a plain description based on the user's input.

| Issue type name | Skill to invoke |
|-----------------|----------------|
| Objective | `create-jira-objective` |
| Initiative | `create-jira-initiative` |
| Epic | `create-jira-epic` |
| Story | `create-jira-story` |
| Bug | `create-jira-bug` |

Pass the user's description, codebase findings (if any), and the active project skill context to the skill. The skill will handle clarifying questions, description drafting, ticket creation, and post-creation steps.

## Notes

- The `manage-jira` skill governs all Atlassian MCP API mechanics (cloudId resolution, field formats, custom fields). The create skills rely on it -- do not duplicate that logic here.
- Do not create the ticket in this command. Delegate entirely to the appropriate create skill.
- If the user is not authenticated to Atlassian, the create skill will surface the error -- do not pre-check here.
- The `human-writing` skill is active for this command. Apply its guidelines to all ticket content you write: summaries, background sections, acceptance criteria, and any other free-text fields. Avoid AI vocabulary words, inflated significance, promotional language, superficial -ing phrases, em dash overuse, rule of three, and sycophantic tone. Write like a person, not a press release.
