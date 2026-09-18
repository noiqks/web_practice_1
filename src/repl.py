from src.data import (
    create_client,
    create_message,
    create_output,
    get_clients,
    get_messages,
    get_outputs,
    get_recent_messages,
    update_client,
    update_message,
    update_output,
)


def create_client_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    platform = input("Platform: ")
    user_agent = input("User_agent: ")

    create_client(uid, created, platform, user_agent)
    print("Client создан")


def get_clients_command():
    print(get_clients())


def update_client_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    platform = input("Platform: ")
    user_agent = input("User_agent: ")

    result = update_client(uid, created, platform, user_agent)

    if not result:
        print("Client не найден")
    else:
        print("Client изменён")


def create_message_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    payload = input("Payload: ")
    client = int(input("Client: "))
    tags = input("Tags: ")
    stage = input("Stage: ")
    launched = int(input("Launched: "))

    create_message(
        uid,
        created,
        payload,
        client,
        tags,
        stage,
        launched,
    )
    print("Message создан")


def get_messages_command():
    print(get_messages())


def update_message_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    payload = input("Payload: ")
    client = int(input("Client: "))
    tags = input("Tags: ")
    stage = input("Stage: ")
    launched = int(input("Launched: "))

    result = update_message(
        uid,
        created,
        payload,
        client,
        tags,
        stage,
        launched,
    )

    if not result:
        print("Message не найден")
    else:
        print("Message изменён")


def create_output_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    response = input("Response: ")
    stage = input("Stage: ")
    failure = input("Failure: ")
    message = int(input("Message: "))
    cache_hit = int(input("Cache_hit: "))

    create_output(
        uid,
        created,
        response,
        stage,
        failure,
        message,
        cache_hit,
    )
    print("Output создан")


def get_outputs_command():
    print(get_outputs())


def update_output_command():
    uid = int(input("Uid: "))
    created = int(input("Created: "))
    response = input("Response: ")
    stage = input("Stage: ")
    failure = input("Failure: ")
    message = int(input("Message: "))
    cache_hit = int(input("Cache_hit: "))

    result = update_output(
        uid,
        created,
        response,
        stage,
        failure,
        message,
        cache_hit,
    )

    if not result:
        print("Output не найден")
    else:
        print("Output изменён")


def run():
    print("REPL модели данных")

    commands = {
        "create_client": create_client_command,
        "get_clients": get_clients_command,
        "update_client": update_client_command,
        "create_message": create_message_command,
        "get_messages": get_messages_command,
        "update_message": update_message_command,
        "create_output": create_output_command,
        "get_outputs": get_outputs_command,
        "update_output": update_output_command,
        "get_recent_messages": lambda: print(get_recent_messages()),
    }

    while True:
        command = input("> ")

        if command == "exit":
            break

        if command in commands:
            commands[command]()
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    run()
