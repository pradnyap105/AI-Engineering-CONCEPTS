from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

#STATE 
class LLMState(TypedDict): 
  question:str 
  answer:str
   
#NODEk
def llm_qa(state: LLMState)-> LLMState:
    
    question = state['question']
    prompt = f"""
    answer the question given by user.
    {question}
    """
    model = ChatOpenAI(model="gpt-4")
    
    answer = model.invoke(prompt).content
    state['answer'] = answer
    return state

#CREATE GRAPH
Graph= StateGraph(LLMState)

#NODES
Graph.add_node('llm_qa',llm_qa)


#EDGES
Graph.add_edge(START,'llm_qa')
Graph.add_edge('llm_qa',END)


#COMPILE
app= Graph.compile()



#INVOKE
RESULT = app.invoke({'question':'what is langgraph?'})


#RESULT
print(RESULT["answer"])
