import streamlit as st
import time
import prompts
import boto3
from typing import Dict
import pandas as pd
from langchain_aws import ChatBedrockConverse
from langchain_experimental.tools import PythonAstREPLTool

s3_uri = "path_to_s3_file"
try:
    df = pd.read_excel(s3_uri)
    # rename columns
    df.columns = ['start_date', 'end_date', 'product_code', 'usage_type', 'operation', 'unblended_cost', 'description', 'product_sku', 'pricing_rate_code', 'pricing_rate_id', 'reservation_subscription_id']

except Exception as e:
    print(f"Error: {e}")
    
model_id = "amazon.nova-pro-v1:0"

additionalModelRequestFields={"inferenceConfig": {"topK": 1}}

llm = ChatBedrockConverse(
    region_name="us-region",
    model=model_id,
    temperature=1,
    max_tokens=5120,
    top_p= 1,
    additional_model_request_fields=additionalModelRequestFields
)

# Streamed response emulator
def response_generator():
    # put together the prompt
    code_prompt = prompts.code_prompt_template(query, st.session_state.messages)

    # get generated code
    code_response = llm.invoke(code_prompt)

    # run the code to get the output
    tool = PythonAstREPLTool(locals={"df": df})
    code_output = tool.invoke(code_response.content)

    # put togehter the final prompt for final response
    final_prompt = prompts.final_response_template(query, code_response.content, code_output, st.session_state.messages)
    final_response = llm.invoke(final_prompt)
    
    response = final_response.content
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)

st.title("Chat with a dataset")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Accept user input
if query := st.chat_input("Ask me about the SF CUR Dataset"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query, unsafe_allow_html=True)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})