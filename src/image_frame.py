import sys
import time
from pathlib import Path

import numpy
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL.Image import Resampling

image_mode = 'RGBA'  # 图片模式
image_scale = 0.88  # 缩小比例


# 圆角
def add_rounded(image):
    # 蒙版
    mask = Image.new('L', image.size, color=0)
    draw = ImageDraw.Draw(mask)

    # 圆角
    radius = min(image.size) * 0.03
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # 合并
    temp_image = Image.new(image_mode, image.size, (0, 0, 0, 0))
    temp_image.paste(image, mask=mask)

    return temp_image


# 阴影
def add_shadow(image, color=(255, 255, 255, 255)):
    shadow_radius = int(min(image.size) * 0.1)
    rounded_radius = int(min(image.size) * 0.03)
    temp_image = Image.new(
        image_mode, (image.width + shadow_radius, image.height + shadow_radius), color
    )
    drawing = ImageDraw.Draw(temp_image)
    a = 200 / numpy.square(shadow_radius)
    for i in range(shadow_radius):
        drawing.rounded_rectangle(
            [(0 + i, 0 + i), (temp_image.width - i, temp_image.height - i)],
            radius=rounded_radius,
            fill=(0, 0, 0, int(numpy.square(i) * a)),
        )
    temp_image.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
    temp_image.paste(
        image,
        (
            (temp_image.width - image.width) // 2,
            (temp_image.height - image.height) // 2,
        ),
        image,
    )
    return temp_image


# 文字
def add_text(image, text, color=(255, 255, 255)):
    # 蒙版
    draw = ImageDraw.Draw(image)

    # 标题
    font_size = int(image.height * (1 - image_scale) * 0.2)
    font_path = ImageFont.truetype('Canon.ttf', font_size)

    # 定位
    text_bbox = draw.textbbox((0, 0), text, font=font_path, font_size=font_size)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    height_base = image.height * (1 - image_scale) / 3 + image.height * image_scale
    height_index = (image.height - height_base - text_height) // 2
    position = ((image.width - text_width) // 2, height_base + height_index)

    # 文字
    draw.text(position, text, fill=color, font=font_path)


def main(arg):
    # 打开图片
    start1 = time.time()
    image_path = arg
    raw_image = Image.open(image_path).convert(image_mode)
    end1 = time.time()
    print(f'1. open image {arg}: {(end1 - start1) * 1000} ms')

    # 高斯
    start2 = time.time()
    gaussian_blur = 100  # 模糊半径
    final_image = raw_image.filter(ImageFilter.GaussianBlur(gaussian_blur))
    end2 = time.time()
    print(f'2. add gaussian blur: {(end2 - start2) * 1000} ms')

    # 文字
    start3 = time.time()
    text_content = 'Canon @ pnoker'
    add_text(final_image, text_content)
    end3 = time.time()
    print(f'3. add text: {(end3 - start3) * 1000} ms')

    # 缩小
    start4 = time.time()
    small_image = raw_image.resize(
        (int(raw_image.width * image_scale), int(raw_image.height * image_scale)),
        Resampling.LANCZOS,
    )
    end4 = time.time()
    print(f'4. resize image to {image_scale * 100}%: {(end4 - start4) * 1000} ms')

    # 圆角
    start5 = time.time()
    rounded_image = add_rounded(small_image)
    end5 = time.time()
    print(f'5. add rounded: {(end5 - start5) * 1000} ms')

    # 阴影
    start6 = time.time()
    background_color = (0, 0, 0, 0)
    shadow_color = (0, 0, 0, 255)
    offset = (1, 1)
    shadow_image = add_shadow(rounded_image, background_color)
    end6 = time.time()
    print(f'6. add shadow: {(end6 - start6) * 1000} ms')

    # 合并
    start7 = time.time()
    final_image.paste(
        shadow_image,
        (
            (final_image.width - shadow_image.width) // 2,
            (final_image.height - shadow_image.height) // 3,
        ),
        shadow_image,
    )
    end7 = time.time()
    print(f'7. merge images: {(end7 - start7) * 1000} ms')

    # 保存
    start8 = time.time()
    path = Path(image_path)
    final_image.convert('RGB').save(path.with_name(path.stem + '_S.jpeg'), format='JPEG')
    end8 = time.time()
    print(f'8. save images: {(end8 - start8) * 1000} ms')
    print(f'OK: {(end8 - start1) * 1000} ms')


# pyinstaller --distpath ./output/dist --workpath ./output/build your_script.py
if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        main(arg)
