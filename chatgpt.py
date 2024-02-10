import openai

from keys import openai_apikey
from telegram_bot import HOST, PORT

import memcache

openai.api_key = openai_apikey


async def get_answer(user_id: int, user_message: str) -> str:
    """
    Get an answer from OpenAI
    """
    try:
        acache = memcache.aCacheClient(HOST, PORT)
        user_history = await acache.get(user_id)

        user_history.append({'role': 'user', 'content': user_message})
        system_answer = await openai.ChatCompletion.acreate(
            model='gpt-3.5-turbo',
            messages=user_history,
        )

        total_tokens = system_answer['usage']['total_tokens']
        if total_tokens > 3300: # If the dialogue length has reached the maximum
            user_history = user_history[3:]

        system_answer = system_answer['choices'][0]['message']['content']
        user_history.append({'role': 'system', 'content': system_answer})

        await acache.set(user_id, user_history)

        return system_answer

    except openai.error.RateLimitError:
        return 'I can\'t answer right now, try again in 20 seconds.'

    finally:
        await acache.close()