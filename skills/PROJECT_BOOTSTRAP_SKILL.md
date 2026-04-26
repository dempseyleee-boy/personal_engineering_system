# PROJECT_BOOTSTRAP_SKILL.md

## 1. Skill Purpose

Use this Skill to initialize a project with the Personal Engineering Optimization System.

This Skill guides the Agent to:

```text
read templates/
scan the current project
generate project-specific context files
generate task context files
generate a bootstrap report
```

This Skill does not store project-specific facts itself.

Project-specific facts must be written to:

```text
context/
task_context/
reports/
```

Generic structures must remain in:

```text
templates/
```

---

## 2. When to Use

Use this Skill when:

```text
1. The project is being initialized for the first time.
2. The project does not have a context/ directory.
3. The project does not have PROJECT_CONTEXT.md.
4. The user asks to initialize project context.
5. The user asks to generate project files from templates.
6. The user asks to set up the personal engineering optimization system for a project.
```

Do not use this Skill when:

```text
1. The user is asking a simple question.
2. The user only wants a concept explanation.
3. The project has already been initialized and the task is local.
4. The user explicitly says not to generate files.
```

---

## 3. Required Inputs

Before executing this Skill, the Agent should read:

```text
00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md
templates/00_TEMPLATE_LIBRARY_INDEX.md
```

Then read the required templates:

```text
templates/context/10_PROJECT_CONTEXT_TEMPLATE.md
templates/context/11_USER_PREFERENCES_TEMPLATE.md
templates/context/12_DECISION_LOG_TEMPLATE.md
templates/context/13_TODO_TEMPLATE.md
templates/context/14_TEST_COMMANDS_TEMPLATE.md
templates/context/15_CHANGELOG_TEMPLATE.md
templates/context/16_AGENT_LESSONS_TEMPLATE.md
templates/task_context/20_CONTEXT_PACKAGE_TEMPLATE.md
templates/task_context/21_TASK_CONTEXT_TEMPLATE.md
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

The Agent should also inspect available project files such as:

```text
README.md
AGENTS.md
CLAUDE.md
.cursor/rules/
package.json
pyproject.toml
requirements.txt
Makefile
CMakeLists.txt
build.gradle
Cargo.toml
go.mod
Dockerfile
docker-compose.yml
docs/
src/
tests/
scripts/
config/
```

If these files do not exist, the Agent must continue with available information and mark missing information clearly.

---

## 4. Expected Outputs

The Agent should generate or propose the following project-specific files.

### 4.1 Long-term Context Files

```text
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
context/TODO.md
context/TEST_COMMANDS.md
context/CHANGELOG.md
context/AGENT_LESSONS.md
```

### 4.2 Task Context Files

```text
task_context/CONTEXT_PACKAGE.md
task_context/TASK_CONTEXT.md
```

### 4.3 Report File

```text
reports/PROJECT_BOOTSTRAP_REPORT.md
```

If file writing is not available, the Agent should output the proposed file contents for the user to copy.

---

## 5. Execution Steps

The Agent must follow this order:

```text
1. Read the system entry file.
2. Read the template library index.
3. Scan the current project structure.
4. Identify existing context, task_context, templates, skills, and reports directories.
5. Check whether target files already exist.
6. Do not overwrite existing files unless the user explicitly allows it.
7. Read the required templates.
8. Fill templates using real project information.
9. Mark unknown information as "待补充".
10. Mark inferred information as "临时假设".
11. Generate missing project-specific files.
12. Generate task_context/CONTEXT_PACKAGE.md for the bootstrap task.
13. Generate task_context/TASK_CONTEXT.md for the bootstrap task.
14. Generate reports/PROJECT_BOOTSTRAP_REPORT.md.
15. Run the validation checklist before finishing.
16. Use TASK_CLOSING_CHECKLIST to decide which long-term files should be updated.
```

---

## 6. File Generation Rules

### 6.1 Template Files

```text
templates/ contains generic structures only.
```

The Agent must not write project-specific content into template files.

### 6.2 Context Files

```text
context/ contains long-term project facts.
```

These files should be generated from templates and filled with real project information.

### 6.3 Task Context Files

```text
task_context/ contains current-task information.
```

These files are temporary or task-specific.

### 6.4 Report Files

```text
reports/ contains generated reports.
```

Bootstrap results, missing information, assumptions, and next steps should be recorded here.

---

## 7. Existing File Rules

If a target file already exists, the Agent must:

```text
1. Read the existing file.
2. Compare it with the relevant template.
3. Identify missing sections.
4. Suggest updates.
5. Avoid overwriting unless the user explicitly allows it.
```

Default behavior:

```text
Do not overwrite existing long-term context files.
```

Allowed only when the user says:

```text
overwrite
rebuild
regenerate
replace with template
start fresh
```

---

## 8. Missing Information Rules

If information is missing, the Agent must not invent it.

Use the following labels:

```text
待补充：
Information that is missing and should be provided later.

