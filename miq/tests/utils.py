from io import BytesIO
# import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def get_temp_img(size=50):
    bts = BytesIO()
    img = Image.new("RGB", (size, size))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())

    # img = Image.new('RGB', (size, size))
    # tmp = tempfile.NamedTemporaryFile(suffix='.jpg', prefix="test_img_")
    # img.save(tmp, 'jpeg')
    # tmp.seek(0)

    # return tmp
