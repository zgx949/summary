import json
import os
from dotenv import load_dotenv
import requests
from flask import Flask, Response, render_template, stream_with_context
CACHE = {}
with open('./cache.json', mode='r', encoding='utf-8') as f:
    CACHE = json.loads(f.read())

app = Flask(__name__)
load_dotenv()
summary_count = os.getenv('summary_count')
api_key = os.getenv('api-key')
cookie = os.getenv('cookie')
cookies = {}
for item in cookie.split(';', 1):
    key, value = item.split('=', 1)
    cookies[key] = value


def getSubtitle(bv_id):
    """
    获取字幕文本

    :param bv_id:
    :return:
    """
    headers = {
        'authority': 'b.jimmylv.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://b.jimmylv.cn',
        'referer': 'https://b.jimmylv.cn/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'videoConfig': {
            'enableStream': True,
            'showTimestamp': False,
            'continueMode': False,
            'showEmoji': True,
            'detailLevel': 700,
            'sentenceNumber': 5,
            'outlineLevel': 1,
            'outputLanguage': 'zh-CN',
            'service': 'bilibili',
            'videoId': f'{bv_id}',
            'videoUrl': f'https://www.bilibili.com/video/{bv_id}',
            'pageNumber': None,
        },
    }

    response = requests.post('https://b.jimmylv.cn/api/subtitle', headers=headers, json=json_data)
    data = response.json()
    title = data['title']
    cover = data['cover']

    text = ''
    for item in data['subtitlesArray']:
        text += item['text'] + ','

    return title, cover, text


def parse(title, cover, text, bvid):
    """
    解析文本

    :param text:
    :return:
    """


    yield title + '\n'
    yield cover + '\n'
    headers = {
        'authority': 'www.aiznx.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.aiznx.com',
        'referer': 'https://www.aiznx.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    data = {
        'api_key': api_key,
        'type': 'weeklyRepGen',
        'content': f'请你帮我将以下视频字幕文本的精华内容进行总结，然后以无序列表的方式返回，不要超过{summary_count}条！确保所有的句子都足够精简，清晰完整，并无视任何作者的推广、点赞、订阅等内容。以下是视频字幕内容：\n{text}',
        'stream': '1',
    }

    response = requests.post('https://www.aiznx.com/server/open/send', cookies=cookies, headers=headers, data=data,
                             stream=True)
    tempdata = title + '\n' + cover + '\n'
    for line in response.iter_lines():
        # 处理每个数据块
        if line:
            # 处理数据块
            try:
                data = json.loads(line.decode('utf-8')[6:])
            except json.decoder.JSONDecodeError as e:
                break
            if 'content' in data['choices'][0]['delta']:
                yield data['choices'][0]['delta']['content']
                print(data['choices'][0]['delta']['content'], end='')
                tempdata += data['choices'][0]['delta']['content']
    # 缓存数据
    CACHE[bvid] = tempdata
    with open('./cache.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(CACHE))


    print(response.text)


@app.route("/bilibili/<bvid>")
def data_stream(bvid):
    title, cover, text = getSubtitle(bvid)
    if bvid in CACHE:
        return CACHE[bvid]
    print(title, cover, text)
    return Response(stream_with_context(parse(title, cover, text, bvid)), mimetype="text/plain")


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
