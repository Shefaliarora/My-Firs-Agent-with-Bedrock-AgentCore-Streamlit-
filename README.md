Prerequisites 

Python 3.10+ installed. 

PowerShell/terminal access. 

AWS CLI configured (aws configure) or valid AWS credentials available. 

Internet access for packages and Bedrock (unless you already have offline packages). 

Your bedrock-agentcore package version installed or available. 

Basic familiarity with Python and Streamlit. 

 

0. Project layout (what we’ll create) 

agentcore-runtime-quickstart/ 
├── .bedrock_agentcore/ 
├── .bedrock_agentcore.yaml 
├── my_agent.py 
├── streamlit_app.py 
├── requirements.txt 
└── .venv/ 
 

 Create & activate virtual environment (Windows PowerShell) 

cd C:\users\abhia 
mkdir agentcore-runtime-quickstart 
cd agentcore-runtime-quickstart 
 
python -m venv .venv 
.\.venv\Scripts\Activate.ps1   # use Activate.bat for cmd.exe 
 

You should see (.venv) on the prompt. 

 

2. Create requirements.txt 

Create requirements.txt with the core packages: 

streamlit 
boto3 
bedrock-agentcore 
 

(If you need more packages later — e.g., python-multipart, PyPDF2 — add them.) 

Install: 

pip install -r requirements.txt 
 

 

3. Configure AWS credentials (if not already) 

If you haven’t configured AWS CLI: 

aws configure 
 

Enter your AWS Access Key, Secret Key, region (e.g. us-west-2), output json. 

Ensure the IAM user/role has permissions required by your tools: 

bedrock:InvokeModel (or corresponding Bedrock permissions) 

lambda:InvokeFunction (if using Lambda) 

textract:* (if Textract) 

s3:PutObject, s3:GetObject 

dynamodb:PutItem (if DynamoDB) 

 

4. Add .bedrock_agentcore.yaml (agent identity + tools) 

Create a .bedrock_agentcore.yaml file in project root. 

Example (replace placeholders): 

runtime: 
 model: 
   provider: amazon 
   # Replace with desired model name/version from Bedrock 
   name: amazon.claude-3-sonnet-20240229-v1:0 
 
agent: 
 name: my_demo_agent 
 description: "AgentCore demo agent for trainees" 
 
tools: 
 - name: hello_tool 
   type: python 
   path: my_agent.py 
   entrypoint: hello_tool 
 
 # Example AWS Lambda tool (uncomment & replace values if you use Lambda) 
 # - name: lambda_invoke 
 #   type: aws-lambda 
 #   lambdaArn: arn:aws:lambda:REGION:ACCOUNT:function:myFunction 
 #   region: us-west-2 
 

Notes: 

path should point to your Python file containing the tool functions. 

For AWS tools, replace ARNs and region. 
