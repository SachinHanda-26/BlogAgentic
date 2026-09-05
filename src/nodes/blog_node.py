from src.states.blogState import BlogState
from src.llms.groqllm import GroqLLM

class BlogNode:
    """
    A class to represent blog node
    """
    def __init__(self, llm:GroqLLM):
        self.llm = llm
        
    def title_creation(self, state: BlogState):
        """
        Generates a title for the blog based on the topic.
        """
        if "topic" in state and state["topic"]:
            prompt = f"You are an expert blog writer. Generate a catchy and engaging title for a blog about the following topic: {state['topic']}"
            
            system_msg = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_msg)
            return {"blog":{"title": response.content}}
        
    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = f"You are an expert blog writer. Generate a detailed and engaging blog content for the following topic: {state['topic']}"
            
            system_msg = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_msg)
            return {"blog":{"title": state['blog']['title'],"content": response.content}}
           