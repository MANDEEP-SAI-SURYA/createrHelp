import os
from groq import Groq
from app.memory import memory

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_groq(question, docs):

    history = memory.load_memory_variables({})

    history_text = ""

    if "history" in history:

        for msg in history["history"]:

            history_text += (
                f"{msg.type}: {msg.content}\n"
            )

    context = ""

    for i, doc in enumerate(docs):

        context += f"""
Source {i+1}

Video ID: {doc.get("video_id")}
Type: {doc.get("chunk_type")}
Creator: {doc.get("creator")}

Text:
{doc.get("text")}

--------------------------------
"""

    prompt = f"""
You are a YouTube analytics expert.

Conversation History:
{history_text}

Retrieved Context:
{context}

Instructions:

- Use ONLY the retrieved context.
- If comparing videos, compare:
  - engagement rate
  - creator statistics
  - hook quality
  - content structure
- Mention the creator whenever available.
- Mention engagement rate whenever available.
- Cite evidence using:
  [Video ID: xxxx]
- If information is missing, say so.

Question:
{question}
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    stream=True
)

    answer = ""

    for chunk in response:

        if (
            chunk.choices
            and chunk.choices[0].delta.content
        ):

            token = chunk.choices[0].delta.content

            answer += token

    memory.save_context(
        {"input": question},
        {"output": answer}
    )

    sources = []

    for doc in docs:

        sources.append(
            f"Video ID: {doc.get('video_id')} | "
            f"Type: {doc.get('chunk_type')}"
        )

    answer += "\n\nSources:\n"
    answer += "\n".join(set(sources))

    return answer


def stream_groq(question, docs):

    history = memory.load_memory_variables({})

    history_text = ""

    if "history" in history:

        for msg in history["history"]:

            history_text += (
                f"{msg.type}: {msg.content}\n"
            )

    context = ""

    for i, doc in enumerate(docs):

        context += f"""
Source {i+1}

Video ID: {doc.get("video_id")}
Type: {doc.get("chunk_type")}
Creator: {doc.get("creator")}

Text:
{doc.get("text")}

--------------------------------
"""

    prompt = f"""
You are a YouTube analytics expert.

Conversation History:
{history_text}

Retrieved Context:
{context}

Instructions:

- Use ONLY the retrieved context.
- Mention creator when available.
- Cite sources using [Video ID: xxxx]

Question:
{question}
"""

    
    print("Retrieved Docs:")
    for doc in docs:
        print(doc)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in response:

        if (
            chunk.choices
            and chunk.choices[0].delta.content
        ):
            yield chunk.choices[0].delta.content