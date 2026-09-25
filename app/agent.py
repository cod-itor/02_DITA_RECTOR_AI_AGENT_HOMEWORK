import ollama
from schemas import ALL_TOOLS_SCHEMA
from harness import execute_tool_safely

class ShoppingAgent:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.max_loops = 5
        
    def run(self, user_request: str, user_role: str = "customer"):
        SYSTEM_PROMPT = """You are a precise AI Shopping Agent. 
You must always use tools to fetch information. 
If a tool returns an error (like OUT_OF_STOCK, PERMISSION_DENIED, HUMAN_REJECTED), you MUST explain the error to the user based on the JSON response code.
Do not guess, make up information, or hallucinate prices or stock numbers."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ]
        
        print(f"\n--- Agent started (Role: {user_role}) ---")
        
        for loop_count in range(self.max_loops):
            print(f"[Loop {loop_count + 1}] Requesting model...")
            
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                tools=ALL_TOOLS_SCHEMA
            )
            
            messages.append(response["message"])
            
            if not response["message"].get("tool_calls"):
                print("\n[Final Answer]")
                print(response["message"]["content"])
                return response["message"]["content"]
                
            for tool_call in response["message"]["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"] 
                
                print(f"-> Tool Call: {tool_name}({arguments})")
                tool_result = execute_tool_safely(tool_name, arguments, user_role)
                print(f"<- Tool Result: {tool_result}")
                
                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "name": tool_name
                })
                
        print("\n[Warning] Maximum iteration limit reached.")
        return "Agent stopped due to loop limit."
