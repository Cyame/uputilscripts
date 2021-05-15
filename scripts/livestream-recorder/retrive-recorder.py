#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Daniel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Install:
# $ pip3 install aiohttp asyncio backoff
#
# Usage:
# $ python3 recorder.py YOUTUBE_VIDEO_ID

import aiohttp
import asyncio
import backoff
import json
import logging
import os
import re
import time
import sys

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0',
}

@backoff.on_exception(backoff.constant, Exception, interval=3, max_tries=3)
async def load_config(session, vid):
    async with session.get('https://www.youtube.com/watch?v={}'.format(vid)) as resp:
        html_page = await resp.text()

    track_config = json.loads(re.findall('"adaptiveFormats":(\[.*?])', html_page)[0])
    audio_target = max(filter(lambda x: x['mimeType'].startswith('audio/mp4'), track_config), key=lambda x: x['bitrate'])
    video_target = max(filter(lambda x: x['mimeType'].startswith('video/mp4'), track_config), key=lambda x: x['bitrate'])

    if 'contentLength' in audio_target:
        logging.warning('stream ends, use \n{} \n{}'.format(audio_target['url'], video_target['url']))
        exit()

    return {
        'audio_url': audio_target['url'],
        'audio_itag': audio_target['itag'],
        'video_url': video_target['url'],
        'video_itag': video_target['itag'],
        'expire': time.time() + 3 * 60 * 60,
    }

@backoff.on_exception(backoff.constant, Exception, interval=3, max_tries=3)
async def load_head(session, url):
    async with session.head(f'{url}&headm=1') as resp:
        return int(resp.headers.get('X-Head-Seqnum'))

@backoff.on_exception(backoff.constant, Exception, interval=3, max_tries=3)
async def save_segment(session, url, path):
    async with session.get(url) as resp:
        assert resp.status == 200
        data = await resp.read()

    with open(path, 'wb') as f:
        f.write(data)

async def producer(session, queue, vid):
    config = {'expire': 0}
    seq = 0

    while True:
        if time.time() > config['expire']:
            try:
                config = await load_config(session, vid)
            except Exception:
                logging.exception("refresh config failed")

            logging.info(f'current audio itag: {config["audio_itag"]}, url: {config["audio_url"]}')
            logging.info(f'current video itag: {config["video_itag"]}, url: {config["video_url"]}')

        audio_head = await load_head(session, config['audio_url'])
        video_head = await load_head(session, config['audio_url'])
        head = min(audio_head, video_head)

        logging.info(f'current audio_head: {audio_head}, video_head: {video_head}')

        if seq == head:
            logging.info(f'stream end at: {head}')
            break

        while seq < head:
            await queue.put((f'{config["audio_url"]}&sq={seq}', f'{vid}.{config["audio_itag"]}.{seq}.mp4'))
            await queue.put((f'{config["video_url"]}&sq={seq}', f'{vid}.{config["video_itag"]}.{seq}.mp4'))
            seq += 1

        await asyncio.sleep(30)

async def consumer(session, queue):
    while True:
        url, path = await queue.get()
        try:
            await save_segment(session, url, path)
        except Exception:
            logging.exception("save segment {path} failed")

        logging.debug(f'finish {path}')

        queue.task_done()

async def process(vid):
    os.mkdir(vid)
    os.chdir(vid)

    logging.info(f'process {vid}')

    session = aiohttp.ClientSession(headers=HEADERS)
    queue = asyncio.Queue()

    for _ in range(8):
        asyncio.create_task(consumer(session, queue))

    await producer(session, queue, vid)

    await queue.join()
    await session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(process(sys.argv[1]))
