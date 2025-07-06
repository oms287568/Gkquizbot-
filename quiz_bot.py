import os
import telegram
import pandas as pd
import random
import asyncio

SENT_QUESTIONS_FILE = 'sent_questions.txt'

def get_sent_questions():
    """भेजे गए सवालों की लिस्ट पढ़ता है।"""
    if not os.path.exists(SENT_QUESTIONS_FILE):
        return set()
    with open(SENT_QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def add_sent_question(question):
    """भेजे गए सवाल को रिकॉर्ड में जोड़ता है।"""
    with open(SENT_QUESTIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(question + '\n')

async def send_unique_quiz():
    """
    यह फंक्शन एक यूनिक सवाल भेजता है जो पहले नहीं भेजा गया।
    """
    try:
        # Step 1: Secrets और फाइलों को पढ़ना
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        
        all_questions_df = pd.read_csv('questions.csv')
        all_questions_df.drop_duplicates(subset=['question'], inplace=True)
        
        sent_questions = get_sent_questions()
        
        print(f"कुल यूनिक सवाल: {len(all_questions_df)}, भेजे जा चुके सवाल: {len(sent_questions)}")

        # Step 2: जो सवाल नहीं भेजे गए हैं, उनकी लिस्ट बनाना
        unsent_questions_df = all_questions_df[~all_questions_df['question'].isin(sent_questions)]
        
        # Step 3: अगर सारे सवाल भेजे जा चुके हैं, तो रिकॉर्ड रीसेट करें
        if unsent_questions_df.empty:
            print("सभी सवाल एक बार भेजे जा चुके हैं। रिकॉर्ड रीसेट कर रहा हूँ...")
            open(SENT_QUESTIONS_FILE, 'w').close() # फाइल को खाली करना
            unsent_questions_df = all_questions_df

        # Step 4: एक यूनिक सवाल चुनना
        quiz_data = unsent_questions_df.sample(n=1).to_dict(orient='records')[0]
        
        question = quiz_data['question']
        options = [str(quiz_data['option1']), str(quiz_data['option2']), str(quiz_data['option3']), str(quiz_data['option4'])]
        correct_option_id = int(quiz_data['correct_answer_index'])
        
        # Step 5: क्विज़ भेजना
        print(f"'{question}' वाला यूनिक क्विज़ {chat_id} पर भेज रहा हूँ...")
        bot = telegram.Bot(token=bot_token)
        await bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_option_id
        )
        
        # Step 6: भेजे गए सवाल को रिकॉर्ड में जोड़ना
        add_sent_question(question)
        print("SUCCESS: क्विज़ सफलतापूर्वक भेजा गया और रिकॉर्ड किया गया!")

    except FileNotFoundError:
        print("ERROR: questions.csv फाइल नहीं मिली।")
    except Exception as e:
        print(f"ERROR: एक बड़ी त्रुटि हुई: {e}")

if __name__ == "__main__":
    asyncio.run(send_unique_quiz())
