import time

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL.Image import Resampling

image_mode = 'RGBA'  # 图片模式


# 圆角
def add_rounded(image):
    # 蒙版
    mask = Image.new('L', image.size, color=0)
    draw = ImageDraw.Draw(mask)

    # 圆角
    radius = min(image.size) * 0.01
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # 合并
    alpha_image = Image.new(image_mode, image.size, (0, 0, 0, 0))
    alpha_image.paste(image, mask=mask)

    return alpha_image


# 阴影
def add_shadow(image, color=(255, 255, 255, 255)):
    radius = int(min(image.size) * 0.05)
    background_image = Image.new("RGBA", (image.width + radius, image.height + radius), color)
    drawing = ImageDraw.Draw(background_image)
    for i in range(radius):
        drawing.rectangle(
            [(0 + i, 0 + i), (background_image.width - i, background_image.height - i)],
            fill=(0, 0, 0, int(i / radius * 32)),
        )
    background_image.filter(ImageFilter.GaussianBlur(radius=100 ))
    background_image.paste(image, ((background_image.width - image.width) // 2, (background_image.height - image.height) // 2), image)
    return background_image


# 文字
def add_text(image, text, font='Herculanum.ttf', color=(255, 255, 255)):
    # 蒙版
    draw = ImageDraw.Draw(image)

    # 字体
    font_size = int(min(image.size) * 0.03)
    if font:
        font = ImageFont.truetype(font, font_size)
    else:
        font = ImageFont.load_default()

    # 定位
    text1_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text1_bbox[2] - text1_bbox[0]
    text_height = text1_bbox[3] - text1_bbox[1]
    position1 = ((image.width - text_width) // 2, (image.height - text_height * 2))

    # 文字
    draw.text(position1, text, fill=color, font=font)


# 打开图片
start1 = time.time()
raw_image_path = '../images/IMG_0379.jpg'
raw_image = Image.open(raw_image_path).convert(image_mode)
end1 = time.time()
print(f"1. open image: {(end1 - start1) * 1000} ms")

# 高斯
start2 = time.time()
gaussian_blur = 50  # 模糊半径
final_image = raw_image.filter(ImageFilter.GaussianBlur(gaussian_blur))
end2 = time.time()
print(f"2. add gaussian blur: {(end2 - start2) * 1000} ms")

# 文字
start3 = time.time()
text_content = '@pnoker'
add_text(final_image, text_content)
end3 = time.time()
print(f"3. add text: {(end3 - start3) * 1000} ms")

# 缩小
start4 = time.time()
scale_factor = 0.88  # 缩小比例
small_image = raw_image.resize((int(raw_image.width * scale_factor), int(raw_image.height * scale_factor)), Resampling.LANCZOS)
end4 = time.time()
print(f"4. resize image to {scale_factor * 100}%: {(end4 - start4) * 1000} ms")

# 圆角
start5 = time.time()
rounded_image = add_rounded(small_image)
end5 = time.time()
print(f"5. add rounded: {(end5 - start5) * 1000} ms")

# 阴影
start6 = time.time()
background_color = (0, 0, 0, 0)
shadow_color = (0, 0, 0, 255)
offset = (1, 1)
shadow_image = add_shadow(rounded_image, background_color)
# shadow_image = rounded_image
end6 = time.time()
print(f"6. add shadow: {(end6 - start6) * 1000} ms")

# 合并
start7 = time.time()
final_image.paste(shadow_image, ((final_image.width - shadow_image.width) // 2, (final_image.height - shadow_image.height) // 3), shadow_image)
end7 = time.time()
print(f"7. merge images: {(end7 - start7) * 1000} ms")

# 保存
start8 = time.time()
final_image.convert('RGB').save("../images/demo_t.png", format="JPEG")
end8 = time.time()
print(f"8. save images: {(end8 - start8) * 1000} ms")
print(f"OK: {(end8 - start1) * 1000} ms")
