import time

clients = {}
messages = {}
outputs = {}


def create_client(uid: int, created: int, platform: str, user_agent: str):
    clients[uid] = {
        "uid": uid,
        "created": created,
        "platform": platform,
        "user_agent": user_agent,
    }


def get_clients():
    return list(clients.values())


def update_client(uid: int, created: int, platform: str, user_agent: str):
    if uid not in clients:
        return False

    create_client(uid, created, platform, user_agent)
    return True


def create_message(
    uid: int,
    created: int,
    payload: str,
    client: int,
    tags: str,
    stage: str,
    launched: int,
):
    messages[uid] = {
        "uid": uid,
        "created": created,
        "payload": payload,
        "client": client,
        "tags": tags,
        "stage": stage,
        "launched": launched,
    }


def get_messages():
    return list(messages.values())


def update_message(
    uid: int,
    created: int,
    payload: str,
    client: int,
    tags: str,
    stage: str,
    launched: int,
):
    if uid not in messages:
        return False

    create_message(uid, created, payload, client, tags, stage, launched)
    return True


def create_output(
    uid: int,
    created: int,
    response: str,
    stage: str,
    failure: str,
    message: int,
    cache_hit: int,
):
    outputs[uid] = {
        "uid": uid,
        "created": created,
        "response": response,
        "stage": stage,
        "failure": failure,
        "message": message,
        "cache_hit": cache_hit,
    }


def get_outputs():
    return list(outputs.values())


def update_output(
    uid: int,
    created: int,
    response: str,
    stage: str,
    failure: str,
    message: int,
    cache_hit: int,
):
    if uid not in outputs:
        return False

    create_output(uid, created, response, stage, failure, message, cache_hit)
    return True


def get_recent_messages():
    seven_minutes = 7 * 60
    current_time = int(time.time())
    result = []

    for client in clients.values():
        if client["created"] >= current_time - seven_minutes:
            for message in messages.values():
                if message["client"] == client["uid"]:
                    result.append(
                        {
                            "user_agent": client["user_agent"],
                            "payload": message["payload"],
                            "tags": message["tags"],
                        }
                    )

    return result
