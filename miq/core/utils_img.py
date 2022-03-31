from PIL import Image as PImage

IMG_SIZE = (800, 1200)
THUMB_SIZE = (450, 450)


def get_thumbnail(file, width=THUMB_SIZE[0], height=THUMB_SIZE[1]):

    if not file:
        # logger.warn(f'No file to resize')
        return

    thumb = PImage.open(file)
    th_width, th_height = thumb.size
    if th_width > width and th_height > height:
        thumb.thumbnail((width, height), PImage.ANTIALIAS)
        # logger.info(f'Resized file[{file}]')

    # if save:
        # thumb.save(self.thumbnail.path)

    return thumb


def crop_img_to_square(file):
    """
    Crops a given image file to square
    """

    if not file:
        return

    img = PImage.open(file)
    width, height = img.size
    if width > IMG_SIZE[0] and height > IMG_SIZE[1]:
        # keep ratio but shrink down
        img.thumbnail((width, height), PImage.ANTIALIAS)
        # img.show()

    # check which one is smaller
    if height < width:
        # make square by cutting off equal amounts left and right
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
        cropped = img.crop((left, top, right, bottom))

    elif width < height:
        # make square by cutting off bottom
        left = 0
        right = width
        # top = 0
        # bottom = width
        top = (height - width) / 2
        bottom = (height + width) / 2
        cropped = img.crop((left, top, right, bottom))
    else:
        cropped = img

    return cropped
