from json import dumps
import json
from httplib2 import Http
import requests
import time

def get_recent_questions(tag):
    url = f"https://api.stackexchange.com/2.2/questions?order=desc&sort=creation&tagged={tag}&site=stackoverflow"
    response = requests.get(url)
    return json.loads(response.text)

def get_questions_last_x_mins(tag):
    questions = get_recent_questions(tag)
    current_time = time.time()
    recent_questions = []
    for question in questions['items']:
        # The API returns time in Unix timestamp format, we convert it to seconds
        creation_time = question['creation_date']
        if current_time - creation_time <= 7200:  # Check if the question was created in the last 2 hours (7200 seconds)
            recent_questions.append(question)
    return recent_questions

def create_message(question):
    message = ""
    message += f"{question['title']}\n{question['link']}\n\n"
    return message

def send_notification(message):    
    # url = "URL_PLACEHOLDER"
    url = "https://chat.googleapis.com/v1/spaces/AAAAvSeABMg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_7ItRMWVmFaCSrLR5yVzJcVuHHCP9ArzX-gNSi98DTI"

    app_message = {"text": message}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )

questions = get_questions_last_x_mins('wso2-api-manager')
for question in questions:
    msg = create_message(question)
    send_notification(msg)
print("Sent " + str(len(questions)) + " message(s)")
