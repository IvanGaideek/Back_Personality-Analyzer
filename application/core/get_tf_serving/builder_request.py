from tensorflow_serving.apis.predict_pb2 import PredictRequest
from tensorflow import cast, make_tensor_proto, float32


def get_predict_request(data, name_model, signature_name, input_name):
    request = PredictRequest()
    request.model_spec.name = name_model
    request.model_spec.signature_name = signature_name
    input_tensor = cast(data, float32)
    request.inputs[input_name].CopyFrom(make_tensor_proto(input_tensor, shape=input_tensor.shape))
    return request
