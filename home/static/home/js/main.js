// ---------- Live clock ----------
function updateClock() {
    const clock = document.getElementById("clock");
    if (!clock) return;
    clock.textContent = new Date().toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });
}
updateClock();
setInterval(updateClock, 1000);

// ---------- Theme toggle (with localStorage) ----------
const toggle = document.getElementById("theme-toggle");
function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    if (toggle) toggle.textContent = theme === "dark" ? "☀️" : "🌙";
}
applyTheme(localStorage.getItem("theme") || "light");
if (toggle) {
    toggle.addEventListener("click", () => {
        const next =
            document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        localStorage.setItem("theme", next);
        applyTheme(next);
    });
}

// ---------- Animated counters ----------
function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const suffix = el.textContent.replace(/[\d.,]/g, "");
    const duration = 1200;
    const start = performance.now();

    function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = (target * eased).toFixed(decimals);
        el.textContent = Number(value).toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals,
        }) + suffix;
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

const counterObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.5 }
);

document.querySelectorAll(".stat-value").forEach((el) => counterObserver.observe(el));

// ---------- Footer year ----------
const yearSpan = document.getElementById("year");
if (yearSpan) yearSpan.textContent = new Date().getFullYear();
