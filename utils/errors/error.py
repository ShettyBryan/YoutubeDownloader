import logging
import sys
from typing import Any


class ErrorCodes():
    noAudioOrVideoLinks = {
        "code": 100,
        "message": "No audio or video links provided"
    }

    emptyPath = {
        "code": 110,
        "message": "Path is empty"
    }

    fileNotFound = {
        "code": 120,
        "message": "File not found"
    }


def exitHandler(error: dict[str, Any], log: logging.Logger):
    log.error(error["message"])
    sys.exit(error["code"])
