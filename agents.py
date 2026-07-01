import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from tools import search_web, scrape_url
from dotenv import load_dotenv
load_dotenv()

# --- Two-tier model strategy ---
# Tool-calling agents NEED the 70b model — smaller models hallucinate
# fake tool names (e.g. "brave_search") instead of using the real tools.
# Writer/critic chains don't use tools, so the cheaper 8b model works fine
# and saves the bulk of our token budget.

llm_tools = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    max_retries=2,
    request_timeout=30,
)

llm_text = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_retries=2,
    request_timeout=30,
)


def build_search_agent():
    return create_agent(
        model=llm_tools,
        tools=[search_web],
        system_prompt=(
            "You are a research search agent. You MUST use the 'search_web' tool "
            "to find information. Do NOT invent or hallucinate any other tool names. "
            "The ONLY tool available to you is 'search_web'. "
            "Call it with a clear, specific search query."
        ),
    )

def build_reader_agent():
    return create_agent(
        model=llm_tools,
        tools=[scrape_url],
        system_prompt=(
            "You are a web reader agent. You MUST use the 'scrape_url' tool "
            "to fetch content from URLs. Do NOT invent or hallucinate any other tool names. "
            "The ONLY tool available to you is 'scrape_url'. "
            "Call it with a valid URL from the search results."
        ),
    )

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system", "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human", """Write a detailed research report on the topic below.

        Topic: {topic}

        Research Gathered:
        {research}

        Structure the report as:
        - Introduction
        - Key Findings (minimum 3 well-explained points)
        - Conclusion
        - Sources (list all URLs found in the research)

        Be detailed, factual and professional."""
    ),
])

writer_chain = writer_prompt | llm_text | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    (
        "human", """Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ..."""
    ),
])

critic_chain = critic_prompt | llm_text | StrOutputParser()