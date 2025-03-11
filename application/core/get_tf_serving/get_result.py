import grpc
import numpy as np
from tensorflow_serving.apis import prediction_service_pb2_grpc

from core.config import settings
from core.get_tf_serving.builder_request import get_predict_request
from core.get_tf_serving.preprocessing_texts import preprocess_text_fraud_detection, preprocess_text_fraud_mbti
from core.get_tf_serving.tokenizer import get_tokenizer
from fastapi import HTTPException

tokenizer_mbti = get_tokenizer(settings.neural_tf.mbti_neural.path_tokenizer_mbti)
tokenizer_fraud_detection = get_tokenizer(settings.neural_tf.fraud_detection_neural.path_tokenizer_fraud_detection)


def get_response(request, timeout=5):
    url = f"{settings.neural_tf.host}:{settings.neural_tf.port}"
    channel = grpc.insecure_channel(url)
    predict_service = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    try:
        response = predict_service.Predict(request, timeout=timeout)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            # Специфическая обработка DEADLINE_EXCEEDED
            print(f"Debug info: {e.debug_error_string()}")
            raise HTTPException(status_code=504, detail="Deadline Exceeded: The operation took too long.")
        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            print("Debug info:", e.debug_error_string())
            raise HTTPException(status_code=503, detail="Service Unavailable: The service is temporarily unavailable.")
        else:
            # Обработка других типов ошибок
            print(f"gRPC Error: {e.code()}")
        raise  # Повторное выбрасывание ошибки, если потребуется обработать выше
    response_output_name = list(dict(response.outputs).keys())[0]  # выходы
    return response, response_output_name


def get_result_mbti(texts: list):
    processed_texts = preprocess_text_fraud_mbti(texts)
    tokenized_texts = tokenizer_mbti.to_data_for_model(processed_texts)
    request = get_predict_request(tokenized_texts,
                                  settings.neural_tf.mbti_neural.name_model,
                                  settings.neural_tf.mbti_neural.signature_name,
                                  settings.neural_tf.mbti_neural.input_name,)
    setting_timeout = settings.neural_tf.mbti_neural.timeout
    response, output_name = get_response(request, setting_timeout)
    output_proto = response.outputs[output_name]
    y_proba = np.array(output_proto.float_val).round(4)
    y_proba = y_proba.reshape(-1, 4)  # 4 классификаций MBTI (буквы)
    return y_proba


def get_result_fraud_detection(texts: list):
    processed_texts = []
    for text in texts:
        processed_texts.append(preprocess_text_fraud_detection(text))
    tokenized_texts = tokenizer_fraud_detection.to_data_for_model(processed_texts)
    request = get_predict_request(tokenized_texts,
                                  settings.neural_tf.fraud_detection_neural.name_model,
                                  settings.neural_tf.fraud_detection_neural.signature_name,
                                  settings.neural_tf.fraud_detection_neural.input_name,)
    setting_timeout = settings.neural_tf.fraud_detection_neural.timeout
    response, output_name = get_response(request, setting_timeout)
    output_proto = response.outputs[output_name]
    y_proba = np.array(output_proto.float_val).round(4)
    return y_proba
