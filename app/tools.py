DB = {
    1: {"name": "macbook pro laptop", "price": 1200, "stock": 5},
    2: {"name": "dell xps laptop", "price": 1000, "stock": 0},
    3: {"name": "logitech mouse", "price": 50, "stock": 20}
}

def search_products(keyword: str) -> dict:
    results = []
    for pid, details in DB.items():
        if keyword.lower() in details["name"].lower():
            results.append({"id": pid, "name": details['name'], "price": details['price']})
    
    if not results:
        return {"status": "error", "code": "NO_RESULTS", "message": "No products found matching that keyword."}
    return {"status": "success", "results": results}

def check_stock(product_id) -> dict:
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        return {"status": "error", "code": "INVALID_INPUT", "message": f"product_id must be a valid integer, you provided: {product_id}"}
        
    if product_id not in DB:
        return {"status": "error", "code": "PRODUCT_NOT_FOUND", "message": f"Product ID {product_id} not found."}
        
    stock = DB[product_id]["stock"]
    
    if stock == 0:
        return {"status": "error", "code": "OUT_OF_STOCK", "message": f"Product {product_id} is out of stock."}
        
    return {"status": "success", "stock": stock}

def delete_product(product_id) -> dict:
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        return {"status": "error", "code": "INVALID_INPUT", "message": f"product_id must be a valid integer, you provided: {product_id}"}
        
    if product_id in DB:
        del DB[product_id]
        return {"status": "success", "message": f"Product ID {product_id} has been deleted."}
    return {"status": "error", "code": "PRODUCT_NOT_FOUND", "message": f"Product ID {product_id} not found."}
    
TOOL_MAP = {
    "search_products": search_products,
    "check_stock": check_stock,
    "delete_product": delete_product
}
