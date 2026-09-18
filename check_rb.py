import subprocess
import requests

token = subprocess.check_output(['C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Users\\finan\\AppData\\Local\\Temp\\opencode\\get_token.sh']).decode().strip()

url = "https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-625954cf-19da-48e8-bac0-275fad9b4bd1"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
r = requests.get(url, headers=headers)
print(r.text)
