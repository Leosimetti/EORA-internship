from fastapi import APIRouter, Depends, status, HTTPException, Request
from .users import UserDB, fastapi_users
from .users import collection as user_db
from .models import Bot
from telebot import TeleBot
import urllib.parse
import os
from pprint import pprint

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

            telegram_bot = TeleBot(bot.token)
            telegram_bot.remove_webhook()

            url = urllib.parse.urljoin(os.getenv("URL"), f"/bots/webhook/{bot.token}")
            print(url)

            telegram_bot.set_webhook(url)

            bot_list = list(map(lambda x: dict(x), bot_list))
            bot_list.append(dict(bot))
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
async def list_current_user__bots(request: Request, token: str):

    sas = await request.body()
    print("Body: \n" + sas.decode() + "\n")

    telegram_bot = TeleBot(token)
    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(urllib.parse.urljoin(os.getenv("URL"), f"/webhook/{token}"))

    return sas.decode()


@router.delete("/", status_code=status.HTTP_201_CREATED,
               responses={
                   404: {"description": "The requested bot does not exist"},
               })
async def delete_a_bot_by_name_or_token(bot: Bot, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    bot_list = user.bots

    if bot in bot_list:
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
