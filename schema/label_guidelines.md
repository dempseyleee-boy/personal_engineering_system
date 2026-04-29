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
- Record concrete referenced objects such as files, URLs, logs, configs, tables, or named outputs.
- Use `artifacts` for objects that are treated as deliverables, inspectable references, persisted files, or explicit external resources.
- Do not automatically promote every verb object into `artifacts`.
- If the text says to run a script or command, keep the instruction in `actions`. Only also add an `artifact` when the script/command itself is treated as a named file or reusable object in the labeling policy for that sample set.
- For the current round-1 gold set, executable mentions like `run verify_cache.sh` should remain actions unless the script is explicitly labeled as an output/reference object in gold.
- Output files, logs, saved reports, configs, and retained files should still be labeled as `artifacts` when explicitly named.

### timestamps
- Keep original text and normalize only when the source supports it.
- Normalize only when the text gives enough information to map to a specific date/time without guessing the missing parts.

### numeric_values
- Preserve raw value text and normalized numeric value when conversion is unambiguous.
- "Unambiguous" means the number format and unit are explicit enough that one reasonable normalized value exists.

## Hallucination Rule
- If the source does not support it, do not label it.
