from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State
class TempState(TypedDict):
    celsius: int
    fahrenheit: int

# 2. Nodes
def celsius_to_fahrenheit(state: TempState) -> dict:
    """Converts Celsius to Fahrenheit."""
    
    result = (state["celsius"] * 9/5) + 32
    
    return {
        "fahrenheit": result
    }


# 3. Create Graph
graph_builder = StateGraph(TempState)    

# 4. Add Node
graph_builder.add_node("convert", celsius_to_fahrenheit)

# 5. Add Edges
graph_builder.add_edge(START, "convert")
graph_builder.add_edge("convert", END)

# 6. Compile Graph
graph = graph_builder.compile()


# 7. Invoke
result = graph.invoke({
    "celsius": 25
})

print("Celsius:", result["celsius"])
print("Fahrenheit:", result["fahrenheit"])
