from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Format retrieved chunks with game labels and delimiters
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        if i > 0:
            context += "\n\n---\n\n"
        context += f"[{chunk['game']}]\n{chunk['text']}"

    # System prompt — grounding instruction (from spec)
    system_prompt = """You are a rules reference assistant. Answer ONLY by directly quoting or closely paraphrasing the retrieved rules. Use NO other knowledge, reasoning, or inference.

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
- ❌ "Unlike other games..." (comparative reasoning)"""

    # User message — context + query
    # Identify the primary game from the first chunk
    primary_game = retrieved_chunks[0]["game"] if retrieved_chunks else "Unknown"
    
    user_message = f"""Here are the retrieved rule sections:

{context}

---

Answer this question using ONLY the rules above: {query}

IMPORTANT: Start your response with [{primary_game}] before the answer. Example format:
[{primary_game}] Your answer text here."""

    # Call the LLM
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,  # Low temperature for factual grounding
    )

    response_text = response.choices[0].message.content
    
    # If the model invoked the "I don't have that information" fallback,
    # don't prepend a game tag — it's a meta-response, not a rule citation.
    if "I don't have that information in the loaded rulebooks" in response_text:
        return response_text
    
    return response_text
