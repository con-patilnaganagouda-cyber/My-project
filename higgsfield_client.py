"""Higgsfield AI API client for image and video generation."""

import os
import time
import httpx
from typing import Optional


BASE_URL = "https://platform.higgsfield.ai"


class HiggsFieldError(Exception):
    pass


class HiggsFieldClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("HF_API_KEY") or os.environ.get("HF_KEY")
        if not self.api_key:
            raise HiggsFieldError(
                "Higgsfield API key not found. Set HF_API_KEY environment variable."
            )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, payload: dict) -> dict:
        with httpx.Client(timeout=60) as client:
            resp = client.post(f"{BASE_URL}{path}", json=payload, headers=self.headers)
        if resp.status_code not in (200, 201, 202):
            raise HiggsFieldError(f"API error {resp.status_code}: {resp.text}")
        return resp.json()

    def _get(self, path: str) -> dict:
        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{BASE_URL}{path}", headers=self.headers)
        if resp.status_code != 200:
            raise HiggsFieldError(f"API error {resp.status_code}: {resp.text}")
        return resp.json()

    # ------------------------------------------------------------------
    # Image generation
    # ------------------------------------------------------------------

    def generate_image(
        self,
        prompt: str,
        model: str = "nano-banana-pro",
        negative_prompt: str = "",
        seed: Optional[int] = None,
        enhance_prompt: bool = True,
        aspect_ratio: str = "1:1",
    ) -> dict:
        payload = {
            "prompt": prompt,
            "model": model,
            "enhance_prompt": enhance_prompt,
            "aspect_ratio": aspect_ratio,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if seed is not None:
            payload["seed"] = seed
        return self._post("/requests", payload)

    # ------------------------------------------------------------------
    # Text-to-video generation
    # ------------------------------------------------------------------

    def generate_video(
        self,
        prompt: str,
        model: str = "seedance-2.0",
        duration: int = 5,
        resolution: str = "1080p",
        seed: Optional[int] = None,
        enhance_prompt: bool = True,
    ) -> dict:
        payload = {
            "prompt": prompt,
            "model": model,
            "duration": duration,
            "resolution": resolution,
            "enhance_prompt": enhance_prompt,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._post("/requests", payload)

    # ------------------------------------------------------------------
    # Image-to-video generation
    # ------------------------------------------------------------------

    def image_to_video(
        self,
        prompt: str,
        image_url: str,
        model: str = "seedance-2.0",
        duration: int = 5,
        camera_fixed: bool = False,
        seed: Optional[int] = None,
        enhance_prompt: bool = True,
    ) -> dict:
        payload = {
            "prompt": prompt,
            "image_url": image_url,
            "model": model,
            "duration": duration,
            "camera_fixed": camera_fixed,
            "enhance_prompt": enhance_prompt,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._post("/requests", payload)

    # ------------------------------------------------------------------
    # Status & results
    # ------------------------------------------------------------------

    def get_status(self, request_id: str) -> dict:
        return self._get(f"/requests/{request_id}/status")

    def get_result(self, request_id: str) -> dict:
        return self._get(f"/requests/{request_id}")

    def cancel(self, request_id: str) -> dict:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{BASE_URL}/requests/{request_id}/cancel", headers=self.headers
            )
        return resp.json()

    def wait_for_completion(
        self,
        request_id: str,
        poll_interval: int = 5,
        timeout: int = 300,
    ) -> dict:
        """Poll until the request completes or times out."""
        elapsed = 0
        while elapsed < timeout:
            result = self.get_status(request_id)
            status = result.get("status", "").lower()
            if status in ("completed", "failed", "nsfw", "cancelled"):
                if status == "completed":
                    return self.get_result(request_id)
                raise HiggsFieldError(f"Generation ended with status: {status}")
            time.sleep(poll_interval)
            elapsed += poll_interval
        raise HiggsFieldError(f"Timed out after {timeout}s waiting for {request_id}")
