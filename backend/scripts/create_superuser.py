#!/usr/bin/env python
import asyncio
import os
import sys
import traceback
from datetime import datetime, timedelta
import hashlib
import secrets

# Добавляем корень проекта в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from sqlmodel import select
    from core.config import settings
    from core.db import get_db_session_instance
    # Удаляем импорт get_password_hash
    from enums.user import UserRoleEnum
    from models.user import User
    
    print("✅ Все необходимые модули успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    traceback.print_exc()
    sys.exit(1)

# Реализуем собственную функцию хеширования пароля
def get_password_hash(password: str) -> str:
    """Создает хеш пароля с использованием SHA-256"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return f"{salt}${password_hash}"


async def create_superuser():
    """Создание суперпользователя с ролью SUPER_ADMIN"""
    try:
        # Учетные данные суперпользователя по умолчанию
        email = os.environ.get("SUPERUSER_EMAIL", "admin@wbtrack.app")
        password = os.environ.get("SUPERUSER_PASSWORD", "admin123")
        first_name = os.environ.get("SUPERUSER_FIRST_NAME", "Super")
        last_name = os.environ.get("SUPERUSER_LAST_NAME", "Admin")
        
        print(f"🔍 Попытка создания суперпользователя с email: {email}")
        
        # Получаем сессию базы данных с помощью контекстного менеджера
        async with get_db_session_instance() as session:
            # Проверяем, существует ли уже суперпользователь
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"ℹ️ Суперпользователь с email {email} уже существует.")
                return
            
            # Создаем нового суперпользователя
            hashed_password = get_password_hash(password)
            
            # Устанавливаем даты подписки на год
            now = datetime.utcnow()
            one_year_later = now + timedelta(days=365)
            
            print("🔧 Создание объекта суперпользователя...")
            
            # Выводим все поля модели User для отладки
            print(f"📋 Поля модели User: {[attr for attr in dir(User) if not attr.startswith('_')]}")
            
            superuser = User(
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                is_verified=True,
                is_superuser=True,
                first_name=first_name,
                last_name=last_name,
                role=UserRoleEnum.SUPER_ADMIN,
                is_subscription_active=True,
                subscription_start_date=now,
                subscription_end_date=one_year_later,
                created_at=now
            )
            
            print("💾 Сохранение суперпользователя в базу данных...")
            session.add(superuser)
            await session.commit()
            await session.refresh(superuser)
            
            print(f"✅ Суперпользователь успешно создан с email: {email}")
            print(f"📝 ID пользователя: {superuser.id}")
            print("⚠️ Пожалуйста, измените пароль по умолчанию после первого входа!")
            
    except Exception as e:
        print(f"❌ Ошибка при создании суперпользователя: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Запуск скрипта создания суперпользователя...")
    try:
        asyncio.run(create_superuser())
        print("✅ Скрипт успешно завершен")
    except Exception as e:
        print(f"❌ Необработанная ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)