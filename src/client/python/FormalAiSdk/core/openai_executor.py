import os
import openai

class OpenAIExecutor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.deployment = os.getenv("OPENAI_MODEL")
        if not self.api_key or not self.api_base or not self.deployment:
            raise ValueError("Missing required OpenAI environment variables")
        self.is_azure = "azure" in self.api_base

        if self.is_azure:
            self.client = openai.AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.api_base
            )
        else:
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.api_base)

    def execute(self, prompt, role="user"):
        messages = [{"role": role, "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
        )
        return response.choices[0].message.content
