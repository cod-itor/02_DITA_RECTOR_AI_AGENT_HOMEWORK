from agent import ShoppingAgent

def main():
    agent = ShoppingAgent(model_name="llama3.2")
    
    print("Welcome to the AI Shopping Agent!")
    
    print("\n\n=== TEST 1: Customer searching and checking stock ===")
    agent.run(
        user_request="Find me a laptop, then check if the cheapest one is in stock.", 
        user_role="customer"
    )
    
    print("\n\n=== TEST 2: Customer trying to delete a product ===")
    agent.run(
        user_request="Delete product ID 1.", 
        user_role="customer"
    )
    
    print("\n\n=== TEST 3: Admin trying to delete a product ===")
    agent.run(
        user_request="Delete product ID 1.", 
        user_role="admin"
    )

if __name__ == "__main__":
    main()
