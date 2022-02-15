import requests
from bs4 import BeautifulSoup
import vk_api
import re


def get_post_id(link):
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
    data = list()
    for item in post_data:
        data.append(re.sub(r'-.*_', '', item))
    return data


if __name__ == "__main__":
    tl = get_post_id("https://vk.com/true_lentach")
    bot = get_post_id("https://vk.com/bot_maxim")
    print(tl)
    print(bot)
    token = "100e8c2a347754f2303efa9742782f1450f333b72f3bdc322f492422adb911d34eb84d76b979933425189"
    user = '+79092273227'
    my_pass = ''
    vk_session = vk_api.VkApi(user, my_pass)  # token=token
    vk_session.auth()
    vk = vk_session.get_api()
    tl_comments = list()
    for item in tl:
        tl_comments.append(vk.wall.getComments(owner_id=-125004421, post_id=int(item), v=5.131))
    print(tl_comments)

