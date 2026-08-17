from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1.state

class NumberState(TypedDict):
    number: int
    result: str

# 2.node
def check_number(state:NumberState)-> dict:

    number = state["number"]
    if number % 2 ==0:
        result = "Even number"
    else:
        result = "Odd number"

    return {
        "result": result
    }  
   


# 3.StateGraph

graph_builder = StateGraph(NumberState)

# 4.add node
graph_builder.add_node("check_number", check_number)


# 5.add edges
graph_builder.add_edge(START, "check_number")
graph_builder.add_edge("check_number", END)


# 6.compile graph
graph = graph_builder.compile()


# 7.invoke graph

# 7. Invoke Graph
result = graph.invoke({
    "number": 10
})

# 8.print result
print("Number:", result["number"])
print("Result:", result["result"])