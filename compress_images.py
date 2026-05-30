from PIL import Image
import os

def compress_image(image_path, max_size_kb=200, quality=85, min_quality=50):
    """压缩图片到指定大小以下"""
    file_size = os.path.getsize(image_path) / 1024

    if file_size <= max_size_kb:
        print(f"  跳过: {os.path.basename(image_path)} ({file_size:.1f}KB - 已符合要求)")
        return

    img = Image.open(image_path)
    original_size = file_size

    current_quality = quality
    output_path = image_path

    while current_quality >= min_quality:
        img.save(output_path, 'JPEG', quality=current_quality, optimize=True)
        current_size = os.path.getsize(output_path) / 1024

        if current_size <= max_size_kb:
            print(f"  压缩成功: {os.path.basename(image_path)} ({original_size:.1f}KB -> {current_size:.1f}KB, 质量={current_quality})")
            return

        current_quality -= 5

    img.save(output_path, 'JPEG', quality=min_quality, optimize=True)
    final_size = os.path.getsize(output_path) / 1024
    print(f"  压缩完成: {os.path.basename(image_path)} ({original_size:.1f}KB -> {final_size:.1f}KB, 质量={min_quality})")

def process_directory(directory):
    """处理目录下所有图片"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    print(f"\n开始扫描目录: {directory}\n")

    processed_count = 0
    skipped_count = 0

    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()

        if ext in image_extensions:
            image_path = os.path.join(directory, filename)

            if os.path.isfile(image_path):
                file_size = os.path.getsize(image_path) / 1024

                if file_size > 500:
                    compress_image(image_path)
                    processed_count += 1
                else:
                    print(f"  跳过: {filename} ({file_size:.1f}KB - 小于500KB)")
                    skipped_count += 1

    print(f"\n处理完成！")
    print(f"  压缩了 {processed_count} 张图片")
    print(f"  跳过了 {skipped_count} 张图片")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    if os.path.exists(images_dir):
        process_directory(images_dir)
    else:
        process_directory(script_dir)

    print("\n按回车键退出...")
    input()