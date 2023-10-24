import openai
import requests
import time

openai.api_key = "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"
TOKEN = "6527924588:AAF1XypagzejmKDSsTwwCzk6AM6tAmr9ZMA"

def get_updates(offset):
       url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
       params = {"timeout": 100, "offset": offset}
       response = requests.get(url, params=params)
       return response.json()["result"]

def send_messages(chat_id, text):
       url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
       params = {"chat_id": chat_id, "text": text}
       response = requests.post(url, params=params)
       return response

def get_openai_response(prompt):
       model_engine = "davinci:ft-personal-2023-10-23-17-03-55"
       response = openai.Completion.create(
              engine = model_engine,
              prompt = prompt,
              max_tokens = 200,
              n = 1,
              stop = " END",
              temperature = 0.5
       )
       return response.choices[0].text.strip()

def main():
    print("Starting bot...")
    offset = 0
    while True:
            updates = get_updates(offset)
            if updates:
                    for update in updates:
                        offset = update["update_id"]+1
                        chat_id = update["message"]["chat"]['id']
                        user_message = update["message"]["text"]
                        print(f"Received message: {user_message}")
                        GPT = get_openai_response(user_message)
                        send_messages(chat_id, GPT)
            else:
                time.sleep(1)
if __name__ == '__main__':
       main()