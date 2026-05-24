from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from config import GROQ_API_KEY
from tools import get_weather, get_news


def create_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.25,
        max_tokens=1200,
    )

    tools = [get_weather, get_news]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert City Intelligence Analyst for a premium SaaS dashboard.

Your job is to deliver accurate, actionable insights using live tools only.

STRICT RULES:
- For any weather question → ALWAYS call get_weather first.
- For any news, current events or local updates → ALWAYS call get_news.
- For travel safety, "is it safe", or combined queries → ALWAYS call BOTH tools.
- Never invent data, dates, or statistics.
- After receiving tool results (JSON), synthesize a clear, professional final answer.
- For safety queries, explicitly state a verdict in the first line: SAFE, CAUTION ADVISED, or AVOID / HIGH RISK, followed by 2-4 concise bullet reasons and practical advice.
- Keep final answers concise yet insightful. Use short paragraphs and bullets.
- Always ground every claim in the tool data provided.
"""
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,   # important for rich UI + transparency
    )

    return executor
