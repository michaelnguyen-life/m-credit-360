const token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJlckVaZFpkNkRsc21pdjhsMDZIaVB3bHZYWnotLVlGYXlZcVJiczlxc09rIn0.eyJleHAiOjE3ODk1NzcxODksImlhdCI6MTc4OTU3NTM4OSwianRpIjoiZGEyNWNhNWMtOWE5MS00NzExLWI2Y2EtNjY4NGZkMTBmYjY5IiwiaXNzIjoiaHR0cHM6Ly9zaWduaW4udm5nY2xvdWQudm4vYXV0aC9yZWFsbXMvaWFtIiwic3ViIjoiODJmYTI2YWYtNmI5Yy00ZTI4LWFkMDEtMWM5M2E3MzY3OWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYjA3NTMzMTgtMmE5Ny00YmJmLWFlNzEtNDExNmYyNGQxNjZjIiwic2NvcGUiOiIiLCJjbGllbnRIb3N0IjoiMTAuMTY2LjIuMTAiLCJhdXRoQWNjb3VudElkIjoxMTQ1NTMsImNsaWVudEFkZHJlc3MiOiIxMC4xNjYuMi4xMCIsImNsaWVudF9pZCI6ImIwNzUzMzE4LTJhOTctNGJiZi1hZTcxLTQxMTZmMjRkMTY2YyIsImF1dGhVc2VyVHlwZSI6InVzZXItc2EifQ.Yloo8sgUyxk6yF_vBMSdkeamNvACAXq_diEjuxDo4pkAmKFrXKYPMAsg8ZQctx8r6HWdCpUvxQ2eWXcMXxXaLiqS7p7aUq8LSJJX_2T_iD3VIiCzGmmY_Cs-9VFfwoSHA8L2XPWBoizWhN0q4xiPYu9e_NLUOE3od2ifLekVztbDRUh65RCCfjbFnL7_S3yH_D2QUIETzo-ST2g9HTAszMdCoahMuws8v3vHTJwZUMOapzEONXIZxY5Bp7IIKkAFQntT37cO7OUBMqkLT0wMdTzl0PNULT8LbEwlx895Qerkbx2NGUY8H5gfvTdaGLZSCBmg1GUhJ6Ej0jvlIQDFmg';
const body = {
    imageUrl: "vcr.vngcloud.vn/111480-abp114553/m-credit-360:final_v4",
    flavorId: "runtime-s2-general-2x4",
    description: "M-Credit 360 Omni-Butler V4",
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
