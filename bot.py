import asyncio

from pyrogram import Client, filters
import json, os
from arsenic import get_session, keys, browsers, services
from asyncio import sleep
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent)
api_id = 14381680
api_hash = "e062fd165636c6a327fa0be3b8ec3276"
app = Client("my_bot",api_id=api_id, api_hash=api_hash, bot_token="5549634695:AAGGjpNzc7INyc3T9BnB3bHIiC0eAXYTP0Q")

admin = 618260788

    
def read():
    with open("class.json", "r") as openfile:
        global obj 
        obj= json.load(openfile)
async def getter():
    result = []
    browser = browsers.Firefox(**{'moz:firefoxOptions': {
            'args': ['-headless', '-log', "{'level': 'warning'}", '--no-sandbox']}
        })
    servic = services.Geckodriver(binary="/home/sadlord/Desktop/telegram-bot/univercity/geckodriver")
    async with get_session(servic, browser) as driver:
        await driver.get("http://vu.kashmar.ac.ir/vu/meeting.list.php?fid=6226916")
        ul = await driver.get_element('ul[class=pagination]')
        li = await ul.get_elements('li')
        for i in range(len(li)-2):
            res = await driver.get_element('table[id=dtBasicExample]')
            res = await res.get_element('tbody')
            results = await res.get_elements('tr')
            for i in results:
                td = await i.get_elements('td')
                title = await td[0].get_text()
                a = await td[2].get_element('a')
                link = await a.get_attribute('href')
                result.append({"title": title, "link": link})
            button = await driver.get_element('li[id=dtBasicExample_next]')
            await button.click()
            sleep(1)
        json_obj = json.dumps(result)
        with open("class.json", "w", encoding="utf-8") as file:
            file.write(json_obj)
            

async def get_links(query):
    result = []
    for i in obj:
        if query in i['title']:
            result.append(InlineQueryResultArticle(
                title=i['title'],
                input_message_content=InputTextMessageContent(
                        f"📝**{i['title']}**✅\n🔗{i['link']}"
                    )
                ))
    if len(result) == 0:
        result.append(InlineQueryResultArticle(
                title="not found",
                input_message_content=InputTextMessageContent(
                        "⭕**not found**‼"
                    )
                ))
    return result
@app.on_inline_query()
async def answer(client, inline_query):
    try:
        await inline_query.answer(
            results=await get_links(inline_query.query),
            cache_time=1
        )
    except:
        pass

@app.on_message(filters.text & filters.user(admin))
async def admins(c, m):
    commands = m.text
    if commands == "getlink":
        await getter()
        await m.reply("ok")
        read()
        await m.reply("read ok")

if os.path.exists("class.json"):
    with open("class.json", "r") as openfile:
        obj = json.load(openfile)
else:
    asyncio.run(getter())
read()
app.run()  # Automatically start() and idle()