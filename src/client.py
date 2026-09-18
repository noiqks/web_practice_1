import socket

from src.rpc import (
    create_request,
    log_response,
    parse_response,
)


def recv_exact(connection, size):
    data = b""

    while len(data) < size:
        part = connection.recv(size - len(data))

        if not part:
            return None

        data += part

    return data


class RPCClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def connect(self):
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.close()

    def _request(self, operation_code: int, xml_body: str):
        connection = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        connection.connect((self.host, self.port))

        request = create_request(operation_code, xml_body)
        connection.sendall(request)

        response_code = recv_exact(connection, 2)

        if response_code is None:
            connection.close()
            return None

        body_size = recv_exact(connection, 5)

        if body_size is None:
            connection.close()
            return None

        response_body = recv_exact(
            connection,
            int.from_bytes(body_size, "little"),
        )

        if response_body is None:
            connection.close()
            return None

        response = response_code + body_size + response_body

        operation_code, xml_body = parse_response(response)
        log_response(operation_code, xml_body)

        connection.close()

        return xml_body

    def create_client(
        self,
        uid: int,
        created: int,
        platform: str,
        user_agent: str,
    ):
        xml_body = (
            f"<client>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<platform>{platform}</platform>"
            f"<user_agent>{user_agent}</user_agent>"
            f"</client>"
        )

        return self._request(1, xml_body)

    def get_clients(self):
        return self._request(2, "<clients></clients>")

    def update_client(
        self,
        uid: int,
        created: int,
        platform: str,
        user_agent: str,
    ):
        xml_body = (
            f"<client>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<platform>{platform}</platform>"
            f"<user_agent>{user_agent}</user_agent>"
            f"</client>"
        )

        return self._request(3, xml_body)

    def create_message(
        self,
        uid: int,
        created: int,
        payload: str,
        client: int,
        tags: str,
        stage: str,
        launched: int,
    ):
        xml_body = (
            f"<message>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<payload>{payload}</payload>"
            f"<client>{client}</client>"
            f"<tags>{tags}</tags>"
            f"<stage>{stage}</stage>"
            f"<launched>{launched}</launched>"
            f"</message>"
        )

        return self._request(4, xml_body)

    def get_messages(self):
        return self._request(5, "<messages></messages>")

    def update_message(
        self,
        uid: int,
        created: int,
        payload: str,
        client: int,
        tags: str,
        stage: str,
        launched: int,
    ):
        xml_body = (
            f"<message>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<payload>{payload}</payload>"
            f"<client>{client}</client>"
            f"<tags>{tags}</tags>"
            f"<stage>{stage}</stage>"
            f"<launched>{launched}</launched>"
            f"</message>"
        )

        return self._request(6, xml_body)

    def create_output(
        self,
        uid: int,
        created: int,
        response: str,
        stage: str,
        failure: str,
        message: int,
        cache_hit: int,
    ):
        xml_body = (
            f"<output>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<response>{response}</response>"
            f"<stage>{stage}</stage>"
            f"<failure>{failure}</failure>"
            f"<message>{message}</message>"
            f"<cache_hit>{cache_hit}</cache_hit>"
            f"</output>"
        )

        return self._request(7, xml_body)

    def get_outputs(self):
        return self._request(8, "<outputs></outputs>")

    def update_output(
        self,
        uid: int,
        created: int,
        response: str,
        stage: str,
        failure: str,
        message: int,
        cache_hit: int,
    ):
        xml_body = (
            f"<output>"
            f"<uid>{uid}</uid>"
            f"<created>{created}</created>"
            f"<response>{response}</response>"
            f"<stage>{stage}</stage>"
            f"<failure>{failure}</failure>"
            f"<message>{message}</message>"
            f"<cache_hit>{cache_hit}</cache_hit>"
            f"</output>"
        )

        return self._request(9, xml_body)

    def get_recent_messages(self):
        return self._request(10, "<recent_messages></recent_messages>")
