# Memory

## Durable
- items.md format: each item starts with '- Q:' / '- A:', plus optional 'topic:', 'ref:', 'date:' sub-fields; parse_items.py is authoritative parser
- Multi-stage issues use sub-orchestrator children (one per stage) with stacked branches; each stage's PR targets the previous stage's branch, not main
