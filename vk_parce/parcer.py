import requests
from bs4 import BeautifulSoup


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
    posts = soup.findAll('div', class_='_post')
    post_data = [item['data-post-id'] for item in posts]
    return post_data


if __name__ == "__main__":
    tl = get_post_id("https://vk.com/true_lentach")
    bot = get_post_id("https://vk.com/bot_maxim")
    print(tl)
    print(bot)

