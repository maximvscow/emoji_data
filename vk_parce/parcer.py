import json
import requests
from bs4 import BeautifulSoup
import vk_api
import re
import pandas as pd
from collections import defaultdict


def get_post_ids(link):
    headers = {
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    session = requests.session()
    response = session.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.findAll('div', class_='post--with-likes')
    post_data = [item['data-post-id'] for item in posts]
    ids = list()
    for item in post_data:
        ids.append(re.sub(r'-.*_', '', item))
    return ids


def get_comments(link, post_ids):
    short_name = re.sub(r'https://vk.com/', '', link)
    api_req = vk.groups.getById(group_id=short_name, v=5.131)
    req_json = json.dumps(api_req[0], ensure_ascii=False)
    req_py = json.loads(req_json)
    own_id = "".join(["-", str(req_py["id"])])
    comments = list()
    for i in post_ids:
        comments.append(vk.wall.getComments(owner_id=int(own_id), post_id=int(i), v=5.131))
    return comments


if __name__ == "__main__":
    gr_urls = ["https://vk.com/true_lentach", "https://vk.com/bot_maxim", "https://vk.com/public143177265", "https://vk.com/dayvinchik" ]
    token = "100e8c2a347754f2303efa9742782f1450f333b72f3bdc322f492422adb911d34eb84d76b979933425189"
    user = '+79092273227'
    my_pass = 'ApiCheck13'
    vk_session = vk_api.VkApi(user, my_pass)  # token=token
    vk_session.auth()
    vk = vk_session.get_api()
    d = defaultdict(list)
    d2 = defaultdict(list)
    all_comments = list()
    for element in gr_urls:
        data = get_post_ids(element)
        all_comments.append(get_comments(element, data))
    for item in all_comments: # TODO: Вывести в отдельную функцию и добавить больше колонок в дф
        for post in item:
            post_comments_js = json.dumps(post, ensure_ascii=False)
            post_comments = json.loads(post_comments_js)
            for i in post_comments['items']:
                d[i['from_id']].append(i['text'])
    df = pd.DataFrame(list(d.items()), columns=['id', 'comment'])
    print(df)
    df.to_csv("df3.csv")
