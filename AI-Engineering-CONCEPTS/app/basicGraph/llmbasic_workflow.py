from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Added missing import
from langgraph.graph import END, START, StateGraph

load_dotenv()


# STATE - Fixed syntax and indentation
class LLMState(TypedDict):
    question: str
    answer: str


# NODE
def llm_qa(state: LLMState) -> LLMState:
    question = state["question"]
    prompt = f"""
    answer the question given by user.
    {question}
    """
    model = ChatOpenAI(model="gpt-4o")  # Good practice to use gpt-4o

    answer = model.invoke(prompt).content
    state["answer"] = answer
    return state


# CREATE GRAPH
Graph = StateGraph(LLMState)

# NODES
Graph.add_node("llm_qa", llm_qa)

# EDGES
Graph.add_edge(START, "llm_qa")
Graph.add_edge("llm_qa", END)

# COMPILE
app = Graph.compile()

# INVOKE
RESULT = app.invoke({"question": "what is langgraph?"})

# PRINT RESULT - Added to view output
print(RESULT["answer"])
