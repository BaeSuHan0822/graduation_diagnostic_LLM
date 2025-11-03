from langchain.agents import create_agent

def get_weather(city : str) -> str :
    """_summary_

    Args:
        city (str): _description_

    Returns:
        str: _description_
    """
    return f"It's always sunny in {city}"

agent = create_agent(
    model = "claude-sonnet-20240229",
    tools = [get_weather],
    system_prompt="You are a helpful assistant"
)

agent.invoke({
    "messages" : [{"role" : "user", "content" : "what is the weather in sf"}]
})