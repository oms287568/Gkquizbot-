import os
import telegram
import pandas as pd
import random
import asyncio

async def send_daily_quizzes():
    """
    यह फंक्शन एक साथ दो रैंडम क्विज़ उठाकर टेलीग्राम पर भेजता है।
    """
    try:
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        bot = telegram.Bot(token=bot_token)
        df = pd.read_csv('questions.csv')
        
        # एक की जगह दो रैंडम सवाल चुनना
        if len(df) < 2:
            print("चेतावनी: CSV फाइल में 2 से कम सवाल हैं, इसलिए सिर्फ 1 ही भेजा जा रहा है।")
            quiz_samples = df.sample(n=1)
        else:
            quiz_samples = df.sample(n=2)
        
        print(f"2 क्विज़ {chat_id} पर भेजे जा रहे हैं...")

        # दोनों सवालों को एक-एक करके भेजने के लिए लूप
        for index, quiz_data in quiz_samples.iterrows():
            question = quiz_data['question']
            options = [str(quiz_data['option1']), str(quiz_data['option2']), str(quiz_data['option3']), str(quiz_data['option4'])]
            correct_option_id = int(quiz_data['correct_answer_index'])
            
            # टेलीग्राम पर क्विज़ भेजना
            await bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                is_anonymous=False,
                type='quiz',
                correct_option_id=correct_option_id
            )
            print(f"'{question}' वाला क्विज़ सफलतापूर्वक भेजा गया।")
            
            # दो क्विज़ के बीच 2 सेकंड का छोटा सा ब्रेक
            await asyncio.sleep(2)
            
        print("SUCCESS: सभी क्विज़ सफलतापूर्वक भेजे गए!")

    except FileNotFoundError:
        print("ERROR: questions.csv फाइल नहीं मिली। कृपया सुनिश्चित करें कि यह फाइल मौजूद है।")
    except Exception as e:
        print(f"ERROR: एक बड़ी त्रुटि हुई: {e}")

if __name__ == "__main__":
    asyncio.run(send_daily_quizzes())
