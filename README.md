# Image to Text API

This repository provides a RESTful API to convert images to text captions using a Flask server. The underlying model is based on the BlipForConditionalGeneration from Hugging Face's Transformers library, which is pre-trained on the Salesforce/blip-image-captioning-base.

## Table of Contents
1. [Requirements](#requirements)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [API Reference](#api-reference)

## Requirements

- Python 3.7+
- Flask
- Pillow (PIL)
- torch
- Transformers
- gunicorn (for production deployment)

You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your_github_username/image-to-text-api.git
cd image-to-text-api
```

2. Run the Flask server with gunicorn (recommended for production):

```bash
gunicorn --bind 0.0.0.0:2000 --workers 10 wsgi:app
```

Or run the Flask server directly (suitable for development and testing):

```bash
python image_to_text_server.py
```

## Usage

To use the API, send a POST request with an image file attached to the `/caption_image` endpoint:

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "image=@your_image.jpg" http://0.0.0.0:2000/caption_image
```

The API will return a JSON object containing the generated caption:

```json
{
  "caption": "a detailed description of the image"
}
```

## API Reference

### POST /caption_image

Generates a caption for the uploaded image.

**Request:**

- Form-data:

| Parameter | Description           | Required | Type   |
|-----------|-----------------------|----------|--------|
| image     | Image file to caption | Yes      | binary |

**Response:**

- JSON:

```json
{
  "caption": "a detailed description of the image"
}
```

**Example:**

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "image=@your_image.jpg" http://0.0.0.0:2000/caption_image
```
