# Learning Items
#
# Format spec:
#   Items are separated by lines containing only "---".
#   Field names are case-insensitive: Q:, q:, TOPIC:, Topic: are all accepted.
#
# Required fields:
#   Q:     Question or prompt
#   A:     Answer or explanation
#
# Optional fields:
#   Topic: Category for grouping/filtering (default: uncategorized)
#   Ref:   Source reference or URL
#   Date:  Date added (YYYY-MM-DD)
#   Note:  Extra context or memory hints
#
# Multi-line values: indent continuation lines with two or more spaces.

Q: What are per layer embeddings (PLE)? How do they fit into the model architecture?
A: A model learns a separate, distinct embedding vector for each layer of the network,
  which is then injected into that layer's computation. At each layer ℓ, a learned
  embedding eℓ ∈ ℝ^d is added to the hidden states before or after the
  attention/MLP operations. One common pattern: hℓ = LayerNorm(hℓ-1 + eℓ)
Topic: architectures
Ref: arXiv:2601.10639; Gemma 3n model overview (https://ai.google.dev/gemma/docs/gemma-3n)
Date: 2026-05-25

---

Q: What is DeepSeek Engram?
A: They learn a lookup table of embeddings keyed by hashes of multiple tokens.
Topic: architectures
Ref: DeepSeek Gave LLMs a Real Memory (It's Not RAG) - YouTube (https://www.youtube.com/watch?v=87Q8nf1XHKA)
Date: 2026-05-25

---

Q: Is gut microbiome more diverse in patients with IBD or less diverse?
A: Less diverse.
Topic: microbiome
Ref: The Inflammatory Bowel Disease Multi'omics Database (https://ibdmdb.org/)
Date: 2026-05-25
