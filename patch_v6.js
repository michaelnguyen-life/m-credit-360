const token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlckVaZFpkNkRsc21pdjhsMDZIaVB3bHZYWnotLVlGYXlZcVJiczlxc09rIn0.eyJleHAiOjE3ODk1NzgwMzAsImlhdCI6MTc4OTU3NjIzMCwianRpIjoiYjk4YmQ0YjUtNWI0NC00NGM2LWFkYzctY2Y4OTAzM2M0MjFjIiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm5nY2xvdWQudm4vYXV0aC9yZWFsbXMvaWFtIiwic3ViIjoiODJmYTI2YWYtNmI5Yy00ZTI4LWFkMDEtMWM5M2E3MzY3OWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYjA3NTMzMTgtMmE5Ny00YmJmLWFlNzEtNDExNmYyNGQxNjZjIiwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMTY2LjIuMTAiLCJhdXRoQWNjb3VudElkIjoxMTQ1NTMsImNsaWVudEFkZHJlc3MiOiIxMC4xNjYuMi4xMCIsImNsaWVudF9pZCI6ImIwNzUzMzE4LTJhOTctNGJiZi1hZTcxLTQxMTZmMjRkMTY2YyIsImF1dGhVc2VyVHlwZSI6InVzZXItc2EifQ.PANcP5nUvS7sZzaMGdHUnGxEpOOp5c9hnG873GSjDL1l7NicaUsS1W4uICHyi7DMVJGzJSV8r3S8LLj-szQn892MWb7EHpc0MambHd1Tq4EZn87LDHHjhBu6XRi1QpNoA7l0jVOAOeb98aM4izNXC3uTFeXhXBHDrusFIoNKQLEaYvIMrnkHRy2kFIbqjEwR-VATzXUzpJFbKZGK8_vHYgp0RLhHT-tluLecm356nFcME62DVwQaQh7P8vDipBmA94UTj4Y1wYB0DtWNxqwxE_KbAmHTtxw0c-hCrXf12-iyRKik98EmqN3pDzIaEge7V_ujzlcOYwPGxayYe9uAxw';
const body = {
    imageUrl: "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v6",
    flavorId: "runtime-s2-general-2x4",
    description: "M-Credit 360 Omni-Butler V6 (Fixed Logic)",
    environmentVariables: {
      "ENABLE_ZALO_BOT": "true",
      "ZALO_BOT_TOKEN": "1594214031862095447:dNzbsXIUJIsmbInvjIHyzhZekmVhCymQZmQXtQVYFwKkTyoRXRIjmkZresuZFFCI",
      "GREENNODE_MAAS_URL": "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions",
      "URL_ASSESS": "http://localhost:8080/assess",
      "URL_MEMO": "http://localhost:8080/build-memo-docx",
      "PORT": "8080",
      "PYTHONUNBUFFERED": "1"
    },
    autoscaling: {
      minReplicas: 1,
      maxReplicas: 1,
      cpuUtilization: 50,
      memoryUtilization: 50
    },
    poc: false,
    imageAuth: {
      enabled: true,
      username: "111480-gui114553",
      password: "MfrwBwLT96v2rx3dOlSaU2oks9c1ODvb"
    }
};

fetch('https://agentbase.api.vngcloud.vn/runtime/agent-runtimes/runtime-43870a78-d3e5-4b9f-a1bf-41f03fbd3768', {
    method: 'PATCH',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
})
.then(res => res.text().then(t => ({status: res.status, text: t})))
.then(console.log)
.catch(console.error);
