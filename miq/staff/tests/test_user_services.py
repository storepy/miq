import pytest

from django.urls import reverse_lazy
from rest_framework.test import APIClient

from miq.core.services import user_create
from miq.tests import get_random_user_data,get_or_create_site

# @pytest.mark.parametrize(
#     ('value', 'expected_status_code'),
#     (
#         ('', 400),
#         ('je', 400),
#         ('jea', 200),
#         ('jean', 200),
#     )
# )
def test_user_search_viewset(db):
    get_or_create_site(is_live=False)
    user = user_create(username='jeami', password='test',first_name='jean-michel', last_name='mahouna',email='e@mail.com', is_staff=True)
    user_create(username='testusr', password='test',first_name='valjean apple', last_name='seed',email='e@mail.com')

    client = APIClient()

    path = reverse_lazy('staff:user-search-list')
    r = client.get(path)
    assert r.status_code == 302

    client.login(username=user.username, password='test') 
    for i in range(10):
        user_create(**get_random_user_data())

    r = client.get(path)
    assert r.status_code == 400
    
    r = client.get(path, params={'q': ''})
    assert r.status_code == 400
    
    r = client.get(path, params={'q': 'je'})
    assert r.status_code == 400
    
    r = client.get(path, {'q': 'jea'})

    assert r.status_code == 200
    assert len(r.data['results']) == 2


