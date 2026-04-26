# CONTEXT_ENGINEERING_SKILL.md

## 1. Skill Purpose

Use this Skill to decide what context an Agent should read, summarize, assemble, and use before executing a task.

This Skill helps the Agent:

```text
read long-term context files
select task-relevant information
compress irrelevant or long content
resolve context conflicts
generate task_context/CONTEXT_PACKAGE.md
generate task_context/TASK_CONTEXT.md when needed
```

This Skill does not replace the task itself.

It prepares the correct context for task execution.

---

## 2. When to Use

Use this Skill when:

```text
1. The task is complex.
2. The task depends on project files.
3. The task depends on user preferences.
4. The task depends on previous decisions.
5. The task involves code, documents, templates, reports, experiments, or project planning.
6. The user asks the Agent to continue or optimize a project.
7. The Agent needs to generate a high-quality task prompt.
```

Do not use full Context Package generation when:

```text
1. The user asks a simple concept question.
2. The task is a quick one-off answer.
3. No project or long-term context is relevant.
```

For simple tasks, the Agent may generate a lightweight `TASK_CONTEXT.md` or answer directly.

---

## 3. Required Inputs

Before generating context, the Agent should read available files in this order:

```text
00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
context/TODO.md
context/TEST_COMMANDS.md
context/CHANGELOG.md
context/AGENT_LESSONS.md
```

Then read task-specific files:

```text
README.md
AGENTS.md
CLAUDE.md
.cursor/rules/
source files
documents
configuration files
logs
test files
scripts
data descriptions
```

Then read templates when needed:

```text
templates/task_context/20_CONTEXT_PACKAGE_TEMPLATE.md
templates/task_context/21_TASK_CONTEXT_TEMPLATE.md
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

---

## 4. Expected Outputs

For complex tasks, generate:

```text
task_context/CONTEXT_PACKAGE.md
```

For lightweight tasks, generate or propose:

```text
task_context/TASK_CONTEXT.md
```

The generated context should include:

```text
1. Current task
2. Project background summary
3. User preference summary
4. Relevant decision summary
5. Current status
6. Relevant files
7. Relevant commands
8. Key constraints
9. Output requirements
10. Completion criteria
11. Risks and uncertainty
```

---

## 5. Core Process

The core Context Engineering process is:

```text
Recall
  ↓
Compress
  ↓
Assemble
  ↓
Use
  ↓
Update if needed
```

Meaning:

```text
Recall:
Find relevant information.

Compress:
Remove noise and keep only useful facts.

Assemble:
Put information in a priority-aware order.

Use:
Generate the task prompt and execute the task.

Update:
After the task, update only affected long-term files.
```

---

## 6. Execution Steps

The Agent must follow this order for complex tasks:

```text
1. Preserve the user's original request.
2. Identify the task type.
3. Read long-term context files.
4. Read task-specific files.
5. Identify relevant information.
6. Remove irrelevant information.
7. Summarize long content.
8. Detect context conflicts.
9. Resolve conflicts using priority rules.
10. Generate task_context/CONTEXT_PACKAGE.md.
11. Use PROMPT_ENGINEERING_SKILL.md to generate a task prompt.
12. Execute the task.
13. Use TASK_CLOSING_CHECKLIST to decide which files should be updated.
```

---

## 7. Context Priority Rules

When sources conflict, use this priority order:

```text
1. Current explicit user instruction
2. System or project root rules
3. Current task files and current error/log/code
4. context/PROJECT_CONTEXT.md
5. context/USER_PREFERENCES.md
6. context/DECISION_LOG.md
7. Skill files
8. README.md and general project documents
9. Old notes or outdated records
```

Rules:

```text
newer confirmed decisions override older decisions
current user instruction overrides old project notes
deprecated decisions must not be used as current truth
uncertain conflicts must be marked and reported
```

---

## 8. Context Compression Rules

When content is too long, the Agent must compress it.

Keep:

```text
1. Task goal
2. User constraints
3. File paths
4. Function, class, or interface names
5. Error type and line number
6. Commands
7. Important decisions
8. Output requirements
9. Completion criteria
10. Risks
```

Remove or summarize:

```text
1. Repeated explanations
2. Irrelevant background
3. Long unrelated code
4. Old deprecated plans
5. Unrelated logs
6. Casual discussion
```

The Agent should state when information was compressed.

---

## 9. Context Package Rules

For complex tasks, generate:

```text
task_context/CONTEXT_PACKAGE.md
```

It must include:

```text
1. Current task
2. Project background summary
3. User preference summary
4. Decision summary
5. Current status
6. Relevant files
7. Relevant commands
8. Key constraints
9. Output requirements and completion criteria
```

Do not include:

```text
1. Full unrelated files
2. Full historical conversation
3. All project documents
4. Unverified assumptions without labels
5. Project-specific facts inside templates
```

---

## 10. Task Context Rules

For smaller tasks, generate:

```text
task_context/TASK_CONTEXT.md
```

Use it when:

```text
1. The task has a clear boundary.
2. The task is smaller than a full project operation.
3. The task still needs tracking.
4. The task has inputs, outputs, constraints, and completion criteria.
```

Do not use it for simple one-off explanations.

---

## 11. Missing Information Rules

If information is missing, the Agent must not invent it.

Use:

```text
待补充:
Information missing and should be provided later.

临时假设:
Information inferred from available context but not confirmed.

需要用户确认:
Information that affects important decisions and should be confirmed.
```

The Agent may continue if the task can proceed safely with clearly marked assumptions.

---

## 12. Prohibited Actions

The Agent must not:

```text
1. Execute complex tasks without checking relevant context.
2. Read everything blindly without filtering.
3. Put all files into the context package.
4. Ignore current user instructions.
5. Let old context override new instructions.
6. Delete key constraints during compression.
7. Invent files, commands, decisions, or project facts.
8. Write project-specific content into templates/.
9. Update all long-term files after every task.
10. Claim context is complete when important files are missing.
```

---

## 13. Validation Checklist

Before using a Context Package, check:

```text
1. Is the current task clear?
2. Is the project background summarized?
3. Are user preferences included if relevant?
4. Are relevant decisions included?
5. Is the current status included?
6. Are relevant files listed?
7. Are relevant commands listed?
8. Are key constraints listed?
9. Are output requirements clear?
10. Are completion criteria clear?
11. Are assumptions marked?
12. Are conflicts identified?
13. Is irrelevant information removed?
14. Are templates kept generic?
```

If any item is missing, the Agent must either fix it or explain why it is missing.

---

## 14. Closing Rule

After task execution, use:

```text
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

to decide whether to update:

```text
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
context/TODO.md
context/TEST_COMMANDS.md
context/CHANGELOG.md
context/AGENT_LESSONS.md
```

Do not update a long-term file just because it was read.

Only update when the task created new long-term information.

---

## 15. Final Principle

Context Engineering is not about giving the Agent more information.

It is about giving the Agent the right information, in the right order, with the right priority.

Final rule:

```text
Long-term files store stable project facts.
Task context files store current task facts.
Templates store generic structures.
Skills define Agent behavior.
```
