#!/usr/bin/env python3
"""
prep_photo.py
Removes background from a portrait photo, enhances contrast (CLAHE),
crops/resizes it, and saves as source-prepped.png.

Usage: python scripts/prep_photo.py hero.png
"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

OUTPUT_SIZE = (600, 750)  # width, height


def enhance_contrast(bgr_image: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def crop_to_subject(rgba: Image.Image) -> Image.Image:
    alpha = np.array(rgba.split()[-1])
    ys, xs = np.where(alpha > 10)
    if len(xs) == 0 or len(ys) == 0:
        return rgba
    pad = 20
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, rgba.width)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, rgba.height)
    return rgba.crop((x0, y0, x1, y1))


def main(input_path: str, output_path: str = "source-prepped.png"):
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    result_bytes = remove(input_bytes)  # U2Net background removal
    with open("_tmp_nobg.png", "wb") as f:
        f.write(result_bytes)

    rgba = Image.open("_tmp_nobg.png").convert("RGBA")
    rgba = crop_to_subject(rgba)

    # Contrast enhance the RGB channels while preserving alpha
    rgb = np.array(rgba.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    bgr_enhanced = enhance_contrast(bgr)
    rgb_enhanced = cv2.cvtColor(bgr_enhanced, cv2.COLOR_BGR2RGB)

    enhanced = Image.fromarray(rgb_enhanced).convert("RGBA")
    enhanced.putalpha(rgba.split()[-1])

    enhanced = enhanced.resize(OUTPUT_SIZE, Image.LANCZOS)
    enhanced.save(output_path)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_photo>")
        sys.exit(1)
    main(sys.argv[1])
