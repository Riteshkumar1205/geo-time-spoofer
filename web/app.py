#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
import subprocess
import os
import logging

app = Flask(__name__)
LOG = logging.getLogger("webapp")
LOG.setLevel(logging.INFO)

def open_chrome_url(url, chrome_path=None, profile=None, headless=False, env=None):
    if not chrome_path:
        for p in (
            "/usr/bin/google-chrome-stable",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
            "/usr/bin/chromium"
        ):
            if os.path.exists(p):
                chrome_path = p
                break
    if not chrome_path:
        raise FileNotFoundError("Chrome/Chromium binary not found. Set CHROME_PATH env var or install a browser.")

    args = [chrome_path]
    if headless:
        args += ["--headless", "--no-sandbox", "--disable-gpu"]
    args += ["--new-window", url]
    if profile:
        args += [f"--profile-directory={profile}"]

    use_env = os.environ.copy()
    if env:
        use_env.update(env)

    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=use_env, close_fds=True)
    LOG.info("Started chrome process pid=%s for url=%s", proc.pid, url)
    return proc

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        alt = request.form.get("alt", "")
        form_url = request.form.get("form_url", "").strip()
        open_in_chrome = request.form.get("open_in_chrome")
        chrome_profile = request.form.get("chrome_profile")
        chrome_headless = bool(request.form.get("chrome_headless"))

        try:
            latf = float(lat)
            lonf = float(lon)
        except Exception:
            return render_template("index.html", error="Invalid latitude or longitude", lat=lat, lon=lon, alt=alt, form_url=form_url)

        # Decide target URL: if a form_url is provided and valid-looking, use it; else default to Google Maps
        target_url = None
        if form_url:
            target_url = form_url
        else:
            zoom = request.form.get("zoom", "18")
            target_url = f"https://www.google.com/maps/@{latf},{lonf},{zoom}z"

        # Attempt to open Chrome on the server if requested (do not crash user request)
        if open_in_chrome:
            try:
                chrome_bin = os.environ.get("CHROME_PATH", None)
                env = {}
                if os.environ.get("DISPLAY"):
                    env["DISPLAY"] = os.environ.get("DISPLAY")
                if os.environ.get("XAUTHORITY"):
                    env["XAUTHORITY"] = os.environ.get("XAUTHORITY")
                open_chrome_url(target_url, chrome_path=chrome_bin, profile=chrome_profile, headless=chrome_headless, env=env)
            except Exception as e:
                LOG.exception("Failed to open Chrome on host: %s", e)

        # Redirect the client (submitter) to the target URL so they see it
        return redirect(target_url)

    return render_template("index.html")
    
if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
