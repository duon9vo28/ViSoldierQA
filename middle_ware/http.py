import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from starlette.middleware.base import BaseHTTPMiddleware
from my_utils.logger import Logger

LOGGER = Logger(__file__, log_file='http.log')

class LogMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        LOGGER.log.info(
            f"{request.client.host} - {request.method} - {request.url.path} - {response.status_code} - {process_time:.2f}s"
        )
        
        return response