临时假设：
Information inferred from available context but not confirmed.

需要用户确认：
Information that affects important project direction and should be confirmed.
```

The Agent should still generate useful draft files when possible.

---

## 9. Prohibited Actions

The Agent must not:

```text
1. Invent project goals.
2. Invent user preferences.
3. Invent test commands.
4. Invent historical decisions.
5. Overwrite existing context files without explicit permission.
6. Write project-specific facts into templates/.
7. Treat one-time task requirements as long-term preferences.
8. Put ordinary TODO items into DECISION_LOG.md.
9. Put long-term project background into TODO.md.
10. Put changelog details into PROJECT_CONTEXT.md.
11. Claim the project is fully initialized when required files are missing.
12. Claim commands were verified if they were not run.
```

---

## 10. Required File Mapping

The Agent should use this mapping:

```text
templates/context/10_PROJECT_CONTEXT_TEMPLATE.md
  -> context/PROJECT_CONTEXT.md

templates/context/11_USER_PREFERENCES_TEMPLATE.md
  -> context/USER_PREFERENCES.md

templates/context/12_DECISION_LOG_TEMPLATE.md
  -> context/DECISION_LOG.md

templates/context/13_TODO_TEMPLATE.md
  -> context/TODO.md

templates/context/14_TEST_COMMANDS_TEMPLATE.md
  -> context/TEST_COMMANDS.md

templates/context/15_CHANGELOG_TEMPLATE.md
  -> context/CHANGELOG.md

templates/context/16_AGENT_LESSONS_TEMPLATE.md
  -> context/AGENT_LESSONS.md

templates/task_context/20_CONTEXT_PACKAGE_TEMPLATE.md
  -> task_context/CONTEXT_PACKAGE.md

templates/task_context/21_TASK_CONTEXT_TEMPLATE.md
  -> task_context/TASK_CONTEXT.md
```

---

## 11. Bootstrap Report Requirements

The bootstrap report should include:

```text
1. Bootstrap date.
2. Project scan summary.
3. Files generated.
4. Existing files not overwritten.
5. Missing information.
6. Temporary assumptions.
7. Questions requiring user confirmation.
8. Risks.
9. Suggested next steps.
```

Recommended path:

```text
reports/PROJECT_BOOTSTRAP_REPORT.md
```

---

## 12. Validation Checklist

Before finishing, the Agent must check:

```text
1. Did I read the system entry file?
2. Did I read the template library index?
3. Did I inspect the project structure?
4. Did I check for existing target files?
5. Did I avoid overwriting existing files without permission?
6. Did I generate or propose PROJECT_CONTEXT.md?
7. Did I generate or propose USER_PREFERENCES.md?
8. Did I generate or propose DECISION_LOG.md?
9. Did I generate or propose TODO.md?
10. Did I generate or propose TEST_COMMANDS.md?
11. Did I generate or propose CHANGELOG.md?
12. Did I generate or propose AGENT_LESSONS.md?
13. Did I generate or propose CONTEXT_PACKAGE.md?
14. Did I generate or propose TASK_CONTEXT.md?
15. Did I generate or propose PROJECT_BOOTSTRAP_REPORT.md?
16. Did I mark missing information?
17. Did I mark temporary assumptions?
18. Did I avoid inventing project facts?
19. Did I avoid polluting templates with project facts?
20. Did I provide next steps?
```

If any item is not completed, the Agent must explain why.

---

## 13. Closing Rule

After project bootstrap, the Agent must use:

```text
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

to decide whether to update:

```text
context/TODO.md
context/CHANGELOG.md
context/DECISION_LOG.md
context/AGENT_LESSONS.md
```

Typical updates after bootstrap:

```text
TODO.md:
Record next setup or review tasks.

CHANGELOG.md:
Record generated context and task_context files.

DECISION_LOG.md:
Record any confirmed initialization or structure decisions.

AGENT_LESSONS.md:
Only update if Agent behavior problems occurred.
```

---

## 14. Final Principle

The purpose of this Skill is not to finish all project planning.

The purpose is to create a reliable starting context system so future Agent tasks can work from project files instead of relying on temporary chat memory.

Final rule:

```text
Templates define structure.
Context files store project facts.
Task context files store current task facts.
Reports store generated summaries.
Skills define Agent behavior.
```
