from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel
from models.base import BaseTableID

if TYPE_CHECKING:
    from models.office import Office

class OfficeReportBase(SQLModel):
    """Base model for office daily reports"""
    report_date: date = Field(index=True, description="Дата отчета")
    turnover: float = Field(default=0.0, description="Оборот")
    expensive_turnover: float = Field(default=0.0, description="Оборот дорогостоя")
    sales: float = Field(default=0.0, description="Продажа")
    returns: float = Field(default=0.0, description="Возврат")
    supplier_delivery_fee: float = Field(default=0.0, description="Доплата за выдачу товара поставщика")
    supplier_storage_fee: float = Field(default=0.0, description="Доплата за хранение товара поставщика")
    supplier_acceptance_fee: float = Field(default=0.0, description="Приемка товара поставщика")
    courier_sales: float = Field(default=0.0, description="Продажа курьером")
    courier_returns: float = Field(default=0.0, description="Возврат проданного курьером")
    own_courier_sales: float = Field(default=0.0, description="Продажа товара, доставленного собственным курьером")
    own_courier_returns: float = Field(default=0.0, description="Возврат товара, доставленного собственным курьером")
    expensive_goods_sales: float = Field(default=0.0, description="Продажа дорогостоя товара")
    expensive_goods_returns: float = Field(default=0.0, description="Возврат дорогостоя товара")
    balance_change: float = Field(default=0.0, description="Изменение баланса")
    pickup_point_activation: float = Field(default=0.0, description="Поступление при активации ПВЗ")
    hanging_goods_fee: float = Field(default=0.0, description="Доплата за зависший товар")
    acceptance_speed_bonus: float = Field(default=0.0, description="Доплата за скорость приемки")
    rating_bonus: float = Field(default=0.0, description="Доплата за рейтинг")
    furniture_deduction: float = Field(default=0.0, description="Удержание за мебель")
    signboard_bonus: float = Field(default=0.0, description="Доплата за вывеску")
    offer_violation_cancellation: float = Field(default=0.0, description="Отмена удержания за нарушения Оферты")
    vat_bonus: float = Field(default=0.0, description="Доплата НДС")
    supplier_return_delivery_fee: float = Field(default=0.0, description="Доплата за выдачу возврата поставщику")
    subsidy_bonus: float = Field(default=0.0, description="Доплата субсидий")
    defect_deduction: float = Field(default=0.0, description="Удержание за брак")
    additional_motivation: float = Field(default=0.0, description="Дополнительная мотивация")
    unreturned_goods_fee: float = Field(default=0.0, description="Доплата за невозвращенный товар")
    package_compensation: float = Field(default=0.0, description="Компенсация за пакеты")
    substitution_cancellation: float = Field(default=0.0, description="Отмена удержания за подмену товара")
    zero_substitution_effect: float = Field(default=0.0, description="Нулевой эффект подмены")
    incorrect_defect_mark_bonus: float = Field(default=0.0, description="Доплата за некорректную отметку о браке")
    marketplace_acceptance_fee: float = Field(default=0.0, description="Доплата за приемку поставок МаркетПлейса")
    inventory_deduction_return: float = Field(default=0.0, description="Возврат удержаний за непроведённую инвентаризацию")
    video_violation_cancellation: float = Field(default=0.0, description="Отмена удержания за непредоставление видео")
    repackaging_motivation: float = Field(default=0.0, description="Мотивация за переупаковку товара")
    acceptance_speed_compensation: float = Field(default=0.0, description="Возмещение за скорость приемки")
    balance_correction: float = Field(default=0.0, description="Корректировка баланса")
    safe_package_compensation: float = Field(default=0.0, description="Компенсация сейф пакетов")
    locks_bonus: float = Field(default=0.0, description="Доплата за замки")
    courier_delivery_motivation: float = Field(default=0.0, description="Мотивация за выдачу заказа курьеру")
    courier_delivery_count_motivation: float = Field(default=0.0, description="Мотивация за количество выдач курьеру")
    branding_bonus: float = Field(default=0.0, description="Доплата за брендинг")
    ticket_payment_return: float = Field(default=0.0, description="Возврат оплаты за тикет")
    high_substitution_share: float = Field(default=0.0, description="Высокая доля подмен")
    guaranteed_income: float = Field(default=0.0, description="Гарантированный доход")
    customer_rating_bonus: float = Field(default=0.0, description="Мотивация за оценки клиентов")
    owner_rating: float = Field(default=0.0, description="Рейтинг собственника")
    referral_program: float = Field(default=0.0, description="Реферальная программа")
    employee_verification: float = Field(default=0.0, description="Проверка сотрудника")
    repackaging_materials_compensation: float = Field(default=0.0, description="Компенсация заказа расходных материалов для переупаковки")
    customer_requests: float = Field(default=0.0, description="Обращения клиентов")
    wb_track_registration_reward: float = Field(default=0.0, description="Вознаграждение за оформление отправления WB Track")
    wb_track_materials_compensation: float = Field(default=0.0, description="Компенсация заказа расходных материалов для упаковки отправления WB track")
    wb_track_delivery_reward: float = Field(default=0.0, description="Вознаграждение за выдачу отправления WB Track")
    return_deadline_violation_cancellation: float = Field(default=0.0, description="Отмена нарушения сроков возврата")
    total: float = Field(default=0.0, description="Итог")

class OfficeReport(OfficeReportBase, BaseTableID, table=True):
    """Model for storing daily office reports with relationships"""
    
    office_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("office.id", ondelete="CASCADE"),
        ),
        description="ID офиса"
    )
    office: "Office" = Relationship(back_populates="reports")