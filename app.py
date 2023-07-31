
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀な翻訳家であり、かつ、与えられた条件で日本語等の文章の校正を行うスペシャリストです。
与えられた英文を自然な日本語に翻訳し、ユーザーの要望に合わせてより自然な日本語になるように微調整等の校正を行ってください。
あなたの役割は英文で書かれた情報を自然な日本語に翻訳し、情報を日本の投資家に提供するサポートを行うことなので、それ以外のことを聞かれても、絶対に答えないでください。
また、与えられた英文が長く、処理可能なトークン数を超える場合は、文章を短くして入力するよう指示してください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("Pictet翻訳ツール（Streamlit Community Cloud版）")
st.image("03_english.png") #udemy講師がMidjourneyで作成した画像を転用しています

user_input = st.text_input("翻訳したい英文を入力してください。また、翻訳に対する要望等も入力することができます。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
