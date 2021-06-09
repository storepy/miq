import tempfile
from PIL import Image


def get_temp_img(size=50, close=False):
    img = Image.new('RGB', (size, size))
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg')
    img.save(tmp, 'jpeg')
    tmp.seek(0)

    return tmp
