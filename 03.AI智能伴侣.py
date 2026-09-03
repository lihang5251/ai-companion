import streamlit as st
import os
from openai import OpenAI
import datetime
import json
#运行方式:终端输入 streamlit run xxx.py
print("------> 重新执行此文件,渲染展示页面")

# 设置页面的配置项
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    # 布局(居中或铺满)
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/lihang5251/ai-companion",
        'About': "# 这是一个AI Chat,您可以与它进行对话,它会按照您设定的关系和人设进行聊天~"
    }#控制选项的作用
)

#大标题
st.title("AI Chat")

#logo
st.logo("./resources/logo.png")

#创建与AI大模型交互的客户端对象(DEEPSEEK_API_KEY和对应的值)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
    )

# ========== 密码验证 ==========
PASSWORD = "A114514"  # ← 改成你自己的密码

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    pwd = st.text_input("请输入密码", type="password", placeholder="请输入访问密码")
    if pwd == PASSWORD:
        st.session_state["authenticated"] = True
        st.rerun()
    elif pwd:
        st.error("密码错误，请重试")
    st.stop()
# ========== 密码验证结束 ==========

#保存会话信息函数
def save_session():
    if st.session_state["current_session"]:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state["nick_name"],
            "character": st.session_state["character"],
            "relation": st.session_state["relation"],
            "num_messages": st.session_state["num_messages"],
            "is_ok": st.session_state["is_ok"],
            "reply_type": st.session_state["reply_type"],
            "messages": st.session_state["messages"],
            "current_session": st.session_state["current_session"]
        }
    # 如果sessions文件夹不存在,则创建一个
    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    # 保存会话数据
    with open(f"sessions/{st.session_state['current_session']}.json", "w", encoding = "utf-8") as f:
        json.dump(session_data, f, ensure_ascii = False, indent = 4)

#加载所有的会话列表信息
def load_sessions():
    session_list = []
    #加载sessions目录下的文件
    if os.path.exists("sessions"):
        # 遍历sessions目录下的所有文件,如果文件名以json结尾,则加载该文件
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
                print(filename[:-5])
    session_list.sort(reverse = True)#将会话列表按时间排序,最新的会话在最前面
    return session_list
#加载指定的会话信息
def load_session(session_name):
    try :
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding = "utf-8") as f:
                session_data = json.load(f)
                st.session_state["current_session"] = session_data["current_session"]
                st.session_state["nick_name"] = session_data["nick_name"]
                st.session_state["character"] = session_data["character"]
                st.session_state["relation"] = session_data["relation"]
                st.session_state["num_messages"] = session_data["num_messages"]
                st.session_state["is_ok"] = session_data["is_ok"]
                st.session_state["reply_type"] = session_data["reply_type"]
                st.session_state["messages"] = session_data["messages"]
    except Exception :
        st.error("加载会话失败!")

def delete_session(session_name):
    try :
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")#删除文件
    except Exception :
        st.error("删除会话失败!")
    #如果删除的会话是当前会话,则将当前会话设置为历史中的第一个会话
    if session_name == st.session_state["current_session"]:
        st.session_state["current_session"] = load_sessions()[0]
# 初始化聊天信息
session_list = load_sessions()
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
if "current_session" not in st.session_state:
    # 初始化当前会话名字,格式为:年-月-日_时-分-秒
    st.session_state["current_session"] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# 显示聊天记录
st.text(f"当前会话:{st.session_state['current_session']}")
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

#制造左边侧边栏(通过session_state记录用户输入的所有信息)
with st.sidebar:
    st.subheader("伴侣信息")
    #新建会话按钮,点击按钮返回True,否则返回False
    if st.button("新建会话",width = "stretch",icon = "✏️"):

        #2.创建新的会话
        if st.session_state["messages"]:
            st.session_state["messages"] = []
            st.session_state["current_session"] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_session()
            st.rerun()#重新运行当前页面,刷新页面

        #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])# 把页面分成两列：左列占4份宽，右列占1份宽
        with col1:#  进入左列，下面缩进的内容都放在左列
            #三元运算符:如果条件为True,则执行第一个表达式,否则执行第二个表达式 --> 值1 if 条件 else 值2
            if st.button(session,width = "stretch",icon ="📄",type="primary" if session == st.session_state["current_session"] else "secondary") :
                load_session(session)
                st.rerun()
        with col2:# 进入右列，下面缩进的内容都放在右列
            if st.button("",width = "stretch",icon ="❌",key =f"delete_{session}"):
                delete_session(session)
                st.rerun()
    #分割线
    st.divider()


    #昵称输入框
    nick_name = st.text_input("昵称",placeholder="请输入对方的昵称",value = st.session_state.nick_name)
    #与用户关系输入框
    relation = st.text_input("与您的关系",placeholder="请输入对方与您的关系",value = st.session_state.relation)
    # 一次回复几条消息输入框,默认值为1条
    num_messages = st.number_input("一次回复几条消息",value = st.session_state.num_messages, min_value=1, max_value=10)
    #是否禁止任何场景或状态描述性文字输入框
    is_ok = st.text_input("是否禁止任何场景或状态描述性文字",placeholder="请输入是否禁止任何场景或状态描述性文字",value = st.session_state.is_ok)
    #回复方式输入框
    reply_type = st.text_input("回复方式",placeholder="请输入回复方式",value = st.session_state.reply_type)
    # 性格输入区域
    character = st.text_area("人设,角色设定",placeholder="请输入人设,角色设定",value = st.session_state.character)

    # 保存用户输入的信息
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
    #保存会话信息
    save_session()
