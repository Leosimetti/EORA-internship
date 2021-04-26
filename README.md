# EORA-internship
Test task for the EORA-internship in the form of a Telegram-bot management system.

## Workflow that is available in the documantation

1. Register at the `POST /auth/register`
2. Login at the `POST /auth/cookie/login` so that you get a cookie from the website
3. Get verified at `POST /cheat-verify` (It can be done the long way as well)
4. Add some bots at `POST /bots`
5. The bots work
6. ???


## How to deploy on your PC
Since there is a DockerFile for the server - deploying it along with the database is as simple as executing command in the project root
```console
docker-compose up 
```
The server will launch on port 80

A mongoDB instance will start on port 27017

A mongoExpress intance to view DB conent will start on port 8081

P.S all the ports can be changed in the docker-compose file

## Deployed version with documentation
A CI/CD flow that automatically runs tests and deploys to heroku was set up.
You can go to https://eora-internship-test.herokuapp.com/docs#/ to see the latest API with documentation and try it out.
