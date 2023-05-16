from fastapi import APIRouter,Depends, Request,HTTPException,status
from configs import db
from models import OperationInput, OperationCreating, OperationViewModel, TotalViewModel,User
from fastapi.encoders import jsonable_encoder
from configs.throttling import call_limiter
from models.response import Response
from fastapi.responses import JSONResponse
from .auth_endpoints import get_current_active_user
from typing_extensions import Annotated
router = APIRouter()


@router.get('/sum/',response_model=Response)
async def sum_up(request: Request, model: OperationInput = Depends()):
    clientIp = request.client.host
    res = call_limiter(clientIp)
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


@router.get('/history/', response_model=Response[list[OperationViewModel]])
async def get_all_operations(current_user: Annotated[User, Depends(get_current_active_user)]):
    operations = await db["operation"].find().to_list(1000)
    return Response[list[OperationViewModel]](data=operations,message='ok',status=status.HTTP_200_OK)


@router.get('/total/', response_model=Response[list[TotalViewModel]])
async def get_all_sums(current_user: Annotated[User, Depends(get_current_active_user)]):
    operations = await db["operation"].find().to_list(1000)
    return Response[list[TotalViewModel]](data=operations,message='ok',status=status.HTTP_200_OK)
