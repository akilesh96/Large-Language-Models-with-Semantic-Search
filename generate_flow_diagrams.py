from graphviz import Digraph

def create_old_process_flow():
    dot = Digraph("Old_Process", format="png")
    
    # Nodes
    dot.node("A", "Start")
    dot.node("B", "Function Called\n(dbname, DataFrame, dbserver_instance)")
    dot.node("C", "Chunk DataFrame")
    dot.node("D", "Call Second Function")
    dot.node("E", "Save Chunked Data as CSV\n(Temp Path)")
    dot.node("F", "Use Subprocess to Push CSV\nto SQL using BCP")
    dot.node("G", "End")

    # Edges
    dot.edge("A", "B")
    dot.edge("B", "C")
    dot.edge("C", "D")
    dot.edge("D", "E")
    dot.edge("E", "F")
    dot.edge("F", "G")

    # Save
    dot.render("old_process_flow")

def create_new_process_flow():
    dot = Digraph("New_Process", format="png")
    
    # Nodes
    dot.node("A", "Start")
    dot.node("B", "Function Called\n(dbname, DataFrame, dbserver_instance)")
    dot.node("C", "Chunk DataFrame")
    dot.node("D", "Call Second Function")
    dot.node("E", "Save Data as CSV & Push to SQL using BCP")
    
    dot.node("F", "MemoryError or OSError(Errno 12)?", shape="diamond")
    dot.node("G", "Retry Up to 5 Times\nwith 5 min Sleep", shape="parallelogram")
    dot.node("H", "Other Exception?\n(Send to Parent Process)", shape="parallelogram")

    dot.node("I", "BCP Success?", shape="diamond")
    dot.node("J", "Multiprocessing Pipe to\nSend Exceptions to Parent Process")
    dot.node("K", "End")

    # Edges
    dot.edge("A", "B")
    dot.edge("B", "C")
    dot.edge("C", "D")
    dot.edge("D", "E")

    dot.edge("E", "I", label="Push Completed?")
    dot.edge("I", "K", label="Yes", style="bold")  # End if BCP push is successful
    dot.edge("I", "F", label="No", style="dashed")  # Handle exceptions if BCP fails

    dot.edge("F", "G", label="Yes", style="bold")
    dot.edge("G", "E", label="Retry from CSV Save & BCP Push")
    dot.edge("G", "J", label="Retry Limit Exceeded", style="bold")

    dot.edge("F", "H", label="No", style="dashed")
    dot.edge("H", "J", label="Send to Parent Process")

    dot.edge("J", "K")  # Final end

    # Save
    dot.render("new_process_flow_combined")

# Generate both flow diagrams
create_old_process_flow()
create_new_process_flow()

print("Flow diagrams generated successfully!")
