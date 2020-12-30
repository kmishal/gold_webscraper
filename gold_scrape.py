# Make api request
import requests
# Beautiful soup to format and parse HTML data
from bs4 import BeautifulSoup
# twilio api to send sms
from twilio.rest import Client
# module to extract data from config.ini
import configparser
get_config = configparser.ConfigParser()
# Read data from config.ini
get_config.read('config.ini')


gold_dic = {
    '22k': [],
    '24k': []
}


def scrape_data():
    message = ''
    result = requests.get(get_config['Requests']['domain_name'])

    soup = BeautifulSoup(result.content, 'lxml')

    gold_data = soup.select('.gold_silver_table.right-align-content')

    for i in range(0, 2):
        strip_str = gold_data[i].select(
            '.odd_row')[1].get_text().strip().replace('\n', '').split("₹")
        if i == 0:
            gold_dic['22k'] = tuple([str.strip() for str in strip_str])
        elif i == 1:
            gold_dic['24k'] = tuple([str.strip() for str in strip_str])

    for key in gold_dic:
        # print gold rate
        grams, today, yesterday, hike = gold_dic[key]
        message += f'{key} rate {grams} - T - Rs {today} - Y - Rs {yesterday} \n'

    return message


def send_msg(msg_body):
    account_sid = get_config['twilio_data']['account_sid']
    auth_token = get_config['twilio_data']['auth_token']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=msg_body,
        from_=get_config['twilio_data']['from_mobile'],
        to=get_config['twilio_data']['to_mobile']
    )

    print(f"message sent at {message.date_created}")


if __name__ == "__main__":
    message_body = scrape_data()
    send_msg(message_body)
