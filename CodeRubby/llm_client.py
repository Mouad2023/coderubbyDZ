import os
from openai import OpenAI, APIError, RateLimitError
import time

class LLMClient:
    def __init__(self, api_key, site_url="https://your-site.com", site_name="Your Site Name"):
        self.api_key = api_key
        self.base_url = "https://api.novita.ai/v3/openai"
        self.model = "deepseek/deepseek-r1-turbo"  # Novita AI model
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url
        )

    def query(self, prompt, max_retries=5, initial_delay=5):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI trained in software development. Provide concise, technically accurate responses. Format code answers with proper syntax and explain complex concepts using practical examples. When unsure, ask clarifying questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
                response_format={"type": "text"}
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            for attempt in range(max_retries):
                retry_after = e.response.headers.get('Retry-After', None)
                if attempt < max_retries - 1:
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else initial_delay * (2 ** attempt)
                    print(f"Rate limit hit, retrying in {delay} seconds (Retry-After: {retry_after or 'unknown'})...")
                    time.sleep(delay)
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[
                                {"role": "system", "content": "You are an expert AI trained in software development. Provide concise, technically accurate responses. Format code answers with proper syntax and explain complex concepts using practical examples. When unsure, ask clarifying questions."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1000,
                            temperature=0.7,
                            response_format={"type": "text"}
                        )
                        return response.choices[0].message.content
                    except RateLimitError:
                        continue
                else:
                    return f"❌ Request Error: Max retries reached for 429 Too Many Requests, Response: {str(e)}"
            return f"❌ Request Error: {str(e)}"
        except APIError as e:
            return f"❌ API Error: {str(e)}"
        except Exception as e:
            return f"❌ General Error: {str(e)}"