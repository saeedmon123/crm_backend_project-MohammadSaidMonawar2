
from ninja import Schema
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


#Enum
#=================================================


class StatusChoices(Enum):
    New = "New"
    Contacted = "Contacted"
    Converted="Converted"

class SourceChoices(Enum):
    Website_Form = "Website_Form"
    Referral = "Referral"
    Cold_Call = "Cold_Call"
    Ads = "Ads"

class RoleChoices(Enum):
    Sales_Representative = "Sales_Representative"
    Customer_Support_Agent = "Customer_Support_Agent"
    Account_Manager = "Account_Manager"

class InteractionTypeChoices(Enum):
    Phone_Call = "Phone_Call"
    Email = "Email"
    Meeting = "Meeting"

class ParticipantTypeChoices(str,Enum):
    Lead = "Lead"
    Customer = "Customer"

class CoinChoices(Enum):
    US_Dollar = "US_Dollar"
    Euro = "Euro"
    British_Pound = "British_Pound"
    Japanese_Yen = "Japanese_Yen"

class OrderStatusChoices(Enum):
    UnPaid = "UnPaid"
    Paid = "Paid"

class PaymentMethodChoices(Enum):
    Credit_Card = "Credit_Card"
    Debit_Card = "Debit_Card"
    PayPal = "PayPal"
    Bank_Transfer = "Bank_Transfer"

class SubscriptionStatusChoices(Enum):
    Active = "Active"
    Cancelled = "Cancelled"
    Expired = "Expired"

class TierChoices(Enum):
    Bronze = "Bronze"
    Silver = "Silver"
    Gold = "Gold"
    Platinum = "Platinum"

class PromotionTypeChoices(Enum):
    Coupon = "Coupon"
    Offer = "Offer"
    Discount_Code = "Discount_Code"

class DiscountTypeChoices(str,Enum):
    Percentage = "Percentage"
    Fixed_Amount = "Fixed_Amount"

class CategoryChoices(str,Enum):
    Electronics = "Electronics"
    Clothing = "Clothing"
    Books = "Books"
    Furniture = "Furniture"
    Food = "Food"
    Toys = "Toys"
    Tools = "Tools"
    Healthcare = "Healthcare"

class DurationUnitChoices(Enum):
    Days = "Days"
    Months = "Months"
    Years = "Years"
#-----------------------------------------------------------------------------------------


class CustomerSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    date_created: Optional[datetime] = None
    last_contacted: Optional[datetime] = None
    LoyaltyThreshold_id: Optional[int] = None
    Subscription_id: Optional[int] = None
    Subscription_type: Optional[str] = None


class update_loyalty(Schema):
    customer_id:int
    LoyaltyThreshold_id: int

class update_subscription(Schema):
    customer_id:int
    Subscription_id: int
    Subscription_type: str
    
 

