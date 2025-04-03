from fastapi import APIRouter, Depends, status

from api.dependencies.user import current_active_user
from crud.office import office_crud
from crud.office_expenses import office_expenses_crud
from models.user import User
from schemas.office_expenses import (
    IOfficeExpensesCreate,
    IOfficeExpensesRead,
    IOfficeExpensesUpdate,
)

router = APIRouter()

@router.post("/", response_model=IOfficeExpensesRead)
async def create_office_expenses(
    expenses:  IOfficeExpensesCreate,
    current_user: User = Depends(current_active_user)
):
    """Создание новых финансовых параметров для ПВЗ.

    Parameters:
    - **expenses**: Параметры расходов офиса
        - rent: Аренда помещения филиала
        - utilities: Коммунальные платежи
        - internet: Оплата интернета
        - cameras: Оплата видеонаблюдения
        - vat_rate: Ставка НДС
        - simplified_tax_rate: Ставка УСН
        - rf_payment: ЗП руководителя филиала
        - revision_payment: Оплата сотрудника по ревизии
        - min_salary: Минимальная ЗП на филиале
        - commission_rate: Процент от оборота
        - total_without_tax: Сумма всех обязательных платежей без налогов
    Returns:
    - **200**: Успешное создание
        - Возвращает созданный объект с ID
    - **404**: Офис не найден или нет доступа
    - **422**: Ошибка валидации данных
    """

    await office_expenses.verify_office_access(office_id=expenses.office_id, user_id=current_user.id)
    return await office_expenses_crud.create(obj_in=expenses)

@router.get("/{office_id}", response_model=IOfficeExpensesRead)
async def get_office_expenses(
    office_id: int,
    current_user: User = Depends(current_active_user)
):
    """Получение финансовых паарметров ПВЗ по office_id

    Parameters:
    - **office_id**: ID офиса

    Returns:
    - **200**: Успешное получение данных
        - Возвращает объект с финансовыми параметрами
    - **404**: Офис не найден или нет доступа
    """
    await office_expenses_crud.verify_office_access(office_id=office_id, user_id=current_user.id)
    return await office_expenses_crud.get_expenses_or_404(office_id=office_id)

@router.put("/{office_id}", response_model=IOfficeExpensesRead)
async def update_office_expenses(
    office_id: int,
    expenses_update: IOfficeExpensesUpdate,
    current_user: User = Depends(current_active_user)
):
    """Обновление финансовых параметров ПВЗ

    Parameters:
    - **office_id**: ID офиса
    - **expenses_update**: Обновляемые параметры
        - Все поля опциональны
        - Обновляются только переданные поля

    Returns:
    - **200**: Успешное обновление
        - Возвращает обновленный объект
    - **404**: Офис не найден или нет доступа
    - **422**: Ошибка валидации данных
    """
    await office_expenses_crud.verify_office_access(office_id=office_id, user_id=current_user.id)
    existing_expenses = await office_expenses_crud.get_expenses_or_404(office_id=office_id)
    return await office_expenses_crud.update(db_obj=existing_expenses, obj_in=expenses_update)


@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_office_expenses(
    office_id: int,
    current_user: User = Depends(current_active_user)
):
    """
    Удаление финансовых параметров офиса.

    Parameters:
    - **office_id**: ID офиса

    Returns:
    - **204**: Успешное удаление
    - **404**: Офис не найден или нет доступа
    """
    await office_crud.get_office_by_user_id(
        office_id=office_id,
        user_id=current_user.id
    )
    await office_expenses_crud.verify_office_access(office_id, current_user.id)
    existing_expenses = await office_expenses_crud.get_expenses_or_404(office_id)
    await office_expenses_crud.delete(db_obj=existing_expenses)
