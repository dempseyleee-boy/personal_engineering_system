# Label Guidelines

## Purpose
Define how to create gold JSON for bilingual technical extraction samples.

## Labeling Principles
- Only label information directly supported by source text.
- Do not infer unstated entities or actions.
- Preserve bilingual surface forms when useful, but normalize canonical values separately.
- "Source supports it" means the text names it, states it, or gives a direct paraphrase with the same meaning.

## Field Rules
### doc_type
- Choose the closest predefined type: `bug_report`, `runbook`, `api_note`, `config_guide`, `incident_summary`, `experiment_note`, `deployment_instruction`, `spec_fragment`, `other`.

### entities
- Label concrete named items only.
- Label as entities: specific services, models, APIs, files, tables, fields, people, teams, environments, libraries, and named metrics.
- Do not label generic roles, unnamed systems, vague groups, or concepts unless the text names a specific object.
- Use `surface_form` for original text and `normalized_name` for canonical forms.

### parameters
- Extract explicit key/value pairs and config-like settings.
- Use `parameters` for settings such as flags, thresholds, versions, or mode selections.

### constraints
- Record hard requirements, prohibitions, or limits.
- Use `constraints` for rules about what must, must not, or cannot happen when no discrete key/value pair is stated.

### actions
- Record explicit required, planned, failed, or completed actions.
- Use `actions` for tasks or events with a clear verb. `status` is an annotation attribute of the action mention, not part of the canonical action identity.

### artifacts
- Record files, URLs, logs, commands, and config items.
- Use `artifacts` for referenced objects that can be inspected or executed. If the text tells someone to run a command, record the command as an artifact and the instruction itself as an action.

### timestamps
- Keep original text and normalize only when the source supports it.
- Normalize only when the text gives enough information to map to a specific date/time without guessing the missing parts.

### numeric_values
- Preserve raw value text and normalized numeric value when conversion is unambiguous.
- "Unambiguous" means the number format and unit are explicit enough that one reasonable normalized value exists.

## Hallucination Rule
- If the source does not support it, do not label it.
