#!/usr/bin/env python3
"""Export learning items to an Anki-importable tab-separated (TSV) file.

Import into Anki: File > Import > select the .txt output, set field separator to Tab.
Fields: Front (question) | Back (answer) | Tags (topic)
"""
import argparse
import sys
from parse_items import parse_items


def main() -> None:
    parser = argparse.ArgumentParser(description="Export items to Anki TSV format.")
    parser.add_argument("file", nargs="?", default="items.md", help="Input file (default: items.md)")
    parser.add_argument("--topic", help="Filter by topic")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    items = parse_items(args.file)
    if args.topic:
        items = [i for i in items if i.get("topic", "").lower() == args.topic.lower()]

    if not items:
        print("No items found.", file=sys.stderr)
        sys.exit(1)

    out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    try:
        for item in items:
            front = item["q"].replace("\t", " ").replace("\n", " ")
            back = item["a"].replace("\t", " ").replace("\n", " ")
            tags = item.get("topic", "").replace(" ", "_")
            out.write(f"{front}\t{back}\t{tags}\n")
    finally:
        if args.output:
            out.close()

    if args.output:
        print(f"Exported {len(items)} item(s) to {args.output}")


if __name__ == "__main__":
    main()
