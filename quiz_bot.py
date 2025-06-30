import os
import telegram
import asyncio

async def send_final_test():
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=bot_token)
    
    print(f"फाइनल टेस्ट मैसेज {chat_id} पर भेज रहा हूँ...")
    try:
        await bot.send_message(
            chat_id=chat_id,
            text="Hello! This is the final reset test."
        )
        print("मैसेज भेजने का कमांड सफलतापूर्वक दिया गया।")
    except Exception as e:
        print(f"मैसेज भेजते समय त्रुटि हुई: {e}")

if __name__ == "__main__":
    asyncio.run(send_final_test())
