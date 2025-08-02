import argparse
import os

import cv2 as cv
import numpy as np

from color_algorithms import get_algorithm_function, get_available_algorithms


def save_resized_texture(texture, output_path="resized_texture.png"):
    """
    Save the resized 7x6 texture as an image for verification
    """
    texture_rgb = cv.cvtColor(texture, cv.COLOR_BGR2RGB)
    texture_resized = cv.resize(texture_rgb, (7, 6))
    
    # Scale up for visibility (each pixel becomes a 50x50 square)
    square_size = 50
    img_width = 7 * square_size
    img_height = 6 * square_size
    
    enlarged_img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    
    for v in range(6):
        for u in range(7):
            colour_rgb = texture_resized[v, u]
            colour_bgr = (colour_rgb[2], colour_rgb[1], colour_rgb[0])
            
            x1 = u * square_size
            y1 = v * square_size
            x2 = (u + 1) * square_size
            y2 = (v + 1) * square_size
            
            enlarged_img[y1:y2, x1:x2] = colour_bgr
    
    cv.imwrite(output_path, enlarged_img)
    return enlarged_img

def serialize_image_to_uv(source_image, texture, algorithm_func):
    """
    Convert source image to UV coordinates by mapping to closest texture colours
    """
    if source_image.shape[1] != 100 or source_image.shape[0] != 66:
        source_image = cv.resize(source_image, (100, 66))
    
    texture_rgb = cv.cvtColor(texture, cv.COLOR_BGR2RGB)
    texture_resized = cv.resize(texture_rgb, (7, 6))
    
    save_resized_texture(texture)
    
    serialized_list = []
    width = source_image.shape[1]
    height = source_image.shape[0]
    
    # Match the game's order: for (int i = 0; i < width; i++) { for (int j = 0; j < height; j++) }
    for i in range(width):
        for j in range(height-1, -1, -1):
            pixel_colour = source_image[j, i]
            
            best_u, best_v = algorithm_func(pixel_colour, texture_resized)
            
            best_u = np.clip(best_u, 0, 6)
            best_v = np.clip(best_v, 0, 5)
            best_u = np.clip((best_u / 6.0), 0.01, 0.99)
            best_v = np.clip(1.0 - (best_v / 5.0), 0.01, 0.99)
            
            serialized_list.append(f"{best_u:.2f}:{best_v:.2f}")
    
    return ",".join(serialized_list)

def create_uv_preview_image(serialized_data, texture, output_path="image_preview.png"):
    """
    Create a visual image from the UV coordinates to show what the serialized data looks like
    """
    uv_pairs = serialized_data.split(',')
    
    width = 100
    height = 66
    
    texture_rgb = cv.cvtColor(texture, cv.COLOR_BGR2RGB)
    texture_resized = cv.resize(texture_rgb, (7, 6))
    
    preview_img = np.zeros((height, width, 3), dtype=np.uint8)
    
    num = 0
    for i in range(width):
        for j in range(height):
            if num >= len(uv_pairs):
                break
                
            uv_pair = uv_pairs[num]
            array2 = uv_pair.split(':')
            x = float(array2[0])
            y = float(array2[1])
            
            texture_u = int(x * 7)
            texture_v = int((1.0 - y) * 6)
            
            texture_u = max(0, min(6, texture_u))
            texture_v = max(0, min(5, texture_v))
            
            colour_rgb = texture_resized[texture_v, texture_u]
            colour_bgr = (colour_rgb[2], colour_rgb[1], colour_rgb[0])
            
            preview_img[j, i] = colour_bgr
            
            num += 1
    
    preview_img = cv.flip(preview_img, 0)
    cv.imwrite(output_path, preview_img)
    print(f"Preview saved: {output_path}")
    return preview_img

def normalize_image_path(image_path):
    """
    Normalize image path to handle both full paths and relative paths from images/ folder
    """
    if os.path.isabs(image_path):
        return image_path
    
    if image_path.startswith('./') or image_path.startswith('.\\') or '/' in image_path or '\\' in image_path:
        return image_path
    
    return os.path.join('images', image_path)

