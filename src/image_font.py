import argparse
import sys

from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(image_path, text, x, y, font_path, font_size, output_path):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font not found at {font_path}, using default font.")
            font = ImageFont.load_default()

        draw.text((x, y), text, font=font, fill=(0, 0, 0))  # Default to black text
        image.save(output_path)
        print(f"Image saved to {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")


def main():
    parser = argparse.ArgumentParser(description="Add text to an image.")
    parser.add_argument("--image", required=True, help="Path to source image")
    parser.add_argument("--text", required=True, help="Text to add")
    parser.add_argument("--x", type=int, default=0, help="X coordinate")
    parser.add_argument("--y", type=int, default=0, help="Y coordinate")
    parser.add_argument("--font", default="/System/Library/Fonts/Helvetica.ttc", help="Path to font file")
    parser.add_argument("--size", type=int, default=20, help="Font size")
    parser.add_argument("--output", required=True, help="Path to output image")

    args = parser.parse_args()

    add_text_to_image(args.image, args.text, args.x, args.y, args.font, args.size, args.output)


if __name__ == "__main__":
    text_list = ["张晓华", "陈沅", "郝丽平", "李嘉欣", "李彦魁", "罗青", "邵汀潇", "王灿发", "王莹", "谢永恒", "翟雅娴"]
    for idx, txt in enumerate(text_list):
        x_pos = "177" if len(txt) == 3 else "188"
        sys.argv = [
            sys.argv[0],
            "--image", "images/RAW.png",
            "--text", txt,
            "--x", x_pos,
            "--y", "707",
            "--font", "/Users/pnoker/Library/Fonts/WangZhi-KuaiXueShiQingTie.ttf",
            "--size", "25",
            "--output", f"5组/{txt}.png"
        ]
        main()
