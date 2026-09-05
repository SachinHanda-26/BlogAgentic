import uvicorn 
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## API's
app = FastAPI()

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    
    ## Get the LLM
    groqllm = GroqLLM()
    llm = groqllm.get_llm()
    
    ## Get the Graph
    graph_builder = GraphBuilder(llm)
    if topic:
        graph = graph_builder.setup_graph("topic")
        state = graph.invoke({"topic": topic})
        
        return {"data": state}
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)