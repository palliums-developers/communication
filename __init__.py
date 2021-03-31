import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./src"))
import src
comm_client = client
comm_server = server

__all__ = [
        "comm_client"
        "comm_server"
        ]
