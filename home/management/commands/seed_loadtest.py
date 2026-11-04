"""Create 1000 load-test images (~1 MB JPEG each) and 40 news posts.

Run on every deploy (entrypoint.sh) BEFORE collectstatic, so the static images
are collected into STATIC_ROOT automatically.
"""
import colorsys
import io
import random
from pathlib import Path

from django.core.management.base import BaseCommand
from PIL import Image

from home.models import NewsPost, StressImage

IMAGES = 1000
NEWS = 40
CATEGORIES = ["tech", "sports", "fashion", "food", "travel", "news"]
LABELS = dict(StressImage.CATEGORIES)

IMAGE_SIZE = (1600, 1200)
QUALITY = 90

STATIC_LOADTEST = Path(__file__).resolve().parent.parent.parent / "static" / "home" / "loadtest"

NEWS_WORDS = [
    "Market", "Server", "Cloud", "Release", "Update", "Security", "Database",
    "Frontend", "Backend", "API", "Deploy", "Scale", "Cache", "Queue",
    "Design", "Review", "Launch", "Feature", "Patch", "Upgrade",
]


def make_image(category_index: int, seed: int) -> bytes:
    """Generate a photo-style ~1 MB JPEG (color noise, category-tinted)."""
    rng = random.Random(seed)
    base_hue = category_index * 60
    small = Image.new("RGB", (400, 300))
    px = small.load()
    for y in range(300):
        for x in range(400):
            h = (base_hue + rng.randint(0, 50)) % 360
            s = rng.uniform(0.35, 0.9)
            v = rng.uniform(0.4, 1.0)
            px[x, y] = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h / 360, s, v))
    img = small.resize(IMAGE_SIZE, Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY)
    return buf.getvalue()


class Command(BaseCommand):
    help = "Seed 1000 ~1 MB load-test images and 40 news posts."

    def handle(self, *args, **options):
        StressImage.objects.all().delete()
        NewsPost.objects.all().delete()

        STATIC_LOADTEST.mkdir(parents=True, exist_ok=True)

        images = []
        for i in range(1, IMAGES + 1):
            category_index = (i - 1) % len(CATEGORIES)
            category = CATEGORIES[category_index]
            filename = f"img_{i:06d}.jpg"
            (STATIC_LOADTEST / filename).write_bytes(make_image(category_index, i))
            images.append(
                StressImage(
                    title=f"{LABELS[category]} image {i}",
                    category=category,
                    image_path=f"home/loadtest/{filename}",
                )
            )
        StressImage.objects.bulk_create(images, batch_size=500)

        posts = []
        for i in range(1, NEWS + 1):
            a = NEWS_WORDS[i % len(NEWS_WORDS)]
            b = NEWS_WORDS[(i * 3) % len(NEWS_WORDS)]
            posts.append(
                NewsPost(
                    title=f"{a} {b} — story {i}",
                    body=(
                        f"This is synthetic news item {i} used to load-test the page. "
                        f"It belongs to the {a} and {b} beat. " * 12
                    ),
                )
            )
        NewsPost.objects.bulk_create(posts, batch_size=200)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {IMAGES} images (~1 MB each) and {NEWS} news posts ({STATIC_LOADTEST})."
            )
        )
