# -*- coding: utf-8 -*-

#版本1.0
import os
import requests
import json
import re

import botpy
from botpy import logging

from botpy.message import DirectMessage
from botpy.message import Message
from botpy.ext.cog_yaml import read

#---------配置---------

url = "https://127.0.0.1:443/opencommand/api" #此地址需要带端口和结尾的/opencommand/api

console_token = ""#填写控制台的token，可在opencommand处看到教程

console_token_mode = 2 #使用控制台执行命令的身份组权限 1-全体成员 2-管理员 4-频道创建者 5-子频道管理员

console_token_use = True #允许频道主等身份组使用控制台执行命令，默认开启

#----------------------



usertoken = {"null":"null"}
customcommand = {"prop um 1":"解锁地图"}

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")


    async def on_at_message_create(self, message: Message):
        message.content = message.content[23:]
        #/帮助命令
        if("/帮助" in message.content ):
                    backw = "本机器人由啊这.制作\n服务端需要先安装opencommand插件\n以下是本机器人的使用帮助\n1.先进入游戏\n使用/绑定 uid 命令\n2.进入游戏，查看机器人发送的验证码\n3.使用/验证 验证码 命令绑定uid\n4.使用! 以玩家身份执行gc的命令 使用# 以控制台身份执行gc的命令"


        #/状态命令
        elif("/状态" in message.content ):
                    data = {"action": "online"}
                    x = requests.post(url, json=data,verify=False)
                    online = json.loads(x.text)
                    online_data = online["data"]
                    player_list = online_data["playerList"]
                    backw = "当前服务器在线人数为" + str(online_data["count"] )
                    if(online_data["count"] > 0):
                        if(online_data["count"] <= 20):
                            backw = backw +"\n在线玩家为：" + " ｜ ".join(player_list)
                        else:
                            backw = backw + "\n在线玩家过多，不进行展示"
                    else:
                        backw = backw +""       


        #其它的情况？
        else:
            backw = "未知命令，请使用/帮助 获取帮助"

        #反馈
        _message = await message.reply(content="[GCbot]" + str(backw))
















if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道 
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
