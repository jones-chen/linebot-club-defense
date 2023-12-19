from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import LineBotApiError

app = Flask(__name__)

# 一、參數設定
# 1. LINE Bot - Channel Access Token, Channel Secret
# https://developers.line.biz/console/channel/2002323663/basics
ChannelAccessToken = "VNCu7mavfcXIhfc5imUjuk3PexGzpNlWSBIL0FysEjLGo7WpAuL81dk+pgnsgRiZoe6bT80r0GqbJlmU6fEiVP4KCLNJVQL8rz9wbS6VVxJgJEX8/ih6/UMNXLx6O8XO8R7PRcTZ88RB9VT3ANzxFQdB04t89/1O/w1cDnyilFU="
ChannelSecret  = "246b34c7daaafaa17694fdf88e4775fd"
line_bot_api = LineBotApi(ChannelAccessToken)
handler = WebhookHandler(ChannelSecret)

# 存儲用戶權限的字典
user_permissions = {}

# 設定機器人的 ID，這可以在加入群組事件中獲取
BOT_ID = 'YOUR_BOT_ID'

# 設定管理員和共同管理員的權限
ADMIN = 3
CO_ADMIN = 2
NORMAL_MEMBER = 1

# 設定翻群次數的閾值
KICK_PEOPLE_NUM_THRESHOLD = 5
KICK_TIME_THRESHOLD = 60

# Dummy data
KickTimeCount = 40 #在幾秒內
KickPeopleNum = 6  # 踢出多少人
userList = [
    {'name':'Jones','permission':3},
    {'name':'somebody','permission':1}
]


# 定義 LINE 機器人的 Webhook 路由
@handler.add(JoinEvent)
def handle_join_event(event):
    group_id = event.source.group_id
    admin_user_id = event.source.user_id

    # 在用戶權限字典中添加管理員
    user_permissions[admin_user_id] = ADMIN

# 定義 LINE 機器人的 Webhook 路由
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    # 檢查用戶權限，若不存在則預設為一般成員
    user_permission = user_permissions.get(user_id, NORMAL_MEMBER)

    if message_text.startswith('/kick'):
        # 檢查權限
        if user_permission >= CO_ADMIN:
            target_user_id = message_text.split(' ')[1]
            kick_user(target_user_id)
        else:
            reply_message(event.reply_token, '權限不足，無法踢出成員。')

    elif message_text.startswith('/flip_group'):
        # 檢查權限
        if user_permission >= CO_ADMIN:
            flip_group(user_id)
        else:
            reply_message(event.reply_token, '權限不足，無法翻群。')

# 定義踢出用戶的函數
def kick_user(user_id):
    try:
        line_bot_api.kick_chat_member('YOUR_GROUP_ID', user_id)
    except LineBotApiError as e:
        print(e)

# 定義翻群的函數
def flip_group(admin_user_id):
    # 檢查一分鐘內翻群次數(若權限小於共同管理員，時間內，踢出人數超過上限)
    for user_id, permission in userList :
        if permission < CO_ADMIN and KickTimeCount <= KICK_TIME_THRESHOLD and KickPeopleNum >= KICK_PEOPLE_NUM_THRESHOLD]
    
    # 踢除觸發條件的用戶
    kick_user(user_id)

# 處理回覆訊息的函數
def reply_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

# 處理 LINE 機器人的 Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


if __name__ == "__main__":
    app.run()