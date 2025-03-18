from pydantic import BaseModel
from typing import Optional


class LoadingDatabase(BaseModel):
    selectedTable: str
    personColumn: str
    classColumn: str


class RequestDataMbti(BaseModel):
    text: str
    person: str
    loading_database: LoadingDatabase
    writingDatabase: bool


class RequestDataFraudDetect(BaseModel):
    text: str
    person: str
    loading_database: LoadingDatabase
    writingDatabase: bool
    needAnalysisPhone: bool
    writingPhoneColumn: str
    locationPhoneColumn: str
    providerPhoneColumn: str


class ResponseDataMbti(BaseModel):
    analysis: list[str]
    person: str
    writingDatabase: bool


class ResponseDataFraudDetect(BaseModel):
    analysis: list[bool]  # True if fraud, False if not
    person: str
    writingDatabase: bool
    phone: Optional[str]
    writingInfPhoneDatabase: bool
    locationPhone: Optional[str]
    providerPhone: Optional[str]
    messagePhone: Optional[str]
