import os
import telegram
import pandas as pd
import random
import asyncio

async def send_single_quiz():
    """
    यह फंक्शन एक रैंडम क्विज़ उठाकर टेलीग्राम पर भेजता है।
    """
    try:
        # Step 1: Secrets से टोकन और चैट आईडी लेना
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        
        # Step 2: बॉट ऑब्जेक्ट बनाना
        bot = telegram.Bot(token=bot_token)
        
        # Step 3: CSV फाइल से सवालों को पढ़ना
        df = pd.read_csv('questions.csv')
        
        # --- बदलाव यहाँ है ---
        # डुप्लीकेट हटाना और सिर्फ एक रैंडम सवाल चुनना
        df.drop_duplicates(subset=['question'], inplace=True)
        quiz_data = df.sample(n=1).to_dict(orient='records')[0]
        # --------------------
        
        # Step 4: क्विज़ के लिए डेटा तैयार करना
        question = quiz_data['question']
        options = [str(quiz_data['option1']), str(quiz_data['option2']), str(quiz_data['option3']), str(quiz_data['option4'])]
        correct_option_id = int(quiz_data['correct_answer_index'])
        
        print(f"'{question}' वाला क्विज़ {chat_id} पर भेज रहा हूँ...")
        
        # Step 5: टेलीग्राम पर क्विज़ भेजना
        await bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=False,
            type='quiz',
            correct_option_id=correct_option_id
        )
        print("SUCCESS: क्विज़ सफलतापूर्वक भेजा गया!")

    except FileNotFoundError:
        print("ERROR: questions.csv फाइल नहीं मिली।")
    except Exception as e:
        print(f"ERROR: एक बड़ी त्रुटि हुई: {e}")

if __name__ == "__main__":
    asyncio.run(send_single_quiz())
