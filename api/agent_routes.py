from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from agent.banking_agent import BankingAgent
from config.logger_config import logger

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])

class AgentQueryRequest(BaseModel):
    query: str
    provider: str = Field(default="groq", description="LLM provider: 'groq' or 'ollama'")

class AgentQueryResponse(BaseModel):
    query: str
    response: str
    provider: str
    model: str

@router.post("/query", response_model=AgentQueryResponse)
def query_agent(request: AgentQueryRequest):
    try:
        agent = BankingAgent(provider=request.provider)
        answer = agent.run(request.query)
        return AgentQueryResponse(
            query=request.query,
            response=answer,
            provider=request.provider,
            model=agent.model_name
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error executing agent query ({request.provider}): {e}")
        raise HTTPException(status_code=500, detail=str(e))
