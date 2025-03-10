from pydantic import BaseModel, Field


class SubscriptionApproval(BaseModel):
    duration_days: int = Field(
        ...,
        description="Duration of subscription in days",
        ge=1,
        le=365
    ) 