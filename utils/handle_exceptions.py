
from models.response import ResponseViewModel
from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from configs.throttling import bad_call_limiter


async def not_found_error(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp, 3)
    if not res["call"]:
        response = ResponseViewModel(
            message='bad call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(),status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = ResponseViewModel(
        message='endpoint not found', status=status.HTTP_404_NOT_FOUND)
    return JSONResponse(response.dict(), status_code=status.HTTP_404_NOT_FOUND)


exception_handlers = {404: not_found_error}
