from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.analyze_phone.find_inf_phone import get_information_about_phone
from core.get_tf_serving.get_result import get_result_fraud_detection
from core.get_tf_serving.production_result import convert_to_prod_res_fraud_detection
from core.models import db_helper
from core.schemas.tf_analyzers import RequestDataFraudDetect, ResponseDataFraudDetect
from core.schemas.user import User
from crud import users as users_crud


router_fraud_detection = APIRouter(tags=["fraud_detection"])


@router_fraud_detection.post("/fraud-detection-analyzer", response_model=ResponseDataFraudDetect)
async def submit_data(
        # session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request_data: RequestDataFraudDetect,
        current_user: Annotated[User, Depends(users_crud.get_current_user)],
):
    writing_database = request_data.writingDatabase  # Переменная для отслеживания успешности записи
    flag_number = request_data.needAnalysisPhone
    try:
        # Получение данных пользователя
        user_id = current_user.id
        text = request_data.text
        person = request_data.person
        loading_database = request_data.loading_database

        analysis = get_result_fraud_detection([text])
        analysis = convert_to_prod_res_fraud_detection(analysis)
        # Логика обработки запроса
        # Например, можно сохранять данные в указанной таблице см. writing_database
        response = {
                "analysis": analysis,
                "person": person,
                "writingDatabase": writing_database,
                "phone": None,
                "locationPhone": None,
                "providerPhone": None,
                "messagePhone": None
            }

        if flag_number:
            inf_about_phone: dict = get_information_about_phone(text)
            # Логика обработки запроса БД
            response["phone"] = inf_about_phone['phone']
            response["locationPhone"] = inf_about_phone['country']
            response["providerPhone"] = inf_about_phone['carrier']
            response["messagePhone"] = inf_about_phone['message']
        response["writingInfPhoneDatabase"] = False
        return response
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please contact us if the problem still occurs."
        )