const token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlckVaZFpkNkRsc21pdjhsMDZIaVB3bHZYWnotLVlGYXlZcVJiczlxc09rIn0.eyJleHAiOjE3ODk1Nzg0MTgsImlhdCI6MTc4OTU3NjYxOCwianRpIjoiOGFiNzgzYjMtMDcxNS00NGE3LWIyMmYtOWE4YWYzYjBlZmM3IiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm5nY2xvdWQudm4vYXV0aC9yZWFsbXMvaWFtIiwic3ViIjoiODJmYTI2YWYtNmI5Yy00ZTI4LWFkMDEtMWM5M2E3MzY3OWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYjA3NTMzMTgtMmE5Ny00YmJmLWFlNzEtNDExNmYyNGQxNjZjIiwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMTY2LjIuOSIsImF1dGhBY2NvdW50SWQiOjExNDU1MywiY2xpZW50QWRkcmVzcyI6IjEwLjE2Ni4yLjkiLCJjbGllbnRfaWQiOiJiMDc1MzMxOC0yYTk3LTRiYmYtYWU3MS00MTE2ZjI0ZDE2NmMiLCJhdXRoVXNlclR5cGUiOiJ1c2VyLXNhIn0.cdqcNd6EpIKMDxZ8EzkGGvwDvINudGdUUTXWfa3CBs3VRdhs_GdJw_TfR3yzuhVIsGMYh4pzZ8rEhObQaP18Nex1T_JeaHmJKd8eAK-88SOzxHNuj_vikNni2-LpHM7rrVAqMTZrgtfWmIf4BoWRmOS0LEIYbxqc0idNpUL2Z2_QPFq6N0KfK4vpjAC0LOf0CkjdfR82XZSBJhMOAUEsVeMyLMrAOle7GotfjxrePcR4WvGMu5QUglM2CPemsfXZW01NnWa6i083un0wrnD-Nw_2ZS5uV3yRp8PN1mx_dJxVVhVRiG-7v2IQzbpBOHy4Cu4IIoMSYz82Sn4x_M074g';
const body = {
    imageUrl: "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v7",
    flavorId: "runtime-s2-general-2x4",
    description: "M-Credit 360 Omni-Butler V7 (QA Approved)",
    environmentVariables: {
      "ENABLE_ZALO_BOT": "true",
      "ZALO_BOT_TOKEN": "1594214031862095447:dNzbsXIUJIsmbInvjIHyzhZekmVhCymQZmQXtQVYFwKkTyoRXRIjmkZresuZFFCI",
      "GREENNODE_API_KEY": "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d",
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
