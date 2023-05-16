# fastapi-limit-example
FastAPI Limit Example




## Requirements:
- python 3.11
- install dependencies using

```sh
[linux]   pip3 install -r requirements.txt
[windows]  pip install -r requirements.txt
```

- Copy `.env.sample` and rename it to `.env`. Then fill the variables
- Create MongoDb database with name `DorsaDb`
- run command `python -m main` in the root folder.
- redis server. for development you can run docker command:
    `docker run -p 6379:6379 --name redis_service -d redis`


## Run
You can run this project in two ways:

1. Run in development:
    Just run file `main_dev.py` in your IDE to have debugging options.

2. Run in production:
    Execute this command in this directory:
    ```python
    python uvicorn main:app
    ```

Default Swagger Url:
http://127.0.0.1:8000/docs


## Endpoints
there 3 main endpoints:
1. `v1/sum` for sum up a,b from query parameters.

![v1/sum](./assets/sum.jpg)
2. `v1/history` for get all sum requests historiy.

![v1/history](./assets/history.jpg)
3. `v1/total` for get only total from last requests.

![v1/total](./assets/total.jpg)


Example Info:
![endpoints](./assets/call_endpoints.jpg)



## Seeds
there is on seed file in the `seeds` directory. You can edit this file to insert user in `user` collection if not exists.

Default user:

```
    username: admin
    password: admin
```

## Authentication
Use 'v1/auth' and pass username and password to issue token. after the token issued, use that in header key Authorization with prefix `Bearer ` for example:
`Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY4NDI0NzM5Nn0.13ClZz0-KiwylTMQdGkRuF1mm5vFQsdfyVn_7kGPic0`

### Authenticated Endpoints
These endpoints require token(Authorization key in HEADER):

1. `v1/auth/me`: to response detail of user who issued token.
2. `v1/total`: total computed from previous sum requests.
3. `v1/history`: history of previous sum requests.

## Limiter
For limit api calls, I used redis server to keep api call count. Below is the limiter code:
```python
import redis,os
redis_client = redis.Redis(host=os.getenv('REDIS_HOST'))
def limiter(key, limit):
    req = redis_client.incr(key)
    ttl=60
    if req == 1:
        redis_client.expire(key, ttl)
    else:
        ttl = redis_client.ttl(key)
    if req > limit:
        return {
            "call": False,
            "ttl": ttl
        }
    else:
        return {
            "call": True,
            "ttl": ttl
        }

def call_limiter(ip, limit=os.getenv('LIMIT_CALL_PER_HOUR',3)):
    limit=int(limit)
    key=f'call_{ip}'
    return limiter(key, limit)

def bad_call_limiter(ip, limit=os.getenv('LIMIT_BAD_CALL_PER_HOUR',4)):
    limit=int(limit)
    key=f'bad_call_{ip}'
    return limiter(key, limit)
```


In this project, two kind of limits is implemented:
1. call limiter to limit call of specific endpoint. `LIMIT_CALL_PER_HOUR` is the environment variable to specify count of call.
2. bad call limiter to limit call of bad request and not found. `LIMIT_BAD_CALL_PER_HOUR` is the environment variable to specify count of call.

You can change throttle time from `THROTTLE` variable in `.env` file.

### Limit Call Example:

```python
@router.get('/sum/')
async def sum_up(request: Request, model: OperationInput = Depends(),response_model=Response):
    clientIp = request.client.host
    res = call_limiter(clientIp, 5)
    if not res["call"]:
        response = Response[dict](
            message='call limit reached',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
            data={"ttl": res["ttl"]}
        )
        return JSONResponse(response.dict(), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    total = model.a+model.b
    input_operation = OperationCreating(
        first_operand=model.a, second_operand=model.b, total=total)
    new_operation = await db['operation'].insert_one(input_operation.dict())
    created_operation = await db['operation'].find_one({"_id": new_operation.inserted_id})
    item=OperationViewModel(**created_operation)
    return Response[OperationViewModel](data=item,message='ok',status=status.HTTP_200_OK)
```
#### call limit
![limit call](./assets/throttle_endpoint.jpg)

#### call limit response
![limit call info](./assets/call_limit.jpg)

### Limit Bad Call Example:
This limit include two types of user behaviours:
1. Call endpoint that not exists (not found).
2. Call endpoint in wrong way (bad request).

This limit sums up these two behaviours.

```python
async def not_found_error(request: Request, exc: HTTPException):
    clientIp = request.client.host
    res = bad_call_limiter(clientIp, 3)
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
    res = bad_call_limiter(clientIp, 3)
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

exception_handlers = {
    404: not_found_error,
    RequestValidationError: unproccessable_entity
}

```

#### Bad Call Limit
![limit bad call info](./assets/bad_call_info.jpg)

#### Not Found Call Limit
![limit not found call](./assets/not_found_call_info.jpg)

#### Mixed Bad Call Limit
![limit mixed bad call](./assets/mix_call_limit.jpg)


#### bad call limit response
![limit bad call](./assets/bad_call_limit.jpg)



