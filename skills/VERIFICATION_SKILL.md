# VERIFICATION_SKILL.md

## 1. Skill Purpose

Use this Skill to verify whether an Agent task is actually complete, correct, and safe to consider finished.

This Skill helps the Agent:

```text
define completion criteria
choose verification methods
run or recommend validation steps
record verification results
mark unverified work honestly
identify risks
avoid claiming completion without evidence
```

This Skill does not replace testing tools.

It defines how verification should be planned, executed, and reported.

---

## 2. When to Use

Use this Skill when:

```text
1. The Agent generates or modifies files.
2. The Agent writes or changes code.
3. The Agent creates templates or Skill files.
4. The Agent updates project context files.
5. The Agent generates reports or documents.
6. The Agent proposes technical plans.
7. The Agent completes a task that affects future work.
8. The user asks whether something is done correctly.
```

Do not use full verification flow when:

```text
1. The user asks a simple concept question.
2. The answer is purely conversational.
3. The task has no deliverable or lasting output.
```

Even for simple tasks, the Agent should be honest about uncertainty.

---

## 3. Required Inputs

Before verifying, the Agent should read:

```text
task_context/CONTEXT_PACKAGE.md
task_context/TASK_CONTEXT.md
context/TEST_COMMANDS.md
context/TODO.md
context/CHANGELOG.md
```

If relevant, also read:

```text
context/PROJECT_CONTEXT.md
context/DECISION_LOG.md
context/USER_PREFERENCES.md
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

For code or project tasks, inspect:

```text
source files
test files
configuration files
build scripts
logs
generated outputs
```

---

## 4. Expected Outputs

The Agent should output a verification result containing:

```text
1. What was verified
2. Verification method
3. Commands run or recommended
4. Results
5. Unverified items
6. Risks
7. Completion status
8. Next steps
```

Recommended completion statuses:

```text
Verified
Partially Verified
Not Verified
Failed
Blocked
Not Applicable
```

---

## 5. Verification Types

Use the appropriate verification type.

### 5.1 Code Verification

Check:

```text
1. Does the code run?
2. Do tests pass?
3. Does lint or type check pass if available?
4. Was the change limited to the task scope?
5. Were unrelated files avoided?
6. Are errors handled?
7. Is the behavior consistent with the task goal?
```

### 5.2 Document Verification

Check:

```text
1. Does the document match the requested topic?
2. Is the structure clear?
3. Are sections complete?
4. Does it avoid unrelated project-specific content when it is a template?
5. Are placeholders used correctly?
6. Is the document reusable if intended as a template?
```

### 5.3 Template Verification

Check:

```text
1. Is the template generic?
2. Does it avoid concrete project facts?
3. Does it contain placeholders?
4. Does it explain when to use it?
5. Does it define what should and should not go inside?
6. Does it map clearly to the target generated file?
```

### 5.4 Skill Verification

Check:

```text
1. Does the Skill have a clear purpose?
2. Does it define when to use and when not to use?
3. Does it list required inputs?
4. Does it define expected outputs?
5. Does it give ordered execution steps?
6. Does it define prohibited actions?
7. Does it include a validation checklist?
8. Does it include a closing rule?
9. Is it concise enough for Agent execution?
```

### 5.5 Project Bootstrap Verification

Check:

```text
1. Were templates read?
2. Was project structure inspected?
3. Were target files generated or proposed?
4. Were existing files protected?
5. Were missing fields marked?
6. Were assumptions marked?
7. Was a bootstrap report generated?
8. Were templates kept free of project-specific facts?
```

### 5.6 Planning Verification

Check:

```text
1. Is the goal clear?
2. Are steps actionable?
3. Are dependencies identified?
4. Are risks stated?
5. Are outputs defined?
6. Is there a way to verify progress?
```

---

## 6. Execution Steps

The Agent must follow this order:

```text
1. Identify the task deliverable.
2. Identify completion criteria.
3. Identify available verification commands or methods.
4. Read TEST_COMMANDS.md if available.
5. Determine what can be automatically verified.
6. Determine what requires manual review.
7. Run safe verification commands if allowed.
8. If commands cannot be run, state why.
9. Compare output against task requirements.
10. Record verified items.
11. Record unverified items.
12. Record risks.
13. Assign completion status.
14. Suggest next steps.
15. Use TASK_CLOSING_CHECKLIST if long-term files should be updated.
```

---

## 7. Command Execution Rules

If commands are available in:

```text
context/TEST_COMMANDS.md
```

the Agent should use their risk level:

```text
Low:
Can run automatically if tools are available.

