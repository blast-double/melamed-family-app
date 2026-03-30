"""
Lightweight Gemini API wrapper using requests.
Replaces google-generativeai SDK (~50 MB with grpcio).
"""

import os
import requests

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


def _get_api_key():
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not set")
    return key


def generate_content(prompt, model="gemini-2.0-flash", response_mime_type=None):
    """
    Generate content from a prompt.
    Replaces: genai.GenerativeModel(model).generate_content(prompt)
    Returns the text response.
    """
    api_key = _get_api_key()
    url = f"{BASE_URL}/models/{model}:generateContent?key={api_key}"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    if response_mime_type:
        body["generationConfig"] = {"responseMimeType": response_mime_type}

    resp = requests.post(url, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    candidates = data.get("candidates", [])
    if not candidates:
        raise ValueError(f"No candidates in Gemini response: {data}")

    return candidates[0]["content"]["parts"][0]["text"]


def embed_content(text, model="models/gemini-embedding-001", task_type="retrieval_query", output_dimensionality=None):
    """
    Generate text embeddings via Gemini API.
    Model: gemini-embedding-001 (native 3072-dim, truncatable via outputDimensionality).
    Returns list of floats.
    """
    api_key = _get_api_key()
    url = f"{BASE_URL}/{model}:embedContent?key={api_key}"

    body = {
        "model": model,
        "content": {"parts": [{"text": text}]},
        "taskType": task_type.upper().replace(" ", "_"),
    }
    if output_dimensionality is not None:
        body["outputDimensionality"] = output_dimensionality

    resp = requests.post(url, json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    return data["embedding"]["values"]
