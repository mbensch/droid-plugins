---
name: create-jira-objective
version: 1.0.0
user-invocable: false
description: |
  Create a well-structured Jira Objective with S.M.A.R.T criteria, key results, and milestones.
  Invoked internally by the /jira-create command. Objectives are the highest level of the work hierarchy,
  sitting above Initiatives, Epics, and Stories.
---

# Create Jira Objective

Objectives represent the highest level of strategic work. They answer "what are we trying to achieve?" rather than "what are we building?". Every objective must be S.M.A.R.T and decompose into clear milestones that will each become a Jira Initiative.

## Objective Description Format

Every objective MUST use this exact structure. Do not deviate.

```markdown
## Description
[1-2 sentences. A high-level strategic outcome, written as a S.M.A.R.T goal: Specific, Measurable, Achievable, Relevant, and Time-bound.]

## Key Results
* [Measurable indicator that signals progress or completion — 1-3 items]

## Milestones / Phases
* **[Milestone name]** — [One sentence describing what this phase delivers. Each milestone maps to a Jira Initiative.]
```

### Rules

- **Description**: 1-2 sentences only. Must be S.M.A.R.T:
  - **Specific** — clear about what will be achieved
  - **Measurable** — includes a concrete metric or threshold
  - **Achievable** — realistic given available resources and time
  - **Relevant** — tied to a meaningful business or product outcome
  - **Time-bound** — includes a timeframe or deadline
  If any S.M.A.R.T element is missing, ask the user to provide it before drafting.
- **Key Results**: 1-3 bullet points. Each is a measurable indicator of progress. Quantify everything: "Reduce p99 API latency to under 200ms by Q3" not "Improve API performance".
- **Milestones / Phases**: Each milestone names a logical phase of work and will become a separate Jira Initiative. 2-5 milestones is typical. Order them chronologically.
- If any section lacks information, use AskUser rather than leaving placeholders.
- Clear, strategic, executive tone throughout.
- **Always use Markdown formatting.** The MCP tools convert Markdown to ADF internally. Never use Jira wiki markup.

### Summary Line

- Concise strategic statement naming the objective.
- Must imply the outcome, not the work: "Achieve sub-200ms API response times across all production endpoints by Q3" not "API performance project".

## Workflow

### 1. Parse the Request

Extract from the user's message or context passed from `/jira-create`:
- The strategic outcome (for Description)
- Measurable success signals (for Key Results)
- Logical phases or milestones (for Milestones / Phases)
- Timeframe or deadline (required for S.M.A.R.T)
- Team preference (if mentioned)

### 2. Validate S.M.A.R.T Criteria

Before drafting, check every S.M.A.R.T element:

- **Missing metric**: "What does success look like numerically? E.g. a conversion rate, latency threshold, or revenue figure."
- **Missing timeframe**: "When should this objective be achieved?"
- **Too vague**: "Can you be more specific about what 'improve' means here?"
- **Not achievable**: Flag if the goal seems unrealistic and ask the user to confirm scope.

Use AskUser for any gaps. Do not draft until all five S.M.A.R.T elements are present.

### 3. Identify Milestones

If the user has not provided milestones, ask:
- "How would you break this objective into phases? Each phase will become a Jira Initiative."

If milestones are unclear, suggest 2-3 logical phases based on the objective and ask the user to confirm or adjust.

### 4. Draft the Description

Write the description following the mandatory format. Before creating, review:

- Does the Description meet all five S.M.A.R.T criteria?
- Are Key Results quantified and measurable?
- Does each Milestone map to a distinct phase of work that could become an Initiative?

### 5. Create the Ticket

Use `atlassian___createJiraIssue` via the `manage-jira` skill:

- `issueTypeName`: Use the issue type name provided by the active project skill, or discover it via `atlassian___getJiraProjectIssueTypesMetadata` if not specified
- `projectKey`: From the selected project in `/jira-create`

### 6. Post-Creation Steps

After creating the ticket, follow any post-creation steps defined by the active project skill (e.g. `cars-project`). These may include setting required custom fields such as team. If no project skill is active, skip this step.

## What This Skill Does NOT Cover

- Creating the child Initiatives for each milestone -- run `/jira-create` again for each one.
- Other issue types -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
