import numpy as np
from PIL import Image, ImageDraw, ImageFilter,ImageFont
from PIL.Image import Resampling


# 圆角
def add_rounded(image):
    # 蒙版
    mask = Image.new('L', image.size, color=0)
    draw = ImageDraw.Draw(mask)

    # 圆角
    radius=min(image.size)*0.01
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # 合并
    alpha_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    alpha_image.paste(image, mask=mask)

    return alpha_image


# 渐变
def add_gradient(image, color=(0, 0, 0), alpha=255):
    # 蒙版
    draw = ImageDraw.Draw(image)

    # 渐变
    start_color = color + (alpha,)
    end_color = color + (0,)
    center = (image.size[0] // 2, image.size[1] // 2)
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            d = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            f = min(d / max(image.size), 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * f)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * f)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * f)
            a = int(start_color[3] + (end_color[3] - start_color[3]) * f)
            draw.point((x, y), fill=(r, g, b, a))

    return image

# 光晕
def add_glow(image, color=(0, 0, 0), radius=10):
    # 蒙版
    width, height = image.size
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)

    # 矩形
    for i in range(radius):
        # 计算渐变颜色
        a = int(i * i * i / radius * 255)
        # 绘制矩形
        draw.rectangle(
            [i + radius, i + radius, width - i - radius, height - i - radius],
            outline=color + (a,),
            width=1
        )

    # 高斯
    glow = glow.filter(ImageFilter.GaussianBlur(radius // 2))

    # 合并
    glow_image = Image.alpha_composite(image, glow)
    glow_image.save("../images/demo_5.png", format="PNG", optimize=True)

    return glow_image


# 阴影
def add_shadow(image, background_color=(255,255,255,255), shadow_color=(0,0,0,32),  offset=(1, 1)):
    # 蒙版
    border = int(max(50,min(500,min(image.size)*0.1)))
    print(f"shadow border: {border}px, image size: {image.size}")
    total_width = image.size[0] + abs(offset[0]) + 2 * border
    total_height = image.size[1] + abs(offset[1]) + 2 * border
    shadow_image = Image.new(image.mode, (total_width, total_height), background_color)

    # 阴影
    iterations=border
    shadow_left = border + max(offset[0], 0)
    shadow_top = border + max(offset[1], 0)
    shadow_image.paste(shadow_color, [shadow_left, shadow_top, shadow_left + image.size[0], shadow_top + image.size[1]])
    for _ in range(iterations):
        shadow_image = shadow_image.filter(ImageFilter.BLUR)

    # 圆角
    shadow_image = add_rounded(shadow_image)

    # 合并
    shadow_image.paste(image, (border - min(offset[0], 0), border - min(offset[1], 0)))

    return shadow_image

# 文字
def add_text(image, text, font_path=None,  text_color=(255, 255, 255)):
    # 蒙版
    draw = ImageDraw.Draw(image)
    
    # 字体
    font_size= min(image.size)*0.04
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    
    # 居中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = image.size
    position = ((image_width - text_width) // 2, (image_height*0.9+(image_height*0.1 - text_height) // 2))
    
    # 文字
    draw.text(position, text, fill=text_color, font=font)
    
    return image

# 打开图片
original_image = Image.open("../images/IMG_0379.jpg").convert("RGBA")

# 高斯
gaussian_blur = 50  # 模糊半径
gaussian_image = original_image.filter(ImageFilter.GaussianBlur(gaussian_blur))

# 缩小
scale_factor = 0.8  # 缩小比例
small_image = original_image.resize((int(original_image.width * scale_factor), int(original_image.height * scale_factor)), Resampling.LANCZOS)

# 圆角
rounded_image = add_rounded(small_image)

# 阴影
background_color=(0,0,0,0)
shadow_color=(0,0,0,255)
offset=(1, 1)
shadow_image = add_shadow(rounded_image,background_color,shadow_color,offset)

# 文字
text_to_add = '@pnoker'
font_path = 'Arial.ttf'
text_color=(255, 255, 255)
text_image=add_text(shadow_image,text_to_add,font_path,text_color)

# 合并
gaussian_image.paste(text_image, ((gaussian_image.width - text_image.width) // 2, (gaussian_image.height - text_image.height) // 3), text_image)

# 保存
gaussian_image.save("../images/demo_t.png", format="PNG", optimize=True)