class LeadSchema(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    status: str
    source: str
    created_date: datetime
    notes: str


class InteractionSchema(Schema):
    participant_type: str
    participant_id: int
    interaction_type: str
    interaction_details: str
    outcome: str
    responsible_user: str
    interaction_date: datetime
    follow_up_required: bool

class ProductSchema(Schema):
    id: int
    name: str
    description: str
    category: str
    unit_price: float
    quantity_available: int
    br_code: str
    coin_type: str

class OrderSchema(Schema):
    id: int
    customer_id: int
    order_date: str
    total_amount: float
    status: str
    loyalty_point_used: Optional[int] = None
    promotion_id: Optional[int] = None

class CreateOrderSchema(BaseModel):
    participant_id: int
    participant_type: str  # Adjust this according to your actual type
    product_ids: List[int]
    quantities: List[int]
    promotion_id: Optional[int] = None
    UseLoyalty: bool = False
    RedeemPoints: Optional[int] = None

class OrderItemSchema(Schema):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class PaymentSchema(Schema):
    id: int
    order_id: int
    amount: float
    payment_date: datetime
    payment_method: str

class FeedbackSchema(Schema):
    id: int
    customer_id: int
    order_id: int
    rating: int
    review: str
    feedback_date: datetime

class LoyaltyThresholdSchema(Schema):
    onepointforXdollar: int  # Points earned per X dollars spent
    minimum_order_amount: float  # Minimum order amount to earn points
    min_points_to_redeem: int  # Minimum points required to start redeeming
    points_expiry_days: int  # Number of days before points expire
    tier_name: list[str]  # Name of the tier (e.g., Bronze, Silver, Gold)
    points_for_next_tier: list[int]  # Points required to reach the next tier
    tier_discount: list[float]  # Discount percentage for this tier

class LoyaltyModelSchema(Schema):
    loyaltyThreshold: int
    customer: int
    points: int
    tier: str
    last_updated: datetime
    
class loyaltyRedepmtionSchema(Schema):
    id:int
    LoyaltyModel:int
    Customer:int
    points_used:int
    redemption_date:int





class PromotionSchema(Schema):
    id: int
    name: str
    description: str
    type: str
    start_date: datetime
    
    end_date: datetime
    discount_type: str
    discount_value: float
    expiration_date: datetime
    usage_limits: int
    category:CategoryChoices = CategoryChoices.Electronics

class PromotionRedemptionSchema(Schema):
    id: int
    promotion: int
    customer: int
    redemption_date: datetime


class SubscriptionSchema(Schema):
    id: int
    types: List[str]
    price: List[int]
    duration: int
    duration_unit: str  

class SubscribedCustomerSchema(Schema):
    id: int
    customer_id: int
    subscribtion:str
    subscribtion_type:str
    start_date: datetime
    end_date: datetime
    status: str  

#Filter
#===================
from ninja import FilterSchema

class SortingSchema(Schema):
    sort_by: Optional[str] = None
    sort_order:Optional[str]='asc'

class CustomerFilterSchema(FilterSchema):
    first_name: Optional[str] = None
    last_name:Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city:Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    date_created: Optional[datetime] = None
    last_contacted: Optional[datetime] = None

class LeadFilterSchema(FilterSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    created_date: Optional[datetime] = None
    status: Optional[str] = None
    source: Optional[str] = None


class InteractionFilterSchema(FilterSchema):
    participant_type: Optional[str] = None
    participant_id: Optional[int] = None
    interaction_type: Optional[str] = None
    interaction_details: Optional[str] = None
    outcome: Optional[str] = None
    responsible_user: Optional[str] = None
    interaction_date: Optional[datetime] = None
    follow_up_required: Optional[bool] = None

class ProductFilterSchema(FilterSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = None
    quantity_available: Optional[int] = None
    br_code: Optional[str] = None
    coin_type: Optional[str] = None

class OrderFilterSchema(FilterSchema):
    customer_id: Optional[int] = None
    order_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    loyalty_point_used: Optional[int] = None
    promotion_id: Optional[int] = None
    status: Optional[str] = None


class OrderItemFilterSchema(FilterSchema):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class PaymentFilterSchema(FilterSchema):
    order_id: Optional[int] = None
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None

class FeedbackFilterSchema(FilterSchema):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    feedback_date: Optional[datetime] = None

class LoyaltyThresholdFilterSchema(FilterSchema):
    onepointforXdollar: Optional[int] = None
    minimum_order_amount: Optional[float] = None
    min_points_to_redeem: Optional[int] = None
    points_expiry_days: Optional[int] = None
    tier_name: Optional[List[str]] = None
    points_for_next_tier: Optional[List[int]] = None
    tier_discount: Optional[List[float]] = None

class LoyaltyModelFilterSchema(FilterSchema):
    loyaltyThreshold: Optional[int] = None
    customer: Optional[int] = None
    points: Optional[int] = None
    tier: Optional[str] = None
    last_updated: Optional[datetime] = None

class PromotionFilterSchema(FilterSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    expiration_date: Optional[datetime] = None
    usage_limits: Optional[int] = None
    category: Optional[str] = None

class PromotionRedemptionFilterSchema(FilterSchema):
    promotion: Optional[int] = None
    customer: Optional[int] = None
    redemption_date: Optional[datetime] = None

class SubscriptionFilterSchema(FilterSchema):
    types: Optional[List[str]] = None
    price: Optional[List[int]] = None
    duration: Optional[int] = None
    duration_unit: Optional[str] = None

class SubscribedCustomerFilterSchema(FilterSchema):
    customer_id: Optional[int] = None
    subscribtion: Optional[str] = None
    subscribtion_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None

class LoyaltyRedemptionFilterSchema(FilterSchema):
    LoyaltyModel: Optional[int] = None
    Customer: Optional[int] = None
    points_used: Optional[int] = None
    redemption_date: Optional[int] = None