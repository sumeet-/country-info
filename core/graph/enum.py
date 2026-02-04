from enum import Enum


class Node(str, Enum):
    INTENT = "intent"
    API_DATA = "api_data"
    SYNTHESIS = "synthesis"
    HANDLE_ERROR = "handle_error"
