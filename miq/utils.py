from pprint import pprint
import requests
from json import dumps
from urllib.parse import quote_plus

from .core.utils import get_dict_key


def map_ig_graphql_to_user(data):
    user = data
    if 'graphql' in data.keys():
        # user = data['graphql__user']
        user = get_dict_key(data, 'graphql__user')

    i = {
        **user,
        'media_count': get_dict_key(user, 'edge_owner_to_timeline_media__count'),
        'seo_category_infos': data.get('seo_category_infos'),
        'show_view_shop': data.get('show_view_shop'),
    }

    media = get_dict_key(user, 'edge_owner_to_timeline_media__edges') or []
    i['media'] = media

    if (len(media) > 0) and (post := media[0]):
        i['avg_likes_count'] = sum(get_dict_key(i, 'node__edge_liked_by__count') for i in media) / len(media)
        i['avg_comments_count'] = sum(get_dict_key(i, 'node__edge_media_to_comment__count') for i in media) / len(media)

    caps = []
    for u in [get_dict_key(i, 'node__edge_media_to_caption__edges') for i in media]:
        if len(u) > 0 and (text := get_dict_key(u[0], 'node__text')):
            caps.append(text)
    i['captions'] = caps

    locs = {}
    for loc in [get_dict_key(i, 'node__location') for i in media]:
        if not loc:
            continue
        locs[loc['id']] = loc
    i['locations'] = locs

    tagged = {}
    for u in [get_dict_key(i, 'node__edge_media_to_tagged_user__edges') for i in media]:
        if not len(u):
            continue

        u = get_dict_key(u[0], 'node__user')
        tagged[u['id']] = u
    i['tagged'] = tagged

    return i


sessionid = "11523892542%3AS9jzLFlZelEiVV%3A24"


def get_ig_username_info(username: str, sessionid: str = sessionid, s=requests.Session()):
    cookies = {'sessionid': sessionid}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96'}

    r = s.get(
        # f'https://www.instagram.com/unpetitvoyou/?__a=1&__d=dis',
        f'https://www.instagram.com/{username}/?__a=1&__d=dis',
        headers=headers, cookies=cookies
    )

    if r.status_code == 404:
        return

    try:
        return r.json()
    except Exception:
        return


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


# res = requests.get(
#     # f'https://i.instagram.com/api/v1/users/5530250209/info/',
#     # "https://i.instagram.com/api/v1/feed/user/5530250209/",
#     "https://i.instagram.com/api/v1/friendships/5530250209/following/",
#     # f'https://i.instagram.com/api/v1/users/{userId["id"]}/info/',
#     headers={'User-Agent': 'Instagram 64.0.0.14.96'},
#     cookies={'sessionid': sessionid}
# ).json()\
#     # ["user"]


# pprint(res)
