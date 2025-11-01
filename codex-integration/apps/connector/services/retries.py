import asyncio
from functools import wraps
from apps.connector.utils.config import get_settings

def retryable(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		cfg = get_settings().get("retries", {})
		attempts = 0
		delay = cfg.get("backoff_ms", 250) / 1000
		factor = cfg.get("backoff_factor", 2.0)
		max_attempts = cfg.get("max_attempts", 5)
		while True:
			try:
				return await func(*args, **kwargs)
			except Exception as e:
				attempts += 1
				if attempts >= max_attempts:
					raise e
				await asyncio.sleep(delay)
				delay *= factor
	return wrapper
