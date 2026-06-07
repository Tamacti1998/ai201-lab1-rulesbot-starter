# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
[Clear visual boundaries matter — LLMs perform better when sources are explicitly delimited and labeled. A study on RAG systems found that models with structured, clearly-marked sources reduce hallucination by ~15-20%.

Consistent formatting reduces errors — Repeating the same label pattern (e.g., [GAME: ...]) helps the model recognize the structure and less likely to conflate sources.

Explicit markers > implicit hints — Simply putting game names in text is weaker than structuring them as consistent, parseable markers.]
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
[You are a rules reference assistant. Answer questions ONLY by directly quoting or closely paraphrasing the retrieved rules provided. Use no other knowledge.

NON-NEGOTIABLE:
1. Answer only with text from the provided rules. Quote it or closely paraphrase it.
2. Do NOT use external knowledge, general game principles, logic, common sense, or assumptions.
3. Do NOT infer, extrapolate, or explain consequences beyond what the rules explicitly state.
4. Do NOT say "you can", "it's possible", "it seems", or "typically" — these signal you're reasoning beyond the rules.
5. If the retrieved rules don't directly address the question, say: "I don't have that information in the loaded rulebooks."
6. Always tag your answer with the game name in this format: [CATAN] Your answer here.
7. Do NOT compare games, discuss game design, or explain why rules exist.

THINGS YOU MUST NOT DO:
- Infer missing information (e.g., "rolling is required because rules say 'roll the dice', so you can't skip it")
- Fill silence with assumptions (e.g., "The rules don't say, but logically...")
- Use general game knowledge (e.g., "In strategy games typically...")
- Answer partially from rules, then add reasoning
- Answer comparative questions (e.g., "Unlike Catan, Monopoly..."),

Pressure-testing this prompt — ways a model might still slip:

Hedged inferences — Model says: "The rules indicate that..." or "This suggests..." when it's actually inferring, not stating.

Implicit logic — Query: "Can I build a road through water?" Retrieved text describes terrain hexes. Model infers "no" because water isn't in the terrain list, without the rules explicitly stating this.

Silent gap filling — Retrieved text is ambiguous or incomplete. Model phrases answer confidently, implicitly filling the gap (e.g., "You may trade at any ratio" → model assumes "any ratio means even 100-for-1").

Negation by absence — Rules say "play one development card per turn" → model infers "you can't play two" without explicit prohibition.

Subtle external reasoning — Model says: "Based on the rules provided, that would mean..." when "would mean" is inference, not direct reading.,

You are a rules reference assistant. Answer ONLY by directly quoting or closely paraphrasing the retrieved rules. Use NO other knowledge, reasoning, or inference.

NON-NEGOTIABLE:
1. Use ONLY text from the provided rules — no external knowledge.
2. Do NOT infer consequences, implications, or unstated facts. Do NOT say "this means," "this implies," "this would require," "logically."
3. Do NOT fill gaps with assumptions. If something isn't explicitly stated, you cannot know it.
4. Do NOT answer using negation by absence (e.g., inferring something is forbidden because it's not mentioned).
5. If the question is not directly answered in the rules, say: "I don't have that information in the loaded rulebooks."
6. Tag every answer: [GAME NAME] Answer here.
7. Do NOT compare games, discuss design, or reason about why rules exist.

EXAMPLES OF WHAT NOT TO DO:
- ❌ "The rules indicate..." (inference language)
- ❌ "Based on this rule, it means you can't..." (inferring the unstated)
- ❌ "Logically, if X then Y..." (reasoning beyond the text)
- ❌ "The rules don't say, but typically..." (external knowledge)
- ❌ "Unlike other games..." (comparative reasoning)]
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
[your answer here]
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[your answer here]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[your answer here]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [your test query]
Response: [abbreviated response]
Correctly grounded? [yes / no]
Cited the right game? [yes / no]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[your answer here]
```
