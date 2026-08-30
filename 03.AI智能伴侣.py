import streamlit as st
import os
from openai import OpenAI

#运行方式:终端输入 streamlit run xxx.py
print("------> 重新执行此文件,渲染展示页面")

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    # 布局(居中或铺满)
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.haust.edu.cn/',
        'Report a bug': "https://www.gdut.edu.cn/",
        'About': "# 这是一个AI智能伴侣,您可以与它进行对话,它会使用温柔可爱的语气回答您的问题~"
    }#控制选项的作用
)

#大标题
st.title("AI智能伴侣")

#logo
st.logo("./resources/logo.png")

#创建与AI大模型交互的客户端对象(DEEPSEEK_API_KEY和对应的值)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
    )


# 初始化聊天信息
if "messages" not in st.session_state:#st.session_state:streamlit的记忆,用于存储用户输入的消息和AI大模型的回复
    st.session_state["messages"] = []
if "nick_name" not in st.session_state:
    st.session_state["nick_name"] = "小甜甜"
if "character" not in st.session_state:
    st.session_state["character"] = "你是一名非常可爱的ai助理,你的名字叫小甜甜,请你使用温柔可爱的语气回答用户的问题"
if "relation" not in st.session_state:
    st.session_state["relation"] = "好友"
if "num_messages" not in st.session_state:
    st.session_state["num_messages"] = 1
if "is_ok" not in st.session_state:
    st.session_state["is_ok"] = "允许"
if "reply_type" not in st.session_state:
    st.session_state["reply_type"] = "回复简短，像微信聊天一样"
# 显示聊天记录
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

#制造左边侧边栏(通过session_state记录用户输入的昵称和伴侣性格)
with st.sidebar:
    st.subheader("伴侣信息")
    #昵称输入框
    nick_name = st.text_input("昵称",placeholder="请输入伴侣的昵称",value = st.session_state.nick_name)
    #与用户关系输入框
    relation = st.text_input("与您的关系",placeholder="请输入与您的关系",value = st.session_state.relation)
    # 一次回复几条消息输入框,默认值为1条
    num_messages = st.number_input("一次回复几条消息",value = st.session_state.num_messages, min_value=1, max_value=10)
    #是否禁止任何场景或状态描述性文字输入框
    is_ok = st.text_input("是否禁止任何场景或状态描述性文字",placeholder="请输入是否禁止任何场景或状态描述性文字",value = st.session_state.is_ok)
    #回复方式输入框
    reply_type = st.text_input("回复方式",placeholder="请输入回复方式",value = st.session_state.reply_type)
    # 性格输入区域
    character = st.text_area("伴侣性格",placeholder="请输入伴侣的性格",value = st.session_state.character)
    if nick_name:
        st.session_state["nick_name"] = nick_name
    if character:
        st.session_state["character"] = character
    if relation:
        st.session_state["relation"] = relation
    if num_messages:
        st.session_state["num_messages"] = num_messages
    if is_ok:
        st.session_state["is_ok"] = is_ok
    if reply_type:
        st.session_state["reply_type"] = reply_type

system_prompt = """
你叫%s，现在是用户的真实%s，请完全代入角色。
规则：
1. 每次只回 %s 条消息
2. %s任何场景或状态描述性文字
3. 匹配用户的语言
4. %s
5.有需要的话可以用❤️🌸等 emoji 表情和颜文字
6. 用符合%s性格的方式对话
7. 回复的内容，要充分体现%s的性格特征

助理性格：
‑ %s

你必须严格遵守上述规则来回复用户。
"""

#消息输入框
prompt = st.chat_input("请输入您要咨询的问题ovo~")#定义消息输入框
if prompt:#字符串会自动转换为布尔值,所以用户没输入内容时,会返回False
    st.chat_message("user").write(prompt)#展示消息内容
    print("------>调用AI大模型,用户输入的提示词是:",prompt)
    # 记录用户输入的消息(重点)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    #与AI大模型交互,参数
    response = client.chat.completions.create(
        model="deepseek-v4-flash-vision-exp",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.relation, st.session_state.num_messages, st.session_state.is_ok, st.session_state.reply_type, st.session_state.relation,st.session_state.relation,st.session_state.character)},
            *st.session_state["messages"],
        ],
        stream=True
)
    #--------------------------非流式输出的解析方式-------------------
    # # 打印AI大模型的回复到终端
    # print("<------AI大模型的回复是:",response.choices[0].message.content)
    # #显示AI大模型的回复到页面
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 最后,记录AI大模型的回复
    #st.session_state["messages"].append({"role": "assistant", "content": response.choices[0].message.content})
    #--------------------------流式输出的解析方式-------------------
    response_message = st.empty()#定义一个空的消息框,用于展示AI大模型的回复
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
            # 打印AI大模型的回复到终端
            print(content, end = "", flush = True)
    # 最后,记录AI大模型的回复
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

