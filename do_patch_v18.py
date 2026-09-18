import subprocess
import requests

token = subprocess.check_output(['C:\\Program Files\\Git\\bin\\bash.exe', 'C:\\Users\\finan\\AppData\\Local\\Temp\\opencode\\get_token.sh']).decode().strip()

url = "https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-43870a78-d3e5-4b9f-a1bf-41f03fbd3768"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
body = {
    "imageUrl": "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v18",
    "flavorId": "runtime-s2-general-2x4",
    "description": "M-Credit 360 Omni-Butler V18 (Bulletproof Demo)",
    "environmentVariables": {
      "ENABLE_ZALO_BOT": "true",
      "ZALO_BOT_TOKEN": "1594214031862095447:dNzbsXIUJIsmbInvjIHyzhZekmVhCymQZmQXtQVYFwKkTyoRXRIjmkZresuZFFCI",
      "GREENNODE_API_KEY": "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d",
      "GREENNODE_MAAS_URL": "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions",
      "URL_ASSESS": "http://localhost:8080/assess",
      "URL_MEMO": "http://localhost:8080/build-memo-docx",
      "PORT": "8080",
      "PYTHONUNBUFFERED": "1"
    },
    "autoscaling": {
      "minReplicas": 1,
      "maxReplicas": 1,
      "cpuUtilization": 50,
      "memoryUtilization": 50
    },
    "poc": False,
    "imageAuth": {
      "enabled": True,
      "username": "111480-gui114553",
      "password": "MfrwBwLT96v2rx3dOlSaU2oks9c1ODvb"
    }
}

r = requests.patch(url, headers=headers, json=body)
print(r.status_code)
print(r.text)
