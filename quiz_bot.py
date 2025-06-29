import telegram
import pandas as pd
import random
import os

def send_quiz():
    try:
        # GitHub Secrets से टोकन और चैट आईडी लेना
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        
        bot = telegram.Bot(token=bot_token)
        
        df = pd.read_csv('questions.csv')
        quiz_data = df.sample(n=1).to_dict(orient='records')[0]
        
        question = quiz_data['question']
        options = [quiz_data['option1'], quiz_data['option2'], quiz_data['option3'], quiz_data['option4']]
        correct_option_id = int(quiz_data['correct_answer_index'])
        
        bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_option_id
        )
        print("क्विज सफलतापूर्वक भेजा गया!")

    except Exception as e:
        print(f"कोई त्रुटि हुई: {e}")

if __name__ == "__main__":
    send_quiz()
