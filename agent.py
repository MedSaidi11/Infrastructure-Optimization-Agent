from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, END
from smolagents.mcp_client import MCPClient
from data_model import Anomalies, Recommendations, InfrastructureAnalysisState
from logger import logger
import json

class AgenticPipeline:
    def __init__(self, llm, tools: dict = None):
        self.llm = llm
        self.tools = tools
        
    def read_report(self, state: InfrastructureAnalysisState) -> InfrastructureAnalysisState:
        """Step 1: Read the infrastructure report from rapport.json"""
        logger.info("Step 1: Reading infrastructure report...")
        
        try:
            if "read_json_file" in self.tools:
                tool = self.tools["read_json_file"]
                result = tool(file_name="rapport.json")
                state["report_content"] = result
                state["current_step"] = "report_loaded"
                logger.success("Infrastructure report loaded successfully")
            else:
                raise Exception("read_json_file tool not found")
        except Exception as e:
            state["error"] = f"Failed to read report: {str(e)}"
            logger.error(f"Error reading report: {e}")
        
        return state

    def detect_anomalies(self, state: InfrastructureAnalysisState) -> InfrastructureAnalysisState:
        """Step 2: Detect anomalies in the infrastructure report"""
        logger.info("Step 2: Detecting anomalies...")
        
        if not state["report_content"]:
            state["error"] = "No report content available"
            return state
        
        try:
            if "detect_anomalies" in self.tools:
                tool = self.tools["detect_anomalies"]
                prompt = tool(report=state["report_content"])
                messages = [
                    (
                        "system",
                        "You are a helpful assistant that can analyze infrastructure reports and detect anomalies."
                    ),
                    (
                        "user",
                        prompt
                    )
                ]
                llm_with_structured_output = self.llm.with_structured_output(Anomalies)
                result = llm_with_structured_output.invoke(prompt)
                state["anomalies_json"] = result.model_dump()
                state["current_step"] = "anomalies_detected"
                logger.success("Anomalies analysis completed")
            else:
                raise Exception("detect_anomalies tool not found")
        except Exception as e:
            state["error"] = f"Failed to detect anomalies: {str(e)}"
            logger.error(f"Error detecting anomalies: {e}")
        
        return state

    def propose_optimizations(self, state: InfrastructureAnalysisState) -> InfrastructureAnalysisState:
        """Step 3: Propose optimization recommendations"""
        logger.info("Step 3: Proposing optimization recommendations...")
        
        if not state["report_content"]:
            state["error"] = "No report content available"
            return state
        
        try:
            if "propose_optimizations" in self.tools:
                tool = self.tools["propose_optimizations"]
                prompt = tool(report=state["report_content"])
                messages = [
                    (
                        "system",
                        "You are a helpful assistant that can analyze infrastructure reports and propose optimization recommendations."
                    ),
                    (
                        "user",
                        prompt
                    )
                ]
                llm_with_structured_output = self.llm.with_structured_output(Recommendations)
                result = llm_with_structured_output.invoke(prompt)
                state["optimizations_json"] = result.model_dump()
                state["current_step"] = "optimizations_proposed"
                logger.success("Optimization recommendations generated")
            else:
                raise Exception("propose_optimizations tool not found")
        except Exception as e:
            state["error"] = f"Failed to propose optimizations: {str(e)}"
            logger.error(f"Error proposing optimizations: {e}")
        
        return state

    def finalize_results(self, state: InfrastructureAnalysisState) -> InfrastructureAnalysisState:
        """Step 4: Finalize and present results"""
        logger.info("Step 4: Finalizing results...")
        
        state["current_step"] = "completed"
        
        logger.info("\n" + "="*80)
        logger.info("INFRASTRUCTURE ANALYSIS COMPLETE")
        logger.info("="*80)
        
        if state["anomalies_json"]:
            logger.info("\n ANOMALIES DETECTED:")
            try:
                anomalies_data = state["anomalies_json"]
                logger.info(f"   Summary: {anomalies_data.get('summary', 'N/A')}")
                logger.info(f"   Number of anomalies: {len(anomalies_data.get('anomalies', []))}")
                logger.info(f"   Full JSON: {json.dumps(anomalies_data, indent=2)}")
            except:
                logger.info(f"   Raw data: {state['anomalies_json']}")
        
        if state["optimizations_json"]:
            logger.info("\n OPTIMIZATION RECOMMENDATIONS:")
            try:
                opt_data = state["optimizations_json"] 
                logger.info(f"   Summary: {opt_data.get('summary', 'N/A')}")
                logger.info(f"   Number of recommendations: {len(opt_data.get('recommendations', []))}")
                logger.info(f"   Full JSON: {json.dumps(opt_data, indent=2)}")
            except:
                logger.info(f"   Raw data: {state['optimizations_json']}")
        
        logger.success("\n Analysis workflow completed successfully!")
        
        return state

    def should_continue(self, state: InfrastructureAnalysisState) -> str:
        """Determine the next step based on current state"""
        if state.get("error"):
            return "error"
        
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            return "read_report"
        elif current_step == "report_loaded":
            return "detect_anomalies"
        elif current_step == "anomalies_detected":
            return "propose_optimizations"
        elif current_step == "optimizations_proposed":
            return "finalize_results"
        elif current_step == "completed":
            return END
        else:
            return END
    
    def handle_error(self, state: InfrastructureAnalysisState) -> InfrastructureAnalysisState:
        """Handle errors in the workflow"""
        logger.error(f"Workflow error: {state['error']}")
        return state

    def create_workflow(self):
        workflow = StateGraph(InfrastructureAnalysisState)
        
        workflow.add_node("read_report", self.read_report)
        workflow.add_node("detect_anomalies", self.detect_anomalies)
        workflow.add_node("propose_optimizations", self.propose_optimizations)
        workflow.add_node("finalize_results", self.finalize_results)
        workflow.add_node("error", self.handle_error)
        
        workflow.set_entry_point("read_report")
        
        workflow.add_conditional_edges(
            "read_report",
            self.should_continue,
            {
                "detect_anomalies": "detect_anomalies",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "detect_anomalies",
            self.should_continue,
            {
                "propose_optimizations": "propose_optimizations",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "propose_optimizations",
            self.should_continue,
            {
                "finalize_results": "finalize_results",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "finalize_results",
            self.should_continue,
            {
                END: END
            }
        )
        
        workflow.add_edge("error", END)
        
        return workflow.compile()
    
    def __call__(self, initial_state):
        workflow = self.create_workflow()
        return workflow.invoke(initial_state)