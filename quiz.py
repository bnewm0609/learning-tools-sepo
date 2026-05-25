#!/usr/bin/env python3
"""Visualize and quiz learning items interactively."""
import argparse
import random
import sys
from collections import defaultdict
from parse_items import parse_items


def show_by_topic(items: list[dict]) -> None:
    by_topic: dict[str, list] = defaultdict(list)
    for item in items:
        by_topic[item.get("topic", "uncategorized")].append(item)
    for topic in sorted(by_topic):
        group = by_topic[topic]
        print(f"\n== {topic} ({len(group)} items) ==")
        for idx, item in enumerate(group, 1):
            print(f"  {idx}. Q: {item['q']}")
            print(f"     A: {item['a']}")
            if "ref" in item:
                print(f"     Ref: {item['ref']}")


def run_quiz(items: list[dict], shuffle: bool = True) -> None:
    if shuffle:
        random.shuffle(items)
    correct = 0
    for idx, item in enumerate(items, 1):
        print(f"\n[{idx}/{len(items)}] Q: {item['q']}")
        if "topic" in item:
            print(f"  Topic: {item['topic']}")
        input("  Press Enter to reveal answer...")
        print(f"  A: {item['a']}")
        if "ref" in item:
            print(f"  Ref: {item['ref']}")
        rating = input("  Did you know it? [y/n]: ").strip().lower()
        if rating == "y":
            correct += 1
    pct = (100 * correct // len(items)) if items else 0
    print(f"\nResult: {correct}/{len(items)} correct ({pct}%)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Quiz and visualize learning items.")
    parser.add_argument("file", nargs="?", default="items.md", help="Input file (default: items.md)")
    parser.add_argument("--topic", help="Filter by topic")
    parser.add_argument("--list", action="store_true", help="List items grouped by topic instead of quizzing")
    parser.add_argument("--no-shuffle", action="store_true", help="Keep original item order")
    args = parser.parse_args()

    items = parse_items(args.file)
    if args.topic:
        items = [i for i in items if i.get("topic", "").lower() == args.topic.lower()]

    if not items:
        print("No items found.")
        sys.exit(1)

    if args.list:
        show_by_topic(items)
    else:
        run_quiz(items, shuffle=not args.no_shuffle)


if __name__ == "__main__":
    main()
