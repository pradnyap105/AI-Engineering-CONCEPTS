from typing import TypedDict
from langgraph.graph import GraphBuilder,START,END


# 1. State
class studentState(TypedDict):
    score:float
    result:str | None

# 2. Node
def result(state:studentState) -> dict:

    if state["score"] >=50:
        state["result"] = "Pass"
    else:
        state["result"] = "Fail"
    return state

builder = GraphBuilder()
builder.add_node("result",result)
builder.add_edge(START, "result")
builder.add_edge("result", END)

workflow = builder.compile()
# 3. Edges
    
result = workflow.invoke({"score":65})
print(result)