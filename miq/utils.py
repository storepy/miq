import requests
from json import dumps
from urllib.parse import quote_plus


def check_ig_username(username: str):
    data = "signed_body=SIGNATURE." + quote_plus(dumps(
        {"q": f'{username}', "skip_recovery": "1"},
        separators=(",", ":")
    ))

    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            # "X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )
    try:
        if api.json()['user']['username']:
            return True
    except Exception:
        pass

    return False
