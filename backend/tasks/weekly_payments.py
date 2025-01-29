import logging

from core.celery_app import celery_app
from crud.payments_weekly import weekly_payments_crud
from pvz_client.models import WeeklyTransaction
from core.db import get_db_session_instance
import asyncio


logger = logging.getLogger(__name__)


@celery_app.task(
    name="process_weekly_payments",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    rate_limit="10/m"
)
def process_weekly_payments(self, weekly_data: dict) -> dict:
    """
    Celery задача для сохранения недельных выплат по каждому офису.
    """
    logger.info(f"Starting saving weekly payments")

    async def run_task():
        try:
            self.update_state(state="PROGRESS", meta={'progress': 0, 'status': 'Initializing'})
            weekly_transaction = WeeklyTransaction.parse_obj(weekly_data)
            async with get_db_session_instance() as session:

                def progress_callback(current: int, total: int, status: str):
                    progress = int((current / total) * 100) if total > 0 else 0
                    self.update_state(
                        state="PROGRESS",
                        meta={
                            'progress': progress,
                            'status': status
                        }
                    )

                result = await weekly_payments_crud.create_weekly_payments_with_relations(
                    weekly_data=weekly_transaction,
                    db_session=session,
                    progress_callback=progress_callback
                )
                self.update_state(
                    state="SUCCESS",
                    meta={
                        'progress': 100,
                        'status': 'Completed'
                    }
                )
                return {
                    "status": "success",
                    "result": result.id,
                }
        except Exception as e:
            error_info = {
                'exc_type': type(e).__name__,
                'exc_message': str(e),
                'progress': 0,
                'status': f"Error: {str(e)}"
            }
            logger.error(f"Error saving weekly payments: {str(e)}")
            self.update_state(
                state="FAILURE",
                meta=error_info
            )
            raise e

    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_task())
        return result
    except Exception as e:
        logger.error(f"Task failed: {e.__class__.__name__}: {str(e)}")
        self.retry(exc=e)

