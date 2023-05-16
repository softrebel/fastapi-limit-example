
from models.response import Response
from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from configs.throttling import bad_call_limiter

from fastapi.exceptions import RequestValidationError


async def not_found_error(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp)
    if not res["call"]:
        response = Response[dict](
            message='bad call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = Response[dict](
        message='endpoint not found', status=status.HTTP_404_NOT_FOUND)
    return JSONResponse(response.dict(), status_code=status.HTTP_404_NOT_FOUND)


async def unproccessable_entity(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp)
    if not res["call"]:
        response = Response[dict](
            message='bad call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    response = Response[dict](
            message='invalid parameter',
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={"detail": exc.errors(), "body": exc.body}
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.dict(),
    )



async def not_auhenticated(request: Request, exc: HTTPException):
    response = Response[dict](
            message="Authentication Error",
            status=status.HTTP_401_UNAUTHORIZED,
            data={"detail": exc.detail},
        )
    return JSONResponse(response.dict())

exception_handlers = {
    404: not_found_error,
    401:not_auhenticated,
    RequestValidationError: unproccessable_entity,
}
