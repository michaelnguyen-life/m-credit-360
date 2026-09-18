import subprocess
import requests

try:
    token = subprocess.check_output(['C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Users\\finan\\AppData\\Local\\Temp\\opencode\\get_token.sh']).decode().strip()
    url = 'https://agentbase.api.vngcloud.vn/runtime/agent-runtimes'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    print(r.text)
except Exception as e:
    print(f'Error: {e}')
