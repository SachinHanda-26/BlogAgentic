from src.states.blogState import BlogState
from src.llms.groqllm import GroqLLM
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogState import TranslatedBlog

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
            prompt = f"""
               You are an expert blog writer.

               Generate a detailed and engaging blog about:
               {state['topic']}

        Requirements:
        - Write approximately 500-700 words.
        - Use clear headings and paragraphs.
        - Cover the important aspects of the topic.
        - Avoid unnecessary repetition.
        - Keep the content concise.
        """
            
            system_msg = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_msg)
            return {"blog":{"title": state['blog']['title'],"content": response.content}}
           
    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        Translate_prompt = """You are an expert translator. Translate the following blog content to {current_language}.
        - while maintaining the original meaning and tone.
        - Adapt cultural references and idioms to be appropriate for the {current_language}.
        
        ORIGINAL_CONTENT:
        {blog_content}
        """
        
        blog_content = state["blog"]["content"]
        message = [
            HumanMessage(Translate_prompt.format(current_language=state["current_language"], blog_content=blog_content))
        ]
        
        translate_content = (
            self.llm.with_structured_output(TranslatedBlog,
         method="json_schema", strict=True
           ).invoke(message)
)
        return {
            "blog": {
            "title": state["blog"]["title"],
            "content": translate_content.content
        }
         }
    
    def route(self, state: BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation node.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return  state["current_language"]
        