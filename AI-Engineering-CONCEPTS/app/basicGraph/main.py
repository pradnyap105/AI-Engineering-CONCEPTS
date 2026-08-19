from langgraph.graph import StateGraph, START, END
from appointment_subgraph import appointment_subgraph, AppointmentState

# The main graph can use the same state schema if it shares the properties
# or a different one that includes the subgraph's state. We'll reuse AppointmentState for simplicity.
class MainState(AppointmentState):
    pass

def generate_message(state: MainState):
    """Generate the final appointment message based on the status."""
    if state.get("status") == "Confirmed":
        msg = f"Success: Appointment confirmed for {state['patient_name']} with {state['doctor_name']} on {state['appointment_date']}."
    else:
        msg = f"Failed: Appointment rejected for {state['patient_name']}. Please check the date or choose another doctor."
    
    print(f"[Main Graph] Generating message: {msg}")
    return {"final_message": msg}

# Build the main graph
main_builder = StateGraph(MainState)

# Add the compiled subgraph as a node
main_builder.add_node("appointment_subgraph", appointment_subgraph)
main_builder.add_node("generate_message", generate_message)

# Define the flow
main_builder.add_edge(START, "appointment_subgraph")
main_builder.add_edge("appointment_subgraph", "generate_message")
main_builder.add_edge("generate_message", END)

# Compile the main graph
main_graph = main_builder.compile()

if __name__ == "__main__":
    # Test case 1: Successful appointment
    print("--- Test Case 1 ---")
    initial_state_1 = {
        "patient_name": "Alice",
        "appointment_date": "2026-09-01",
        "doctor_name": "Dr. Smith",
    }
    result_1 = main_graph.invoke(initial_state_1)
    print(f"\nFinal State: {result_1['final_message']}\n")

    # Test case 2: Rejected appointment (Doctor unavailable)
    print("--- Test Case 2 ---")
    initial_state_2 = {
        "patient_name": "Bob",
        "appointment_date": "2026-09-02",
        "doctor_name": "Dr. Jones",
    }
    result_2 = main_graph.invoke(initial_state_2)
    print(f"\nFinal State: {result_2['final_message']}\n")
