from fastapi import APIRouter, Depends, status, HTTPException
from .users import UserDB, fastapi_users
from .users import collection as user_db
from .models import Bot

router = APIRouter(tags=["bots"])

@router.post("/add-bot", status_code=status.HTTP_201_CREATED,
             responses={
             })
async def add_bot(bot: Bot, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    bot_list = user.bots
    bot_list = list(map(lambda x: dict(x), bot_list))

    if len(bot_list) < 5:
        if bot in bot_list:
            raise HTTPException(status_code=403, detail="The requested bot already exists")
        else:
            bot_list.append(dict(bot))
            await user_db.update_one(
                {"id": user.id},
                {
                    "$set": {
                        "bots": bot_list,
                    }
                }
            )
            return user.bots
    else:
        raise HTTPException(status_code=403, detail="You already have more than 5 bots")