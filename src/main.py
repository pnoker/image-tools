import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from PIL.Image import Resampling


def add_rounded(image, radius):
    # 蒙版
    mask = Image.new('L', image.size, color=0)
    draw = ImageDraw.Draw(mask)

    # 圆角矩形
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # 合并
    alpha_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    alpha_image.paste(image, mask=mask)

    return alpha_image


def add_gradient(image, color, alpha):
    start_color = color + (alpha,)
    end_color = color + (0,)
    draw = ImageDraw.Draw(image)
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


def add_glow(image, color=(0, 0, 0), radius=10):
    # 蒙版
    width, height = image.size
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)

    # 内聚矩形
    for i in range(radius):
        # 计算渐变颜色
        a = int(i * i * i / radius * 255)
        # 绘制矩形
        draw.rectangle(
            [i + radius, i + radius, width - i - radius, height - i - radius],
            outline=color + (a,),
            width=1
        )

    # 高斯模糊
    glow = glow.filter(ImageFilter.GaussianBlur(radius // 2))

    # 合并
    combined = Image.alpha_composite(image, glow)
    combined.save("/Users/pnoker/Code/image-tools/images/demo_5.png", format="PNG", optimize=True)

    return combined


def add_shadow(image, color=(0, 0, 0), border=10, radius=10):
    # 背景
    shadow_image = Image.new('RGBA', (image.size[0] + 2 * border, image.size[1] + 2 * border), (0, 0, 0, 0))

    # 渐变
    # gradient_image = add_gradient(shadow_image, color, alpha)

    # 光晕
    glow_image = add_glow(shadow_image, color)

    # 圆角
    rounded_shadow_image = add_rounded(glow_image, radius)

    # 合并
    rounded_shadow_image.paste(image, (border, border), image)

    return rounded_shadow_image


# 打开图片
original_image = Image.open("/Users/pnoker/Code/image-tools/images/IMG_0379.jpg").convert("RGBA")

# 缩小
scale_factor = 0.8  # 缩小比例
small_image = original_image.resize((int(original_image.width * scale_factor), int(original_image.height * scale_factor)), Resampling.LANCZOS)

# 圆角
rounded_radius = 10  # 圆角半径
rounded_image = add_rounded(small_image, rounded_radius)

# 阴影
shadow_color = (0, 0, 0)  # 阴影颜色
shadow_border = 20  # 阴影边框
shadow_radius = rounded_radius  # 阴影半径
shadow_image = add_shadow(rounded_image, shadow_color, shadow_border, shadow_radius)

# 高斯模糊
gaussian_blur = 50  # 高斯模糊半径
gaussian_image = original_image.filter(ImageFilter.GaussianBlur(gaussian_blur))

# 合并
gaussian_image.paste(shadow_image, ((gaussian_image.width - shadow_image.width) // 2, (gaussian_image.height - shadow_image.height) // 2), shadow_image)

# 保存
gaussian_image.save("/Users/pnoker/Code/image-tools/images/demo_t.png", format="PNG", optimize=True)
