import requests
import bs4
import telegramBot
import time
starttime = time.time()


def get_all():
    telegramBot.new_posts_note()
    # print(all_us)
    pass

while True:
    get_all()
    time.sleep(10.0 - ((time.time() - starttime) % 10.0))


