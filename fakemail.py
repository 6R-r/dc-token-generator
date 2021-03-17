import requests
import json

from bs4 import BeautifulSoup

class FakeMail:
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    def change(self):
        self.session = requests.Session()
        self.session.headers = FakeMail.headers

        self.emails = []

        response = self.session.get('https://www.fakemail.net/index/index')
        credentials = json.loads(response.content.decode("utf-8-sig"))

        self.address = credentials['email']
        self.password = credentials['heslo']

    def refresh(self):
        response = self.session.get('https://www.fakemail.net/index/refresh')
        emails = json.loads(response.content.decode("utf-8-sig"))

        self.emails = [{
            "id": email["id"] - 1,
            "new": email['precteno'] == 'new',
            "from": {"name": email['od'].split(' <')[0], "email": email['od'].split('<')[1].split('>')[0]},
            "subject": email['predmet'],
            "time": email['kdy']

        } for email in emails]

    def email(self, id):
        response = self.session.get(f'https://www.fakemail.net/email/id/{id+1}')
        return response.content

    def remove(self, id):
        self.session.get(f'https://www.fakemail.net/delete-email/{id+1}')
    