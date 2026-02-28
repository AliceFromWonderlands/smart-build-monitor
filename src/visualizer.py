# Модуль для визуализации результатов анализа аномалий
# Строит графики через matplotlib и сохраняет в файл

# ============================================================================
#                                  ИМПОРТЫ
# ============================================================================

import matplotlib.pyplot as plt  # Библиотека для построения графиков
import matplotlib.dates as mdates  # Форматирование дат на графиках
from pathlib import Path  # Работа с путями к файлам

# Настройка стиля графиков (чтобы было красиво)
plt.style.use('seaborn-v0_8-whitegrid')


# ============================================================================
#                ФУНКЦИЯ 1: ПОСТРОЕНИЕ И СОХРАНЕНИЕ ГРАФИКА
# ============================================================================

def plot_and_save(df, filepath, device_name="pump_01"):
    """
    Строит график температуры с выделением аномалий и сохраняет в файл.
    
    Параметры:
        df (pd.DataFrame): Таблица с данными и предсказаниями
        filepath (str или Path): Путь для сохранения изображения
        device_name (str): Название устройства для заголовка
    
    Возвращает:
        None
    """
    
    # ------------------------------------------------------------------------
    #                       ШАГ 1: Создаём фигуру и оси
    # ------------------------------------------------------------------------
    # figsize=(14, 7) — размер графика в дюймах (ширина, высота)
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # ------------------------------------------------------------------------
    #                 ШАГ 2: Рисуем основную линию (температура)
    # ------------------------------------------------------------------------
    # alpha=0.7 — прозрачность линии (чтобы было видно точки поверх)
    ax.plot(df['timestamp'], df['temperature'], 
            label='Temperature (°C)', 
            color='blue', 
            linewidth=1.5, 
            alpha=0.7)
    
    # ------------------------------------------------------------------------
    #                 ШАГ 3: Выделяем аномалии красными точками
    # ------------------------------------------------------------------------
    anomalies = df[df['is_anomaly_pred'] == 1]
    
    if len(anomalies) > 0:
        ax.scatter(anomalies['timestamp'], anomalies['temperature'],
                   color='red',
                   label='Detected Anomaly',
                   s=100,  # Размер точек
                   zorder=5,  # Поверх линии
                   edgecolors='darkred',
                   linewidths=1.5)
    
    # ------------------------------------------------------------------------
    #       ШАГ 4: Добавляем пороговые линии (зоны нормы и тревоги)
    # ------------------------------------------------------------------------
    # Зона нормы (среднее ± 3 сигмы)
    temp_mean = df['temperature'].mean()
    temp_std = df['temperature'].std()
    
    # Зелёная зона (норма)
    ax.axhspan(temp_mean - 2*temp_std, temp_mean + 2*temp_std,
               alpha=0.2, color='green', label='Normal Zone')
    
    # Жёлтая зона (предупреждение)
    ax.axhspan(temp_mean + 2*temp_std, temp_mean + 3*temp_std,
               alpha=0.2, color='yellow', label='Warning Zone')
    ax.axhspan(temp_mean - 3*temp_std, temp_mean - 2*temp_std,
               alpha=0.2, color='yellow')
    
    # Красная зона (критично)
    ax.axhline(y=temp_mean + 3*temp_std, color='red', linestyle='--', 
               linewidth=1, alpha=0.5, label='Critical Threshold')
    ax.axhline(y=temp_mean - 3*temp_std, color='red', linestyle='--',
               linewidth=1, alpha=0.5)
    
    # ------------------------------------------------------------------------
    #                      ШАГ 5: Настраиваем оформление
    # ------------------------------------------------------------------------
    # Заголовок с названием устройства
    ax.set_title(f'SmartBuild Monitor: Temperature Anomaly Detection\nDevice: {device_name}',
                 fontsize=14, fontweight='bold')
    
    # Подписи осей
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    
    # Форматирование дат на оси X (чтобы не слипались)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45, ha='right')
    
    # Легенда
    ax.legend(loc='upper left', fontsize=10)
    
    # Сетка
    ax.grid(True, alpha=0.3)
    
    # Автоматическое подгоняем размеры (чтобы подписи не обрезались)
    plt.tight_layout()
    
    # ------------------------------------------------------------------------
    #                    ШАГ 6: Сохраняем и показываем
    # ------------------------------------------------------------------------
    # Создаём папку если нет
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем в файл (dpi=150 — хорошее качество для веба)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"   🖼️  График сохранён в {filepath}")
    
    # Показываем график (в окне)
    plt.show()
    
    # Освобождаем память
    plt.close()


# ============================================================================
#                  ФУНКЦИЯ 2: ГРАФИК ПО ВСЕМ МЕТРИКАМ (3 в 1)
# ============================================================================

def plot_all_metrics(df, filepath, device_name="pump_01"):
    """
    Строит комбинированный график по всем метрикам (температура, вибрация, напряжение).
    
    Параметры:
        df (pd.DataFrame): Таблица с данными
        filepath (str или Path): Путь для сохранения
        device_name (str): Название устройства
    
    Возвращает:
        None
    """
    
    # Создаём 3 подграфика вертикально
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    
    metrics = [
        ('temperature', 'Temperature (°C)', 'blue'),
        ('vibration', 'Vibration (mm/s)', 'green'),
        ('voltage', 'Voltage (V)', 'orange')
    ]
    
    anomalies = df[df['is_anomaly_pred'] == 1]
    
    for idx, (col, label, color) in enumerate(metrics):
        ax = axes[idx]
        
        # Основная линия
        ax.plot(df['timestamp'], df[col], color=color, alpha=0.7, label=label)
        
        # Аномалии
        if len(anomalies) > 0:
            ax.scatter(anomalies['timestamp'], anomalies[col],
                       color='red', s=80, zorder=5, edgecolors='darkred')
        
        # Оформление
        ax.set_ylabel(label)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
    
    # Общий заголовок
    axes[0].set_title(f'SmartBuild Monitor: All Metrics\nDevice: {device_name}',
                      fontsize=14, fontweight='bold')
    
    # Подпись оси X (только на нижнем графике)
    axes[2].set_xlabel('Time')
    
    # Форматирование дат
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Сохраняем
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"   🖼️  Комбинированный график сохранён в {filepath}")
    
    plt.show()
    plt.close()


# ============================================================================
#                            БЛОК ДЛЯ ТЕСТИРОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("🧪 Тестирование visualizer.py...")
    
    # Импорты внутри теста (чтобы файл можно было запустить отдельно)
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from src.data_generator import generate_data, save_to_csv
    from src.anomaly_detector import detect_anomalies
    
    # Генерируем тестовые данные
    df = generate_data(n_points=200, anomaly_ratio=0.1)
    df = detect_anomalies(df)
    
    # Сохраняем промежуточный файл
    save_to_csv(df, "data/test_viz.csv")
    
    # Строим графики
    plot_and_save(df, "data/report_temperature.png")
    plot_all_metrics(df, "data/report_all_metrics.png")
    
    print("\n✅ Тест visualizer.py завершён успешно!")