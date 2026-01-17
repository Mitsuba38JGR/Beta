import streamlit as st
import pandas as pd
import os
import ollama
from datetime import datetime
from pyngrok import ngrok

# --- 設定エリア ---
# ngrokの認証トークン（ここに直接書くか、環境変数で設定）
# ※Gitに上げる場合は直接書かず、下の st.text_input で入力する運用が安全です
NGROK_AUTH_TOKEN = "" 

# 保存ファイル名
CSV_FILE = "memo_data.csv"

# --- 関数定義 ---

def init_tunnel():
    """ngrokを使って外部公開用URLを発行する"""
    # すでに接続されているか確認
    tunnels = ngrok.get_tunnels()
    if not tunnels:
        try:
            # Streamlitのポート(8501)を公開
            public_url = ngrok.connect(8501).public_url
            return public_url
        except Exception as e:
            return f"Error: {e}"
    else:
        return tunnels[0].public_url

def get_ai_response(user_input):
    """Local Ollamaで応答"""
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'user', 'content': f"以下の入力を日本語で要約・整理して記録してください: {user_input}"},
        ])
        return response['message']['content']
    except Exception as e:
        return f"AIエラー: {e}"

def save_data(timestamp, user, ai):
    """CSV保存"""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Timestamp", "User", "AI"])
    
    new_data = pd.DataFrame({"Timestamp": [timestamp], "User": [user], "AI": [ai]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- アプリ画面 ---

st.set_page_config(page_title="Wide AI Memo", layout="wide")
st.title("🌏 Wide AI Memo (外出先モード)")

# サイドバーで接続情報を表示
with st.sidebar:
    st.header("接続設定")
    
    # トークン入力（保存はされません）
    token_input = st.text_input("ngrok Authtoken", type="password")
    
    if token_input:
        ngrok.set_auth_token(token_input)
        url = init_tunnel()
        st.success("公開成功！")
        st.code(url, language="text")
        st.caption("↑ このURLをスマホで開いてください")
    else:
        st.warning("Authtokenを入力するとURLが発行されます")

# メイン機能
st.write("家のPCで動いているAIを、外から操作できます。")

with st.form("memo_form", clear_on_submit=True):
    user_input = st.text_area("メモを入力", height=150)
    submitted = st.form_submit_button("記録 & AI処理")

    if submitted and user_input:
        with st.spinner("自宅のPCが考え中..."):
            ai_reply = get_ai_response(user_input)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(now, user_input, ai_reply)
            st.success("自宅のCSVに保存完了！")

# 履歴表示
st.divider()
st.subheader("📂 自宅PC内の記録データ")
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE).iloc[::-1] # 新しい順
    for index, row in df.iterrows():
        with st.expander(f"{row['Timestamp']} - {str(row['User'])[:10]}..."):
            st.markdown(f"**あなた:** {row['User']}")
            st.info(f"**AI:** {row['AI']}")
