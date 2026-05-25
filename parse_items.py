#!/usr/bin/env python3
"""Parse items.md into structured JSON; supports topic filtering."""
import argparse
import json
import re
import sys
from pathlib import Path


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse learning items file to JSON.")
    parser.add_argument("file", nargs="?", default="items.md", help="Input file (default: items.md)")
    parser.add_argument("--topic", help="Filter by topic (case-insensitive)")
    parser.add_argument("--list-topics", action="store_true", help="Print all distinct topics")
    args = parser.parse_args()

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
