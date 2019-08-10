import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

base_url = 'https://trysail.jp'
get_url = base_url + '/pages/update'
post_url = 'https://slack.com/api/chat.postMessage'

BOT_ACCESS_TOKEN = 'xoxb-492163356806-716184467233-tWiO1HMtkrMr1M87zDgVK8CY'


def main():
    html = requests.get(get_url).content
    soup = BeautifulSoup(html, 'html.parser')

    today = datetime.today().date()
    titles = []
    for div in soup.find_all('div', class_='content-list'):
        for li in div.find_all('li'):
            for a in li.find_all('a'):
                url = a.get('href')
                text = a.find('h3').string
                time = a.find('span', class_='time').text.replace('UPDATE', '')
                label = a.find_all('span', class_='label')[1].string

                target_date = datetime.strptime(time, "%Y.%m.%d").date()
                if (today == target_date):
                    titles.append(
                        {
                            'text': text,
                            'url': base_url + url,
                            'label': label
                        }
                    )
                else:
                    break

    if len(titles) == 0:
        print('no content')
        return

    headers = {"Authorization": "Bearer " + BOT_ACCESS_TOKEN}
    for t in titles:
        message = '*' + t['text'] + '*' + '\n' + \
            t['url'] + '\n' + \
            '`' + t['label'] + '`'
        payload = {
            'channel': 'trysail',
            'text': message,
            'mrkdwn': True
        }
        res = requests.post(post_url, headers=headers, data=payload)
        print(res.ok)


main()
