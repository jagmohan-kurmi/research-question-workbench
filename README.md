# Research Question Workbench

A small offline-first CLI for capturing question components, checking missing fields and explicit contradictions, and exporting a transparent worksheet. It never scores novelty or research quality.

## Install and use

```console
python -m pip install .
research-question-workbench fixtures/sample.json --format markdown --output worksheet.md
research-question-workbench fixtures/sample.json --format json
```

Input JSON uses `question`, `pico`, `spider`, and `finer` (with optional `title`, `inclusion`, and `exclusion`). The CLI checks for the question, required framework prompts, and exact text overlaps between inclusion and exclusion lists. Exit codes are `0` (no structural findings), `1` (findings were exported), and `2` (invalid/unreadable input or output). All work is local; no network access is required.

## Scope and safeguards

This tool organizes researcher-supplied information; it does not make scientific judgments, replace domain expertise, or guarantee completeness or validity. Retain source files and review exported material before relying on it.

## Development

```console
python -m unittest discover -s tests -v
```
