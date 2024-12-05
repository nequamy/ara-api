
# ARA API

---

![badge](https://img.shields.io/badge/Language-Python-green) ![badge](https://img.shields.io/badge/ARA_API-Software-blue) ![badge](https://img.shields.io/badge/Beta-v0.8.0-white)

**Applied Robotics Avia API** — это современный API для управления линейкой дронов и самолетов компании **Applied Robotics Avia**, а также для работы с симулятором **AgroTechSim**.


--- 
## 📖 Описание 

Данный проект предлагает единый интерфейс для управления, анализа и автоматизации полетов. **ara-api** сочетает простоту использования, высокую производительность и поддержку множества языков программирования. 

### Основные особенности: 
1. Экранирование работы от конечного пользователя. 
2. Интегрированная документация, загружаемая вместе с API. 
3. Высокая скорость работы благодаря использованию HTTP/2 и gRPC. 
4. Простота запуска и настройки. 
5. Поддержка анализаторов для выполнения лабораторных работ. 
6. Предохранительные меры для безопасности автономных полетов. 

--- 
## 🌟 Возможности 

- **Мульти-языковая поддержка**: Автономное управление доступно на следующих языках: C#/.NET, C++, Dart, Go, Java, Kotlin, Node.js, Objective-C, PHP, Python, Ruby. 
- **Встроенная документация**: будет доступна с версии `v0.9.0`. 
- **Интегрированное WEB-приложение**: будет доступно с версии `v1.0-alpha`. 
- **Протокол gRPC**: используется как внутри приложения, так и для внешнего взаимодействия. 
- **Данные с полетного контроллера**: чтение одометрии, ориентации, IMU, оптического потока и дальномера (v0.8.0-beta)
- **Поддержка AgroTechSim**: будет доступно в версии `v1.0-alpha`
- **Поддержка дронов Applied Robotics Avia**: в версии `v0.8.0-beta` доступна поддержка только для ARA MINI, поддержка остальных дронов будет добавлена в версии `v1.0-alpha`

--- 
## 🛠️ Описание версии v0.8.0 

- Нативная поддержка Python. 
- Увеличена частота обмена данными до 100 Гц (ранее — 10 Гц в `v0.5.0`). 
- Добавлена поддержка встроенной документации. 
- Добавлены PID-регуляторы с Windup и FeedForward. 
- Возможность вывода графиков работы PID-регуляторов. 
- Базовая поддержка Web-приложения.
- Система логирования данных и ошибок приложения.
--- 
## 🚀 Настройка проекта 

**ARA API** использует **Poetry** для управления зависимостями и сборки проекта. Следуйте инструкциям для установки: 

### 1. Установите pipx: 
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
source ~/.bashrc
```
### 2. Установите Poetry
```bash
pipx install poetry
```
### 3. Склонируйте репозиторий
```bash
git clone https://github.com/nequamy/ara-api.git
```
### 4. Инициализация проекта:
```
cd ara-api
poetry shell
poetry install
```
## 📚 Использование
---
### Терминал

1) Непосредственный запуск API:
```bash
foo@bar:~/ara-api/$ poetry run api
```
2) Запуск только документации: 
```bash
foo@bar:~/ara-api/$ poetry run docs
```
3) Запуск примера:
```
foo@bar:~/ara-api/$ cd examples
foo@bar:~/ara-api/$ python3 move_by_point(square).py
```
\
***⚠️Важно!!! Перед началом использования удостоверьтесь, что ваш дрон обновлен до самой актуальной версии***
## 🧩Функции
---
### `takeoff(self, altitude)` 
Вызывает сервис взлёта через `NavigationManagerGRPC`. 
- **Параметры:** 
	- `altitude` (float): Высота, на которую нужно подняться. 
- **Возвращает:** 
	- `str`: Статус операции взлёта. 
--- 
### `land(self)` 
Вызывает сервис посадки через `NavigationManagerGRPC`. 
- **Возвращает:** 
	- `str`: Статус операции посадки. 
--- 
### `move_by_point(self, x, y)` 
Вызывает сервис перемещения через `NavigationManagerGRPC`. 
- **Параметры:**
	- `x` (float): Координата X точки, в которую нужно переместиться. 
	- `y` (float): Координата Y точки, в которую нужно переместиться. 
- **Возвращает:** 
	- `str`: Статус операции перемещения. 
--- 
### `get_imu_data(self)` 
Получает данные IMU (инерциального измерительного устройства) от сервиса драйвера. 
- **Возвращает:** 
	- `dict`: Словарь с данными гироскопа и акселерометра. 
--- 
### `get_sonar_data(self)` 
Получает данные сонаров от сервиса драйвера. 
- **Возвращает:** 
	- `dict`: Словарь с данными о расстоянии, измеренном сонаром. 
--- 
### `get_attitude_data(self)` 
Получает данные ориентации от сервиса драйвера. 
- **Возвращает:** 
	- `dict`: Словарь с данными об углах ориентации. 
--- 
### `get_odometry_data(self)` 
Получает данные одометрии от сервиса драйвера. 
- **Возвращает:** 
	- `dict`: Словарь с данными о положении и скорости. 
--- 
### `get_optical_flow_data(self)`
Получает данные оптического потока от сервиса драйвера. 
- **Возвращает:** 
	- `dict`: Словарь с данными об оптическом потоке.
