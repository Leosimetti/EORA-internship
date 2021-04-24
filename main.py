import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run("app.app:app", host=os.getenv("HOST_IP", "127.0.0.1"), port=5000)
