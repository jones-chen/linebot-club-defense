'''
功能參考：https://www.sacro.tw/linebot/
https://github.com/boybundit/linebot
'''

from flask import Flask, request, abort
import os
import linebot
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError


app = Flask(__name__)
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))     
    # app.run(host='0.0.0.0', port=port)
    app.run()

# 一、參數設定
# 1. LINE Bot - Channel Access Token, Channel Secret
# https://developers.line.biz/console/channel/2002323663/basics
inputFile = "line_data.txt"  # 替换为您的文件路径
with open(inputFile, "r", encoding="utf8") as file_in:
    ChannelAccessToken, ChannelSecret = file_in.read().split('\n')

line_bot_api = linebot.LineBotApi(ChannelAccessToken)
handler = linebot.WebhookHandler(ChannelSecret)

# 設定機器人的 ID，這可以在加入群組事件中獲取
BOT_ID = 'YOUR_BOT_ID'
BOT_STATUS = True 

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

# 存儲用戶權限的字典
user_permissions = {}

# 二、監聽路由
# 首頁
@app.route('/', methods=['GET'])
def home():
    print("Welcome to KP Protector!")
    return "Welcome to KP Protector!"

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

# # 接收使用者訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     print("接收使用者訊息")
#     user_id = event.source.user_id
#     userInput = event.message.text
#     print(f'user_id:{user_id}, userInput:{userInput}')
    
#     # 回傳訊息
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'收到訊息'))

#     # 檢查用戶權限，若不存在則預設為一般成員
#     # user_permission = user_permissions.get(user_id, NORMAL_MEMBER)

#     # if userInput.startswith('/kick'):
#     #     # 檢查權限
#     #     if user_permission >= CO_ADMIN:
#     #         target_user_id = userInput.split(' ')[1]
#     #         kick_user(target_user_id)
#     #     else:
#     #         reply_message(event.reply_token, '權限不足，無法踢出成員。')

#     # elif userInput.startswith('/flip_group'):
#     #     # 檢查權限
#     #     if user_permission >= CO_ADMIN:
#     #         flip_group(user_id)
#     #     else:
#     #         reply_message(event.reply_token, '權限不足，無法翻群。')




# # 將帳號加入群組的時候
# @handler.add(JoinEvent)
# def handle_join_event(event):
#     print("加入群組")
#     group_id = event.source.group_id
#     admin_user_id = event.source.user_id
#     print(f'group_id:{group_id}')
#     print(f'admin_user_id:{admin_user_id}')
    
#     # # 在用戶權限字典中添加管理員
#     # user_permissions[admin_user_id] = ADMIN


# # 定義翻群的函數
# def checkKickLevel(admin_user_id):
#     # 檢查踢人的人，若權限小於共同管理員，而且時間內，踢出人數超過上限)
#     for user_id, permission in admin_user_id :
#         if permission < CO_ADMIN and KickTimeCount <= KICK_TIME_THRESHOLD and KickPeopleNum >= KICK_PEOPLE_NUM_THRESHOLD:
#             # 踢除觸發條件的用戶
#             kick_user(user_id)
#             return '你亂踢人，我踢你'
#         else:
#             return '可以繼續踢'





