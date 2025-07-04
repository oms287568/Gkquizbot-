import os
import telegram
import pandas as pd
import random
import asyncio

async def send_daily_quizzes():
    """
    यह फंक्शन डुप्लीकेट सवालों को हटाकर, दो यूनिक रैंडम क्विज़ भेजता है।
    """
    try:
        # Step 1: Secrets से टोकन और चैट आईडी लेना
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        
        # Step 2: बॉट ऑब्जेक्ट बनाना
        bot = telegram.Bot(token=bot_token)
        
        # Step 3: CSV फाइल से सवालों को पढ़ना
        df = pd.read_csv('questions.csv')
        
        # --- नया और बेहतर हिस्सा ---
        # सवालों में से डुप्लीकेट हटाना ताकि एक ही सवाल दोबारा न आए
        df.drop_duplicates(subset=['question'], inplace=True)
        # ------------------------

        # Step 4: दो यूनिक रैंडम सवाल चुनना
        if len(df) < 2:
            print("चेतावनी: CSV फाइल में 2 से कम यूनिक सवाल हैं, इसलिए सिर्फ 1 ही भेजा जा रहा है।")
            quiz_samples = df.sample(n=1)
        else:
            quiz_samples = df.sample(n=2, replace=False) # replace=False सुनिश्चित करता है कि दोनों सवाल अलग हों
        
        print(f"2 यूनिक क्विज़ {chat_id} पर भेजे जा रहे हैं...")

        # Step 5: दोनों सवालों को एक-एक करके भेजना
        for index, quiz_data in quiz_samples.iterrows():
            question = quiz_data['question']
            options = [str(quiz_data['option1']), str(quiz_data['option2']), str(quiz_data['option3']), str(quiz_data['option4'])]
            correct_option_id = int(quiz_data['correct_answer_index'])
            
            await bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                is_anonymous=False,
                type='quiz',
                correct_option_id=correct_option_id
            )
            print(f"'{question}' वाला क्विज़ सफलतापूर्वक भेजा गया।")
            await asyncio.sleep(2) # दो क्विज़ के बीच थोड़ा ब्रेक
            
        print("SUCCESS: सभी क्विज़ सफलतापूर्वक भेजे गए!")

    except FileNotFoundError:
        print("ERROR: questions.csv फाइल नहीं मिली।")
    except Exception as e:
        print(f"ERROR: एक बड़ी त्रुटि हुई: {e}")

if __name__ == "__main__":
    asyncio.run(send_daily_quizzes())

