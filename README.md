# Практична робота: об'єктно-орієнтоване програмування в Python

Навчальний проєкт демонструє наслідування й поліморфізм, інкапсуляцію, магічні методи, абстрактні класи з композицією та патерн Adapter.

## Запуск

Потрібен Python 3.10 або новіший. Зовнішні пакети не потрібні.

```bash
python main.py
```

## Структура прикладів

1. **Транспорт:** `Vehicle` — базовий клас; `ElectricCar`, `DeliveryTruck` і `Bicycle` перевизначають `travel()`.
2. **Датчик температури:** `TemperatureSensor` приховує значення в `__temperature_c`, перевіряє зміни через setter і обчислює температуру за Фаренгейтом.
3. **Вектор:** `Vector2D` підтримує арифметику, порівняння, індексування, довжину та модуль через спеціальні методи.
4. **Платежі:** абстракція `PaymentProcessor` має реалізації для картки й електронного гаманця. `PaymentService` складається з процесора й журналу аудиту та делегує їм роботу.
5. **Сповіщення:** `NotificationService` використовує цільовий інтерфейс `NotificationChannel`; адаптери під'єднують несумісні SMS і push шлюзи.

## Діаграми

```text
Vehicle
├── ElectricCar
├── DeliveryTruck
└── Bicycle

PaymentProcessor (abstract)
├── CardProcessor
└── WalletProcessor
PaymentService ──has-a──> PaymentProcessor
               └─has-a──> AuditLog

NotificationService ──uses──> NotificationChannel
                                  ▲
                    ┌─────────────┴─────────────┐
                 SmsAdapter                 PushAdapter
                    │                           │
             LegacySmsGateway          LegacyPushGateway
```

Детальний опис виконання й приклади результатів наведені у [PDF-звіті](report.pdf).
