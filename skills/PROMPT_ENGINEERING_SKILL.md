# PROMPT_ENGINEERING_SKILL.md

## 1. Skill Purpose

Use this Skill to convert vague, incomplete, or rough user requests into high-quality prompts that an Agent or LLM can execute reliably.

This Skill helps the Agent:

```text
understand the user's real goal
clarify the task boundary
identify missing context
add role, background, constraints, and output format
generate a clear execution prompt
```

This Skill does not execute the task itself.

It prepares a better prompt for task execution.

---

## 2. When to Use

Use this Skill when:

```text
1. The user provides a vague request.
2. The user asks to optimize a prompt.
3. The user wants to turn an idea into an Agent task.
4. The user wants a prompt for ChatGPT, Cursor, Claude Code, Codex, OpenClaw, or another Agent.
5. The user asks for a reusable prompt template.
6. The task requires clear role, background, constraints, steps, or output format.
```

Do not use this Skill when:

```text
1. The user asks a simple factual question.
2. The task is already fully specified and ready to execute.
3. The user explicitly asks not to rewrite or optimize the prompt.
4. The user only wants a direct answer, not a prompt.
```

---

## 3. Required Inputs

Before generating a prompt, the Agent should identify:

```text
1. User's original request
2. Target user or target Agent
3. Task goal
4. Task background
5. Input materials
6. Constraints
7. Expected output
8. Quality requirements
9. Verification method
10. Missing information
```

If project files are available, the Agent should also read:

```text
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
task_context/CONTEXT_PACKAGE.md
task_context/TASK_CONTEXT.md
```

If these files do not exist, continue with available information and mark missing information clearly.

---

## 4. Expected Outputs

The Agent should output one or more of the following:

```text
1. Optimized prompt
2. Short version prompt
3. Full version prompt
4. Agent-specific prompt
5. Prompt structure explanation
6. Missing information list
7. Usage advice
```

For complex tasks, output both:

```text
简洁版 Prompt
完整版 Prompt
```

---

## 5. Standard Prompt Structure

A high-quality prompt should include:

```text
Role
Background
Goal
Inputs
Constraints
Tasks
Execution Steps
Output Format
Quality Requirements
Verification Method
Uncertainty Handling
```

Recommended structure:

```text
You are 【role】.

Background:
【project or task background】

Goal:
【final result expected】

Inputs:
【provided materials】

Constraints:
1. 【constraint 1】
2. 【constraint 2】
3. 【constraint 3】

Tasks:
1. 【task 1】
2. 【task 2】
3. 【task 3】

Execution Requirements:
1. Understand the task first.
2. Identify missing information.
3. Make reasonable assumptions only when necessary.
4. Provide executable steps.
5. Provide verification methods.

Output Format:
1. Conclusion
2. Analysis
3. Plan
4. Steps
5. Code / table / document if needed
6. Verification
7. Risks
8. Next steps

Quality Requirements:
- Do not be vague.
- Do not invent facts.
- State assumptions clearly.
- Provide practical and verifiable output.
```

---

## 6. Execution Steps

The Agent must follow this order:

```text
1. Preserve the user's original request.
2. Identify the real task goal.
3. Identify the target execution environment.
4. Identify missing information.
5. Extract useful background from available context.
6. Add a suitable expert role.
7. Add task background.
8. Add clear deliverables.
9. Add constraints and prohibited actions.
10. Add execution steps.
11. Add output format.
12. Add quality requirements.
13. Add verification method.
14. Generate the optimized prompt.
15. If useful, generate both short and full versions.
16. Provide usage advice.
```

---

## 7. Prompt Optimization Rules

When optimizing a prompt, improve these areas:

```text
1. Role clarity
2. Background completeness
3. Goal specificity
4. Input definition
5. Task decomposition
6. Constraint clarity
7. Output format
8. Quality criteria
9. Verification method
10. Risk and uncertainty handling
```

The Agent should not simply make the prompt longer.

The goal is:

```text
clearer
more executable
more constrained
more verifiable
```

---

## 8. Missing Information Rules

If information is missing, the Agent must not invent it.

Use these labels:

```text
Missing Information:
Information required but not provided.

Temporary Assumption:
A reasonable assumption based on available context.

Needs User Confirmation:
A point that affects the final result and should be confirmed by the user.
```

When the task can still proceed, generate the prompt with assumptions clearly marked.

---

## 9. Prohibited Actions

The Agent must not:

```text
1. Invent project facts.
2. Invent user preferences.
3. Invent file names or commands.
4. Hide uncertainty.
5. Turn one-time requirements into long-term preferences.
6. Generate an overly broad prompt with no boundaries.
7. Remove important user constraints.
8. Ignore the user's requested output format.
9. Produce a prompt that cannot be verified.
10. Claim the prompt is perfect when key information is missing.
```

---

## 10. Validation Checklist

Before finishing, the Agent must check:

```text
1. Does the prompt include a clear role?
2. Does it include task background?
3. Does it define the final goal?
4. Does it identify inputs?
5. Does it include constraints?
6. Does it include prohibited actions if needed?
7. Does it define output format?
8. Does it define quality requirements?
9. Does it include verification method?
10. Does it mark missing information?
11. Does it avoid invented facts?
12. Is it suitable for the target Agent or model?
```

If any item is missing, the Agent should either fix it or explain why it cannot be filled.

---

## 11. Closing Rule

After generating a prompt, the Agent should decide whether any long-term files need updating.

Usually update:

```text
context/TODO.md
```

if the prompt creates a new task.

Possibly update:

```text
context/USER_PREFERENCES.md
```

only if the user expressed a new long-term preference.

Possibly update:

```text
context/AGENT_LESSONS.md
```

only if the prompt issue reveals a repeatable Agent failure pattern.

Do not update long-term files merely because a prompt was generated.

---

## 12. Final Principle

The purpose of Prompt Engineering is not to make the prompt longer.

The purpose is to make the task:

```text
clear
bounded
executable
verifiable
reusable when needed
```

Final rule:

```text
A good prompt tells the Agent what to do, what not to do, what information to use, what to output, and how success will be verified.
```
