#!/usr/bin/env python3
"""
Example usage of Mage Arena Image Converter
Shows how to use the project programmatically
"""

import cv2 as cv

from color_algorithms import get_algorithm_function, get_available_algorithms
from main import create_uv_preview_image, serialize_image_to_uv


def example_basic_usage():
    """Basic example of converting an image"""
    print("🎮 Mage Arena Image Converter - Example Usage")
    print("=" * 50)
    
    # Load images
    source_image = cv.imread("images/test_flag.png", cv.IMREAD_COLOR)
    texture = cv.imread("mage-arena-texture.png", cv.IMREAD_COLOR)
    
    if source_image is None:
        print("❌ Could not load source image")
        return
    
    if texture is None:
        print("❌ Could not load texture image")
        return
    
    print(f"✅ Loaded source image: {source_image.shape[1]}x{source_image.shape[0]}")
    print(f"✅ Loaded texture image: {texture.shape[1]}x{texture.shape[0]}")
    
    # Get available algorithms
    algorithms = get_available_algorithms()
    print(f"\n📊 Available algorithms: {', '.join(algorithms)}")
    
    # Test with different algorithms
    for alg_name in ['rgb', 'hsv', 'lab']:
        print(f"\n🔄 Testing {alg_name} algorithm...")
        
        # Get the algorithm function
        alg_func = get_algorithm_function(alg_name)
        
        # Convert image to UV coordinates
        serialized_data = serialize_image_to_uv(source_image, texture, alg_func)
        
        # Create preview image
        preview_path = f"previews/example_{alg_name}.png"
        create_uv_preview_image(serialized_data, texture, preview_path)
        
        print(f"✅ Created preview: {preview_path}")
        print(f"📏 Serialized data length: {len(serialized_data)} characters")
    
    print(f"\n🎉 Example completed! Check the previews/ folder for results.")

def example_custom_algorithm():
    """Example of creating a custom color matching algorithm"""
    print("\n🔧 Custom Algorithm Example")
    print("=" * 30)
    
    def custom_rgb_weighted(pixel_colour, texture_resized):
        """
        Custom algorithm that weights red channel more heavily
        """
        pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
        min_dist = float('inf')
        best_u, best_v = 0, 0
        
        for v in range(6):
            for u in range(7):
                texture_colour = tuple(texture_resized[v, u])
                
                # Weighted RGB distance (red channel gets 2x weight)
                r_diff = (pixel_rgb[0] - texture_colour[0]) ** 2
                g_diff = (pixel_rgb[1] - texture_colour[1]) ** 2
                b_diff = (pixel_rgb[2] - texture_colour[2]) ** 2
                
                dist = (2.0 * r_diff) + g_diff + b_diff
                
                if dist < min_dist:
                    min_dist = dist
                    best_u, best_v = u, v
        
        return best_u, best_v
    
    # Load images
    source_image = cv.imread("images/test_flag.png", cv.IMREAD_COLOR)
    texture = cv.imread("mage-arena-texture.png", cv.IMREAD_COLOR)
    
    if source_image is None or texture is None:
        print("❌ Could not load images")
        return
    
    # Use custom algorithm
    print("🔄 Testing custom red-weighted algorithm...")
    serialized_data = serialize_image_to_uv(source_image, texture, custom_rgb_weighted)
    
    # Create preview
    preview_path = "previews/example_custom.png"
    create_uv_preview_image(serialized_data, texture, preview_path)
    
    print(f"✅ Created custom preview: {preview_path}")

def example_batch_processing():
    """Example of processing multiple images"""
    print("\n📦 Batch Processing Example")
    print("=" * 30)
    
    import glob
    import os
    
    # Get all images in images folder
    image_files = glob.glob("images/*.jpg") + glob.glob("images/*.png")
    
    if not image_files:
        print("❌ No images found in images/ folder")
        return
    
    texture = cv.imread("mage-arena-texture.png", cv.IMREAD_COLOR)
    if texture is None:
        print("❌ Could not load texture image")
        return
    
    print(f"📁 Found {len(image_files)} images to process")
    
    # Process each image with the best algorithm
    alg_func = get_algorithm_function('perceptual')  # Use perceptual algorithm
    
    for image_file in image_files:
        print(f"\n🔄 Processing: {os.path.basename(image_file)}")
        
        source_image = cv.imread(image_file, cv.IMREAD_COLOR)
        if source_image is None:
            print(f"❌ Could not load: {image_file}")
            continue
        
        # Convert image
        serialized_data = serialize_image_to_uv(source_image, texture, alg_func)
        
        # Create preview
        base_name = os.path.splitext(os.path.basename(image_file))[0]
        preview_path = f"previews/batch_{base_name}.png"
        create_uv_preview_image(serialized_data, texture, preview_path)
        
        print(f"✅ Created: {preview_path}")
    
    print(f"\n🎉 Batch processing completed!")

if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_custom_algorithm()
    example_batch_processing()
    
    print("\n" + "=" * 50)
    print("📚 Example usage completed!")
    print("Check the previews/ folder for all generated images.")
    print("These examples show how to integrate the converter into your own code.") 