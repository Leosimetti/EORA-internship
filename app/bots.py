from fastapi import APIRouter, Depends, status, HTTPException
from .users import UserDB, fastapi_users
from .users import collection as user_db
from .models import Bot

router = APIRouter(tags=["bots"])


@router.post("/add", status_code=status.HTTP_201_CREATED,
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


@router.post("/list", status_code=status.HTTP_201_CREATED,
             responses={
             })
async def list_current_user__bots(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    return user.bots
