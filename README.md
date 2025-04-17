# Бот для финансового учета

#### Данный бот позволяет записывать свои доходы и расходы

### Так же есть возможность:
- смотреть статистику по расходам
- управлять всеми операциями, категориями и тд через админ-панель
- смотреть историю операций
- устанавливать лимиты на определенные категории операций (dont work now :( )

### Стэк: 
- Python 3.11
- Fastapi 0.115
- python-telegram-bot 22.0
- pydantic 2.11.1
- alembic 1.15.2
- sqladmin 0.20.1 (временно)

## Как запустить локально (windows powershell):

#### Склонировать репозиторий и перейти в директорию проекта:

```bash
git clone https://github.com/germynic31/financial_accounting_bot.git
cd financial_accounting_bot
```

#### Создать виртуальное окружение и установить зависимости:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### Заполнить .env:
```dotenv
SECRET=SECRET
TG_API_KEY=API_KEY
DATABASE_URL_DEV=sqlite:///./database.db
```

#### Выполнить миграции:

```bash
alembic upgrade head
```

#### Запустить бота:
```bash
python .\backend\start_bot.py
```

#### В отдельном терминале запустить админ-панель:
```bash
python .\backend\start_admin.py
```

---

#### Автор: [Герман Деев](https://github.com/germynic31)

