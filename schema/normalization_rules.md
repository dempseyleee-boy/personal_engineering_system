# Normalization Rules

## Purpose
Define canonicalization for bilingual technical extraction scoring.

## Entity Normalization
- Normalize English/Chinese aliases to one canonical name only when the text or local context shows they refer to the same object.
- Strong signals include direct apposition, parentheses, slash forms, or repeated use in the same role with no competing referent.
- Keep original wording in `surface_form`.

## Numeric Normalization
- Convert `100k`, `1e5`, `10万` to a consistent numeric value when unambiguous.

## Unit Normalization
- Treat same-unit language variants such as `ms` and `毫秒` as aliases of the same unit.
- Treat distinct units such as `GB` and `GiB` as different units unless the source or scoring rule explicitly defines a conversion.

## Timestamp Normalization
- Prefer ISO-8601 in `normalized_iso8601`.
- If the date format is ambiguous, preserve text and leave normalization conservative.

## Action Normalization
- Use a verb-led canonical action phrase, for example `restart service` or `update config`.

## Constraint Normalization
- Remove superficial wording differences such as politeness, tense, or redundant lead-in text, but preserve polarity, threshold, scope, and exceptions.
