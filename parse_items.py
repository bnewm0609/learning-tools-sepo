#!/usr/bin/env python3
"""Parse items.md into structured JSON; supports topic filtering."""
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = {"q", "a"}
KNOWN_FIELDS = {"q", "a", "topic", "ref", "date", "note"}


def parse_items(path: str = "items.md") -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"\n---\n", text)
    items = []
    for block in blocks:
        item = {}
        lines = [l for l in block.strip().splitlines() if not l.startswith("#")]
        current_key = None
        current_val_lines: list[str] = []
        for line in lines:
            m = re.match(r"^([A-Za-z]+):\s*(.*)", line)
            if m:
                if current_key:
                    item[current_key] = " ".join(current_val_lines).strip()
                current_key = m.group(1).lower()
                current_val_lines = [m.group(2).strip()]
            elif line.startswith(("  ", "\t")) and current_key:
                current_val_lines.append(line.strip())
        if current_key:
            item[current_key] = " ".join(current_val_lines).strip()
        if "q" in item and "a" in item:
            items.append(item)
    return items


def validate_items(path: str = "items.md") -> list[str]:
    """Check items.md for format errors; returns list of error messages."""
    text = Path(path).read_text(encoding="utf-8")
    errors = []
    sep = "\n---\n"
    pos = 0
    for block in text.split(sep):
        start_line = text[:pos].count("\n") + 1
        non_comment = [l for l in block.strip().splitlines() if not l.startswith("#")]
        fields: dict[str, int] = {}
        for line in non_comment:
            m = re.match(r"^([A-Za-z]+):\s*(.*)", line)
            if m:
                key = m.group(1).lower()
                fields[key] = fields.get(key, 0) + 1
                if fields[key] > 1:
                    errors.append(f"line ~{start_line}: duplicate field '{m.group(1).upper()}:'")
                if key not in KNOWN_FIELDS:
                    errors.append(f"line ~{start_line}: unknown field '{m.group(1)}:'")
                if key in REQUIRED_FIELDS and not m.group(2).strip():
                    errors.append(f"line ~{start_line}: required field '{m.group(1).upper()}:' has no value")
        if fields:
            for field in REQUIRED_FIELDS:
                if field not in fields:
                    errors.append(f"line ~{start_line}: item missing required field '{field.upper()}:'")
        pos += len(block) + len(sep)
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse learning items file to JSON.")
    parser.add_argument("file", nargs="?", default="items.md", help="Input file (default: items.md)")
    parser.add_argument("--topic", help="Filter by topic (case-insensitive)")
    parser.add_argument("--list-topics", action="store_true", help="Print all distinct topics")
    parser.add_argument("--validate", action="store_true", help="Validate format; exits 0 on success, 1 on errors")
    args = parser.parse_args()

    if args.validate:
        errors = validate_items(args.file)
        if errors:
            for err in errors:
                print(err, file=sys.stderr)
            sys.exit(1)
        print("OK")
        return

    items = parse_items(args.file)

    if args.list_topics:
        for t in sorted({i.get("topic", "uncategorized") for i in items}):
            print(t)
        return

    if args.topic:
        items = [i for i in items if i.get("topic", "").lower() == args.topic.lower()]

    json.dump(items, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
