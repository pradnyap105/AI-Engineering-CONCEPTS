from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# =========================================================
# 1. STATE
# =========================================================

class NumberState(TypedDict):
    number: int
    square: int
    result: str


# =========================================================
# 2. SUBGRAPH NODE
# =========================================================

def calculate_square(state: NumberState) -> dict:

    number = state["number"]

    square = number * number

    return {
        "square": square
    }


# =========================================================
# 3. CREATE SUBGRAPH
# =========================================================

sub_builder = StateGraph(NumberState)

sub_builder.add_node("calculate_square", calculate_square)

sub_builder.add_edge(START, "calculate_square")
sub_builder.add_edge("calculate_square", END)

# Compile the SUBGRAPH
square_graph = sub_builder.compile()


# =========================================================
# 4. MAIN GRAPH NODE
# =========================================================

def create_result(state: NumberState) -> dict:

    square = state["square"]

    return {
        "result": f"The square is {square}"
    }


# =========================================================
# 5. CREATE MAIN GRAPH
# =========================================================

main_builder = StateGraph(0)


# Add the SUBGRAPH as a node
main_builder.add_node("square_subgraph", square_graph)

# Add normal node
main_builder.add_node("result", create_result)


# =========================================================
# 6. MAIN GRAPH EDGES
# =========================================================

main_builder.add_edge(START, "square_subgraph")
main_builder.add_edge("square_subgraph", "result")
main_builder.add_edge("result", END)


# =========================================================
# 7. COMPILE MAIN GRAPH
# =========================================================

main_graph = main_builder.compile()


# =========================================================
# 8. INVOKE MAIN GRAPH
# =========================================================

result = main_graph.invoke({
    "number": 5
})


# =========================================================
# 9. PRINT RESULT
# =========================================================

print("Number:", result["number"])
print("Square:", result["square"])
print("Result:", result["result"])