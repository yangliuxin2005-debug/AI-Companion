import streamlit as st
import os
from openai import OpenAI
import json
import datetime

from openai.types import deleted_skill

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

#保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_date = {
            "nake_name": st.session_state.nake_name,
            "character": st.session_state.character,
            "current_session": st.session_state.current_session,
            "message": st.session_state.messages
        }
        # 如果sessions目录不存在，则创建
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        with open("sessions/" + st.session_state.current_session + ".json", "w", encoding="utf-8") as f:
            json.dump(session_date, f, ensure_ascii=False, indent=2)

# 创建一个函数，用用于创建会话名称
def create_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# 将会话文件名转换为可读的显示名称
def format_session_name(session_id):
    # 输入: 2025-08-07-14-30-45  输出: 2025-08-07 14:30:45
    try:
        dt = datetime.datetime.strptime(session_id, "%Y-%m-%d-%H-%M-%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return session_id
#加载出所有会话列表信息
def load_sessions():

    sessions_list = []
    if os.path.exists("sessions"):
        for filename in os.listdir("sessions"):
            if filename.endswith(".json"):
                sessions_list.append(filename[:-5])

    return sessions_list

#加载指定的会话
def load_session(session_name):
    try :
        if os.path.exists(f"sessions/{session_name}.json"):
         #读取会话数据
             with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                 session_data = json.load(f)
                 st.session_state.nake_name = session_data["nake_name"]
                 st.session_state.character = session_data["character"]
                 st.session_state.messages = session_data["message"]
                 st.session_state.current_session = session_name
    except Exception:
        st.error("会话加载失败")

#删除会话的函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除的是当前会话则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = create_session_name()
    except Exception:
        st.error("会话删除失败")

#大标题
st.title("AI智能伴侣")

#生成logo
st.logo("./resources/logo.jpg")

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#初始化名称
if "nake_name" not in st.session_state:
    st.session_state.nake_name = "雨晴"
#初始化性格
if "character" not in st.session_state:
    st.session_state.character = "热情开朗的台湾女孩"
#会话标识
if "current_session" not in st.session_state:
   st.session_state.current_session = create_session_name()

#左侧侧边栏:-with: 创建一个上下文管理器，用于在with代码块中执行代码
with st.sidebar:
    #会话信息
    st.subheader("AI控制面板")
    #设计一个新建会话按钮
    if st.button("新建会话",width="stretch",icon="🔄"):
        #1.保存当前会话信息
        save_session()

        #判断当前会话名称是否为空
        if  st.session_state.messages:
            # 2. 创建一个新的对话
            st.session_state.messages = []
            st.session_state.current_session = create_session_name()
            save_session()
            st.rerun()  # 重新运行一下，加载新的会话信息

    # 加载会话历史
    st.text("会话历史")
    sessions_list = load_sessions()
    for session in sessions_list:
        col1,col2=st.columns([4,1])
        with col1:
            if st.button(format_session_name(session), width="stretch", icon="🗂️",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话
            if st.button("",width="stretch",icon="❌️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


        # st.button(session,width="stretch",icon="🗂️")
        # st.button("",width="stretch",icon="❌️")


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

#展示聊天信息
st.text("会话名称：" + st.session_state.current_session)
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
    save_session()