# Mage Arena Image Converter

A Python tool that converts images into the team flags in the game! After running python script and generated powershell script, you can hit the "load from disk" button to load the image into a flag

## How It Works

1. **Image Processing**: Your image gets resized to 100x66 pixels (the game's display resolution)
2. **Color Matching**: Each pixel is compared to the 42 colors in the Mage Arena texture and mapped to the closest match (different algorithms for differnet mapping results available)
3. **UV Conversion**: The best color matches are converted to UV coordinates (0.0-1.0 range)
4. **Serialization**: The UV data gets converted to freaky ahh binary format the game recognizes for the flag
5. **Registry Writing**: A PowerShell script is generated to write the data to the Windows registry (specifically the Unity PlayerPrefs thing, which lives in the registry ig)

## Prerequisites

- **Windows 10** (this is what I tested on - other versions might work but no guarantees!)
- **Python 3.13** but im guessing down to python 3.8 works too
- **uv** (Python package manager) - [Install uv here](https://docs.astral.sh/uv/getting-started/installation/)
- Or you can use pip

## Quick Start

### Installation Options

**Option A: Using uv (Recommended because its hype)**

```bash
git clone https://github.com/ColtG5/mage-arena-image-to-flag.git
cd mage-arena
uv sync
```

**Option B: Using pip**

```bash
git clone https://github.com/yourusername/mage-arena-image-to-flag.git
cd mage-arena
pip install -r requirements.txt
```

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mage-arena.git
cd mage-arena
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Add Your Image

Place your image file(s) in the `images/` folder. I know JPG and PNG work, others might too idk

### 4. Run the Python converter script main.py

```bash
uv run python main.py --image your_image.jpg
```

### 5. Check the preview of the image in the previews folder

For the algorithm(s) you specified to generate the image with, exists a preview image of what it would look like in game. You can use this to see if it is good or not before editing your registry

### 6. Apply to Game

Run the generated `registry_command.ps1` file as administrator to apply your image to Mage Arena.

## Usage Examples

### Basic Usage

```bash
# Convert an image using the default RGB algorithm
uv run python main.py --image my_flag.png
```

### Try Different Algorithms

```bash
# Use HSV color matching (better for colorful images)
uv run python main.py --image my_flag.png --alg hsv

# Use LAB color matching (perceptually uniform)
uv run python main.py --image my_flag.png --alg lab

# See preview images for all algorithms
uv run python main.py --image my_flag.png --alg all
```

## Available Algorithms

- **`rgb`** (default): Simple RGB color distance - fast and works well for most images
- **`hsv`**: HSV color space matching - better for colorful images
- **`lab`**: LAB color space (perceptually uniform) - most accurate color matching
- **`perceptual`**: Combined RGB + LAB approach - balanced performance and accuracy
- **`weighted`**: RGB with saturation boost - good for vibrant images
- **`simple`**: RGB with grayscale penalty - avoids matching colors to grays
- **`perceptual_hsv`**: Advanced HSV with hue prioritization

## Troubleshooting 🔧

### Common Issues

**"Image file not found"**

- Make sure your image is in the `images/` folder
- Or provide the full path to your image

**"Could not load source image"**

- Check that your image file isn't corrupted
- Try a different image format (JPG, PNG, etc.)

**"Unknown algorithm"**

- Use `uv run python main.py --image your_image.jpg --alg rgb` to see available algorithms

**Registry script doesn't work**

- Run PowerShell as Administrator
- Make sure Mage Arena is installed
- Check that the game is closed when running the script

### Getting Help

If something goes wrong:

1. Check that all dependencies are installed: `uv sync`
2. Try a simple test image first
3. Use the `--alg all` option to test all algorithms
4. Check the generated preview images in the `previews/` folder

## Technical Details

- **Image Resolution**: 100x66 pixels (game's display size)
- **Texture Palette**: 7x6 color grid (42 total colors)
- **UV Coordinates**: Normalized 0.0-1.0 range
- **Binary Format**: Hex-encoded string for Windows registry
- **Registry Path**: `HKEY_CURRENT_USER\Software\jrsjams\MageArena`

## Contributing

Anybody can add anything they want, suggest any features, etc.

## License

MIT License
