import math
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define State
class CircleState(TypedDict):
    radius: float
    area: float


# 2. Calculator Node
def calculate_area(state: CircleState) -> dict:
    radius = state["radius"]

    area = math.pi * radius * radius

    return {
        "area": round(area, 2)
    }


# 3. Build Graph
builder = StateGraph(CircleState)

builder.add_node("calculate_area", calculate_area)

builder.add_edge(START, "calculate_area")
builder.add_edge("calculate_area", END)

graph = builder.compile()


# 4. Run Graph
if __name__ == "__main__":

    result = graph.invoke({
        "radius": 5
    })

    print("Radius:", result["radius"])
    print("Area:", result["area"])