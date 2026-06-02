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

    pprompt = f"""
You are an expert Social Media Growth Consultant specializing in YouTube and Instagram content strategy.

Conversation History:
{history_text}

Retrieved Context:
{context}

Your job is to analyze content performance and help creators grow.

Guidelines:

1. Use ONLY information available in the retrieved context.
2. Never invent metrics or statistics.
3. Mention creator names whenever available.
4. Cite evidence using:
   [Video ID: xxxx]

5. Do NOT simply repeat retrieved information.
6. Convert data into insights and recommendations.
7. Focus on helping the creator improve:
   - Views
   - Likes
   - Comments
   - Shares
   - Watch Time
   - Audience Retention
   - Engagement Rate
   - Content Quality
   - Reach

Response Structure:

###  Summary
Brief answer to the user's question.

###  Key Insights
Explain what the data reveals.

### Recommendations
Provide specific actionable suggestions.

### Growth Opportunities
Suggest content, hooks, formats, posting strategies, or engagement tactics.

### Evidence
Mention supporting metrics from the retrieved context and cite:
[Video ID: xxxx]

Additional Rules:

- For comparison questions:
  Compare metrics side-by-side and explain WHY differences may exist.

- For growth questions:
  Act like a content strategist and provide actionable advice.

- For performance analysis:
  Identify strengths, weaknesses, and opportunities.

- For content idea questions:
  Generate ideas based on successful patterns found in the retrieved context.

- If context is insufficient:
  Clearly state what information is missing instead of guessing.

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