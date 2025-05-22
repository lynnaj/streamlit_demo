import boto3
    
def code_prompt_template(query, conversation_history):
    columns = ['start_date', 'end_date', 'product_code', 'usage_type', 'operation', 'unblended_cost', 'description', 'product_sku', 'pricing_rate_code', 'pricing_rate_id', 'reservation_subscription_id']

    prompt = f"""Given the following Cloud Cost dataset, which is loaded as a dataframe with the following columns: {columns} """ 
    prompt += f"""Note the product_code and unblended_cost are the main columns to answer any questions about cost by AWS service. """
    prompt += f"""You are a data analyst. Generate a Python code to answer the following question: {query} """
    prompt += f"""Use aggregate functions to summarize top 5 or lowest 5 when being asked about details. """
    prompt += f"""Here is the conversation history: {conversation_history}"""
    prompt += f"""\nDo not define load_data(), because it already exist. You have access to the user defined functions. """
    prompt += f"""They can be accessed from the module called `functions` by their function names. """
    prompt += f"""There is a function called `load_data` you could import it by writing `from functions import load_data """
    prompt += f"""Here is an example question, chain-of-thought, and Python code: Which product had the highest cost?\n"""
    prompt += f"""from functions import load_data\nimport pandas as pd\n# Step 1: Load the cloud cost data\n"""
    prompt += f"""cloud_cost_data = load_data()\n"""
    prompt += f"""# Step 2: Filter out negative costs and calculate the total cost for each product\n"""
    prompt += f"""total_cost_per_product = cloud_cost_data[['product_code', 'unblended_cost']].groupby('product_code')['unblended_cost'].sum().reset_index()\n"""
    prompt += f"""# Step 3: Identify the product with the highest total cost\n"""
    prompt += f"""highest_cost_product = total_cost_per_product.loc[total_cost_per_product['unblended_cost'].idxmax()]\n"""
    prompt += f"""# Display the result\n"""
    prompt += f"""print("The product with the highest cost is:")\n"""
    prompt += f"""print(highest_cost_product)\n"""
    prompt += f"""Use only the tables and column_names provided."""
    prompt += f"""Return only Python code and load the necessary modules. """
    prompt += f"""Aggregate data as much as you can and limit output to 10 rows of data, without any explanations or additional text. """
    return prompt

def final_response_template(query, code_response, code_output, conversation_history):
    
    prompt = f"""You are a helpful AI assistant that always responds in Markdown format. """
    prompt += f"""The user is asking the following question:\n{query}. """
    prompt += f"""The AI Data Analyst agent ran the following python code:\n{code_response}. """
    prompt += f"""The result shows:\n{code_output}. """
    prompt += f"""Here is the conversation history:\n{conversation_history} """
    prompt += f"""Be sure to prepend a backlash to dollar signs. No need to use pipes. Use \n\n for new line"""
    prompt += f"""Here is an example response: """
    prompt += f"""The top 5 expenses for March 2018 are: \n\nDEBT SERVICE PROJ FUND PRINCIPAL \$13,235,000 \n\nDEBT SERVICE PROJ FUND INTEREST EXPENSE BONDS \$10,868,690""" 
    prompt += f"""The answer: """
    return prompt
    