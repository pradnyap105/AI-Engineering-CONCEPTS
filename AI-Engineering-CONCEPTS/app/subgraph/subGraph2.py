from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# =========================================================
# 1. STATE
# =========================================================

class AddState(TypedDict):
    a: int
    b: int
    sum: int
    result: str

# =========================================================
# 2. SUBGRAPH NODE
# =========================================================

def calculate_sum(state: AddState) -> dict:
    a = state["a"]
    b = state["b"]
    sum_val = a + b
    return {"sum": sum_val}

# =========================================================
# 3. CREATE SUBGRAPH
# =========================================================

sub_builder = StateGraph(AddState)
sub_builder.add_node("calculate_sum", calculate_sum)
sub_builder.add_edge(START, "calculate_sum")
sub_builder.add_edge("calculate_sum", END)
sum_graph = sub_builder.compile()

# =========================================================
# 4. MAIN GRAPH NODE
# =========================================================

def create_result(state: AddState) -> dict:
    sum_val = state["sum"]
    return {"result": f"The sum is {sum_val}"}

# =========================================================
# 5. CREATE MAIN GRAPH
# =========================================================

main_builder = StateGraph(AddState)
main_builder.add_node("sum_subgraph", sum_graph)
main_builder.add_node("result", create_result)
main_builder.add_edge(START, "sum_subgraph")
main_builder.add_edge("sum_subgraph", "result")
main_builder.add_edge("result", END)

# =========================================================
# 6. COMPILE MAIN GRAPH
# =========================================================

main_graph = main_builder.compile()

# =========================================================
# 7. INVOKE MAIN GRAPH
# =========================================================

result = main_graph.invoke({"a": 3, "b": 7})

# =========================================================
# 8. PRINT RESULT
# =========================================================

print("A:", result["a"])
print("B:", result["b"])
print("Sum:", result["sum"])
print("Result:", result["result"])
