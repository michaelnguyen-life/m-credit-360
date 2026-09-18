import subprocess
import requests

token = subprocess.check_output(['C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Users\\finan\\AppData\\Local\\Temp\\opencode\\get_token.sh']).decode().strip()

url = "https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-43870a78-d3e5-4b9f-a1bf-41f03fbd3768"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
r = requests.get(url, headers=headers)
print(r.text)
