import re
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from rich import print
from typing import Generator

def _has_urls(text: str) -> bool:
    return bool(re.search(r'https?://\S+', text))

def run_research_pipeline(topic: str) -> Generator[tuple[int, dict], None, None]:
    if not topic or not topic.strip():
        yield 0, {"error": "Topic cannot be empty."}
        return

    topic = topic.strip()
    state = {}

    print("\n"+"="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": 
            [{
                "role": "user", 
                "content": f"Find recent, reliable and detailed information about: {topic}"
            }]
        }, {"recursion_limit": 8})
        raw = search_result['messages'][-1].content
        if not raw or raw.strip() == "":
            raw = "No search results found."
        state["search_result"] = raw
    except Exception as e:
        state["search_result"] = f"Search failed: {e}"
    print(state["search_result"])
    yield 1, state

    print("\n"+"="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    if not _has_urls(state.get("search_result", "")):
        state["scraped_result"] = "No URLs found in search results. Skipping scrape."
        print(state["scraped_result"])
    else:
        try:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages":[{
                    "role": "user", 
                    "content": f"""Based on the following search results about '{topic}', 
                    pick the most relevant URL and scrape it for deeper content.\n\n
                    Search Results:\n{state['search_result'][:800]}"""
                }]
            }, {"recursion_limit": 8})
            raw = reader_result['messages'][-1].content
            if not raw or raw.strip() == "":
                raw = "No content scraped."
            state["scraped_result"] = raw
        except Exception as e:
            state["scraped_result"] = f"Scraping failed: {e}"
        print(state["scraped_result"])
    yield 2, state

    print("\n"+"="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
    f"SEARCH RESULTS : \n {state['search_result']} \n\n"
    f"DETAILED SCRAPED CONTENT : \n {state.get('scraped_result', 'N/A')}"
    )

    try:
        state["report"] = writer_chain.invoke({
            "topic" : topic,
            "research" : research_combined
        })
    except Exception as e:
        state["report"] = f"Report generation failed: {e}"
    print(state["report"])
    yield 3, state

    print("\n"+"="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    try:
        state['feedback'] = critic_chain.invoke({
            "report" : state['report']
        })
    except Exception as e:
        state['feedback'] = f"Critic review failed: {e}"
    print(state['feedback'])
    yield 4, state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    for step, state in run_research_pipeline(topic):
        print(f"Step {step} complete.")
