from django.core.paginator import Paginator
from django.shortcuts import render

from .models import NewsPost, StressImage

PER_PAGE = 60


def home(request):
    tab = request.GET.get("tab", "all")

    qs = StressImage.objects.all()
    if tab != "all":
        qs = qs.filter(category=tab)

    paginator = Paginator(qs, PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    tabs = [("all", "All")] + list(StressImage.CATEGORIES)

    context = {
        "page_title": "Load Test — Django Demo",
        "tabs": tabs,
        "active_tab": tab,
        "images": page_obj.object_list,
        "page_obj": page_obj,
        "news": NewsPost.objects.all()[:10],
        "stats": [
            {"label": "Images", "value": StressImage.objects.count()},
            {"label": "News posts", "value": NewsPost.objects.count()},
            {"label": "Images per page", "value": PER_PAGE},
        ],
    }
    return render(request, "home/index.html", context)
