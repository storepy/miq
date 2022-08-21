
# from pprint import pprint
import requests
from json import dumps
from urllib.parse import quote_plus

from .core.utils import get_dict_key, download_img_from_url_to_b64


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


s = requests.Session()
sessionId = "11523892542%3AS9jzLFlZelEiVV%3A24"
cookies = {'sessionid': sessionId}
headers = {'User-Agent': 'Instagram 64.0.0.14.96'}


def get_ig_username_media(data: dict):
    if url := get_dict_key(data, 'graphql__user__profile_pic_url_hd'):
        if img := download_img_from_url_to_b64(url, s=s, headers=headers, cookies=cookies):
            data['graphql']['user']['profile_pic_b64'] = img

    if media := get_dict_key(data, 'graphql__user__edge_owner_to_timeline_media'):
        for m in media.get('edges', []):
            m = m['node']
            if (u := m.get('display_url')) and (img := download_img_from_url_to_b64(u, s=s, headers=headers, cookies=cookies)):
                m['display_url'] = img

            # for c in m.get('edge_sidecar_to_children', []):
            #     c = c['node']


def get_ig_username_info(username: str, s=s):
    r = s.get(
        # f'https://www.instagram.com/unpetitvoyou/?__a=1&__d=dis',
        f'https://www.instagram.com/{username}/?__a=1&__d=dis',
        headers=headers, cookies=cookies
    )

    if r.status_code == 404:
        return

    data = {}
    try:
        data = r.json()
    except Exception:
        return
    else:
        get_ig_username_media(data)
        return data


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

# url = 'https://instagram.fewr1-6.fna.fbcdn.net/v/t51.2885-19/287947947_1280893049112350_9127347944203769740_n.jpg?stp=dst-jpg_s320x320&_nc_ht=instagram.fewr1-6.fna.fbcdn.net&_nc_cat=102&_nc_ohc=mvuhab6IuvYAX-9S3at&edm=ABfd0MgBAAAA&ccb=7-5&oh=00_AT8gmMrJU6SAUNlQQY8xuLi8U5RcT7k7hm4ozXwu-G4ufA&oe=62EAF999&_nc_sid=7bff83'
# r = s.get(url, headers=headers, cookies=cookies)
# print(r)
# b64response = base64.b64encode(r.content)
# print(b64response)
