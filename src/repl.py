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


def run():
    print("REPL модели данных")

    while True:
        command = input("> ")

        if command == "exit":
            break

        elif command == "create_client":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            platform = input("Platform: ")
            user_agent = input("User_agent: ")

            create_client(uid, created, platform, user_agent)
            print("Client создан")

        elif command == "get_clients":
            print(get_clients())

        elif command == "update_client":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            platform = input("Platform: ")
            user_agent = input("User_agent: ")

            result = update_client(uid, created, platform, user_agent)

            if not result:
                print("Client не найден")
            else:
                print("Client изменён")

        elif command == "create_message":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            payload = input("Payload: ")
            client = int(input("Client: "))
            tags = input("Tags: ")
            stage = input("Stage: ")
            launched = int(input("Launched: "))

            create_message(uid, created, payload, client, tags, stage, launched)
            print("Message создан")

        elif command == "get_messages":
            print(get_messages())

        elif command == "update_message":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            payload = input("Payload: ")
            client = int(input("Client: "))
            tags = input("Tags: ")
            stage = input("Stage: ")
            launched = int(input("Launched: "))

            result = update_message(
                uid, created, payload, client, tags, stage, launched
            )

            if not result:
                print("Message не найден")
            else:
                print("Message изменён")

        elif command == "get_outputs":
            print(get_outputs())

        elif command == "create_output":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            response = input("Response: ")
            stage = input("Stage: ")
            failure = input("Failure: ")
            message = int(input("Message: "))
            cache_hit = int(input("Cache_hit: "))

            create_output(
                uid, created, response, stage, failure, message, cache_hit
            )
            print("Output создан")

        elif command == "update_output":
            uid = int(input("Uid: "))
            created = int(input("Created: "))
            response = input("Response: ")
            stage = input("Stage: ")
            failure = input("Failure: ")
            message = int(input("Message: "))
            cache_hit = int(input("Cache_hit: "))

            result = update_output(
                uid, created, response, stage, failure, message, cache_hit
            )

            if not result:
                print("Output не найден")
            else:
                print("Output изменён")

        elif command == "get_recent_messages":
            print(get_recent_messages())

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    run()
