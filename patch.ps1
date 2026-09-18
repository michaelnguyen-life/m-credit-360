$token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlckVaZFpkNkRsc21pdjhsMDZIaVB3bHZYWnotLVlGYXlZcVJiczlxc09rIn0.eyJleHAiOjE3ODk1NzY5ODUsImlhdCI6MTc4OTU3NTE4NSwianRpIjoiYjAzZDNjOTAtZjRkNi00NjE3LWE3ZWEtYTAxNTcwY2RmZTczIiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm5nY2xvdWQudm4vYXV0aC9yZWFsbXMvaWFtIiwic3ViIjoiODJmYTI2YWYtNmI5Yy00ZTI4LWFkMDEtMWM5M2E3MzY3OWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYjA3NTMzMTgtMmE5Ny00YmJmLWFlNzEtNDExNmYyNGQxNjZjIiwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMTY2LjIuOSIsImF1dGhBY2NvdW50SWQiOjExNDU1MywiY2xpZW50QWRkcmVzcyI6IjEwLjE2Ni4yLjkiLCJjbGllbnRfaWQiOiJiMDc1MzMxOC0yYTk3LTRiYmYtYWU3MS00MTE2ZjI0ZDE2NmMiLCJhdXRoVXNlclR5cGUiOiJ1c2VyLXNhIn0.RrqcRp3rQWMTSwfWlCgPXcvlfYkncvHxcwNybv0oDWXeJC8dxemLVBwyTLwb5lahWlV8e9Va3FVIeQpnJ8KDNX_tTGAQLJBfApmn-F7HouYGTG3QLq2kGqCxpa3qyBP3CD1YFOBIF_AL5faRTi1CusVl5ZoS-BfGfksnMWlLsNvwkaj9d4Ht26o02SPyPp2xEEFg9LYxCxuJz2sTtWltmsAS7SNUZcCDhVvg3tXPbFQG7vF8GMUFXIciXWmDrJlbi9-dRuIkT2VDNNBqtBu5YhCgfGSzQmA5xPJfGwQKHvicrUL8OypL6rWfHXHAVqO3KewqgowQ54NHzVXZXFG0Pg'
$body = '{
    "args":  [

             ],
    "description":  "M-Credit 360 Omni-Butler Final",
    "imageAuth":  {
                      "username":  "111480-gui114553",
                      "password":  "MfrwBwLT96v2rx3dOlSaU2oks9c1ODvb",
                      "enabled":  true
                  },
    "imageUrl":  "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v4",
    "poc":  false,
    "command":  [

                ],
    "environmentVariables":  {
                                 "URL_MEMO":  "http://localhost:8080/build-memo-docx",
                                 "GREENNODE_API_KEY":  "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d",
                                 "ZALO_BOT_TOKEN":  "1594214031862095447:dNzbsXIUJIsmbInvjIHyzhZekmVhCymQZmQXtQVYFwKkTyoRXRIjmkZresuZFFCI",
                                 "GREENNODE_MAAS_URL":  "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions",
                                 "PYTHONUNBUFFERED":  "1",
                                 "ENABLE_ZALO_BOT":  "true",
                                 "PORT":  "8080",
                                 "URL_ASSESS":  "http://localhost:8080/assess"
                             },
    "autoscaling":  {
                        "memoryUtilization":  50,
                        "cpuUtilization":  50,
                        "maxReplicas":  1,
                        "minReplicas":  1
                    },
    "flavorId":  "runtime-s2-general-2x4"
}'
Invoke-RestMethod -Uri 'https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-43870a78-d3e5-4b9f-a1bf-41f03fbd3768' -Method PATCH -Headers @{ 'Authorization' = 'Bearer ' + $token; 'Content-Type' = 'application/json' } -Body $body
