"""Практична робота: об'єктно-орієнтоване програмування в Python.

Запуск: python main.py
Зовнішні залежності не потрібні.
"""

from abc import ABC, abstractmethod


def section(title: str) -> None:
    print(f"\n{'=' * 76}\n{title}\n{'=' * 76}")


# Завдання 1. Наслідування і поліморфізм.
class Vehicle:
    """Базовий клас транспортного засобу."""

    def __init__(self, manufacturer: str, model: str) -> None:
        if not manufacturer.strip() or not model.strip():
            raise ValueError("Виробник і модель не можуть бути порожніми.")
        self.manufacturer = manufacturer
        self.model = model

    def travel(self) -> str:
        return f"{self.manufacturer} {self.model} рухається дорогою."

    def __str__(self) -> str:
        return f"{self.manufacturer} {self.model}"

    def __repr__(self) -> str:
        return f"Vehicle(manufacturer={self.manufacturer!r}, model={self.model!r})"


class ElectricCar(Vehicle):
    def __init__(self, manufacturer: str, model: str, range_km: int) -> None:
        super().__init__(manufacturer, model)
        if range_km <= 0:
            raise ValueError("Запас ходу має бути додатним.")
        self.range_km = range_km

    def travel(self) -> str:
        return f"Електромобіль {self} їде без викидів; запас ходу {self.range_km} км."

    def __repr__(self) -> str:
        return f"ElectricCar(manufacturer={self.manufacturer!r}, model={self.model!r}, range_km={self.range_km!r})"


class DeliveryTruck(Vehicle):
    def __init__(self, manufacturer: str, model: str, payload_kg: int) -> None:
        super().__init__(manufacturer, model)
        if payload_kg <= 0:
            raise ValueError("Вантажність має бути додатною.")
        self.payload_kg = payload_kg

    def travel(self) -> str:
        return f"Вантажівка {self} перевозить до {self.payload_kg} кг вантажу."

    def __repr__(self) -> str:
        return f"DeliveryTruck(manufacturer={self.manufacturer!r}, model={self.model!r}, payload_kg={self.payload_kg!r})"


class Bicycle(Vehicle):
    def __init__(self, manufacturer: str, model: str, gears: int) -> None:
        super().__init__(manufacturer, model)
        if gears < 1:
            raise ValueError("Кількість передач має бути не меншою за 1.")
        self.gears = gears

    def travel(self) -> str:
        return f"Велосипед {self} їде за рахунок педалювання; передач: {self.gears}."

    def __repr__(self) -> str:
        return f"Bicycle(manufacturer={self.manufacturer!r}, model={self.model!r}, gears={self.gears!r})"


def task_1() -> None:
    section("ЗАВДАННЯ 1. ІЄРАРХІЯ ТРАНСПОРТНИХ ЗАСОБІВ")
    vehicles: list[Vehicle] = [
        ElectricCar("Nissan", "Leaf", 270),
        DeliveryTruck("MAN", "TGL", 3500),
        Bicycle("Trek", "FX 2", 18),
    ]
    for vehicle in vehicles:
        print(vehicle.travel())
    print(f"repr(vehicles[0]): {vehicles[0]!r}")
    print(f"isinstance(vehicles[0], Vehicle): {isinstance(vehicles[0], Vehicle)}")
    print(f"issubclass(ElectricCar, Vehicle): {issubclass(ElectricCar, Vehicle)}")
    print(f"issubclass(Bicycle, DeliveryTruck): {issubclass(Bicycle, DeliveryTruck)}")
    print("Схема: Vehicle -> ElectricCar, DeliveryTruck, Bicycle")


