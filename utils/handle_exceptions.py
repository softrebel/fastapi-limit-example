
from models.response import ResponseViewModel
from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from configs.throttling import bad_call_limiter

from fastapi.exceptions import RequestValidationError

async def not_found_error(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp, 3)
    if not res["call"]:
        response = ResponseViewModel(
            message='bad call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = ResponseViewModel(
        message='endpoint not found', status=status.HTTP_404_NOT_FOUND)
    return JSONResponse(response.dict(), status_code=status.HTTP_404_NOT_FOUND)


async def unproccessable_entity(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp, 3)
    if not res["call"]:
        response = ResponseViewModel(
            message='bad call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = ResponseViewModel(
            message='invalid parameter',
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={"detail": exc.errors(), "body": exc.body}
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.dict(),
    )

exception_handlers = {
    404: not_found_error,
    RequestValidationError: unproccessable_entity
}
