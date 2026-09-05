from PIL import Image


def image_hash(path):
    with Image.open(path) as img:
        img = img.resize((80, 45)).convert("L")
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        return tuple(1 if p > avg else 0 for p in pixels)


def images_differ(h1, h2, threshold=0.08):
    if h1 is None:
        return True
    diff = sum(a != b for a, b in zip(h1, h2)) / len(h1)
    return diff > threshold
