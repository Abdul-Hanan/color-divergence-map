import cv2
import numpy as np
import os
import sys

def generate_test_image(height=240, width=360):
    """
    Generates a synthetic test image with various color characteristics
    to demonstrate the colorfulness map.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Pure primary colors (high divergence)
    img[0:height//3, 0:width//3] = [0, 0, 255]    # Blue
    img[0:height//3, width//3:2*width//3] = [0, 255, 0] # Green
    img[0:height//3, 2*width//3:width] = [255, 0, 0] # Red

    # Achromatic colors (zero divergence)
    img[height//3:2*height//3, 0:width//4] = [0, 0, 0] # Black
    img[height//3:2*height//3, width//4:2*width//4] = [128, 128, 128] # Gray
    img[height//3:2*height//3, 2*width//4:3*width//4] = [255, 255, 255] # White

    # Secondary colors (medium divergence)
    img[height//3:2*height//3, 3*width//4:width] = [255, 255, 0] # Yellow (B=0, G=255, R=255) max diff = 255
                                                            # (actually BGR, so Blue=0, Green=255, Red=255)
                                                            # (B-G)= -255, (G-R)=0, (R-B)=255. Max=255.

    # Gradient for varying divergence
    # Top-left corner to bottom-right corner gradient
    # Red channel gradient from 0 to 255
    # Green channel constant 128
    # Blue channel gradient from 255 to 0
    for y in range(2*height//3, height):
        for x in range(width):
            r = int(255 * (x / width))
            g = 128
            b = int(255 * (1 - x / width))
            img[y, x] = [b, g, r] # BGR format

    return img

def calculate_color_divergence_map(image_bgr):
    """
    Calculates the "pixel colorfulness map" by finding the maximum absolute
    difference between any two BGR channels for each pixel.

    Args:
        image_bgr (np.array): The input BGR image (H, W, 3).

    Returns:
        np.array: A grayscale image (H, W) where pixel intensity
                  represents color channel divergence (0-255).
    """
    if image_bgr.ndim != 3 or image_bgr.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel BGR image.")

    # Split channels
    b, g, r = cv2.split(image_bgr)

    # Calculate absolute differences for each pair of channels
    # numpy automatically handles the intermediate type for subtraction
    # before applying abs, preventing uint8 wrap-around issues for differences.
    diff_bg = np.abs(b - g)
    diff_gr = np.abs(g - r)
    diff_rb = np.abs(r - b)

    # Determine the maximum difference for each pixel
    # The result will be in the range [0, 255], suitable for uint8 grayscale.
    colorfulness_map = np.maximum(diff_bg, np.maximum(diff_gr, diff_rb))

    # Ensure the output is uint8
    return colorfulness_map.astype(np.uint8)

def main():
    # Define output directory and file names
    output_dir = "output"
    original_image_filename = "original_test_image.png"
    divergence_map_filename = "color_divergence_map.png"

    # Create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory '{output_dir}': {e}", file=sys.stderr)
        sys.exit(1)

    original_image_path = os.path.join(output_dir, original_image_filename)
    divergence_map_path = os.path.join(output_dir, divergence_map_filename)

    print("Starting Color Divergence Map generation project.")
    print("-" * 40)

    # 1. Generate a synthetic test image
    print("Step 1/3: Generating synthetic test image...")
    test_image = generate_test_image()
    print(f"Generated image of shape: {test_image.shape}")

    # Save the original test image (for verification on a headless server)
    print(f"Saving original test image to '{original_image_path}'...")
    if not cv2.imwrite(original_image_path, test_image):
        print(f"Error: Could not save original image to '{original_image_path}'.", file=sys.stderr)
        sys.exit(1)
    print("Original image saved successfully.")

    # 2. Calculate the pixel colorfulness map
    print("Step 2/3: Calculating pixel colorfulness map...")
    try:
        colorfulness_map = calculate_color_divergence_map(test_image)
        print(f"Calculated divergence map of shape: {colorfulness_map.shape}")
    except ValueError as e:
        print(f"Error calculating divergence map: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Save the resulting divergence map
    print(f"Step 3/3: Saving color divergence map to '{divergence_map_path}'...")
    if not cv2.imwrite(divergence_map_path, colorfulness_map):
        print(f"Error: Could not save divergence map to '{divergence_map_path}'.", file=sys.stderr)
        sys.exit(1)
    print("Divergence map saved successfully.")

    print("-" * 40)
    print("Processing complete. Check the 'output' directory for 'original_test_image.png' and 'color_divergence_map.png'.")

if __name__ == "__main__":
    main()