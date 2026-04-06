import httpx
import asyncio
from backend.config import API_TIMEOUT

async def async_get(url, headers=None):
    """Asynchronously send a GET request."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response

async def async_post(url, json=None, headers=None):
    """Asynchronously send a POST request."""
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=headers, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response
