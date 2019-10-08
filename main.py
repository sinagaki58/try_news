import os
from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup

base_url = 'https://trysail.jp'
get_url = base_url + '/pages/update'
post_url = 'https://slack.com/api/chat.postMessage'


def main(event, context):
    html = requests.get(get_url).content
    soup = BeautifulSoup(html, 'html.parser')

    yesterday = (datetime.today() - timedelta(days=1)).date()
    titles = []
    for div in soup.find_all('div', class_='content-list'):
        for li in div.find_all('li'):
            for a in li.find_all('a'):
                url = a.get('href')
                text = a.find('h3').string
                time = a.find('span', class_='time').text.replace('UPDATE', '')

                target_date = datetime.strptime(time, "%Y.%m.%d").date()
                if yesterday == target_date:
                    titles.append(
                        {
                            'text': text,
                            'url': base_url + url
                        }
                    )
                else:
                    break

    if len(titles) == 0:
        print('no content')
        return 'no content'

    headers = {"Authorization": "Bearer " + os.environ['SLACK_BOT']}
    for t in titles:
        message = '*' + t['text'] + '*' + '\n' + \
                  t['url']
        payload = {
            'channel': 'trysail',
            'text': message,
            'mrkdwn': True
        }
        res = requests.post(post_url, headers=headers, data=payload)
        print(*res)


if __name__ == '__main__':
    main(None, None)
