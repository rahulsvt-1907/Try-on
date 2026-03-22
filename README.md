# Stylish AI — Virtual Fashion Try-On (Python)

An AI-powered virtual clothing try-on application built with **Python** and **Flask**.  
Browse a curated clothing catalog and instantly try on any outfit using the **Try-On Diffusion AI** (via RapidAPI).

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3 |
| AI Integration | [Try-On Diffusion API](https://rapidapi.com/tryondiffusion/api/try-on-diffusion) via `requests` |
| Frontend | Jinja2 templates, Tailwind CSS (CDN), Vanilla JS |
| Environment | `python-dotenv` |

## Project Structure

```
Try-on/
├── app.py              # Main Flask application & API routes
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── db/
│   ├── __init__.py
│   └── pins.py         # Clothing catalog data
├── templates/
│   ├── base.html       # Base layout with navbar & profile modal
│   ├── index.html      # Home page — clothing catalog with filters
│   └── tryon.html      # Virtual try-on page
└── static/
    ├── css/styles.css  # Custom styles (glassmorphism)
    ├── js/main.js      # Home page JS (filters, search)
    ├── js/tryon.js     # Try-on page JS (AI API call)
    └── images/logo.png
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your [RapidAPI key](https://rapidapi.com/tryondiffusion/api/try-on-diffusion):

```
RAPIDAPI_KEY=your_rapidapi_key_here
```

### 3. Run the development server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Features

- 🛍️ **Clothing Catalog** — Pinterest-style grid with 30+ curated outfits
- 🔍 **Filter & Search** — Filter by gender (Male/Female), category, and search by name
- 👤 **Profile Management** — Save your measurements and avatar photo (stored in browser)
- ✨ **AI Virtual Try-On** — Upload or describe both an avatar and a clothing item; the AI generates a realistic composite image
- 🌄 **Background Customisation** — Add an optional background scene description
- ⬇️ **Download & Share** — Save the result or share via the native share API

## AI Integration

The application uses the [Try-On Diffusion API](https://rapidapi.com/tryondiffusion/api/try-on-diffusion) to generate realistic try-on images.

**Parameters accepted:**
- `clothing_image` — Clothing item image (JPEG/PNG/WebP, ≤4MB)
- `avatar_image` — Person/model image (JPEG/PNG/WebP, ≤4MB)
- `clothing_prompt` — Text description of the clothing (e.g. *"red floral dress"*)
- `avatar_prompt` — Text description of the avatar (e.g. *"young woman with long hair"*)
- `background_prompt` — Optional background description
- `avatar_sex` — `"male"` or `"female"` (auto-detected if omitted)
- `seed` — Integer for reproducible results

## Authors

Rahul Srivastava & Hemali Dholariya — UDP066 Fashion Stylish AI
