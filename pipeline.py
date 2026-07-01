import time
import re
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def _invoke_with_retry(fn, input_data, max_retries=2):
    """Retry wrapper that handles Groq 429 rate limit errors with backoff."""
    for attempt in range(max_retries):
        try:
            return fn(input_data)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                # Try to extract wait time from the error message
                match = re.search(r"try again in (\d+)m([\d.]+)s", error_str, re.IGNORECASE)
                if match:
                    wait = int(match.group(1)) * 60 + float(match.group(2))
                else:
                    wait = 10 * (attempt + 1)  # fallback: 10s, 20s (was 60s, 120s)
                print(f"\n⚠️  Rate limited! Waiting {wait:.0f}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                raise  # re-raise non-rate-limit errors immediately
    # Final attempt — let it raise if it fails
    return fn(input_data)

def run_reseacrh_pipeline(topic: str) -> dict:
    state = {}

    print("\n"+"="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = _invoke_with_retry(search_agent.invoke, {
        "messages": 
        [{
            "role": "user", 
            "content": f"Find recent, reliable and detailed information about: {topic}"
        }]
    })
    state["search_result"] = search_result['messages'][-1].content
    print(state["search_result"])

    print("\n"+"="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = _invoke_with_retry(reader_agent.invoke, {
        "messages":[{
            "role": "user", 
            "content": f"""Based on the following search results about '{topic}', 
            pick the most relevant URL and scrape it for deeper content.\n\n
            Search Results:\n{state['search_result'][:800]}"""
        }]
    })
    state["scraped_result"] = reader_result['messages'][-1].content
    print(state["scraped_result"])

    print("\n"+"="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
    f"SEARCH RESULTS : \n {state['search_result']} \n\n"
    f"DETAILED SCRAPED CONTENT : \n {state['scraped_result']}"
    )

    state["report"] = _invoke_with_retry(writer_chain.invoke, {
        "topic" : topic,
        "research" : research_combined
    })
    print(state["report"])

    print("\n"+"="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state['feedback'] = _invoke_with_retry(critic_chain.invoke, {
        "report" : state['report']
    })
    print(state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_reseacrh_pipeline(topic)
