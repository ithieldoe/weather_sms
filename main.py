import random
import requests
import os
from twilio.rest import Client

class Quotes:
    def __init__(self):
        with open('proust.txt') as file:
            self.proust = file.read()
            self.quote_list = self.proust.splitlines()
    def pick(self):
        return f'«{random.choice(self.quote_list)}» \n— Марсель Пруст'

b = Quotes()
quote = b.pick()

parameters = {
    'lat': '55.761412',
    'lon': '37.688748',
    'appid': 'cf9b72603e1607dc87b12bc4f0112103',
    'exclude': 'current,minutely,alerts',
    'units': 'metric',
    'lang': 'ru'
}
request = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=parameters)
print(request.status_code)
request_json = request.json()
id_14_hours = [request_json['hourly'][hour]['weather'][0]['id'] for hour in range(14)]
day_description = request_json['daily'][0]['weather'][0]['description']
day_feels_like = round(request_json['daily'][0]['feels_like']['day'])
umbrella = 'Не забудь зонтик ☂️!'
other_stuff = f'(^_^) Желаю хорошего дня, и помни: \n{quote}'
a = [True for id in id_14_hours if id < 700]
if any(a):
    msg = f"( ･ω･)ﾉ Доброе утро!! " \
          f"\nСегодня будет {day_description}, днем ощущается как {day_feels_like}°С. {umbrella} {other_stuff}"
else:
    msg = f"( ･ω･)ﾉ Доброе утро!! " \
          f"\nСегодня будет {day_description}, днем ощущается как {day_feels_like}°С. {other_stuff}"

account_sid = 'ACd077504190b48a7d4e8c88564b4ec9ff'
auth_token = 'c893988ddca47d2a365dd3342a41708c'
tw_phone = os.environ.get('TWILIO_PHONE')
m_phone = os.environ.get('MY_PHONE')
client = Client(account_sid, auth_token)
message_personal = client.messages.create(
                              body=msg,
                              from_=tw_phone,
                              to=m_phone
                          )

print(message_personal.status)