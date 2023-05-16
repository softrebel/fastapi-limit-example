from fastapi import APIRouter,Depends, Request,HTTPException,status
from configs import db
from models import OperationInput, OperationCreating, OperationViewModel, TotalViewModel
from fastapi.encoders import jsonable_encoder
from configs.throttling import call_limiter

router = APIRouter()


@router.get('/sum/', response_model=OperationViewModel)
async def sum_up(request: Request, model: OperationInput = Depends()):
    clientIp = request.client.host
    res = call_limiter(clientIp, 5)
    if not res["call"]:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,      detail={
            "message": "call limit reached",
            "ttl": res["ttl"]
        })
    total = model.a+model.b
    input_operation = OperationCreating(
        first_operand=model.a, second_operand=model.b, total=total)
    new_operation = await db['operation'].insert_one(input_operation.dict())
    created_operation = await db['operation'].find_one({"_id": new_operation.inserted_id})
    return created_operation


@router.get('/history/', response_model=list[OperationViewModel])
async def get_all_operations():
    operations = await db["operation"].find().to_list(1000)
    return operations


@router.get('/total/', response_model=list[TotalViewModel])
async def get_all_sums():
    operations = await db["operation"].find().to_list(1000)
    return operations
