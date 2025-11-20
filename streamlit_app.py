import streamlit as st
import boto3
import json
import uuid

# Your agent runtime ARN
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-west-2:129317715590:runtime/my_agent-Rh57CLEg3e"
REGION = "us-west-2"

# Create client
client = boto3.client("bedrock-agentcore", region_name=REGION)

def invoke_agent(prompt):
    payload = json.dumps({"prompt": prompt}).encode("utf-8")

    response = client.invoke_agent_runtime(
        agentRuntimeArn=AGENT_RUNTIME_ARN,
        runtimeSessionId=str(uuid.uuid4()),
        payload=payload,
        qualifier="DEFAULT"
    )

    # Case 1 → Response contains StreamingBody under "response"
    if "response" in response:
        stream = response["response"]
        raw_bytes = stream.read()
        raw_text = raw_bytes.decode("utf-8")

        data = json.loads(raw_text)
        return data["result"]["content"][0]["text"]

    # Case 2 → Standard "payload"
    if "payload" in response:
        raw = response["payload"].decode("utf-8")
        data = json.loads(raw)
        return data["result"]["content"][0]["text"]

    # Case 3 → "completion" key
    if "completion" in response:
        return response["completion"]["content"][0]["text"]

    # If nothing matched → debug fallback
    return f"Unable to parse response: {response}"
    
    # Parse Bedrock AgentCore result
    payload_bytes = response["payload"]
    response_string = payload_bytes.decode("utf-8")
    response_json = json.loads(response_string)
    
    return response_json["result"]["content"][0]["text"]

# Streamlit UI
st.set_page_config(page_title="My Bedrock Agent", page_icon="🤖")

st.title("🤖 My AgentCore Chatbot (Streamlit UI)")
st.write("Talk to your deployed Amazon Bedrock AgentCore agent.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Invoke agent
    with st.chat_message("assistant"):
        try:
            reply = invoke_agent(prompt)
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
