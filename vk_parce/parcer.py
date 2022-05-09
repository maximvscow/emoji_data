import vk_api
import re
import pandas as pd
import time
import datetime
import json


def get_owner_id(link):
    short_name = re.sub(r'https://vk.com/', '', link)
    api_req = vk.groups.getById(group_id=short_name, v=5.131)
    req_json = json.dumps(api_req[0], ensure_ascii=False)
    req_py = json.loads(req_json)
    owner_id = "".join(["-", str(req_py["id"])])
    return owner_id


def get_posts(link, begin_date):
    owner = get_owner_id(link)
    posts_list = list()
    end_date = date_begin + 86400
    wall = vk.wall.get(owner_id=int(owner), count=5, v=5.131)
    for post in wall['items']:
        if begin_date < post['date'] < end_date:
            post_data = dict()
            post_date = time.gmtime(post['date'])
            readable = time.strftime("%d/%m/%Y", post_date)
            post_data['public'] = link
            post_data['id'] = int(post['id'])
            post_data['date'] = readable
            post_data['text'] = post['text']
            post_data['comments'] = []
            posts_list.append(post_data)
        elif post['date'] < begin_date:
            break
    return posts_list


def get_comments(link, posts):
    owner = get_owner_id(link)
    for post in posts:
        post_id = post['id']
        post_comments = vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), thread_items_count=1, v=5.91)
        for post_comment in post_comments['items']:
            comment = dict()
            comment_id = post_comment['id']
            comment['user'] = post_comment['from_id']
            comment['text'] = post_comment['text']
            post['comments'].append(comment)
            comment_replies = get_replies(link, comment_id, post_id)
            if comment_replies[0]['count'] != 0:
                for reply in comment_replies[0]['items']:
                    comment = dict()
                    comment['user'] = reply['from_id']
                    comment['text'] = reply['text']
                    post['comments'].append(comment)
    return posts


def get_replies(link, comment_id, post_id):
    owner = get_owner_id(link)
    replies = list()
    try:
        replies.append(vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), comment_id=comment_id, v=5.91))
    except vk_api.exceptions.VkApiError:
        print('ApiError')
    return replies


if __name__ == "__main__":
    gr_urls = [r"https://vk.com/true_lentach"]
    token = "ca62f3d9ca62f3d9ca62f3d9c7ca1ea088cca62ca62f3d9a8077c79d0ec187ff848d27c"
    vk_session = vk_api.VkApi()
    vk_session.token = {'access_token': token, 'expires_in': 0}
    vk = vk_session.get_api()
    print('**Парсер сообществ социальной сети ВКонтакте (VK) \n')
    print('Сообщества, из которых собираются данные:')
    for url in gr_urls:
        print(url)
    check = input("Вам необходимо добавить новое сообщество? (да/нет): ")
    try:
        if check == "да":
            new_url = input("Введите ссылку на сообщество: ")
            gr_urls.append(new_url)
    except Exception as e:
        


    date = input("Введите дату, за которую необходимо собрать сообщения со стены,"
                 " в формате %d/%m/%Y (например 01/01/2022): ")
    date_begin = int(datetime.datetime.strptime(date, "%d/%m/%Y").timestamp())
    for url in gr_urls:
        all_posts = get_posts(url, date_begin)
        full_posts_data = get_comments(url, all_posts)
        for post in full_posts_data:
            post = json.dumps(post)
            json_post = json.loads(post)
            print(json_post)

