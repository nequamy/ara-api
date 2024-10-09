import numpy as np


def exponential_ramp(min_value, target_value, max_value, num_steps=100):
    """
    Создает массив чисел, плавно увеличивающихся от минимального значения до целевого значения по экспоненциальной кривой,
    но не превышающих максимальное значение.
    
    Args:
    min_value (float): Минимальное значение.
    target_value (float): Целевое значение.
    max_value (float): Максимальное значение.
    num_steps (int): Количество шагов для вычисления массива.
    
    Returns:
    numpy.ndarray: Массив значений.
    """
    # Убеждаемся, что целевое значение не превышает максимальное
    target_value = min(target_value, max_value)
    
    # Вычисляем экспоненциальный коэффициент
    k = np.log(target_value / min_value) / (num_steps - 1)
    
    # Создаем массив значений
    values = min_value * np.exp(k * np.arange(num_steps))
    
    # Ограничиваем значения максимальным значением
    values = np.int32(np.minimum(values, max_value))
    
    return values

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

min_value = 1000
target_value = 1700
max_value = 2000
values = exponential_ramp(min_value, target_value, max_value)

print(remap(2, 0, 3, 1000, 2000))
