from pydantic import BaseModel


class LoadingDatabase(BaseModel):
    selectedTable: str
    personColumn: str
    classColumn: str


class RequestData(BaseModel):
    text: str
    person: str
    loading_database: LoadingDatabase
