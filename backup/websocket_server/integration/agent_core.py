import boto3
import json
import os

region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

ARNS = {}
if len(ARNS.keys()) == 0:
    # Get AgentCore Runtime ARNS
    agentcore_control = boto3.client('bedrock-agentcore-control', region)
    rt_response= agentcore_control.list_agent_runtimes()
    for rt in rt_response["agentRuntimes"]:
        agent_rt_name = rt["agentRuntimeName"]
        ARNS[agent_rt_name] = rt["agentRuntimeArn"]

agentcore_client = boto3.client('bedrock-agentcore',region_name=region)

def invoke_agent_core(tool_name, payload):
    try:
        global ARNS
        
        # Map tool names to agent runtime names
        tool_to_agent_map = {
            "orchestration_panel": "ac_orchestration_agent",
            "ac_bank_agent": "ac_bank_agent",
            "ac_mortgage_agent": "ac_mortgage_agent",
        }
        
        # Get the agent runtime name from the map, or use the tool name directly
        agent_name = tool_to_agent_map.get(tool_name.lower(), tool_name.lower())
        arn = ARNS.get(agent_name)
        
        if not arn:
            return {"result": f"AgentCore runtime doesn't exist for tool '{tool_name}' (looking for agent '{agent_name}'). Available agents: {list(ARNS.keys())}"}
        
        # Ensure payload is a string (JSON)
        if isinstance(payload, dict):
            payload_str = json.dumps(payload, ensure_ascii=False)
        else:
            payload_str = payload

        print(f"Calling AgentCore runtime: {agent_name}")
        print(f"Payload: {payload_str}")

        boto3_response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=arn,
            qualifier="DEFAULT",
            payload=payload_str.encode('utf-8')
        )

        if "text/event-stream" in boto3_response.get("contentType", ""):
            content = []
            for line in boto3_response["response"].iter_lines(chunk_size=1):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                        print(line)
                        content.append(line)
            return "\n".join(content)
        else:
            try:
                events = []
                for event in boto3_response.get("response", []):
                    events.append(event)
            except Exception as e:
                events = [f"Error reading EventStream: {e}"]
            return json.loads(events[0].decode("utf-8"))
    except Exception as e:
        return {"result": f"Failed to call agent core runtime: {e}"}