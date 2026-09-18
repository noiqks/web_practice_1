def create_request(operation_code: int, xml_body: str):
    body = xml_body.encode("utf-8")
    body_size = len(body)

    request = (
        operation_code.to_bytes(1, "little")
        + body_size.to_bytes(3, "little")
        + body
    )

    return request


def parse_request(request: bytes):
    operation_code = int.from_bytes(request[0:1], "little")

    body_size = int.from_bytes(request[1:4], "little")

    xml_body = request[4 : 4 + body_size].decode("utf-8")

    return operation_code, xml_body


def create_response(operation_code: int, xml_body: str):
    body = xml_body.encode("utf-8")
    body_size = len(body)

    response = (
        operation_code.to_bytes(2, "little")
        + body_size.to_bytes(5, "little")
        + body
    )

    return response


def parse_response(response: bytes):
    operation_code = int.from_bytes(response[0:2], "little")

    body_size = int.from_bytes(response[2:7], "little")

    xml_body = response[7 : 7 + body_size].decode("utf-8")

    return operation_code, xml_body


def log_response(operation_code: int, xml_body: str):
    with open("journal.log", "a", encoding="utf-8") as file:
        file.write(f"Код операции: {operation_code}\nОтвет: {xml_body}\n")
