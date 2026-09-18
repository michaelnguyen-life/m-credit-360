const token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlckVaZFpkNkRsc21pdjhsMDZIaVB3bHZYWnotLVlGYXlZcVJiczlxc09rIn0.eyJleHAiOjE3ODk1NzkwMDYsImlhdCI6MTc4OTU3NzIwNiwianRpIjoiZjI1OTYxNDQtOTBhNS00MDczLWJhNWUtYjljM2JlOGJjZGFlIiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm5nY2xvdWQudm4vYXV0aC9yZWFsbXMvaWFtIiwic3ViIjoiODJmYTI2YWYtNmI5Yy00ZTI4LWFkMDEtMWM5M2E3MzY3OWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYjA3NTMzMTgtMmE5Ny00YmJmLWFlNzEtNDExNmYyNGQxNjZjIiwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMTY2LjIuOSIsImF1dGhBY2NvdW50SWQiOjExNDU1MywiY2xpZW50QWRkcmVzcyI6IjEwLjE2Ni4yLjkiLCJjbGllbnRfaWQiOiJiMDc1MzMxOC0yYTk3LTRiYmYtYWU3MS00MTE2ZjI0ZDE2NmMiLCJhdXRoVXNlclR5cGUiOiJ1c2VyLXNhIn0.AhLE60ocKK6m59W6HXy6AF-_Ilf_TOmadyN2hn-nEzuEpjO_Y90Bd-1TR6K-cu3jImMCpICsZAXawSGfoiJifh80wIEcSzR3AzAxUf3QMchL5hsBLNWQptRqbyD0IpRSpVs0e8bFoW80-C205fXhLhCSamk0Zxw90t8T4iQOBWhjNIv-qPatueLoO2ahCIBQ-Po_Gmhbwp-JEByCqpdzXdhlmUlnNhzDBR-qQ9rMLxHpWpPzQoPlOzSsI9QFsjmPc_Xb22mSF0UD-JMcyFdBfVxEuLzcylYTH4hQF20DE-EHPnvIVmSO4W_9XEgOgCmHPWUZ89yH3wR4nq_VikFOvQ';
const body = {
    imageUrl: "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v9",
    flavorId: "runtime-s2-general-2x4",
    description: "M-Credit 360 Omni-Butler V9 (QA Syntax Fixes)",
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
