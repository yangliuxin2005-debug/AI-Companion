import streamlit as st
import os
from openai import OpenAI
#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="👱🏼‍♀️",
    #布局
    layout="wide",
    #控制的是侧边栏目状态
    initial_sidebar_state="expanded",
    menu_items={}
)
#大标题
st.title("AI智能伴侣")

#生成logo
st.logo("./resources/logo.jpg")

#系统提示词
system_promt="你叫玛丽，是一位热情开朗的助手"

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])


#创建OpenAI客户端(key 获取方式：https://deepseek.com/docs/api-keys)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

prompt=st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("------->调用大模型，提示词:",prompt)
    #保存用户的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content":system_promt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    print("<--------大模型返回的结果",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})