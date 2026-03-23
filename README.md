# 🎯 AI Virtual Try-On System

An interactive AI-powered virtual try-on experience built on Google Colab, using Stable Diffusion and ControlNet models from Hugging Face. Upload a person image and a clothing image — the system generates a realistic preview of the person wearing that clothing.

---

## ✨ Features

- **Stable Diffusion Inpainting** — Seamlessly integrates clothing onto a person's image using advanced inpainting techniques.
- **ControlNet Integration** — Provides precise control over pose and clothing placement for more accurate results.
- **Gradio Interface** — Clean, user-friendly web UI accessible directly from the Colab notebook.
- **Hugging Face Models** — Leverages powerful pre-trained models for high-quality, realistic outputs.

---

## 🚀 Getting Started

### 1. Run the Notebook

Open the notebook in Google Colab and execute all code cells in order from top to bottom.

### 2. Access the App

Once the final cell finishes running, a public Gradio URL will appear in the output. Click it to open the virtual try-on interface in your browser.

### 3. Upload Images

- **Person Image** — Upload a clear photo of a person.
- **Clothing Image** — Upload the garment you want to try on.

### 4. Adjust Settings *(Optional)*

Under **Advanced Settings**, you can tune:

| Setting | Description |
|---|---|
| `Prompt` | Text to guide the AI generation style |
| `Strength` | Controls how strongly the new clothing is applied (0.0–1.0) |

### 5. Generate

Click **✨ Generate Try-On** and wait for the result to appear.

---

## 🎯 Tips for Best Results

- **Use high-quality images** — Clear, high-resolution photos produce significantly better outputs.
- **Ensure good lighting** — Consistent, well-lit images in both inputs improve blending quality.
- **Front-facing poses** — The model performs best with the subject facing forward or at a slight angle.
- **Simple backgrounds** — Images with plain or uncluttered backgrounds tend to yield cleaner results.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Image Generation | Stable Diffusion Inpainting |
| Pose & Placement Control | ControlNet |
| Model Hosting | Hugging Face |
| UI | Gradio |
| Runtime | Google Colab |

---

## 📋 Requirements

All dependencies are installed automatically when you run the notebook cells. No manual setup is needed beyond opening the notebook in Google Colab.

---

## ⚠️ Known Limitations

- Complex patterns or textures on clothing may not transfer perfectly.
- Non-standard poses (side profile, seated, etc.) may produce less accurate results.
- Generation quality is influenced by the resolution and clarity of the input images.

---

## 📄 License

This project uses models and libraries subject to their respective licenses on Hugging Face. Refer to each model's license page before any commercial use.