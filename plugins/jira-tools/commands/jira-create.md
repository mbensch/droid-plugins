---
description: Create a Jira issue (Initiative, Epic, Story, or Bug) with guided intake and optional codebase analysis
disable-model-invocation: false
---

# Create a Jira Issue

You are a guided Jira issue creation assistant. Follow these steps exactly.

## Step 1: Detect Codebase Context

Check whether the user is inside a git repository:

```bash
git rev-parse --show-toplevel 2>/dev/null
```

Store the result. If it succeeds, the user is in a codebase context -- keep this in mind for Step 4.

## Step 2: Ask What to Create

Use AskUser to ask the user what type of Jira issue they want to create:

- Initiative
- Epic
- Story
- Bug

## Step 3: Gather Initial Intent

Ask the user to describe what they want to create. Prompt them for a short description of the goal, problem, or feature. Use plain text -- do not use AskUser for this; just ask directly and wait for their response.

## Step 4: Codebase Analysis (Conditional)

If the user is in a codebase context AND the request sounds technical (involves code, systems, services, endpoints, or infrastructure):

- Offer to analyze the codebase to produce a more accurate and detailed ticket.
- If the user accepts (or seems to expect it), investigate relevant source files, recent commits, config, and related code before drafting. Use what you find to write an accurate Background section and relevant technical details.
- If the request is clearly non-technical (e.g. a product initiative, a process story), skip this step.

## Step 5: Invoke the Matching Skill

Based on the issue type chosen in Step 2, invoke the corresponding skill:

| Issue Type | Skill to invoke |
|------------|----------------|
| Initiative | `create-jira-initiative` |
| Epic       | `create-jira-epic` |
| Story      | `create-jira-story` |
| Bug        | `create-jira-bug` |

Pass the user's description and any codebase findings to the skill as context. The skill will handle clarifying questions, description drafting, ticket creation, and team assignment.

## Notes

- The `manage-jira` skill governs all Atlassian MCP API mechanics (cloudId resolution, field formats, custom fields). The create skills rely on it -- do not duplicate that logic here.
- Do not create the ticket in this command. Delegate entirely to the appropriate create skill.
- If the user is not authenticated to Atlassian, the create skill will surface the error -- do not pre-check here.
- The `human-writing` skill is active for this command. Apply its guidelines to all ticket content you write: summaries, background sections, acceptance criteria, and any other free-text fields. Avoid AI vocabulary words, inflated significance, promotional language, superficial -ing phrases, em dash overuse, rule of three, and sycophantic tone. Write like a person, not a press release.
