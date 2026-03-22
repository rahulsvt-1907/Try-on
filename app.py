import os
import io
import requests
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from db.pins import pins

load_dotenv()

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_URL = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
RAPIDAPI_HOST = "try-on-diffusion.p.rapidapi.com"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    categories = sorted(set(pin["category"] for pin in pins if pin.get("category")))
    return render_template("index.html", pins=pins, categories=categories)


@app.route("/tryon")
def tryon():
    return render_template("tryon.html")


@app.route("/api/try-on", methods=["POST"])
def try_on():
    clothing_image = request.files.get("clothing_image")
    avatar_image = request.files.get("avatar_image")

    if not clothing_image or not avatar_image:
        return jsonify({"error": "Missing clothing_image or avatar_image"}), 400

    if not allowed_file(clothing_image.filename) or not allowed_file(avatar_image.filename):
        return jsonify({"error": "Images must be JPEG or PNG"}), 400

    clothing_bytes = clothing_image.read()
    avatar_bytes = avatar_image.read()

    if len(clothing_bytes) > MAX_FILE_SIZE or len(avatar_bytes) > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 4MB limit"}), 400

    files = {
        "clothing_image": (clothing_image.filename, io.BytesIO(clothing_bytes), clothing_image.content_type),
        "avatar_image": (avatar_image.filename, io.BytesIO(avatar_bytes), avatar_image.content_type),
    }

    data = {}
    for field in ("clothing_prompt", "avatar_prompt", "background_prompt", "avatar_sex", "seed"):
        value = request.form.get(field, "").strip()
        if value:
            data[field] = value

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    try:
        response = requests.post(RAPIDAPI_URL, headers=headers, files=files, data=data, timeout=60)
    except requests.Timeout:
        return jsonify({"error": "API request timed out"}), 504
    except requests.RequestException as exc:
        return jsonify({"error": f"API request failed: {exc}"}), 502

    if response.status_code == 401:
        return jsonify({"error": "Invalid API key"}), 401
    if response.status_code == 429:
        return jsonify({"error": "API rate limit exceeded"}), 429
    if response.status_code != 200:
        return jsonify({"error": "API request failed"}), response.status_code

    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        return jsonify({"error": "Unexpected response format"}), 500

    return send_file(io.BytesIO(response.content), mimetype=content_type)


@app.route("/api/proxy-image")
def proxy_image():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    from urllib.parse import urlparse
    allowed_hosts = ("i.pinimg.com", "images.unsplash.com")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.netloc not in allowed_hosts:
        return jsonify({"error": "URL not allowed"}), 403

    # Build a safe URL from validated components to prevent SSRF
    safe_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        safe_url += f"?{parsed.query}"

    try:
        response = requests.get(safe_url, timeout=15, stream=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        return jsonify({"error": f"Failed to fetch image: {exc}"}), 502

    content_type = response.headers.get("Content-Type", "image/jpeg")
    return send_file(io.BytesIO(response.content), mimetype=content_type)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
