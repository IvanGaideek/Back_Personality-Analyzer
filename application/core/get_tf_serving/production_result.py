def convert_to_prod_res_mbti(y_tensor) -> list[str]:
    labels_mapping = {
        0: ['E', 'S', 'F', 'P'],  # Если элемент равен 0
        1: ['I', 'N', 'T', 'J']  # Если элемент равен 1
    }
    y_tensor = (y_tensor > 0.5).astype(int)  # Применяем порог 0.5 для бинаризации значений
    result_labels = []

    # Итерация по каждому элементу в массиве
    for row in y_tensor:
        label = ''
        for i, val in enumerate(row):
            label += labels_mapping[val][i]
        result_labels.append(label)
    return result_labels


def convert_to_prod_res_fraud_detection(y_tensor) -> list[int]:
    y_tensor = (y_tensor > 0.5).astype(int)  # Применяем порог 0.5 для бинаризации значений
    return y_tensor
