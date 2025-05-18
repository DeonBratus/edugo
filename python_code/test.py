import requests
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000"

def measure_time(func):
    """Декоратор для измерения времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\nВремя выполнения {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@measure_time
def test_math_operations():
    """Тест математических операций (+, *, -)"""
    data = [
        {"type": "calc", "op": "+", "var": "x", "left": 2, "rignt": 3},
        {"type": "calc", "op": "*", "var": "y", "left": "x", "rignt": 4},
        {"type": "calc", "op": "-", "var": "z", "left": "y", "rignt": 5},
        {"type": "print", "var": "z"},
    ]
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 200
    results = response.json()
    assert {"var": "z", "value": 15.0} in results  # (2+3)*4 -5 = 15

@measure_time
def test_print_operation():
    """Тест печати переменной"""
    data = [
        {"type": "calc", "op": "+", "var": "a", "left": 10, "rignt": 20},
        {"type": "print", "var": "a"},
    ]
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 200
    assert {"var": "a", "value": 30.0} in response.json()

@measure_time
def test_invalid_operation():
    """Тест неверного типа операции"""
    data = [{"type": "invalid", "var": "x"}]
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert "Invalid Operation" in response.text

@measure_time
def test_empty_request():
    """Тест пустого запроса"""
    response = requests.post(BASE_URL, json=[])
    assert response.status_code == 200
    assert response.json() == []

@measure_time
def test_swagger_docs():
    """Проверка доступности Swagger UI"""
    response = requests.get(f"{BASE_URL}/swagger/doc.json")
    assert response.status_code == 200
    assert "Operation API" in response.text

def make_request(data):
    """Функция для выполнения одного запроса"""
    return requests.post(BASE_URL, json=data)

@measure_time
def test_load_performance():
    """Нагрузочный тест: 100 запросов с 10 параллельными потоками"""
    data = [
        {"type": "calc", "op": "+", "var": "x", "left": 2, "rignt": 3},
        {"type": "print", "var": "x"},
    ]
    
    num_requests = 100
    workers = 10
    
    print(f"\nЗапуск нагрузочного теста: {num_requests} запросов с {workers} потоками")
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        start_time = time.time()
        futures = [executor.submit(make_request, data) for _ in range(num_requests)]
        results = [f.result() for f in futures]
        end_time = time.time()
    
    total_time = end_time - start_time
    rps = num_requests / total_time
    print(f"Общее время: {total_time:.2f} сек")
    print(f"Запросов в секунду: {rps:.2f}")
    
    # Проверяем, что все запросы успешны
    for response in results:
        assert response.status_code == 200
        assert {"var": "x", "value": 5.0} in response.json()

if __name__ == "__main__":
    pytest.main(["-v", __file__])