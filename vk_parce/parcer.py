import json
import vk_api
import re
import pandas as pd


def get_owner_id(link):
    short_name = re.sub(r'https://vk.com/', '', link)
    api_req = vk.groups.getById(group_id=short_name, v=5.131)
    req_json = json.dumps(api_req[0], ensure_ascii=False)
    req_py = json.loads(req_json)
    owner_id = "".join(["-", str(req_py["id"])])
    return owner_id


def get_posts(link):
    owner = get_owner_id(link)
    posts = list()
    wall = vk.wall.get(owner_id=int(owner), count=1, v=5.131)
    for post in wall['items']:
        posts.append(post['id'])
    return posts


def get_comments(link, post_ids):
    owner = get_owner_id(link)
    comments = list()
    comments_id = list()
    for post_id in post_ids:
        post_comments = vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), thread_items_count=1, v=5.91)
        for post_comment in post_comments['items']:
            comments_id.append(post_comment['id'])
            comments.append(post_comment['text'])
        comments_replies = get_replies(link, comments_id, post_id)
        for comment_replies in comments_replies:
            if comment_replies['count'] != 0:
                for reply in comment_replies['items']:
                    comments.append(reply['text'])
    return comments


def get_replies(link, comments_id, post_id):
    owner = get_owner_id(link)
    replies = list()
    for comment_id in comments_id:
        try:
            replies.append(vk.wall.getComments(owner_id=int(owner), post_id=int(post_id), comment_id=comment_id, v=5.91))
        except vk_api.exceptions.VkApiError:
            print('ApiError')
    return replies


if __name__ == "__main__":
    gr_urls = [r"https://vk.com/true_lentach", r"https://vk.com/bad_novosti"]
    token = "ca62f3d9ca62f3d9ca62f3d9c7ca1ea088cca62ca62f3d9a8077c79d0ec187ff848d27c"
    vk_session = vk_api.VkApi()
    vk_session.token = {'access_token': token, 'expires_in': 0}
    vk = vk_session.get_api()
    comments_series = pd.Series(object)
    for url in gr_urls:
        all_posts = get_posts(url)
        posts_comments = get_comments(url, all_posts)
        group_series = pd.Series(posts_comments, copy=False, dtype=object)
        comments_series = pd.concat([comments_series, group_series], ignore_index=True)
    comments_series.to_csv('data.csv')
