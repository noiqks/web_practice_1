import socket
import xml.etree.ElementTree as ET

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
from src.rpc import create_response

HOST = "127.0.0.1"
PORT = 5000
CREATE_CLIENT = 1
GET_CLIENTS = 2
UPDATE_CLIENT = 3
CREATE_MESSAGE = 4
GET_MESSAGES = 5
UPDATE_MESSAGE = 6
CREATE_OUTPUT = 7
GET_OUTPUTS = 8
UPDATE_OUTPUT = 9
GET_RECENT_MESSAGES = 10


def result_to_xml(result):
    root = ET.Element("result")

    if isinstance(result, list):
        for item in result:
            record = ET.SubElement(root, "record")

            for key, value in item.items():
                field = ET.SubElement(record, key)
                field.text = str(value)

    elif isinstance(result, bool):
        root.text = str(result)

    elif result is None:
        root.text = ""

    else:
        root.text = str(result)

    return ET.tostring(
        root,
        encoding="unicode",
    )


def handle_client(operation_code, root):
    if operation_code == CREATE_CLIENT:
        return create_client(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("platform"),
            root.findtext("user_agent"),
        )

    if operation_code == GET_CLIENTS:
        return get_clients()

    if operation_code == UPDATE_CLIENT:
        return update_client(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("platform"),
            root.findtext("user_agent"),
        )


def handle_message(operation_code, root):
    if operation_code == CREATE_MESSAGE:
        return create_message(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("payload"),
            int(root.findtext("client")),
            root.findtext("tags"),
            root.findtext("stage"),
            int(root.findtext("launched")),
        )

    if operation_code == GET_MESSAGES:
        return get_messages()

    if operation_code == UPDATE_MESSAGE:
        return update_message(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("payload"),
            int(root.findtext("client")),
            root.findtext("tags"),
            root.findtext("stage"),
            int(root.findtext("launched")),
        )


def handle_output(operation_code, root):
    if operation_code == CREATE_OUTPUT:
        return create_output(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("response"),
            root.findtext("stage"),
            root.findtext("failure"),
            int(root.findtext("message")),
            int(root.findtext("cache_hit")),
        )

    if operation_code == GET_OUTPUTS:
        return get_outputs()

    if operation_code == UPDATE_OUTPUT:
        return update_output(
            int(root.findtext("uid")),
            int(root.findtext("created")),
            root.findtext("response"),
            root.findtext("stage"),
            root.findtext("failure"),
            int(root.findtext("message")),
            int(root.findtext("cache_hit")),
        )


def handle_request(operation_code, xml_body):
    root = ET.fromstring(xml_body)

    if operation_code in (CREATE_CLIENT, GET_CLIENTS, UPDATE_CLIENT):
        return handle_client(operation_code, root)

    if operation_code in (CREATE_MESSAGE, GET_MESSAGES, UPDATE_MESSAGE):
        return handle_message(operation_code, root)

    if operation_code in (CREATE_OUTPUT, GET_OUTPUTS, UPDATE_OUTPUT):
        return handle_output(operation_code, root)

    if operation_code == GET_RECENT_MESSAGES:
        return get_recent_messages()

    return None


def recv_exact(connection, size):
    data = b""

    while len(data) < size:
        part = connection.recv(size - len(data))

        if not part:
            return None

        data += part

    return data


def receive_request(connection):
    operation_code = recv_exact(connection, 1)

    if operation_code is None:
        return None

    body_size = recv_exact(connection, 3)

    if body_size is None:
        return None

    operation_code = int.from_bytes(
        operation_code,
        "little",
    )

    body_size = int.from_bytes(
        body_size,
        "little",
    )

    body = recv_exact(connection, body_size)

    if body is None:
        return None

    xml_body = body.decode("utf-8")

    return operation_code, xml_body


def run():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server.bind((HOST, PORT))
    server.listen()

    print(f"RPC-сервер запущен: {HOST}:{PORT}")

    while True:
        connection, address = server.accept()
        print(f"Подключение: {address}")

        request = receive_request(connection)

        if request is None:
            connection.close()
            continue

        operation_code, xml_body = request

        print(f"Код операции: {operation_code}")
        print(f"XML: {xml_body}")

        result = handle_request(
            operation_code,
            xml_body,
        )

        xml_response = result_to_xml(result)

        response = create_response(
            operation_code,
            xml_response,
        )

        connection.sendall(response)


if __name__ == "__main__":
    run()
