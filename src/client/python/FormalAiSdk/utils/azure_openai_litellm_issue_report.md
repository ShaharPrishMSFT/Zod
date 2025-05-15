# Azure OpenAI + LiteLLM Integration Issue Report

## Summary

This document details an issue encountered when attempting to use [LiteLLM](https://github.com/BerriAI/litellm) with Azure OpenAI deployments. The official OpenAI Python SDK works with the same credentials and deployment, but LiteLLM returns a 404 "Resource not found" error. All private information has been replaced with placeholders.

---

## Environment

- **Azure OpenAI Resource:** `<AZURE_RESOURCE_NAME>`
- **Deployment Name:** `<AZURE_DEPLOYMENT_NAME>` (e.g., `gpt-4.1`)
- **API Key:** `<AZURE_OPENAI_API_KEY>`
- **API Version:** `2025-01-01-preview`
- **Endpoint:**  
  - For SDK: `https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview`
  - For LiteLLM: Same as above, or base endpoint as tested
- **Python Packages:**
  - `openai>=1.0.0`
  - `litellm` (latest as of 2025-05-13)

---

## What Works

### Direct OpenAI SDK Call (Success)

**Code:**
```python
import openai

client = openai.AzureOpenAI(
    api_key="<AZURE_OPENAI_API_KEY>",
    api_version="2025-01-01-preview",
    azure_endpoint="https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview"
)
response = client.chat.completions.create(
    model="<AZURE_DEPLOYMENT_NAME>",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response)
```

**Output:**
```
Using deployment: <AZURE_DEPLOYMENT_NAME>
Using endpoint: https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview
SUCCESS: OpenAI API call succeeded.
Response:
ChatCompletion(id='...', choices=[...], ...)
```

---

## What Does NOT Work

### LiteLLM Call (Failure)

**Code:**
```python
import litellm

response = litellm.completion(
    model="<AZURE_DEPLOYMENT_NAME>",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response)
```
**Environment:**
- `OPENAI_API_KEY=<AZURE_OPENAI_API_KEY>`
- `OPENAI_API_BASE=https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview`
- `OPENAI_MODEL=<AZURE_DEPLOYMENT_NAME>`

**Output (scrubbed):**
```
Using endpoint: https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview
Using model: <AZURE_DEPLOYMENT_NAME>
LiteLLM debug mode enabled.
...
POST Request Sent from LiteLLM:
curl -X POST \
https://<AZURE_RESOURCE_NAME>.openai.azure.com/openai/deployments/<AZURE_DEPLOYMENT_NAME>/chat/completions?api-version=2025-01-01-preview/ \
-d '{'model': '<AZURE_DEPLOYMENT_NAME>', 'messages': [{'role': 'user', 'content': 'Hello'}], 'extra_body': {}}'

RAW RESPONSE:
Error code: 404 - {'error': {'code': '404', 'message': 'Resource not found'}}

ERROR: LiteLLM minimal call failed: litellm.NotFoundError: NotFoundError: OpenAIException - Resource not found
```

---

## Additional Notes

- Changing the endpoint to `/openai` or `/openai/deployments` does **not** resolve the issue for LiteLLM.
- The same credentials and deployment name work with the OpenAI SDK but not with LiteLLM.
- LiteLLM always returns a 404 "Resource not found" error from Azure.

---

## Steps to Reproduce

1. Create an Azure OpenAI deployment and note the deployment name.
2. Set up environment variables as above.
3. Run the direct OpenAI SDK script (should succeed).
4. Run the LiteLLM script (should fail with 404).

---

## Conclusion

- **OpenAI SDK:** Works with Azure OpenAI when using the full deployment endpoint and deployment name as the model.
- **LiteLLM:** Fails with 404 "Resource not found" even when configured identically.
- **Suspected Cause:** LiteLLM may not fully support Azure OpenAI's endpoint structure or may require additional configuration not documented.

---

## Request for Help

If you have experience with LiteLLM and Azure OpenAI, or know of a working configuration, please advise. Otherwise, this may be a bug or missing feature in LiteLLM's Azure support.
