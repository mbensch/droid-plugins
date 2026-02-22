---
name: create-jira-initiative
version: 1.0.0
user-invocable: false
description: |
  Create a well-structured Jira Initiative with consistent formatting optimized for both human readers and AI agents.
  Invoked internally by the /jira-create command. Handles clarifying questions and MCP-based ticket creation.
---

# Create Jira Initiative

## Initiative Description Format

Every initiative MUST use this exact structure. Do not deviate.

```markdown
## Background
[One paragraph. Strategic context: why this initiative exists, what problem or opportunity it addresses at the business or product level.]

## Objectives
* [Strategic objective this initiative is working toward]
* [Another objective]

## Key Results / Success Metrics
* [Measurable indicator that signals progress or completion]
* [Another metric]

## Out of Scope
[Only if the user explicitly calls out exclusions. Omit this section entirely otherwise.]

## Additional Information / Links
* [Strategy docs, OKRs, stakeholder contacts, related initiatives or epics]
```

### Rules

- **Background**: One paragraph. Strategic-level context only. Do not list epics or implementation details here. Focus on the "why": what business problem, user need, or opportunity is being addressed.
- **Objectives**: 2-4 bullet points. Each objective is a strategic aim ("Improve developer experience to reduce time-to-first-commit for new engineers"). Not tasks.
- **Key Results / Success Metrics**: 2-5 measurable indicators. Quantify where possible ("p50 build time below 2 minutes", "Net Promoter Score increases by 10 points"). If metrics are not yet defined, note that they are TBD and will be tracked via a linked doc.
- **Out of Scope**: Only present when the user explicitly provides exclusions. Never add speculatively.
- **Additional Information / Links**: Include links to strategy documents, OKRs, stakeholder contacts, or related initiatives. Never duplicate information already present in other Jira fields. Omit if empty.
- If any section lacks information, use AskUser to prompt the user rather than leaving placeholders.
- Clear, executive tone throughout -- initiatives are read by stakeholders, not just engineers.
- **Always use Markdown formatting.** The MCP tools convert Markdown to ADF internally. Never use Jira wiki markup (`h2.`, `{{code}}`, `{code}`, `#` for numbered lists). Use `## Heading`, `` `code` ``, triple-backtick fenced code blocks, and `1.` for numbered lists.

### Summary Line

- High-level strategic phrase naming the initiative.
- Not a task or deliverable -- name the effort, not the outcome: "Developer Experience Platform", not "Build developer experience platform".
- Capitalise as a proper name.

## Workflow

### 1. Parse the Request

Extract from the user's message or the context passed from `/jira-create`:
- The strategic driver or business problem (for Background)
- Strategic aims (for Objectives)
- Measurable indicators of success (for Key Results / Success Metrics)
- Explicit exclusions (for Out of Scope)
- Links to strategy docs, OKRs, or related work (for Additional Information)
- Team preference (if mentioned)

### 2. Ask Clarifying Questions

Use AskUser when genuinely ambiguous. Common questions:

- **Missing objectives**: "What is this initiative ultimately trying to achieve for the business or users?"
- **No success metrics**: "How will you measure success? Are there OKRs or KPIs tied to this initiative?"
- **Too tactical**: "This sounds more like an epic than an initiative. Should we create it as an epic instead, or keep it at the initiative level?"
- **Missing team**: "Which team should own this initiative?"
- **Scope**: "Does this initiative span multiple teams or a single team?"

Do NOT ask about format -- the format is fixed.

### 3. Draft the Description

Write the description following the mandatory format. Before creating, review:

- Is Background one paragraph at a strategic (not implementation) level?
- Are Objectives strategic aims, not tasks?
- Are Key Results measurable?
- Is Out of Scope only present if the user explicitly said something is excluded?

### 4. Create the Ticket

Use `atlassian___createJiraIssue` via the `manage-jira` skill for API mechanics:

- `issueTypeName`: Always `"Initiative"`
- `projectKey`: Ask the user if not obvious from context

### 5. Post-Creation Steps

After creating the ticket, follow any post-creation steps defined by the active project skill (e.g. `cars-project`). These may include setting required custom fields such as team. If no project skill is active, skip this step.

## What This Skill Does NOT Cover

- Other issue types (Epic, Story, Bug) -- separate skills.
- Transitioning, editing, or commenting on existing tickets -- use `manage-jira` skill.
- Codebase analysis -- initiatives are strategic and do not require code investigation.
