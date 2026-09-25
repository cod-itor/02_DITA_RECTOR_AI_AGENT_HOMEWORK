SEARCH_PRODUCTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": "Search for products by a keyword (like 'laptop' or 'mouse').",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The search term to look for in product names."
                }
            },
            "required": ["keyword"]
        }
    }
}

CHECK_STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "check_stock",
        "description": "Check the current inventory stock level for a specific product ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "The unique integer ID of the product."
                }
            },
            "required": ["product_id"]
        }
    }
}

DELETE_PRODUCT_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_product",
        "description": "Delete a product from the database. Requires admin privileges.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "The unique integer ID of the product to delete."
                }
            },
            "required": ["product_id"]
        }
    }
}

ALL_TOOLS_SCHEMA = [SEARCH_PRODUCTS_SCHEMA, CHECK_STOCK_SCHEMA, DELETE_PRODUCT_SCHEMA]
