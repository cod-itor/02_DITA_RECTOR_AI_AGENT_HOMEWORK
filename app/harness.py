import json
import concurrent.futures
from tools import TOOL_MAP

ALLOWLIST = ["search_products", "check_stock", "delete_product"]

TOOL_RISK_TIERS = {
    "search_products": "GREEN",
    "check_stock": "GREEN",
    "delete_product": "RED" 
}

def _run_tool_with_timeout(func, kwargs, timeout_seconds=3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, **kwargs)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            return {"status": "error", "code": "TIMEOUT", "message": "Tool execution took too long."}
        except Exception as e:
            return {"status": "error", "code": "EXECUTION_CRASH", "message": str(e)}

def execute_tool_safely(tool_name: str, arguments: dict, user_role: str) -> str:
    if tool_name not in ALLOWLIST:
        return json.dumps({"status": "error", "code": "UNAUTHORIZED_TOOL"})
        
    if tool_name not in TOOL_MAP:
        return json.dumps({"status": "error", "code": "TOOL_NOT_FOUND"})
        
    risk_tier = TOOL_RISK_TIERS.get(tool_name, "RED")
    
    if risk_tier == "RED":
        if user_role != "admin":
            return json.dumps({"status": "error", "code": "PERMISSION_DENIED", "message": "Only admins can run RED tools."})
            
        print(f"\n[SECURITY] Tool requested: '{tool_name}' | Args: {arguments}")
        approval = input("Approve execution? (y/n): ").strip().lower()
        if approval != 'y':
            return json.dumps({"status": "error", "code": "HUMAN_REJECTED", "message": "Action denied by human."})
            
    func = TOOL_MAP[tool_name]
    result_dict = _run_tool_with_timeout(func, arguments, timeout_seconds=3)
    
    return json.dumps(result_dict)
