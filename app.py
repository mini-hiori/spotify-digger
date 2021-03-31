import sys
import traceback
from fetch_songs import main
import os
import json


def handler(event, context):
    """
    lambda用main関数
    """
    try:
        main()
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({"result": "OK"})
        }
    except BaseException:
        error_message = traceback.format_exc()
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({"result": "NG", "error_message": error_message})
        }
