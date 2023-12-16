#!/usr/bin/env python3
"""NoSQL database example implemented with Python"""

import socket
import handler_lib as helper

HOST = "localhost"
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Provide source of feedback for NoSQL DB calls
STATS = {
    "PUT": {"success": 0, "error": 0},
    "GET": {"success": 0, "error": 0},
    "PUTLIST": {"success": 0, "error": 0},
    "GETLIST": {"success": 0, "error": 0},
    "INCREMENT": {"success": 0, "error": 0},
    "APPEND": {"success": 0, "error": 0},
    "DELETE": {"success": 0, "error": 0},
    "STATS": {"success": 0, "error": 0}
}

# Look-up Table
COMMAND_HANDLERS = {
    "PUT": helper.handle_put,
    "GET": helper.handle_get,
    "PUTLIST": helper.handle_putlist,
    "GETLIST": helper.handle_getlist,
    "INCREMENT": helper.handle_increment,
    "APPEND": helper.handle_append,
    "DELETE": helper.handle_delete,
    "STATS": helper.handle_stats
    }

DATA = {}


def main():
    """Main entry point for setup"""
    SOCKET.bind( (HOST, PORT) )
    SOCKET.listen(1)

    while 1:
        connection, address = SOCKET.accept()
        print( f"New connection from [{address}]" )
        data = connection.recv(4096).decode()
        command, key, value = helper.parse_message(data)

        if command == "STATS":
            response = helper.handle_stats(STATS)

        elif command in (
            "GET",
            "GETLIST",
            "INCREMENT",
            "DELETE"
        ):
            response = COMMAND_HANDLERS[command](key, DATA)

        elif command in (
            "PUT",
            "PUTLIST",
            "APPEND"
        ):
            response = COMMAND_HANDLERS[command](key, value, DATA)

        else:
            response = ( False, f"Unknown command type [{command}]" )

        helper.update_stats(command, response[0], STATS)
        connection.sendall( f"{response[0]};{response[1]}" )
        connection.close()


if __name__ == "__main__":
    main()
