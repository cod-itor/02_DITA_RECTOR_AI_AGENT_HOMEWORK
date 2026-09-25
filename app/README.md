# Topic 07 - Autonomous Agent Homework

## 1. Project Overview
This project implements a simple agentic "Shopping Agent" using Python and `ollama` (with the `llama3.2` model). The agent receives user requests, executes tools, observes the results, and loops until it produces a final answer. 

Crucially, the application (not just the LLM prompt) enforces strict security controls. The project implements the core requirements alongside **all five advanced extensions** (HITL, Risk Classification, Allowlist, Stronger Failure Boundaries, and Timeout Controls).

## 2. Available Tools
*   `search_products`: Searches the inventory based on a keyword and returns a structured JSON list of matching items.
*   `check_stock`: Takes a product ID and returns the current stock quantity.
*   `delete_product`: Takes a product ID and deletes it from the database.

## 3. Agent Loop (Decision → Action → Observation)
The agent operates via a continuous loop (`agent.py`):
1. **Request:** The user's prompt is appended to the message history.
2. **Decision:** The LLM evaluates the history and schemas, deciding to return a text response or a `tool_call`.
3. **Action (Harness interception):** If a tool is called, `harness.py` intercepts the request to evaluate Risk Classification, the Allowlist, and RBAC permissions. If approved, the tool executes.
4. **Observation:** The tool returns a structured JSON dictionary which is appended back to the LLM's message history as an observation.
5. The loop repeats until the LLM returns a final text answer.

## 4. Permission Rule & Risk Classification
The application enforces Role-Based Access Control (RBAC) tied to **Risk Tiers**:
*   **GREEN Tools** (`search_products`, `check_stock`): Can be executed automatically by any user (`customer` or `admin`).
*   **RED Tools** (`delete_product`): Dangerous write-operations. The harness strictly requires `user_role == "admin"`. If a customer attempts it, execution is blocked.

Furthermore, RED tools trigger a **Human-in-the-Loop (HITL)** pause, requiring physical terminal confirmation (`y/n`) before execution occurs.

## 5. Safety & Controls
*   **Allowlist:** Any tool requested by the LLM that is not explicitly defined in `ALLOWLIST` is immediately rejected.
*   **Validation:** Inputs like `product_id` are cast to integers. If the LLM passes a string (e.g., `"1"`), the code safely casts it. If it passes gibberish, it catches the exception.
*   **Stronger Failure Boundaries:** Instead of crashing the python script, exceptions and errors are caught by the harness and returned as structured JSON codes (e.g., `{"status": "error", "code": "OUT_OF_STOCK"}`) so the LLM can recover.
*   **Timeout Controls:** Tools are executed via `ThreadPoolExecutor` with a strict 3-second timeout to prevent infinite hangs.
*   **Loop Limit:** The agent has a hard limit of `max_loops = 5` to prevent infinite token loops.

## 6. Example Run
You can test the agent yourself by running:
```bash
poetry run python app/main.py
```

Below is the terminal output from a live test, demonstrating the agent loop, structured errors, and the HITL approval flow:

```text
=== TEST 1: Customer searching and checking stock ===
--- Agent started (Role: customer) ---
[Loop 1] Requesting model...
-> Tool Call: search_products({'keyword': 'laptop'})
<- Tool Result: {"status": "success", "results": [{"id": 1, "name": "macbook pro laptop", "price": 1200}, {"id": 2, "name": "dell xps laptop", "price": 1000}]}
[Loop 2] Requesting model...

[Final Answer]
Based on the search results, I found two laptops: MacBook Pro and Dell XPS. To check if the cheapest one is in stock, I'll call the "check_stock" tool.

=== TEST 2: Customer trying to delete a product ===
--- Agent started (Role: customer) ---
[Loop 1] Requesting model...
-> Tool Call: delete_product({'product_id': 1})
<- Tool Result: {"status": "error", "code": "PERMISSION_DENIED", "message": "Only admins can run RED tools."}
[Loop 2] Requesting model...

[Final Answer]
I apologize, but I am not authorized to delete the product with ID 1. The 'PERMISSION_DENIED' error indicates that I do not have the necessary permissions.

=== TEST 3: Admin trying to delete a product ===
--- Agent started (Role: admin) ---
[Loop 1] Requesting model...
-> Tool Call: delete_product({'product_id': 1})

[SECURITY] Tool requested: 'delete_product' | Args: {'product_id': 1}
Approve execution? (y/n): y
<- Tool Result: {"status": "success", "message": "Product ID 1 has been deleted."}
[Loop 2] Requesting model...

[Final Answer]
The product has been successfully deleted from the database.
```
