from django.shortcuts import render


def home(request):
    context = {
        "page_title": "Welcome — Django Demo",
        "features": [
            {
                "icon": "⚡",
                "title": "Fast by design",
                "text": "Django handles the heavy lifting, so you can ship ideas quickly.",
            },
            {
                "icon": "🔒",
                "title": "Secure by default",
                "text": "Built-in protections against common web vulnerabilities come out of the box.",
            },
            {
                "icon": "🧩",
                "title": "Batteries included",
                "text": "Admin, ORM, auth, and more — everything you need to get going.",
            },
        ],
        "stats": [
            {"label": "Uptime", "value": 99.9, "suffix": "%", "decimals": 1},
            {"label": "Happy users", "value": 12000, "suffix": "+", "decimals": 0},
            {"label": "Features", "value": 42, "suffix": "", "decimals": 0},
        ],
    }
    return render(request, "home/index.html", context)
