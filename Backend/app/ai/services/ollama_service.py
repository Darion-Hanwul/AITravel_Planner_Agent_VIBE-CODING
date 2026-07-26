import json
from typing import AsyncGenerator, Dict, Any, Optional

import httpx

from app.config.settings import settings

class OllamaService:

    def __init__(self) -> None:

        self.base_url = (
            settings.OLLAMA_BASE_URL.rstrip("/")
        )

        self.model = (
            settings.OLLAMA_MODEL
        )

        self.generate_url = (
            f"{self.base_url}/api/generate"
        )

    async def generate(
        self,
        prompt: str,
        num_predict: int = 6789,
        temperature: float = 0.4,
        top_p: float = 0.9,
        num_ctx: int = 8192,
        keep_alive: str = "30m",
        timeout: Optional[float] = 300.0,
    ) -> Dict[str, Any]:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": keep_alive,
            "options": {
                "num_predict": num_predict,
                "temperature": temperature,
                "top_p": top_p,
                "num_ctx": num_ctx,
            },
        }

        timeout_config = httpx.Timeout(
            connect=30.0,
            read=timeout,
            write=60.0,
            pool=60.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout_config
        ) as client:

            response = await client.post(
                self.generate_url,
                json=payload,
            )

            response.raise_for_status()

            return response.json()

    async def generate_stream(
        self,
        prompt: str,
        num_predict: int = 6792,  
        temperature: float = 0.4,
        top_p: float = 0.9,
        num_ctx: int = 8192,     
        keep_alive: str = "30m",
        timeout: Optional[float] = 600.0,
    ) -> AsyncGenerator[str, None]:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "keep_alive": keep_alive,
            "options": {
                "num_predict": num_predict,
                "temperature": temperature,
                "top_p": top_p,
                "num_ctx": num_ctx,
            },
        }

        timeout_config = httpx.Timeout(
            connect=30.0,
            read=timeout,
            write=60.0,
            pool=60.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout_config
        ) as client:

            async with client.stream(
                "POST",
                self.generate_url,
                json=payload,
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():

                    if not line:
                        continue

                    try:

                        data = json.loads(
                            line
                        )

                    except json.JSONDecodeError:

                        continue

                    if data.get(
                        "done",
                        False,
                    ):

                        break

                    chunk = data.get(
                        "response",
                        "",
                    )

                    if chunk:

                        yield chunk