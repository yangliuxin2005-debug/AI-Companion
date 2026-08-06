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

#左侧侧边栏:-with: 创建一个上下文管理器，用于在with代码块中执行代码
with st.sidebar:
    # logo
    st.image("./resources/logo.jpg")
    # 副标题
    st.subheader("伴侣信息")
    #昵称
    nake_name = st.text_input("请输入你的昵称",placeholder="请输入你的昵称",value="雨晴")
    if nake_name:
        st.session_state.nake_name = nake_name
    #性格
    character = st.text_area("请输入你的性格",placeholder="请输入你的性格",value="热情开朗的台湾女孩")
    if character :
        st.session_state.character = character


#系统提示
system_promt=  """你叫%s,是用户真实的伴侣，请带入伴侣角色
              要求1.要像微信聊天一样回复我的消息，信息简短
              2.每次只回复一条消息
              3.用符合伴侣性格的回复方式
              4.可以带一些颜字表情
              伴侣的性格： %s
              你必须严格遵守以上要求"""


#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#初始化名称
if "nake_name" not in st.session_state:
    st.session_state.nake_name = "雨晴"
#初始化性格
if "character" not in st.session_state:
    st.session_state.character = "热情开朗的台湾女孩"
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

    print([
            {"role": "system", "content":system_promt},
            *st.session_state.messages
        ])
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content":system_promt % (st.session_state.nake_name,st.session_state.character)},
            *st.session_state.messages
        ],
        # 是否流式输出（当输出结果为流式时，请将此参数设置为True）
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
   #流式输出处理
    response_message = st.empty ()
    full_response= ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_response)

   # 打印大模型返回的结果（非流式输出）
   #  print("<--------大模型返回的结果",response.choices[0].message.content)
   #  st.chat_message("assistant").write(response.choices[0].message.content)

    #输出大模型返回的结果（流式输出）

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})