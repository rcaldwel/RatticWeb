from django.conf import settings

import json
import os


def open_icons_in_folder(path):
    from PIL import Image
    images = []
    for f in os.listdir(path):
        img = Image.open(os.path.join(path, f))
        images.append((f, img))

    return images


def build_layout(images):
    data = {}
    curx = 0
    cury = 0
    i = 0
    for (name, img) in images:
        (width, height) = img.size
        data[name] = {}
        data[name]['filename'] = name
        data[name]['xoffset'] = curx
        data[name]['yoffset'] = 0
        data[name]['width'] = width
        data[name]['height'] = height
        data[name]['css-class'] = 'rattic-icon-' + str(i)
        curx += width
        cury = max(cury, height)
        i += 1

    return (curx, cury, data)


def build_css_class(data):
    css = '/* ' + data['filename'] + '*/\n'
    css += '.' + data['css-class'] + ' {\n'
    css += '    height: %spx;\n' % data['height']
    css += '    width: %spx;\n' % data['width']
    css += '    background-position: -%spx -%spx;\n' % (data['xoffset'], data['yoffset'])
    css += '}\n\n'

    return css


def build_css(data):
    css = '/* This file is generated by ./manage.py spritemaker */\n'

    for f in data.keys():
        css += build_css_class(data[f])

    return css


def draw_sprite(images, data, size):
    from PIL import Image
    sprite = Image.new('RGBA', size)
    for (name, img) in images:
        xloc = data[name]['xoffset']
        yloc = data[name]['yoffset']
        sprite.paste(img, (xloc, yloc), img)

    return sprite


def make_sprite(path):
    images = open_icons_in_folder(path)
    (mx, my, data) = build_layout(images)
    css = build_css(data)
    sprite = draw_sprite(images, data, (mx, my))

    return (data, sprite, css)


def get_icon_data():
    if get_icon_data._icons is None:
        get_icon_data._icons = json.loads(open(os.path.join('cred',
            settings.CRED_ICON_JSON), 'r').read())

    return get_icon_data._icons
get_icon_data._icons = None


def get_icon_list():
    return get_icon_data().keys()
