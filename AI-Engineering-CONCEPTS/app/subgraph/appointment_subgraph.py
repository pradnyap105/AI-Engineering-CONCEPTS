from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional
# Define the state schema for the appointment validation subgraph
# Define the state schema for the appointment validation subgraph
class AppointmentState(TypedDict):
    patient_name: str
    appointment_date: str
    doctor_name: str
    date_valid: bool
    doctor_available: bool
    status: str
    final_message: Optional[str]

def check_date(state: AppointmentState):
    """Check if the appointment date is provided."""
    # In a real app, you would parse the date and check if it's in the future
    is_valid = bool(state.get("appointment_date"))
    print(f"[Subgraph] Checking date '{state.get('appointment_date')}': {'Valid' if is_valid else 'Invalid'}")
    return {"date_valid": is_valid}

def check_availability(state: AppointmentState):
    """Check if the requested doctor is available."""
    # Simulating availability check: only "Dr. Smith" is available
    doctor = state.get("doctor_name")
    is_available = doctor == "Dr. Smith"
    print(f"[Subgraph] Checking availability for '{doctor}': {'Available' if is_available else 'Unavailable'}")
    return {"doctor_available": is_available}

def validate(state: AppointmentState):
    """Validate the appointment based on date and availability."""
    if state.get("date_valid") and state.get("doctor_available"):
        status = "Confirmed"
    else:
        status = "Rejected"
    
    print(f"[Subgraph] Validating appointment: {status}")
    return {"status": status}

# Build the appointment validation subgraph
builder = StateGraph(AppointmentState)

# Add nodes
builder.add_node("check_date", check_date)
builder.add_node("check_availability", check_availability)
builder.add_node("validate", validate)

# Define the flow
builder.add_edge(START, "check_date")
builder.add_edge("check_date", "check_availability")
builder.add_edge("check_availability", "validate")
builder.add_edge("validate", END)

# Compile the subgraph
appointment_subgraph = builder.compile()
