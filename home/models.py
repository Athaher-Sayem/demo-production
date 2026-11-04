from django.db import models


class StressImage(models.Model):
    CATEGORIES = [
        ("tech", "Tech"),
        ("sports", "Sports"),
        ("fashion", "Fashion"),
        ("food", "Food"),
        ("travel", "Travel"),
        ("news", "News"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    image_path = models.CharField(max_length=200)  # static-relative path, e.g. home/loadtest/img_000001.svg
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class NewsPost(models.Model):
    title = models.CharField(max_length=160)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
