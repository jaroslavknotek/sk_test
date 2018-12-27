from itertools import groupby
import json
from PIL import Image


def construct_image(imgs):
    """
    Obtains an array of equaly sized images and put them together in a singe image.
    Missing images will disrupt whole image
    :param imgs: array of tuples
        Array of images and its metadata
        Tuples consist of ( coordinates,image)
        Coordinates are used to properly order images before joining
    :return: Image
        single image
    """

    if len(imgs) == 0:
        return None
    # taking the first
    w, h = imgs[0][1].size
    img_array = order_2d(imgs)
    x_count = len(img_array[0])
    y_count = len(img_array)
    height = h * y_count
    width = w * x_count
    new_im = Image.new('RGB', (width, height))
    for y in range(y_count):
        for x in range(x_count):
            _, im = img_array[y][x]
            new_im.paste(im, (x * w, y * h))
    return new_im


def order_2d(tiles):
    """
    Method gets pair of coordinates and data and returns 2d array.
    :param tiles: tuple
        pair ((x,y), data ) where x and y are integers
    :return: 2d array
    """

    sorted_vals = sorted(tiles, key=lambda x: x[0][1])
    grouped = groupby(sorted_vals, lambda x: x[0][1])

    return [sorted(vals, key=lambda x: x[0][0]) for _, vals in grouped]


def decode_content(request):
    """
    Decodes content of the request and turn it into json
    :param request: request
    :return:
    """
    print(request.content)
    decoded = request.content.decode('utf8')  # .replace("'", '"')
    return json.loads(decoded)