# Завдання 2. Інкапсуляція та властивості.
class TemperatureSensor:
    MIN_C = -50.0
    MAX_C = 150.0

    def __init__(self, sensor_id: str, temperature_c: float) -> None:
        if not sensor_id.strip():
            raise ValueError("Ідентифікатор датчика не може бути порожнім.")
        self._sensor_id = sensor_id
        self.__temperature_c = 0.0
        self.temperature_c = temperature_c

    @property
    def temperature_c(self) -> float:
        return self.__temperature_c

    @temperature_c.setter
    def temperature_c(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Температура має бути числом, а не bool або рядком.")
        if not self.MIN_C <= value <= self.MAX_C:
            raise ValueError(f"Температура має бути в межах {self.MIN_C}..{self.MAX_C} °C.")
        self.__temperature_c = float(value)

    @property
    def temperature_f(self) -> float:
        return self.temperature_c * 9 / 5 + 32

    def __str__(self) -> str:
        return f"Датчик {self._sensor_id}: {self.temperature_c:.1f} °C"


def task_2() -> None:
    section("ЗАВДАННЯ 2. ІНКАПСУЛЯЦІЯ ДАТЧИКА")
    sensor = TemperatureSensor("T-17", 21.5)
    print(sensor)
    print(f"Обчислювана температура у Фаренгейтах: {sensor.temperature_f:.1f} °F")
    sensor.temperature_c = 24
    print(f"Після зміни базового значення: {sensor.temperature_f:.1f} °F")
    for bad_value in ("гаряче", 200):
        try:
            sensor.temperature_c = bad_value  # type: ignore[assignment]
        except (TypeError, ValueError) as error:
            print(f"Відхилено {bad_value!r}: {type(error).__name__}: {error}")
    try:
        print(sensor.__temperature_c)  # type: ignore[attr-defined]
    except AttributeError:
        print("Прямий доступ sensor.__temperature_c: AttributeError")
    print(f"Доступ через name mangling: {sensor._TemperatureSensor__temperature_c:.1f} °C")
    print(f"Захищена конвенція _sensor_id доступна за домовленістю: {sensor._sensor_id}")


# Завдання 3. Магічні методи для вектора.
class Vector2D:
    def __init__(self, x: float, y: float) -> None:
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Координати вектора мають бути числами.")
        self.x = float(x)
        self.y = float(y)

    def __str__(self) -> str:
        return f"({self.x:g}, {self.y:g})"

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x!r}, y={self.y!r})"

    def __add__(self, other: object) -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: object) -> "Vector2D":
        if isinstance(scalar, bool) or not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: object) -> "Vector2D":
        return self * scalar

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return abs(self) < abs(other)

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> float:
        return (self.x, self.y)[index]

    def __abs__(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5


def task_3() -> None:
    section("ЗАВДАННЯ 3. МАГІЧНІ МЕТОДИ VECTOR2D")
    first = Vector2D(3, 4)
    second = Vector2D(1, 2)
    print(f"str(first): {str(first)}")
    print(f"repr(first): {repr(first)}")
    print(f"first + second: {first + second}")
    print(f"first - second: {first - second}")
    print(f"first * 2: {first * 2}")
    print(f"2 * second: {2 * second}")
    print(f"first == second: {first == second}")
    print(f"second < first (за довжиною): {second < first}")
    print(f"len(first): {len(first)}")
    print(f"first[0], first[-1]: {first[0]}, {first[-1]}")
    print(f"abs(first): {abs(first):.1f}")


# Завдання 4. Абстракція та композиція у системі платежів.
class PaymentProcessor(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Назва провайдера платежу."""

    @abstractmethod
    def authorize(self, amount: float) -> str:
        """Авторизує суму та повертає ідентифікатор."""

    @abstractmethod
    def capture(self, authorization_id: str) -> str:
        """Підтверджує списання за авторизацією."""

    def process(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Сума платежу має бути додатною.")
        authorization_id = self.authorize(amount)
        return self.capture(authorization_id)


class CardProcessor(PaymentProcessor):
    @property
    def provider_name(self) -> str:
        return "Банківська картка"

    def authorize(self, amount: float) -> str:
        return f"CARD-{amount:.2f}"

    def capture(self, authorization_id: str) -> str:
        return f"Оплату {authorization_id} підтверджено карткою."


class WalletProcessor(PaymentProcessor):
    @property
    def provider_name(self) -> str:
        return "Електронний гаманець"

    def authorize(self, amount: float) -> str:
        return f"WALLET-{amount:.2f}"

    def capture(self, authorization_id: str) -> str:
        return f"Оплату {authorization_id} підтверджено гаманцем."


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[str] = []

    def record(self, message: str) -> None:
        self.entries.append(message)
        print(f"[аудит] {message}")


class PaymentService:
    """Має процесор і журнал; делегує їм операції."""

    def __init__(self, processor: PaymentProcessor, audit_log: AuditLog) -> None:
        self.processor = processor
        self.audit_log = audit_log

    def pay(self, amount: float) -> str:
        result = self.processor.process(amount)
        self.audit_log.record(f"{self.processor.provider_name}: {amount:.2f} грн")
        return result


def task_4() -> None:
    section("ЗАВДАННЯ 4. АБСТРАКТНИЙ ПРОЦЕСОР І КОМПОЗИЦІЯ")
    try:
        PaymentProcessor()  # type: ignore[abstract]
    except TypeError as error:
        print(f"PaymentProcessor не створюється: {type(error).__name__}")

    services = [
        PaymentService(CardProcessor(), AuditLog()),
        PaymentService(WalletProcessor(), AuditLog()),
    ]
    for service in services:
        print(f"{service.processor.provider_name}: {service.pay(125.50)}")
    print("PaymentService має PaymentProcessor і AuditLog та делегує їм роботу.")


# Завдання 5. Adapter для інтеграції застарілих каналів сповіщень.
class NotificationChannel:
    """Цільовий інтерфейс, очікуваний клієнтом."""

    def send(self, recipient: str, message: str) -> str:
        raise NotImplementedError("Підклас має реалізувати send().")


class LegacySmsGateway:
    def send_sms(self, phone_number: str, body: str) -> str:
        return f"SMS на {phone_number}: {body}"


class SmsAdapter(NotificationChannel):
    def __init__(self, gateway: LegacySmsGateway) -> None:
        self.gateway = gateway

    def send(self, recipient: str, message: str) -> str:
        return self.gateway.send_sms(phone_number=recipient, body=message)


class LegacyPushGateway:
    def publish(self, device_token: str, title: str, content: str) -> str:
        return f"Push на {device_token}: [{title}] {content}"


class PushAdapter(NotificationChannel):
    def __init__(self, gateway: LegacyPushGateway) -> None:
        self.gateway = gateway

    def send(self, recipient: str, message: str) -> str:
        title, separator, content = message.partition(":")
        if not separator:
            title, content = "Сповіщення", message
        return self.gateway.publish(device_token=recipient, title=title.strip(), content=content.strip())


class NotificationService:
    """Клієнт працює лише з цільовим інтерфейсом NotificationChannel."""

    def notify(self, channel: NotificationChannel, recipient: str, message: str) -> str:
        return channel.send(recipient, message)


def task_5() -> None:
    section("ЗАВДАННЯ 5. ADAPTER ДЛЯ КАНАЛІВ СПОВІЩЕННЯ")
    service = NotificationService()
    sms_channel = SmsAdapter(LegacySmsGateway())
    print(service.notify(sms_channel, "+380501112233", "Книгу потрібно повернути завтра."))

    # Розширення: нові gateway та adapter додаються без зміни NotificationService.
    push_channel = PushAdapter(LegacyPushGateway())
    print(service.notify(push_channel, "device-42", "Нове замовлення: готове до видачі."))
    print("NotificationService не змінювався: обидва адаптери мають інтерфейс send().")


def main() -> None:
    print("ПРАКТИЧНА РОБОТА: ОБ'ЄКТНО-ОРІЄНТОВАНЕ ПРОГРАМУВАННЯ")
    task_1()
    task_2()
    task_3()
    task_4()
    task_5()


if __name__ == "__main__":
    main()
