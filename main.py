from langchain_mistralai import ChatMistralAI
from smolagents.mcp_client import MCPClient
from data_model import Anomalies, Recommendations, InfrastructureAnalysisState
from agent import AgenticPipeline
from logger import logger
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatMistralAI(
    model="mistral-large-latest",
    max_retries=3  
)

mcp = MCPClient([{"url": "http://localhost:8000/sse"}], structured_output=False)
tools = {tool.name: tool for tool in mcp.get_tools()}

initial_state = {
        "report_content": None,
        "anomalies_json": None,
        "optimizations_json": None,
        "current_step": "start",
        "error": None
    }

pipeline = AgenticPipeline(llm=llm, tools=tools)

if __name__ == "__main__":
    logger.info("Starting Infrastructure Analysis Workflow")
    logger.info("="*50)    
    
    final_state = pipeline(initial_state=initial_state)
    
    with open("output.json", "w") as f:
        output = {
            **final_state.get("anomalies_json"),
            **final_state.get("optimizations_json"),
        }
        json.dump(output, f, indent=4)
    
    logger.info("\n🎯 Final Results:")
    logger.info(f"   Status: {'Success' if not final_state.get('error') else 'Failed'}")
    if final_state.get("error"):
        logger.error(f"   Error: {final_state['error']}")
