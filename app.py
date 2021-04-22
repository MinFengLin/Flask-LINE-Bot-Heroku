import os
import time, datetime
from datetime import datetime

from flask import Flask, abort, request
from bs4 import BeautifulSoup
import requests

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
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

    time_now = datetime.today().date()
    get_message = time_now
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    momo_urls = ['https://m.momoshop.com.tw/goods.momo?i_code=7809731&mdiv=category&cc3=4302400000&cc1=4302400245',
                'https://m.momoshop.com.tw/goods.momo?i_code=7874514&mdiv=category&cc3=4302400000&cc1=4302400245']

    for i, m_url in enumerate(momo_urls):
        response = requests.get(m_url, headers=headers)
        soup = BeautifulSoup(response.text)
        m_title_result = soup.find(id="goodsName")
        m_price_result = soup.find(class_="priceArea")
        get_message += "\n" + m_title_result.getText() + "\n" + m_price_result.getText() + "\n\n"

    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
