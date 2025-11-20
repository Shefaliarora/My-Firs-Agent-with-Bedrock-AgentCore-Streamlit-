from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

print("FILE STARTING...")

app = BedrockAgentCoreApp()
agent = Agent()

@app.entrypoint
def invoke(payload):
    print("INVOKE CALLED...")
    user_message = payload.get("prompt", "Hello from Windows Agent!")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    print("MAIN BLOCK RUNNING...")
    app.run()
