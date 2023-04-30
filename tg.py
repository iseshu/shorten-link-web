import httpx
import os
import re
import json
import string
import random
token = os.environ.get("TOKEN")
url = os.environ.get("URL","https://127.0.0.1:8000/")
start_inline = keyboard = {
    'inline_keyboard': [
        [{'text': 'View On GitHub', 'url': 'https://github.com/iseshu/shorten-link-web'}]
    ]
}
async def create_url(url):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if url in data['links']:
        return {'url': url,"id": data['ids'][data['links'].index(url)]}
    else:
        id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        with open('data.json', 'w') as f:
            data['ids'].append(id)
            data['links'].append(url)
            json.dump(data, f)
        return {"id":id,"url":url}

async def telegram(data):
    urls = re.findall("(?P<url>https?://[^\s]+)", data['message']['text'])
    if len(urls)>0:
        url = urls[0]
        dat = await create_url(url)
        short_url = dat['id']
        text = f"✔️ Successfully created\nMain Links: `{url}`\nShotrend Link :\n`{url}o/{short_url}`\nCreate your own Url Website"
        params = {"chat_id": data['message']['chat']['id'],"text": text,"parse_mode":"markdown","reply_markup":json.dumps(start_inline)}
        httpx.get(f"https://api.telegram.org/bot{token}/sendMessage",params=params)
    else:
        text = f"**Hello {data['message']['chat']['first_name']}**,\nI'm a simple url shotern bot \nJust send me url to short it\nYou can also create this and even website from git repo"
        params = {"chat_id": data['message']['chat']['id'],"text": text,"parse_mode":"markdown","reply_markup":json.dumps(start_inline)}
        httpx.get(f"https://api.telegram.org/bot{token}/sendMessage",params=params)
       
            

