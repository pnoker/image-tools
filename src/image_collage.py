import argparse
import sys
from PIL import Image


def create_collage(image_paths, cols, rows, output_path, cell_width=None, cell_height=None, background_color=(255, 255, 255)):
    """
    创建拼图
    
    Args:
        image_paths: 图片文件路径列表
        cols: 列数
        rows: 行数
        output_path: 输出文件路径
        cell_width: 每个单元格的宽度（可选，默认使用第一张图片的宽度）
        cell_height: 每个单元格的高度（可选，默认使用第一张图片的高度）
        background_color: 背景颜色，默认白色
    """
    try:
        # 加载所有图片
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                print(f"无法加载图片 {path}: {e}")
                continue
        
        if not images:
            print("没有有效的图片文件")
            return
        
        # 如果没有指定单元格大小，使用第一张图片的尺寸
        if cell_width is None or cell_height is None:
            first_img = images[0]
            cell_width = cell_width or first_img.width
            cell_height = cell_height or first_img.height
        
        # 计算画布大小
        canvas_width = cols * cell_width
        canvas_height = rows * cell_height
        
        # 创建画布
        canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)
        
        # 按顺序放置图片
        for i, img in enumerate(images):
            if i >= cols * rows:
                print(f"警告：图片数量超过网格容量（{cols * rows}张），多余的图片将被忽略")
                break
            
            # 计算位置
            row = i // cols
            col = i % cols
            x = col * cell_width
            y = row * cell_height
            
            # 调整图片大小以适应单元格
            resized_img = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
            
            # 将图片粘贴到画布上
            canvas.paste(resized_img, (x, y))
        
        # 保存结果
        canvas.save(output_path)
        print(f"拼图已保存到: {output_path}")
        
    except Exception as e:
        print(f"创建拼图时出错: {e}")


def main():
    parser = argparse.ArgumentParser(description="创建图片拼图")
    parser.add_argument("--images", nargs='+', required=True, help="图片文件路径列表")
    parser.add_argument("--cols", type=int, required=True, help="列数")
    parser.add_argument("--rows", type=int, required=True, help="行数")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--width", type=int, help="每个单元格的宽度（可选）")
    parser.add_argument("--height", type=int, help="每个单元格的高度（可选）")
    parser.add_argument("--bg-color", default="255,255,255", help="背景颜色（R,G,B），默认白色")
    
    args = parser.parse_args()
    
    # 解析背景颜色
    try:
        background_color = tuple(map(int, args.bg_color.split(',')))
        if len(background_color) != 3:
            raise ValueError()
    except:
        print("背景颜色格式错误，使用默认白色")
        background_color = (255, 255, 255)
    
    # 验证参数
    if args.cols <= 0 or args.rows <= 0:
        print("列数和行数必须大于0")
        return
    
    if len(args.images) == 0:
        print("请提供至少一张图片")
        return
    
    # 创建拼图
    create_collage(
        image_paths=args.images,
        cols=args.cols,
        rows=args.rows,
        output_path=args.output,
        cell_width=args.width,
        cell_height=args.height,
        background_color=background_color
    )


if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) == 1:
        # 如果没有命令行参数，使用示例数据
        print("使用示例参数运行...")
        sys.argv = [
            sys.argv[0],
            "--images", "images/RAW.png", "images/RAW.png", "images/RAW.png", "images/RAW.png",
            "--cols", "2",
            "--rows", "2", 
            "--output", "collage_example.png",
            "--width", "200",
            "--height", "200"
        ]
    
    main()