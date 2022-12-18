
import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    URIImagemapAction,
    URITemplateAction,
    ImagemapSendMessage,
    MessageImagemapAction,
    ImagemapArea,
    BaseSize)
import configparser

from fsm import LifeNumCounterMachine
from analysis import analysisGenerator

machine = LifeNumCounterMachine(
    states=['input_birth','show_analysis','watch_today_density','pure_relax'],
    transitions=[
        {'trigger' : 'lifeNumPath' , 'source' : 'user' , 'dest' : 'input_birth' , 'conditions' : 'look_life_num'},
        {'trigger' : 'lifeNumPath' , 'source' : 'input_birth' , 'dest' : 'show_analysis' , 'conditions' : 'is_going_to_watch_analysis'},
        {'trigger' : 'is_going_to_watch_density' , 'source' : 'user' , 'dest' : 'watch_today_density'},
        {'trigger' : 'is_going_to_pure_relax','source' : 'user','dest' : 'pure_relax'},
        {'trigger' : 'goBack' , 
        'source' : ['user','input_birth','show_analysis','watch_today_density','pure_relax'] , 
        'dest' : 'user'}
    ],
    initial = 'user',
    auto_transitions = False,
    show_conditions = True
)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=[ "POST"])
def callback():

    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef': #填入line在verify時回傳的user_id
        return 'OK'
    get_message = event.message.text

    # Send To Line
    
    #reply = TextSendMessage(text=f"{get_message}")
    if machine.state == 'user' and get_message!="我要放鬆心情" and get_message!="我要看本日運勢" and get_message!="我要計算生命靈數":
        reply = []
        reply.append( 
            TemplateSendMessage(
            alt_text='Buttons tempelate',
            template = ButtonsTemplate(
                title='選擇你要的功能',
                text="想要計算生命靈數，選擇『計算生命靈數』\n 想要看本日運勢，選擇『本日運勢』\n 想要放鬆心情，『放鬆心情』",
                actions=[
                    MessageTemplateAction(
                        label='計算生命靈數',
                        text='我要計算生命靈數'
                    ),
                    MessageTemplateAction(
                        label='本日運勢',
                        text="我要看本日運勢"
                    ),
                    MessageTemplateAction(
                        label="放鬆心情",
                        text="我要放鬆心情"
                    )
                ]
            )
        )
        )
        machine.goBack()
        print(machine.state)
    elif machine.state == 'user' and get_message =="我要計算生命靈數":
        reply = TextSendMessage(text="請輸入您得西曆生日 xxxx/xx/xx")
        machine.lifeNumPath(event)
    elif machine.state == "input_birth":
        try:
            machine.lifeNum = 0
            machine.lifeNumPath(event)
            your_analysis = analysisGenerator(machine.lifeNum)
            reply = TextSendMessage(text = your_analysis.analysis())
        except:
            reply = TextSendMessage(text="要重新回到選單請輸入『restart』，計算生命靈數請以 xxxx/xx/xx 輸入生日")

    elif machine.state == 'user' and get_message == "我要放鬆心情":
        reply = []
        reply.append(
            ImagemapSendMessage(
            base_url='https://i.imgur.com/1D0A2bG.jpeg',
            alt_text='url',
            base_size=BaseSize(height=1040,width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.youtube.com/watch?v=bM0OWBXg3ZE&ab_channel=%E4%B8%8D%E8%A8%B1%E8%8A%B1%E5%BF%83',
                    area={
                             "x": 0,
                            "y": 0,
                            "width": 1040,
                            "height": 1040
                        }
                    )
            ]
        )
        ) 
        reply.append(
            TextSendMessage(text="點擊圖片觀看影片")
            )
        machine.is_going_to_pure_relax()
    elif machine.state == "user" and get_message == "我要看本日運勢":
        reply = []
        reply.append(
            ImagemapSendMessage(
            base_url='https://i.imgur.com/dEJFDwb.jpeg',
            alt_text='url',
            base_size=BaseSize(height=1040,width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://astro.click108.com.tw/daily_0.php',
                    area={
                            "x": 0,
                            "y": 0,
                            "width": 1040,
                            "height": 1040
                        }
                    )
            ]
        ))
        reply.append(
            TextSendMessage(text="點擊圖片觀看本日運勢")
        )
        machine.is_going_to_watch_density()
    elif machine.state == 'user' and get_message == "":
        analysisGen = analysisGenerator(machine.lifeNum)
        comment = analysisGen.analysis()
        print(machine.lifeNum)
        machine.advance(event)
        print(machine.state)
        reply = TextSendMessage(text=f"{comment}")
    elif get_message == "restart":
        reply = []
        reply.append( 
            TemplateSendMessage(
            alt_text='Buttons tempelate',
            template = ButtonsTemplate(
                title='選擇你要的功能',
                text="想要計算生命靈數，選擇『計算生命靈數』\n 想要看本日運勢，選擇『本日運勢』\n 想要放鬆心情，『放鬆心情』",
                actions=[
                    MessageTemplateAction(
                        label='計算生命靈數',
                        text='我要計算生命靈數'
                    ),
                    MessageTemplateAction(
                        label='本日運勢',
                        text="我要看本日運勢"
                    ),
                    MessageTemplateAction(
                        label="放鬆心情",
                        text="我要放鬆心情"
                    )
                ]
            )
        )
        )
        machine.goBack()
        machine.lifeNum = 0
    else:
        reply = TextSendMessage(text="要重新回到選單請輸入『restart』")


    line_bot_api.reply_message(event.reply_token, reply)

if __name__ == "__main__":
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    app.run(port=5002)
    