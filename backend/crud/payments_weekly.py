import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.payments_weekly import WeeklyPayments
from crud.base import CRUDBase
from crud.office import office_crud
from crud.categories_operation import categories_operation_crud
from crud.operation_name import operation_name_crud
from crud.transaction import transaction_crud
from schemas.payments_weekly import IWeeklyPaymentsBaseRead, IWeeklyPaymentsBaseCreate, IWeeklyPaymentsBaseUpdate
from schemas.payments_pickpoint import IPickpointPaymentsCreate
from schemas.transaction import ITransactionBaseCreate
from pvz_client.models import WeeklyTransaction

logger = logging.getLogger(__name__)


class WeeklyPaymentsCRUD(CRUDBase[WeeklyPayments, IWeeklyPaymentsBaseCreate, IWeeklyPaymentsBaseUpdate]):
    async def create_weekly_payments_with_relations(
        self, 
        *,
        weekly_data: WeeklyTransaction,
        db_session: AsyncSession | None = None,

    ) -> WeeklyPayments:
        """Create weekly payments with relations
        
        :param weekly_data: Weekly transaction data
        :param db_session: Database session
        :return: weekly payments
        """
        session: AsyncSession = db_session or self.db.session

        async with session.begin():
            try:
                # create WeeklyPayments using schemas
                weekly_payment_data = IWeeklyPaymentsBaseCreate(
                    date_from=weekly_data.date_from,
                    date_to=weekly_data.date_to,
                    base_accrued=weekly_data.base_accrued,
                    expensive_accrued=weekly_data.expensive_accrued,
                    other_accrued=weekly_data.other_accrued,
                    total=weekly_data.total,
                )

                weekly_payment = await self.create_or_update(
                    obj_in=weekly_payment_data,
                    index_elements=["date_from", "date_to"],
                    db_session=session,
                )

                # create PickpointPayments
                pickpoint_payments = []
                if weekly_data.pickpoint_payments:
                    for pp_data in weekly_data.pickpoint_payments:
                        office = await office_crud.get_by_external_office_id(office_id=pp_data.pickpoint_id, db_session=session)
                        
                        if not office:
                            logger.error(f"Office wich external_id={pp_data.pickpoint_id} not found in the database")
                            raise ValueError(f"Office with external_id={pp_data.pickpoint_id} not found")
                        
                        pickpoint_payment_data = IPickpointPaymentsCreate(
                            office_id=office.id,
                            base_accrued=pp_data.base_accrued,
                            expensive_accrued=pp_data.expensive_accrued,
                            other_accrued=pp_data.other_accrued,
                            total=pp_data.total,
                        )

                        pp = await self.create_or_update(
                            obj_in=pickpoint_payment_data,
                            index_elements=["office_id"],
                            db_session=session,
                        )

                        pickpoint_payments.append(pp)

                        # create transaction 
                        if pp_data.categories:
                            for category in pp_data.categories:
                                db_category = await category_crud.get_by_external_id(
                                    external_id=category.id,
                                    db_session=session
                                )

                                if not db_category:
                                    logger.error(f"Category with external_id={category.id} not found in the database")
                                    raise ValueError(f"Category with external_id={category.id} not found")

                                # for every oparations create Transaction
                                for operation in category.operations:
                                    # get OperationName by external_id
                                    operation_name = await operation_name_crud.get_by_external_id(
                                        external_id=operation.id,
                                        db_session=session
                                    )

                                    if not operation_name:
                                        logger.error(f"OperationName with external_id={operation.id} not found")
                                        raise ValueError(f"OperationName with external_id={operation.id} not found")

                                    transaction_data = ITransactionBaseCreate(
                                        sum=operation.sum,
                                        count=operation.count,
                                        operation_name_id=operation_name.id,
                                        weekly_payments_id=weekly_payment.id,
                                        pickpoint_payments_id=pp.id
                                    )
                                    await transaction_crud.create_or_update(
                                        obj_in=transaction_data,
                                        index_elements=["weekly_payments_id", "pickpoint_payments_id", "operation_name_id"],
                                        db_session=session
                                    )
                
                # update relations between weekly_payment  and pickpoint_payments
                weekly_payment.pickpoint_payments = pickpoint_payments
                await session.flush()

                return weekly_payment

            except Exception as e:
                logger.error(f"Error creating weekly payment: {str(e)}")
                raise     




          

weekly_payments_crud = WeeklyPaymentsCRUD(WeeklyPayments)  # type: ignore


__all__ = [
    "weekly_payments_crud",
]