def clear_previews_folder():
    """
    Clear the previews folder before processing
    """
    if os.path.exists('previews'):
        for file in os.listdir('previews'):
            if file.endswith('.png'):
                os.remove(os.path.join('previews', file))

def process_image_with_algorithm(source_image_path, texture_path, algorithm_name, output_prefix="image_preview"):
    """
    Process an image with a specific algorithm and create preview
    """
    source_image = cv.imread(source_image_path, cv.IMREAD_COLOR_BGR)
    texture = cv.imread(texture_path, cv.IMREAD_COLOR_BGR)
    
    if source_image is None:
        raise ValueError(f"Could not load source image: {source_image_path}")
    if texture is None:
        raise ValueError(f"Could not load texture image: {texture_path}")
    
    algorithm_func = get_algorithm_function(algorithm_name)
    if algorithm_func is None:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    print(f"Using algorithm: {algorithm_name}")
    
    serialized_data = serialize_image_to_uv(source_image, texture, algorithm_func)
    
    os.makedirs('previews', exist_ok=True)
    
    if algorithm_name == "rgb":
        output_path = os.path.join('previews', f"{output_prefix}.png")
    else:
        output_path = os.path.join('previews', f"{output_prefix}_{algorithm_name}.png")
    
    create_uv_preview_image(serialized_data, texture, output_path)
    
    hex_serialized_data = ','.join([f"0x{hex(ord(c))[2:].upper()}" for c in serialized_data])
    
    return hex_serialized_data

def main():
    parser = argparse.ArgumentParser(description="Convert image to binary data for Mage Arena")
    parser.add_argument("image", nargs='?', help="Path to the source image file (from images/ folder)")
    parser.add_argument("--image", help="Path to the source image file (from images/ folder)")
    parser.add_argument("--alg", default="rgb", 
                       help=f"Colour matching algorithm to use. Available: {', '.join(get_available_algorithms())}, or 'all' to test all algorithms")
    parser.add_argument("--output", default="registry_command.ps1", help="Output file path (default: registry_command.ps1)")
    
    args = parser.parse_args()
    
    # Handle image path from either positional argument or --image flag
    image_path = args.image
    
    if not image_path:
        print("Error: No image path provided. Use --image <filename> or provide as positional argument.")
        print(f"Available algorithms: {', '.join(get_available_algorithms())}")
        return
    
    # Normalize image path
    image_path = normalize_image_path(image_path)
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        print("Make sure the image is in the images/ folder or provide the full path.")
        return
    
    try:
        print(f"Converting {image_path} to mage-arena-texture.png texture")
        
        # Clear previews folder before processing
        clear_previews_folder()
        
        if args.alg == "all":
            # Process with all algorithms
            print("Processing with all algorithms...")
            for alg_name in get_available_algorithms():
                print(f"\n--- Processing with {alg_name} algorithm ---")
                try:
                    process_image_with_algorithm(image_path, "mage-arena-texture.png", alg_name)
                    print(f"✅ {alg_name} algorithm completed successfully")
                except Exception as e:
                    print(f"❌ {alg_name} algorithm failed: {e}")
            
            # Write registry command for default algorithm (rgb)
            binary_data = process_image_with_algorithm(image_path, "mage-arena-texture.png", "rgb")
            path = r"HKEY_CURRENT_USER\Software\jrsjams\MageArena"
            keyname = "flagGrid_h3042110417"
            with open(args.output, "w") as f:
                f.write(f"Set-ItemProperty -Path 'Registry::{path}' -Name '{keyname}' -Type Binary -Value ([byte[]]({binary_data}))\n")
            print(f"PowerShell registry command written to {args.output}")
        else:
            # Process with single algorithm
            binary_data = process_image_with_algorithm(image_path, "mage-arena-texture.png", args.alg)
            
            # Registry path and key name
            path = r"HKEY_CURRENT_USER\Software\jrsjams\MageArena"
            keyname = "flagGrid_h3042110417"
            
            # Write PowerShell command to file
            with open(args.output, "w") as f:
                f.write(f"Set-ItemProperty -Path 'Registry::{path}' -Name '{keyname}' -Type Binary -Value ([byte[]]({binary_data}))\n")
            print(f"PowerShell registry command written to {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
