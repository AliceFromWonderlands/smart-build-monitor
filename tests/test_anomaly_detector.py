# tests/test_anomaly_detector.py
# Тесты для модуля anomaly_detector.py

# ============================================================================
#                                  ИМПОРТЫ
# ============================================================================

import sys
from pathlib import Path

# Добавляем корень проекта в путь, чтобы работали импорты из src/
# Это нужно, чтобы тесты могли найти наши модули
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.anomaly_detector import load_data, detect_anomalies, print_results
from src.data_generator import generate_data, save_to_csv

# ============================================================================
#                      ТЕСТ 1: Проверка загрузки данных
# ============================================================================

def test_load_data():
    """Проверяет, что функция load_data корректно читает CSV файл."""
    
    print("🧪 Тест 1: Загрузка данных...")
    
    # Сначала генерируем тестовые данные
    df = generate_data(n_points=50)
    test_path = "data/test_load.csv"
    save_to_csv(df, test_path)
    
    # Загружаем обратно
    df_loaded = load_data(test_path)
    
    # Проверяем, что количество строк совпадает
    assert len(df_loaded) == 50, "❌ Количество строк не совпадает"
    
    # Проверяем, что колонки на месте
    assert 'temperature' in df_loaded.columns, "❌ Нет колонки temperature"
    assert 'timestamp' in df_loaded.columns, "❌ Нет колонки timestamp"
    
    print("   ✅ Тест 1 пройден: загрузка работает корректно")
    return True


# ============================================================================
#                       ТЕСТ 2: Проверка работы модели
# ============================================================================

def test_detect_anomalies():
    """Проверяет, что модель находит аномалии и добавляет колонку."""
    
    print("🧪 Тест 2: Работа модели...")
    
    # Генерируем данные с 20% аномалий (чтобы точно были)
    df = generate_data(n_points=100, anomaly_ratio=0.2)
    
    # Запускаем детектор
    df_analyzed = detect_anomalies(df)
    
    # Проверяем, что появилась новая колонка
    assert 'is_anomaly_pred' in df_analyzed.columns, "❌ Нет колонки is_anomaly_pred"
    
    # Проверяем, что модель что-то нашла
    anomaly_count = df_analyzed['is_anomaly_pred'].sum()
    assert anomaly_count > 0, "❌ Модель не нашла ни одной аномалии"
    
    print(f"   ✅ Тест 2 пройден: найдено {anomaly_count} аномалий")
    return True


# ============================================================================
#                        ТЕСТ 3: Проверка статистики
# ============================================================================

def test_print_results():
    """Проверяет, что функция печати не вызывает ошибок."""
    
    print("🧪 Тест 3: Вывод статистики...")
    
    df = generate_data(n_points=50)
    df = detect_anomalies(df)
    
    # Просто проверяем, что функция не падает с ошибкой
    try:
        print_results(df)
        print("   ✅ Тест 3 пройден: вывод статистики работает")
        return True
    except Exception as e:
        print(f"   ❌ Тест 3 провален: {e}")
        return False


# ============================================================================
#                            ЗАПУСК ВСЕХ ТЕСТОВ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ЗАПУСК ТЕСТОВ: anomaly_detector")
    print("=" * 60)
    
    all_passed = True
    
    # Запускаем тесты по очереди
    all_passed = test_load_data() and all_passed
    all_passed = test_detect_anomalies() and all_passed
    all_passed = test_print_results() and all_passed
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
    print("=" * 60)