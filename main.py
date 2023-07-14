from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
sender_infos = eval(os.environ["SENDER_INFOS"])
print(sender_infos)
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]


def get_weather(city_name):
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=007f1f43e5760ff51b1d40062d9a6bdc&city=" + city_name
    res = requests.get(url).json()
    print(res)
    weather = res['lives'][0]
    return weather['weather'], weather['temperature_float']


def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) +
                             "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words(type):
    words = requests.get("https://api.shadiao.pro/" + type)
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)


for sender_info in sender_infos:
    print(sender_info)
    wea, temperature = get_weather(sender_info["city"])
    data = {"user_name": {"value": sender_info["user_name"]},"other_name": {"value": sender_info["other_name"]}, "weather": {"value": wea}, "temperature": {"value": temperature}, "live_days": {"value": get_count(sender_info["start_date"])},"other_live_days": {"value": get_count(sender_info["other_start_date"])}, "birthday_left": {"value": get_birthday(sender_info["birthday"])}, "other_birthday_left": {"value": get_birthday(sender_info["other_birthday"])},"words_chp": {"value": get_words(
        'chp'), "color": get_random_color()}, "words_du": {"value": get_words('du'), "color": get_random_color()}, "words_pyq": {"value": get_words('pyq'), "color": get_random_color()}}
    print(data)
    res = wm.send_template(
        sender_info["user_id"], sender_info["template_id"], data)
    print(res)
