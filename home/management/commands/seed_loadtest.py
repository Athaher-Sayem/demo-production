"""Create 1000 load-test images (SVG) and 40 news posts.

Run on every deploy (entrypoint.sh) BEFORE collectstatic, so the static images
are collected into STATIC_ROOT automatically.
"""
from pathlib import Path

from django.core.management.base import BaseCommand

from home.models import NewsPost, StressImage

IMAGES = 1000
NEWS = 40
CATEGORIES = ["tech", "sports", "fashion", "food", "travel", "news"]
LABELS = dict(StressImage.CATEGORIES)

STATIC_LOADTEST = Path(__file__).resolve().parent.parent.parent / "static" / "home" / "loadtest"

NEWS_WORDS = [
    "Market", "Server", "Cloud", "Release", "Update", "Security", "Database",
    "Frontend", "Backend", "API", "Deploy", "Scale", "Cache", "Queue",
    "Design", "Review", "Launch", "Feature", "Patch", "Upgrade",
]


def svg_content(index: int, category: str) -> str:
    hue = (index * 47) % 360
    label = LABELS[category]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="hsl({hue},70%,55%)"/>
      <stop offset="100%" stop-color="hsl({(hue + 60) % 360},70%,35%)"/>
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#g)"/>
  <rect x="20" y="20" width="360" height="260" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="4" rx="12"/>
  <text x="200" y="150" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="34" font-weight="bold" fill="#fff">#{index}</text>
  <text x="200" y="185" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="20" fill="rgba(255,255,255,.9)">{label}</text>
</svg>"""


class Command(BaseCommand):
    help = "Seed 1000 load-test images and 40 news posts."

    def handle(self, *args, **options):
        StressImage.objects.all().delete()
        NewsPost.objects.all().delete()

        STATIC_LOADTEST.mkdir(parents=True, exist_ok=True)

        images = []
        for i in range(1, IMAGES + 1):
            category = CATEGORIES[(i - 1) % len(CATEGORIES)]
            filename = f"img_{i:06d}.svg"
            (STATIC_LOADTEST / filename).write_text(svg_content(i, category), encoding="utf-8")
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
                f"Seeded {IMAGES} images and {NEWS} news posts ({STATIC_LOADTEST})."
            )
        )
