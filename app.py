from flask import Flask, render_template, request
import asyncio
from playwright.async_api import async_playwright
import string

app = Flask(__name__)

# Generate username berdasarkan kata dasar + 1 huruf
def generate_usernames_plus_one(base="jaemin"):
    alphabet = string.ascii_lowercase
    results = set()

    for c in alphabet:
        results.add(c + base)
        results.add(base + c)
    for i in range(1, len(base)):
        for c in alphabet:
            results.add(base[:i] + c + base[i:])
    return sorted(results)

# Cek username dengan Playwright
async def check_username(username, page):
    try:
        await page.goto(f"https://twitter.com/{username}", timeout=8000)
        content = await page.content()
        if "This account doesn’t exist" in content:
            return username, True
    except:
        pass
    return username, False

# Async pengecekan semua
async def check_usernames(usernames):
    available = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for uname in usernames:
            uname, status = await check_username(uname, page)
            if status:
                available.append(uname)
        await browser.close()
    return available

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        base = request.form.get("base_username", "jaemin").strip().lower()
        generated = generate_usernames_plus_one(base)
        available = asyncio.run(check_usernames(generated))
        return render_template("index.html", available=available, base=base)
    return render_template("index.html", available=None)

if __name__ == "__main__":
    app.run(debug=True)
