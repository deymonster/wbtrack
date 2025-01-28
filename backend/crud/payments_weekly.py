import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.payments_weekly import WeeklyPayments
from crud.base import CRUDBase
from crud.office import office_crud
from crud.categories_operation import categories_operation_crud
from crud.operation_name import operation_name_crud
from crud.payments_pickpoint import pickpoint_payments_crud
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
            logger.info(f"Attempting to create or update WeeklyPayments with data: {weekly_payment_data.dict()}")
            weekly_payment = await self.create_or_update(
                obj_in=weekly_payment_data,
                index_elements=["date_from", "date_to"],
                create_exclude={"id"},
                update_exclude={"id"},
                db_session=session,
            )
            logger.info(f"Created or updated WeeklyPayments: {weekly_payment}")

            # create PickpointPayments
            pickpoint_payments = []
            if weekly_data.pickpoint_payments:
                for pp_data in weekly_data.pickpoint_payments:
                    logger.info(f"Fetching office with external_id={pp_data.pickpoint_id}")

                    office = await office_crud.get_by_external_id(external_id=pp_data.pickpoint_id, db_session=session)
                    
                    if not office:
                        logger.error(f"Office wich external_id={pp_data.pickpoint_id} not found in the database")
                        raise ValueError(f"Office with external_id={pp_data.pickpoint_id} not found")
                    
                    pickpoint_payment_data = IPickpointPaymentsCreate(
                        office_id=office.id,
                        weekly_payments_id=weekly_payment.id,
                        base_accrued=pp_data.base_accrued,
                        expensive_accrued=pp_data.expensive_accrued,
                        other_accrued=pp_data.other_accrued,
                        total=pp_data.total,
                    )

                    logger.info(f"Processing PickpointPayments for WeeklyPayments ID: {weekly_payment.id}")
                    pp = await pickpoint_payments_crud.create_or_update(
                        obj_in=pickpoint_payment_data,
                        index_elements=["office_id", "weekly_payments_id"],
                        create_exclude={"id"},
                        update_exclude={"id"},
                        db_session=session,
                    )


                    pickpoint_payments.append(pp)

                    # create transaction
                    transaction_data_list = []
                    if pp_data.categories:
                        for category in pp_data.categories:
                            
                            # for every operations create Transaction
                            for operation in category.operations:
                                # get OperationName by external_id
                                operation_name = await operation_name_crud.get_operation_name_by_external_id(
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
                                transaction_data_list.append(transaction_data)

                                # logger.info(f"Processing Transaction with data: {transaction_data.dict()}")
                                # await transaction_crud.create_or_update(
                                #     obj_in=transaction_data,
                                #     index_elements=["weekly_payments_id", "pickpoint_payments_id", "operation_name_id"],
                                #     create_exclude={"id"},
                                #     update_exclude={"id"},
                                #     db_session=session
                                # )
                    if transaction_data_list:
                        logger.info(f"Creating or updating {len(transaction_data_list)} transactions in bulk for PickpointPayment ID: {pp.id}")
                        await transaction_crud.create_or_update_multi(
                            list_in=transaction_data_list,
                            index_elements=["weekly_payments_id", "pickpoint_payments_id", "operation_name_id"],
                            exclude={"id"},
                            on_conflict_set={"sum", "count"},
                            db_session=session,
                        )
            
            
            await session.refresh(weekly_payment)
            return weekly_payment

        except Exception as e:
            logger.error(f"Error creating weekly payment: {e}", exc_info=True)
            raise     




          

weekly_payments_crud = WeeklyPaymentsCRUD(WeeklyPayments)  # type: ignore


__all__ = [
    "weekly_payments_crud",
]