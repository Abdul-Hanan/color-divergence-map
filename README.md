# Color Divergence Map

Generates a grayscale map indicating pixel color channel divergence for an input image. For each pixel, it calculates the maximum absolute difference between any two of its BGR color channels (`max(abs(B-G), abs(G-R), abs(R-B))`) and visualizes this value as a grayscale image. Brighter pixels in the output map indicate higher color channel divergence, representing more "colorful" or vibrant pixels.

The project runs entirely on a headless server, saving all visual output to files.

## How to Run

1.  **Install Dependencies:**
    Make sure you have `pip` installed. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute the Script:**
    Run the main Python script. It will generate a synthetic test image, process it, and save the results.
    ```bash
    python main.py
    ```

## Output

The script will create an `output/` directory in the project's root. Inside, you will find:

*   `original_test_image.png`: The synthetic image generated for processing.
*   `color_divergence_map.png`: The grayscale map showing pixel colorfulness. Brighter areas indicate higher divergence between color channels.