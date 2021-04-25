from fastapi import APIRouter, Depends, status, HTTPException, Request
from .users import UserDB, fastapi_users
from .users import collection as user_db
from .models import Bot
from telebot import TeleBot
from telebot.types import Message, Update
import urllib.parse
import os
import json

router = APIRouter(tags=["bots"])


@router.post("/", status_code=status.HTTP_201_CREATED,
             responses={
                 403: {"description": "You already have more than 5 bots"},
                 409: {"description": "The requested bot already exists"}
             })
async def adds_a_bot(bot: Bot, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    bot_list = user.bots

    if len(bot_list) < 5:
        if bot in bot_list:
            raise HTTPException(status_code=409, detail="The requested bot already exists")
        else:

            if os.getenv("HOST_IP") is not None:
                telegram_bot = TeleBot(bot.token)
                telegram_bot.remove_webhook()

                url = urllib.parse.urljoin(os.getenv("URL"), f"/bots/webhook/{bot.token}")
                telegram_bot.set_webhook(url)

            bot_list = list(map(lambda x: dict(x), bot_list))
            bot_list.append(bot.dict())
            await user_db.update_one(
                {"id": user.id},
                {
                    "$set": {
                        "bots": bot_list,
                    }
                }
            )
            return bot_list
    else:
        raise HTTPException(status_code=403, detail="You already have more than 5 bots")


@router.get("/", status_code=status.HTTP_201_CREATED,
            responses={
            })
async def list_current_user__bots(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    return user.bots


@router.post("/webhook/{token}", status_code=status.HTTP_201_CREATED,
             responses={
             })
async def endpoint_for_bots(request: Request, token: str):
    sas = await request.body()
    decoded = json.loads(sas.decode())
    print("Body: \n" + sas.decode() + "\n")

    telegram_bot = TeleBot(token)

    @telegram_bot.message_handler()
    def echo(m: Message):
        telegram_bot.send_message(m.chat.id, m.text)

    telegram_bot.process_new_updates([Update.de_json(decoded)])

    return sas.decode()


@router.delete("/", status_code=status.HTTP_201_CREATED,
               responses={
                   404: {"description": "The requested bot does not exist"},
               })
async def delete_a_bot_by_name_or_token(bot: Bot, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    bot_list = user.bots

    if bot in bot_list:

        if os.getenv("HOST_IP") is not None:
            telegram_bot = TeleBot(bot.token)
            telegram_bot.remove_webhook()

        bot_list.remove(bot)
        bot_list = list(map(lambda x: dict(x), bot_list))
        await user_db.update_one(
            {"id": user.id},
            {
                "$set": {
                    "bots": bot_list,
                }
            }
        )
        return bot_list
    else:
        raise HTTPException(status_code=404, detail="The requested bot does not exist")
