# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[your answer here]
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
[{
    "text": "When you roll a 7, you must move the robber to any hex on the board. All players with more than 7 cards discard half their hand (rounded down). Then the player who rolled chooses one adjacent player and steals one card at random from them.",
    "game": "Catan",
    "distance": 0.187
}, 
"text" ← results["documents"][0][i] — the raw chunk text
"game" ← results["metadatas"][0][i]["game"] — extracted from the metadata dict stored during ingestion
"distance" ← results["distances"][0][i] — the cosine distance score (lower = more similar)]
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
[Since we are only passing one query (query_texts=[query]), you always use [0] to extract results for that single query, 
ChromaDB's query() method accepts multiples queries at once for batch efficiencey. The response structure accomodates all queries. ]
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
[I'd recommend: Return all n_results unconditionally, but include the distance scores for the LLM to interpret.,
Tradeoffs:
Approach	Pros	Cons
Filter by threshold (e.g., distance < 0.5)	✓ Prevents hallucination from weak matches<br>✓ No junk context confusing the LLM<br>✓ Honest signal of low confidence	✗ Hard to pick the right threshold<br>✗ Risk of 0 results (bad UX)<br>✗ With only 3 results, you can't afford to drop any
Return all n_results	✓ Always gives the LLM something to work with<br>✓ No threshold tuning needed<br>✓ LLM can weigh weak signals itself	✗ Noisy context could mislead the LLM<br>✗ No safety rail against poor matches                                       |
]
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: [How do you get out of Jail?]
Top result game: [Monopoly]
Distance score: [0.282]
Does it make sense? [Yes, it makes sense. The query "How do you get out of Jail?" semantically aligns with the Monopoly Jail rule chunk. While "Jail" is a key matching term, the embeddings capture the broader context—the question asks about a game mechanic, and the Monopoly chunk explains exactly that mechanic. A distance of 0.282 indicates good relevance, though not a perfect match (which would be closer to 0.0).]
```

**One thing about the query results that surprised you:**

```
[What surprises me is that my initial thought was about keyword matching like in the case of the query. In which both the query and the chunk have the same keyword "Jail." But it seems like that's not the only case, the embeddings rather capture a bigger picture or context about the query and relate it to the chunks, and that's what surprises me.]
```
