import sys
import traceback
from fetch_songs import main
import os


def handler(event, context):
    """
    lambda用main関数
    """
    try:
        main()
        return {"result": "OK"}
    except BaseException:
        error_message = traceback.format_exc()
        return {"result": "NG", "error_message": error_message}
