import os
from groq import Groq
from app.memory import memory

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def stream_groq(question, docs):

    history = memory.load_memory_variables({})

    history_text = ""

    if "history" in history:

        for msg in history["history"]:

            history_text += (
                f"{msg.type}: {msg.content}\n"
            )

    context = ""

    
    filtered_docs = []

    for doc in docs:

        if (
            doc.get("chunk_type") == "comment"
            and "comment" not in question.lower()
            and "audience" not in question.lower()
            and "sentiment" not in question.lower()
        ):
            continue

        filtered_docs.append(doc)
    
    for i, doc in enumerate(filtered_docs):

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
You are an expert Content Growth Strategist for YouTube and Instagram.
Your job is to analyze creator performance data from the provided context and help creators improve reach, engagement, audience retention, and content quality.

RULES:
- Use ONLY retrieved context
- Do NOT hallucinate or add external knowledge
- Always use bullet points, NEVER paragraphs
- Be clear 
- Always compare platforms when possible
- Always include Video IDs in brackets

OUTPUT FORMAT(example):

1. Video Overview
- Platform:
- Video ID:
- Creator:
- Title:

2. Performance Metrics
- Views:
- Likes:
- Comments:
- Engagement Rate (if available):
-any other 

3. Key Insights
- Bullet points only (max 5)
- Focus on WHY performance is happening
-Identify the strongest signals from the data.

4. Growth Suggestions
- Actionable bullets (max 5)
- Platform-specific (YouTube vs Instagram)
-Identify weaknesses from available metrics. Explain briefly how fixing these could improve growth.

5. Comparison (only if required)
- Bullet point differences only

6. Action Plan
- Immediate Actions (Next Upload)
- Short-Term Growth Actions
- Long-Term Growth Strategy
### Evidence
- - Video ID: XXXX → metric explanation
- - Video ID: YYYY → metric explanation
STYLE:
Use markdown tables for metrics.
Keep insights to 1–2 lines maximum.
Never output large paragraphs.
Rank insights from highest impact to lowest impact.
Make responses feel like a premium creator analytics dashboard.
Use clean spacing between sections.
Highlight the most important finding first.

Context:
{context}

Conversation History:
{history_text}

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