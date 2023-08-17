from typing import Any, Dict, List, Literal, Optional

from datetime import datetime

from pydantic import validator
from pydantic.types import Enum

from paddle_billing_client.models.base import LazyBaseModel as BaseModel


class AdjustmentAction(str, Enum):
    refund = "refund"
    credit = "credit"
    chargeback = "chargeback"
    chargeback_warning = "chargeback_warning"


class AdjustmentStatus(str, Enum):
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"


class AdjustmentItem(BaseModel):
    id: str
    item_id: str
    type: str
    amount: str
    proration: Optional[str]
    totals: dict


class AdjustmentBase(BaseModel):
    # How this adjustment impacts the related transaction.
    # 'refund' adjustments must be approved by Paddle, and are created with the status 'pending_approval'.
    # 'chargeback' and 'chargeback_warning' adjustments are created automatically by Paddle.
    action: AdjustmentAction
    transaction_id: str
    reason: Optional[str]
    items: List[AdjustmentItem]


class Adjustment(AdjustmentBase):
    id: str
    subscription_id: Optional[str]
    customer_id: str
    currency_code: str
    # Status of this adjustment. Set automatically by Paddle.
    # 'refund' adjustments must be approved by Paddle,
    # and are created with the status 'pending_approval' until they move to 'approved' or 'rejected' on review.
    # 'credit' adjustments are created with the status 'approved'.
    status: AdjustmentStatus
    totals: dict
    payout_totals: dict
    created_at: datetime
    updated_at: datetime


class AdjustmentQueryParams(BaseModel):
    # Return entities for the specified action.
    action: Optional[AdjustmentAction]
    # Return entities after the specified cursor. Used for working through paginated results.
    after: Optional[str] = None
    # Return entities related to the specified customer. Use a comma separated list to specify multiple customer IDs.
    customer_id: Optional[str]
    # Order returned entities by the specified field and direction ([ASC] or [DESC]).
    order_by: Optional[Literal["[ASC]", "[DESC]"]] = None
    # Set how many entities are returned per page. Default: 50
    per_page: Optional[int] = None
    # Return entities that match the specified status. Use a comma separated list to specify multiple status values.
    status: Optional[str] = None
    # Return entities related to the specified subscription.
    # Use a comma separated list to specify multiple subscription IDs.
    subscription_id: Optional[str]
    # Return entities related to the specified transaction.
    # Use a comma separated list to specify multiple transaction IDs.
    transaction_id: str
    # Return only the IDs specified.
    # Use a comma separated list to get multiple entities.
    id: Optional[str] = None

    @validator("status")
    def check_status(cls, v: str) -> str:
        valid_statuses = ["approved", "pending_approval", "rejected", "reversed"]
        if not all([s in valid_statuses for s in v.split(",")]):
            raise ValueError(
                f"Query param invalid status: {v}, allowed values: {valid_statuses}"
            )
        return v


class AdjustmentResponse(BaseModel):
    data: Adjustment


class AdjustmentsResponse(BaseModel):
    data: List[Adjustment]


class AdjustmentRequest(AdjustmentBase):
    pass


if __name__ == "__main__":
    adjustment = Adjustment(
        id="1",
        action="refund",
        transaction_id="1",
        subscription_id="1",
        customer_id="1",
        reason="1",
        currency_code="USD",
        status="pending_approval",
        items=[],
        totals={},
        payout_totals={},
        created_at="2023-03-21T18:34:44.148562Z",
        updated_at="2023-03-21T18:34:44.148562Z",
    )
    print(adjustment.action == AdjustmentAction.refund)
