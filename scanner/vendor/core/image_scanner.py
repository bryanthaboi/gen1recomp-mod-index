"""
Image normalization, 256-bit dHash computation, Hamming distance, and 3-panel diff generation.
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Optional, Tuple
from PIL import Image, ImageChops, ImageDraw
try:
    import imagehash
except ImportError:
    imagehash = None

from ..config import ImageRules


@dataclass
class ImageMatchResult:
    filename: str
    matched_ref_key: str
    hamming_distance: int
    mod_hash: str
    ref_hash: str
    status: str  # "REJECT", "FLAGGED", or "PASS"
    preview_image: Optional[Image.Image] = None


def normalize_image_for_hashing(img: Image.Image) -> Image.Image:
    """
    Normalizes any RGBA/palette/grayscale image by compositing any transparency
    onto a solid white background before converting to 8-bit grayscale luminance.
    This prevents transparent alpha channels from collapsing into black.
    """
    if img.mode != "RGBA":
        rgba_img = img.convert("RGBA")
    else:
        rgba_img = img

    # Composite over pure white canvas
    white_bg = Image.new("RGBA", rgba_img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba_img)
    return composited.convert("L")


def compute_dhash_pillow(img: Image.Image, hash_size: int = 16) -> str:
    """
    Computes a 16x16 difference hash (256 bits) using standard Pillow.
    Produces 100% bit-for-bit identical hashes to standard dHash without NumPy or SciPy.
    """
    resized = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(resized.getdata())
    diff = []
    for row in range(hash_size):
        row_offset = row * (hash_size + 1)
        for col in range(hash_size):
            diff.append(pixels[row_offset + col + 1] > pixels[row_offset + col])

    bit_string = "".join("1" if b else "0" for b in diff)
    width = (len(bit_string) + 3) // 4
    return f"{int(bit_string, 2):0{width}x}"


def compute_image_hash(
    img: Image.Image,
    hash_size: int = 16,
    hash_type: str = "dhash"
) -> str:
    """
    Computes a perceptual hash (default 16x16 dHash = 256 bits) on the normalized grayscale image.
    Returns the hash as a hexadecimal string.
    """
    normalized = normalize_image_for_hashing(img)
    if hash_type == "phash" and imagehash is not None:
        h = imagehash.phash(normalized, hash_size=hash_size)
        return str(h)

    return compute_dhash_pillow(normalized, hash_size=hash_size)


def calculate_hamming_distance(hex_hash1: str, hex_hash2: str) -> int:
    """
    Computes the Hamming distance between two hexadecimal hash strings
    via bitwise XOR and bit-count.
    """
    val1 = int(hex_hash1, 16)
    val2 = int(hex_hash2, 16)
    return bin(val1 ^ val2).count("1")


def _create_checkerboard_panel(size: Tuple[int, int], grid_size: int = 8) -> Image.Image:
    """Creates a subtle light-gray neutral backdrop suitable for both 2bpp monochrome and color sprites."""
    panel = Image.new("RGBA", size, (238, 241, 246, 255))
    draw = ImageDraw.Draw(panel)
    c1 = (238, 241, 246, 255)
    c2 = (226, 232, 240, 255)
    for y in range(0, size[1], grid_size):
        for x in range(0, size[0], grid_size):
            if ((x // grid_size) + (y // grid_size)) % 2 == 1:
                draw.rectangle((x, y, x + grid_size - 1, y + grid_size - 1), fill=c2)
    return panel


def _fit_image_centered(
    img: Image.Image,
    target_size: Tuple[int, int]
) -> Image.Image:
    """
    Places an image centered onto a checkerboard canvas without stretching or altering pixel aspect ratios.
    Preserves exact 1:1 pixel art placement and ensures transparent 2bpp outlines remain sharp.
    """
    canvas = _create_checkerboard_panel(target_size)
    img_rgba = img.convert("RGBA")

    # If image fits inside canvas, center 1:1 to preserve native pixel steps
    if img_rgba.width <= target_size[0] and img_rgba.height <= target_size[1]:
        offset_x = (target_size[0] - img_rgba.width) // 2
        offset_y = (target_size[1] - img_rgba.height) // 2
        canvas.alpha_composite(img_rgba, (offset_x, offset_y))
    else:
        # Scale down only if image is larger than target canvas, strictly preserving aspect ratio
        scale = min(target_size[0] / img_rgba.width, target_size[1] / img_rgba.height)
        new_w = max(1, int(img_rgba.width * scale))
        new_h = max(1, int(img_rgba.height * scale))
        resized = img_rgba.resize((new_w, new_h), Image.Resampling.NEAREST)
        offset_x = (target_size[0] - new_w) // 2
        offset_y = (target_size[1] - new_h) // 2
        canvas.alpha_composite(resized, (offset_x, offset_y))

    return canvas


def generate_diff_preview(
    mod_img: Image.Image,
    ref_img: Image.Image,
    panel_size: int = 64,
    upscale_factor: int = 2
) -> Image.Image:
    """
    Generates a crisp 3-panel comparison preview:
    [ Mod Asset ] [ Canonical Reference ] [ Pixel Difference ]
    Sprites are centered 1:1 on neutral background to prevent outline clipping or stretching.
    """
    # Determine base panel dimensions
    base_dim = max(panel_size, mod_img.width, mod_img.height, ref_img.width, ref_img.height)
    base_dim = ((base_dim + 7) // 8) * 8
    target_size = (base_dim, base_dim)

    # 1. Center both images on neutral high-contrast checkerboard panels
    mod_norm = _fit_image_centered(mod_img, target_size)
    ref_norm = _fit_image_centered(ref_img, target_size)

    # 2. Compute visual difference
    diff = ImageChops.difference(mod_norm.convert("RGB"), ref_norm.convert("RGB"))

    # 3. Assemble 3-panel base canvas
    pad = 4
    canvas_width = base_dim * 3 + pad * 4
    canvas_height = base_dim + pad * 2
    canvas = Image.new("RGB", (canvas_width, canvas_height), (24, 25, 28))

    # Paste panels
    canvas.paste(mod_norm.convert("RGB"), (pad, pad))
    canvas.paste(ref_norm.convert("RGB"), (base_dim + pad * 2, pad))
    canvas.paste(diff, (base_dim * 2 + pad * 3, pad))

    # 4. Upscale for crisp presentation on high-DPI and Discord embeds
    if upscale_factor > 1:
        canvas = canvas.resize(
            (canvas.width * upscale_factor, canvas.height * upscale_factor),
            Image.Resampling.NEAREST
        )

    return canvas
