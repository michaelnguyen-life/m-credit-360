import requests

url = "https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-43870a78-d3e5-4b9f-a1bf-41f03fbd3768"
r = requests.get(url)
# AgentBase API for runtime status doesn't work without auth, but we can hit the actual deployed URL!
