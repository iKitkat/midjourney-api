from os import getenv

import aiohttp
import json
import requests
from loguru import logger

from lib.api import CALLBACK_URL
from util.fetch import fetch
from PIL import Image
from io import BytesIO

def result_parser(data):
    if 'type' in data:
        logger.debug(f'Enter result_parser')
        if data['type'] == 'end':
            if 'trigger_id' not in data:
                logger.error("Missing trigger_id in result!!")
                return
            trigger_id = data['trigger_id']
            if 'attachments' in data and len(data['attachments']) > 0\
              and 'url' in data['attachments'][0]:
                url = data['attachments'][0]['url']
                logger.info(f"Begin to download url {url} for id {trigger_id}")
                if download_url(trigger_id, url): logger.info("Succeed in download_url")
            else:
                logger.error(f"Error in getting url for trigger_id {trigger_id}!")
    return

def download_url(trigger_id, url):
    db_dir = "/root/img_db/"
    image = open(f'{db_dir}{trigger_id}.jpg','wb')
    response = requests.get(url)
    image.write(response.content)
    image.close()

    img = Image.open(f'{db_dir}{trigger_id}.jpg')
    width, height = img.size
    x = width/2
    y = height/2
    cors = [(0,0,x,y), (x,0,width,y), (0,y,x,height), (x,y,width,height)]
    ind = 1
    for c in cors:
        img.crop(c).save(f'{db_dir}{trigger_id}_{ind}.jpg', quality=95)
        ind += 1
    return True

async def callback(data):
    logger.debug(f"callback data: {data}")
    if not CALLBACK_URL:
        result_parser(data)
        return

    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        await fetch(session, CALLBACK_URL, json=data)


QUEUE_RELEASE_API = getenv("QUEUE_RELEASE_API") \
                    or "http://127.0.0.1:8062/v1/api/trigger/queue/release"


async def queue_release(trigger_id: str):
    logger.debug(f"queue_release: {trigger_id}")

    headers = {"Content-Type": "application/json"}
    data = {"trigger_id": trigger_id}
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
    ) as session:
        await fetch(session, QUEUE_RELEASE_API, json=data)