Medium:
Can run if safe and within task scope; otherwise ask or explain.

High:
Must ask user before running.

No:
Do not run automatically.
```

If commands are unavailable:

```text
Do not invent commands.
Suggest possible verification methods and mark them as proposed.
```

---

## 8. Completion Status Rules

Use these statuses honestly.

```text
Verified:
All required checks passed.

Partially Verified:
Some checks passed, but some could not be completed.

Not Verified:
No meaningful verification was performed.

Failed:
Verification was performed and failed.

Blocked:
Verification could not proceed due to missing files, tools, permissions, or information.

Not Applicable:
Verification does not apply to this task.
```

Do not say "complete" without a status.

---

## 9. Prohibited Actions

The Agent must not:

```text
1. Claim work is verified without running or explaining checks.
2. Invent test results.
3. Invent commands.
4. Ignore failed verification.
5. Hide unverified parts.
6. Treat file generation as proof of correctness.
7. Mark a task Verified when only the document was generated.
8. Run high-risk commands without confirmation.
9. Modify unrelated files during verification.
10. Skip verification for code changes when tests are available.
```

---

## 10. Verification Report Format

Use this output format:

```markdown
# Verification Report

## 1. Verification Target

```text
【What was verified】
```

## 2. Completion Criteria

```text
1. 【criterion 1】
2. 【criterion 2】
3. 【criterion 3】
```

## 3. Verification Methods

```text
1. 【method 1】
2. 【method 2】
3. 【method 3】
```

## 4. Commands Run

```bash
【command 1】
【command 2】
```

If no commands were run:

```text
No commands were run.
Reason:
【reason】
```

## 5. Results

```text
1. 【result 1】
2. 【result 2】
3. 【result 3】
```

## 6. Unverified Items

```text
1. 【unverified item 1】
2. 【unverified item 2】
```

If none:

```text
No known unverified items.
```

## 7. Risks

```text
1. 【risk 1】
2. 【risk 2】
```

If none:

```text
No obvious risks found.
```

## 8. Completion Status

```text
【Verified / Partially Verified / Not Verified / Failed / Blocked / Not Applicable】
```

## 9. Next Steps

```text
1. 【next step 1】
2. 【next step 2】
```
```

---

## 11. Validation Checklist

Before finishing, the Agent must check:

```text
1. Did I identify what needed verification?
2. Did I define completion criteria?
3. Did I check available commands?
4. Did I avoid inventing commands?
5. Did I run safe checks if available and allowed?
6. Did I clearly state if checks were not run?
7. Did I record unverified items?
8. Did I record risks?
9. Did I assign an honest completion status?
10. Did I avoid claiming full completion without evidence?
```

---

## 12. Closing Rule

After verification, use:

```text
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

to decide whether to update:

```text
context/TODO.md
context/CHANGELOG.md
context/TEST_COMMANDS.md
context/AGENT_LESSONS.md
```

Typical updates:

```text
TODO.md:
Update task status based on verification.

CHANGELOG.md:
Record verified or unverified file changes.

TEST_COMMANDS.md:
Add newly discovered reusable verification commands.

AGENT_LESSONS.md:
Record verification failures caused by Agent behavior.
```

Do not update long-term files merely because verification was attempted.

---

## 13. Final Principle

Verification is not a formality.

It is the boundary between:

```text
the Agent produced something
```

and:

```text
the result is reliable enough to use
```

Final rule:

```text
If it was not verified, say so clearly.
If it failed, say so clearly.
If it was partially verified, say exactly what remains unverified.
```
