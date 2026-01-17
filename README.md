# Beta
Upgraded my "Alpha" app.
# Wide AI Memo (ngrok edition)

自宅PCのローカルAI (Ollama) を、外出先のスマホから利用するためのアプリです。
ngrokを利用して、セキュアなトンネルを作成し、外部からアクセス可能にします。

## 特徴
- **API料金ゼロ**: 自宅PCの計算資源を使います。
- **どこでもアクセス**: 4G/5G回線から接続可能。
- **データ所有権**: データは全て自宅PCのCSVに保存されます。

## 前提条件
- PCに [Ollama](https://ollama.com/) が入っていること
- [ngrok](https://ngrok.com/) の無料アカウント（Authtoken）を持っていること

## 使い方
1. ライブラリをインストール
   ```bash
   pip install -r requirements.txt
