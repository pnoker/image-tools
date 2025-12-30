import argparse
import sys

from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(image_path, text, x, y, font_path, font_size, output_path, bg_width, bg_height, bg_color, radius):
    try:
        image = Image.open(image_path).convert("RGBA")

        # Create a transparent overlay for the background block
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font not found at {font_path}, using default font.")
            font = ImageFont.load_default()

        # Draw rounded rectangle (background block)
        # x, y is the top-left coordinate of the block
        draw.rounded_rectangle([(x, y), (x + bg_width, y + bg_height)], radius=radius, fill=bg_color)

        # Calculate text position to center it within the block
        # Using anchor='mm' (middle-middle) for easy centering
        center_x = x + bg_width / 2
        center_y = y + bg_height / 2

        draw.text((center_x, center_y), text, font=font, fill=(255, 255, 255), anchor="mm")

        # Composite the overlay onto the original image
        image = Image.alpha_composite(image, overlay)

        # Convert back to RGB if saving as JPEG, otherwise keep RGBA (e.g. for PNG)
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            image = image.convert("RGB")

        image.save(output_path)
        print(f"Image saved to {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")


def parse_color(color_str):
    try:
        return tuple(map(int, color_str.split(',')))
    except ValueError:
        return (0, 0, 0, 128)  # Default to semi-transparent black


def main():
    parser = argparse.ArgumentParser(description="Add text to an image with a background block.")
    parser.add_argument("--image", required=True, help="Path to source image")
    parser.add_argument("--text", required=True, help="Text to add")
    parser.add_argument("--x", type=int, default=0, help="X coordinate of the block")
    parser.add_argument("--y", type=int, default=0, help="Y coordinate of the block")
    parser.add_argument("--font", default="/System/Library/Fonts/Helvetica.ttc", help="Path to font file")
    parser.add_argument("--size", type=int, default=20, help="Font size")
    parser.add_argument("--output", required=True, help="Path to output image")

    # New arguments for background block
    parser.add_argument("--bg-width", type=int, default=200, help="Width of background block")
    parser.add_argument("--bg-height", type=int, default=100, help="Height of background block")
    parser.add_argument("--bg-color", default="0,0,0,128", help="Background color (R,G,B,A)")
    parser.add_argument("--radius", type=int, default=10, help="Corner radius of background block")

    args = parser.parse_args()

    bg_color = parse_color(args.bg_color)

    add_text_to_image(args.image, args.text, args.x, args.y, args.font, args.size, args.output,
                      args.bg_width, args.bg_height, bg_color, args.radius)


if __name__ == "__main__":
    text_list = ["宋英"]
    for idx, txt in enumerate(text_list):
        # x_pos was manually calculated for centering, now we can use a fixed block position or adjust as needed.
        # Assuming we want to place the block at the same general area.
        # Let's use a fixed x for the block, say 150, and let the text center itself.
        # Or keep the user's logic if they want the block to move. 
        # But for demonstration, I'll update the arguments to use the new features.

        sys.argv = [
            sys.argv[0],
            "--image", "../images/RAW.png",
            "--text", txt,
            "--x", "150",
            "--y", "707",
            "--font", "/Users/pnoker/Library/Fonts/WangZhi-KuaiXueShiQingTie.ttf",
            "--size", "25",
            "--output", f"{txt}.png",
            "--bg-width", "120",
            "--bg-height", "50",
            "--bg-color", "0,0,0,100",  # Semi-transparent black
            "--radius", "10"
        ]
        main()
