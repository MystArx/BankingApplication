import re
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from agent.tools import ALL_TOOLS
from config.settings import GROQ_API_KEY, DEFAULT_GROQ_MODEL, DEFAULT_OLLAMA_MODEL

SYSTEM_PROMPT = """You are an AI Banking Assistant for the Enterprise Banking Analytics Platform.
You have access to tools that fetch live data from the banking REST APIs and database.
Always use the appropriate tools to answer user queries accurately.
Be professional, concise, and helpful.
Do not output raw internal reasoning or thinking traces in the final response.
"""

def clean_reasoning_tags(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    if "</think>" in cleaned:
        cleaned = cleaned.split("</think>")[-1]
    return cleaned.strip()

class BankingAgent:
    def __init__(
        self,
        provider: str = "groq",
        model_name: Optional[str] = None,
        temperature: float = 0.0
    ):
        self.provider = provider.lower()
        self.tools_map = {tool.name: tool for tool in ALL_TOOLS}

        if self.provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is missing in your .env file. Please add GROQ_API_KEY=your_key in .env")
            model = model_name or DEFAULT_GROQ_MODEL
            self.llm = ChatGroq(model=model, groq_api_key=GROQ_API_KEY, temperature=temperature)
            self.model_name = model
        else:
            model = model_name or DEFAULT_OLLAMA_MODEL
            self.llm = ChatOllama(model=model, temperature=temperature)
            self.model_name = model

        self.llm_with_tools = self.llm.bind_tools(ALL_TOOLS)

    def run(self, query: str) -> str:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]

        response = self.llm_with_tools.invoke(messages)
        messages.append(response)

        max_iterations = 5
        iteration = 0

        while getattr(response, "tool_calls", None) and iteration < max_iterations:
            iteration += 1
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call.get("id", f"call_{iteration}")

                if tool_name in self.tools_map:
                    try:
                        tool_result = self.tools_map[tool_name].invoke(tool_args)
                    except Exception as e:
                        tool_result = f"Error executing {tool_name}: {str(e)}"
                else:
                    tool_result = f"Unknown tool: {tool_name}"

                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))

            response = self.llm_with_tools.invoke(messages)
            messages.append(response)

        return clean_reasoning_tags(response.content)
