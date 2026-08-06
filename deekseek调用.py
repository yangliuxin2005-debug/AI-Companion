import os
from openai import OpenAI
# Please install OpenAI SDK first: `pip3 install openai`

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "你叫玛丽，是一位热情开朗的助手"},
        {"role": "user", "content": "亲爱的玛丽 你能为我做些什么呢"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)