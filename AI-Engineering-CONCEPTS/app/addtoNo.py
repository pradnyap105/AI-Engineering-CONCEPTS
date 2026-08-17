from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State
class NumberState(TypedDict):
    a: int
    b: int
    result: int


# 2. Node
def add_numbers(state: NumberState) -> dict:
    result = state["a"] + state["b"]

    return {
        "result": result
    }

# 3. Create Graph
graph_builder = StateGraph(NumberState)    

# 4. Add Node
graph_builder.add_node("add_numbers", add_numbers)


# 5. Add Edges
graph_builder.add_edge(START, "add_numbers")
graph_builder.add_edge("add_numbers", END)

# 6. Compile Graph
graph = graph_builder.compile()    


# 7. Invoke
result = graph.invoke({
    "a": 10,
    "b": 20
})

print("Result:", result["result"])