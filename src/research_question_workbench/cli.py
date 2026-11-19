import argparse
import json
import sys
from pathlib import Path

FIELDS = {
    "pico": ("population", "intervention", "comparison", "outcome"),
    "spider": ("sample", "phenomenon", "design", "evaluation", "research_type"),
    "finer": ("feasible", "interesting", "novel", "ethical", "relevant"),
}

def validate(data):
    if not isinstance(data, dict):
        raise ValueError("worksheet must be a JSON object")
    issues = []
    if not isinstance(data.get("question"), str) or not data["question"].strip():
        issues.append("missing question")
    for group, fields in FIELDS.items():
        values = data.get(group, {})
        if not isinstance(values, dict):
            issues.append(f"{group} must be an object")
            continue
        for field in fields:
            if not isinstance(values.get(field), str) or not values[field].strip():
                issues.append(f"missing {group}.{field}")
    for name in ("inclusion", "exclusion"):
        if name in data and (not isinstance(data[name], list) or not all(isinstance(x, str) for x in data[name])):
            issues.append(f"{name} must be a list of strings")
    included = {x.strip().casefold() for x in data.get("inclusion", []) if isinstance(x, str)} if isinstance(data.get("inclusion", []), list) else set()
    excluded = {x.strip().casefold() for x in data.get("exclusion", []) if isinstance(x, str)} if isinstance(data.get("exclusion", []), list) else set()
    issues.extend(f"contradiction: '{x}' appears in inclusion and exclusion" for x in sorted(included & excluded))
    return issues

def markdown(data, issues):
    lines = [f"# {data.get('title', 'Research question worksheet')}", "", f"Question: {data.get('question', '')}", ""]
    for group, fields in FIELDS.items():
        lines.extend([f"## {group.upper()}", ""])
        values = data.get(group, {})
        for field in fields:
            lines.append(f"- **{field.replace('_', ' ').title()}:** {values.get(field, '') if isinstance(values, dict) else ''}")
        lines.append("")
    for name in ("inclusion", "exclusion"):
        lines.extend([f"## {name.title()} criteria", ""])
        items = data.get(name, [])
        if isinstance(items, list): lines.extend(f"- {item}" for item in items)
        lines.append("")
    lines.extend(["## Structural checks", ""])
    lines.extend((f"- {i}" for i in issues) if issues else ["- No missing fields or explicit inclusion/exclusion overlaps found."])
    lines.extend(["", "These checks do not assess novelty, feasibility, ethics, or scientific merit."])
    return "\n".join(lines) + "\n"

def main(argv=None):
    parser = argparse.ArgumentParser(description="Build and check a PICO/SPIDER/FINER worksheet")
    parser.add_argument("input", help="input worksheet JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", help="output file (default: stdout)")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        issues = validate(data)
        output = json.dumps({"worksheet": data, "checks": issues}, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(data, issues)
        Path(args.output).write_text(output, encoding="utf-8", newline="\n") if args.output else sys.stdout.write(output)
        return 1 if issues else 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
