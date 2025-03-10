from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str = PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class JWTConfig(BaseModel):
    key: SecretStr = SecretStr("")
    algorithm: str = ""
    access_token_expire_minutes: int = 60  # 1 hour
    expire_long_minutes: int = 14400  # 5 days


class MbtiNeural(BaseModel):
    path_tokenizer_mbti: str = "./tokenizer/tokenizer_mbti.pickle"
    name_model: str = 'mbti'
    signature_name: str = 'serving_default'
    input_name: str = 'embedding_2_input'


class FraudDetectionNeural(BaseModel):
    path_tokenizer_fraud_detection: str = "./tokenizer/tokenizer_fraud_detection.pickle"
    name_model: str = 'fraud_detection'
    signature_name: str = 'serving_default'
    input_name: str = 'embedding_input'


class NeuralTfConfig(BaseModel):
    host: str = "localhost"
    port: int = 8500
    mbti_neural: MbtiNeural = MbtiNeural()
    fraud_detection_neural: FraudDetectionNeural = FraudDetectionNeural()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    jwt: JWTConfig = JWTConfig()
    neural_tf: NeuralTfConfig = NeuralTfConfig()


settings = Settings()
