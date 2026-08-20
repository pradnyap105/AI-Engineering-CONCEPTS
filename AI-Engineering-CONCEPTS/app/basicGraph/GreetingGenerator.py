from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State
class UserState(TypedDict):
    name: str
    message: str

# 2. Nodes
def greeting_node(state: UserState) -> dict:
    return {"message": f"Hello, {state['name']}!"}

# 3. Builder
builder = StateGraph(UserState)
builder.add_node("greeting", greeting_node)
builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

graph = builder.compile()

# 7. Invoke
result = graph.invoke({
    "name": "Apurva"
})

print(result["message"])

