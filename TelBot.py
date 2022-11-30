import logging
import config
from aiogram import Bot, Dispatcher, executor, types

from bs4 import BeautifulSoup as bs
import requests
import lxml

logging.basicConfig(level = logging.INFO)

bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("What can this bot do?\n\nThis bot can help you if you forgot the name of a Lego Technic set or what it looks like.\n\nHow to use it?\n\nUse the \".set\" command. Then enter the set number. For example: \".set 42111\"")

@dp.message_handler()
async def main(massage: types.Message):
    if massage.text.startswith(".set"):
        set = massage.text.replace(".set", "")
        set = set.replace(" ", "")
        url = "https://rebrickable.com/sets/" + set + "-1"
        res = requests.get(url)
        soup = bs(res.text, "lxml")

        error = soup.find("div", id = "content")
        error = error.find("strong")
        if error == None:
      

            table = soup.find("table", class_ = "table table-wrap")
            name = table.find_all("td")[1].text
            inventory = table.find_all("a")[1].text

            img = soup.find("img", class_ = "img-responsive").get("src")

            section = soup.find_all("section", class_ = "padding-xxs")[1]
            sale = section.find_all("span", class_ = "trunc")
            sale = [i.text for i in sale]
            try: section.strike.decompose()
            except: pass
            price = section.find_all("a", target = "_blank")
            price = [price[i].text.replace("\n", "") for i in range(1, len(price), 2)]
            text = f"{name}: {set}\ninventory: {inventory}"
            text += "\n"
            for i in range(0, len(sale)):
                text += f"\n{sale[i]}: {price[i]}"

            await massage.answer(text)
            await massage.answer_photo(img)
        else:
            await massage.answer("Not Found")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)