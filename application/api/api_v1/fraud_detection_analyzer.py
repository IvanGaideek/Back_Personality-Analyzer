from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.get_tf_serving.get_result import get_result_fraud_detection
from core.get_tf_serving.production_result import convert_to_prod_res_fraud_detection
from core.models import db_helper
from core.schemas.tf_analyzers import RequestDataFraudDetect, ResponseDataFraudDetect
from core.schemas.user import User
from crud import users as users_crud


router_fraud_detection = APIRouter(tags=["fraud_detection"])


@router_fraud_detection.post("/fraud_detection_analyzer", response_model=ResponseDataFraudDetect)
async def submit_data(
        # session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request_data: RequestDataFraudDetect,
        current_user: Annotated[User, Depends(users_crud.get_current_user)],
):
    writing_database = False  # Переменная для отслеживания успешности записи
    try:
        # Получение данных пользователя
        user_id = current_user.id
        text = request_data.text
        person = request_data.person
        loading_database = request_data.loading_database

        analysis = get_result_fraud_detection([text])
        analysis = convert_to_prod_res_fraud_detection(analysis)
        # Логика обработки запроса
        # Например, можно сохранять данные в указанной таблице

        return {
            "analysis": analysis,
            "person": person,
            "writingDatabase": writing_database
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please contact us if the problem still occurs."
        )