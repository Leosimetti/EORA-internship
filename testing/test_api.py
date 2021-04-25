import json

endpoint = "/bots/"
bot_token = "1709125949:AAGp2dAQLVKUJqr6psnxpV7zGExwhIWs4bk"


def test_add_one(client, authorization_token):
    bot = {"label": "CoolBot", "token": bot_token}

    response = client.post(endpoint,
                           headers={"Authorization": f"Bearer {authorization_token}"},
                           json=bot)
    assert response.status_code == 201, f"{response.status_code} : {response.text}"

    response = client.get(endpoint,
                          headers={"Authorization": f"Bearer {authorization_token}"})
    result = json.loads(response.text)
    assert len(result) == 1, f"Added {len(result)} bots instead of 1"

    resulting_bot = result[0]
    assert resulting_bot == bot, f"Expected {bot}, But got {resulting_bot}"


def test_submit_incorrect_bot_name(client, authorization_token):
    response = client.post(endpoint,
                           headers={"Authorization": f"Bearer {authorization_token}"},
                           json={"label": "sassassassassassassassassassassassas", "token": "1466"})
    assert response.status_code == 422, f"{response.status_code} : {response.text}"


def test_submit_incorrect_token(client, authorization_token):
    response = client.post(endpoint,
                           headers={"Authorization": f"Bearer {authorization_token}"},
                           json={"label": "botyara", "token": "1488"})
    assert response.status_code == 422, f"{response.status_code} : {response.text}"


def test_duplicate(client, authorization_token):
    client.post(endpoint,
                headers={"Authorization": f"Bearer {authorization_token}"},
                json={"label": "botyara", "token": bot_token})
    response = client.post(endpoint,
                           headers={"Authorization": f"Bearer {authorization_token}"},
                           json={"label": "botyara", "token": bot_token})

    assert response.status_code == 409, f"{response.status_code} : {response.text}"


def test_more_than_five(client, authorization_token):
    def new_token(i):
        temp = list(bot_token)
        temp[11] = str(i)
        return "".join(temp)

    for i in range(5):
        response = client.post(endpoint,
                               headers={"Authorization": f"Bearer {authorization_token}"},
                               json={"label": f"botyara{i}", "token": new_token(i)})
        assert response.status_code == 201, f"{response.status_code} : {response.text}"

    response = client.post(endpoint,
                           headers={"Authorization": f"Bearer {authorization_token}"},
                           json={"label": "abobus", "token": bot_token})
    assert response.status_code == 403, f"{response.status_code} : {response.text}"
