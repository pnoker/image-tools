from PIL import Image, ImageFilter, ImageOps,ImageDraw,ImageFont
import time

def add_text_to_image(image, text, font_path=None, font_size=20, text_color=(255, 255, 255)):
    # 打开图像
    image = image.convert("RGBA")
    
    # 创建一个绘图对象
    draw = ImageDraw.Draw(image)

    font_size= min(image.size)*0.05
    
    # 加载字体
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    
    # 计算文本尺寸
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # 计算文本居中的位置
    image_width, image_height = image.size
    position = ((image_width - text_width) // 2, (image_height*0.9+(image_height*0.1 - text_height) // 2))
    
    # 添加文字
    draw.text(position, text, fill=text_color, font=font)
    
    # 保存或显示结果
    image.save('../images/demo_1.png')

def add_shadow(image, background_color=(255,255,255,255), shadow_color=(0,0,0,32), border=10,  offset=(1, 1)):
    print(f"0image: {image}")
    start_time = time.time()
    border = max(10,min(50,min(image.size)//100))
    print(f"border: {border}")
    total_width = image.size[0] + abs(offset[0]) + 2 * border
    total_height = image.size[1] + abs(offset[1]) + 2 * border
    shadow = Image.new(image.mode, (total_width, total_height), background_color)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"1Execution time: {execution_time} seconds")

    # 添加阴影
    start_time = time.time()
    iterations=border
    shadow_left = border + max(offset[0], 0)
    shadow_top = border + max(offset[1], 0)
    shadow.paste(shadow_color, [shadow_left, shadow_top, shadow_left + image.size[0], shadow_top + image.size[1]])
    for _ in range(1):
        start_time = time.time()
        shadow = shadow.filter(ImageFilter.BLUR)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"2Execution time: {execution_time} seconds")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"3Execution time: {execution_time} seconds")

    # 添加图片
    start_time = time.time()
    image_left = border - min(offset[0], 0)
    image_top = border - min(offset[1], 0)
    shadow.paste(image, (image_left, image_top))
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"4Execution time: {execution_time} seconds")

    # 保存结果
    start_time = time.time()
    #shadow.save('output_with_shadow.png')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"5Execution time: {execution_time} seconds")

    return shadow

input_image_path = '../images/demo.png'
image = Image.open(input_image_path)

shadow = add_shadow(image)

# 输入参数
text_to_add = "@pnoker"
font_path = "Arial.ttf"  # 字体路径，如果使用系统默认字体可以设置为 None
font_size = 30  # 字体大小
text_color = (255, 255, 255, 255)  # 文字颜色 (白色)

# 调用函数
add_text_to_image(shadow, text_to_add, font_path, font_size, text_color)