from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogState import BlogState

class GraphBuilder:
    def __init__(self, llm: GroqLLM):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        
    def build_topic_graph(self):
        """
        Builds a graph to generate blogs based on topic.
        """
        
        ## Nodes
        self.graph.add_node("title_creation")
        self.graph.add_node("content_generation")
        
        ## Edges
        self.graph.set_entry_point("title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.set_exit_point("content_generation")
        
