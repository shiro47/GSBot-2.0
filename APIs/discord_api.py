import httpx
from decouple import config
import asyncio

class DiscordAPI():
    def __init__(self) -> None:
        self.headers = {"Authorization": f"Bot {config('TOKEN')}"}
        
    async def get_user_info_by_id(self, discord_id):
        retry_attempts = 3  # Maximum number of retry attempts
        retry_delay = 1  # Initial retry delay in seconds

        async with httpx.AsyncClient() as client:
            for attempt in range(retry_attempts):
                try:
                    response = await client.get(f"https://discord.com/api/users/{discord_id}", headers=self.headers)
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 404:
                        return {"error": "User not found"}
                except (httpx.RequestError, httpx.TimeoutException):
                    pass

                # Retry with exponential backoff
                await asyncio.sleep(retry_delay)
                retry_delay *= 2

        return {"error": "Failed to retrieve user information"}
