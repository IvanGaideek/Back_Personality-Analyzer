from pydantic import BaseModel


class LoadingDatabase(BaseModel):
    selectedTable: str
    personColumn: str
    classColumn: str


class RequestDataMbti(BaseModel):
    text: str
    person: str
    loading_database: LoadingDatabase


class RequestDataFraudDetect(BaseModel):
    text: str
    person: str
    loading_database: LoadingDatabase


class ResponseDataMbti(BaseModel):
    analysis: list[str]
    person: str
    writingDatabase: bool


class ResponseDataFraudDetect(BaseModel):
    analysis: list[bool]  # True if fraud, False if not
    person: str
    writingDatabase: bool
