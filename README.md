# Block Domain Discord bot
## 使い方
### 1
`pip3 install -r requirements.txt`で必要なライブラリをインストールしてください。
### 2
`python3 download.py`でブロックリストをダウンロードしてください。  
- `blocklist_urls.txt`にダウンロードしたいブロックリストのURLを加えることができます。  

### 3
`config.json`にあなたのDiscord botのAPIキーを入れてください。
```
{
    "list_path": "lists",
    "TOKEN": "YOUR_DISCORD_BOT_TOKEN", << ここ
    "delete": 1,
    "send_reply": 1,
    "mention": 1
}
```
必要に応じて設定してください。
- `delete`を1にすることで該当するメッセージを削除します。
- `send_reply`を1にすることで、警告メッセージを送信します。`delete`が1になっている場合は、削除通知メッセージが送信されます。
- `mention`が1にすることで、メッセージを送信した人をメンションします。ただし`delete`が1の時のみ使えます。
- `list_path`はブロックリストを保存するフォルダです。ダウンロード実行前に設定してください。デフォルトではlistsフォルダに保存されます。
### 4
`python3 main.py`で実行してください。