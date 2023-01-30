
from miq.core.utils import truncate_str


def test_truncate_str():
    assert truncate_str('123456789', length=5) == '1234…'