import unittest
from datetime import datetime,timedelta
from django.utils import timezone
from ninja.testing import TestClient
from .schemas import  CustomerSchema, LeadSchema, UserSchema,  InteractionSchema,  ProductSchema, DurationUnitChoices, OrderSchema,  OrderItemSchema, PaymentSchema, FeedbackSchema,  SubscriptionSchema,SubscribedCustomerSchema,CalcPointsSchema, LoyaltyModelSchema,  PromotionSchema,  PromotionRedemptionSchema

class TestSchemas(unittest.TestCase):
    def test_customer_schema(self):
        data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "address": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "country": "USA",
            "postal_code": "12345",
            "date_created": datetime.now(),
            "last_contacted": datetime.now()
        }
        schema = CustomerSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.first_name, "John")
        self.assertEqual(schema.last_name, "Doe")
        self.assertEqual(schema.email, "john@example.com")
        self.assertEqual(schema.phone_number, "123456789")
        self.assertEqual(schema.address, "123 Main St")
        self.assertEqual(schema.city, "Anytown")
        self.assertEqual(schema.state, "CA")
        self.assertEqual(schema.country, "USA")
        self.assertEqual(schema.postal_code, "12345")
        self.assertIsInstance(schema.date_created, datetime)
        self.assertIsInstance(schema.last_contacted, datetime)

    def test_lead_schema(self):
        data = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "phone_number": "987654321",
            "address": "456 Elm St",
            "city": "Othertown",
            "state": "NY",
            "country": "USA",
            "postal_code": "54321",
            "status": "New",
            "source": "Website_Form",
            "created_date": datetime.now(),
            "notes": "Some notes"
        }
        schema = LeadSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.first_name, "Jane")
        self.assertEqual(schema.last_name, "Doe")
        self.assertEqual(schema.email, "jane@example.com")
        self.assertEqual(schema.phone_number, "987654321")
        self.assertEqual(schema.address, "456 Elm St")
        self.assertEqual(schema.city, "Othertown")
        self.assertEqual(schema.state, "NY")
        self.assertEqual(schema.country, "USA")
        self.assertEqual(schema.postal_code, "54321")
        self.assertEqual(schema.status, "New")
        self.assertEqual(schema.source, "Website_Form")
        self.assertIsInstance(schema.created_date, datetime)
        self.assertEqual(schema.notes, "Some notes")

    def test_user_schema(self):
        data = {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "role": "admin"
        }
        schema = UserSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.username, "user123")
        self.assertEqual(schema.email, "user@example.com")
        self.assertEqual(schema.role, "admin")

    def test_interaction_schema(self):
        data = {
            "id": 1,
            "participant_type": "customer",
            "participant_id": 123,
            "interaction_type": "call",
            "interaction_details": "Discussed product details",
            "outcome": "successful",
            "responsible_user": 5,
            "interaction_date": datetime.now(),
            "follow_up_required": True
        }
        schema = InteractionSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.participant_type, "customer")
        self.assertEqual(schema.participant_id, 123)
        self.assertEqual(schema.interaction_type, "call")
        self.assertEqual(schema.interaction_details, "Discussed product details")
        self.assertEqual(schema.outcome, "successful")
        self.assertEqual(schema.responsible_user, 5)
        self.assertIsInstance(schema.interaction_date, datetime)
        self.assertTrue(schema.follow_up_required)

    def test_product_schema(self):
        data = {
            "id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "category": "Electronics",
            "unit_price": 99.99,
            "quantity_available": 100,
            "br_code": "BR123",
            "coin_type": "USD"
        }
        schema = ProductSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.name, "Product A")
        self.assertEqual(schema.description, "Description of Product A")
        self.assertEqual(schema.category, "Electronics")
        self.assertAlmostEqual(schema.unit_price, 99.99)
        self.assertEqual(schema.quantity_available, 100)
        self.assertEqual(schema.br_code, "BR123")
        self.assertEqual(schema.coin_type, "USD")

    def test_order_schema(self):
        data = {
            "id": 1,
            "customer": 123,
            "order_date": datetime.now(),
            "total_amount": 199.99,
            "promotion_id": 5,
            "status": "pending"
        }
        schema = OrderSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.customer, 123)
        self.assertIsInstance(schema.order_date, datetime)
        self.assertAlmostEqual(schema.total_amount, 199.99)
        self.assertEqual(schema.promotion_id, 5)
        self.assertEqual(schema.status, "pending")

    def test_order_item_schema(self):
        data = {
            "id": 1,
            "order": 1,
            "product": 1,
            "quantity": 2,
            "unit_price": 49.99
        }
        schema = OrderItemSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.order, 1)
        self.assertEqual(schema.product, 1)
        self.assertEqual(schema.quantity, 2)
        self.assertAlmostEqual(schema.unit_price, 49.99)


    def test_payment_schema(self):
        data = {
            "id": 1,
            "order": 1,
            "amount": 199.99,
            "payment_date": datetime.now(),
            "payment_method": "Credit Card"
        }
        schema = PaymentSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.order, 1)
        self.assertAlmostEqual(schema.amount, 199.99)
        self.assertIsInstance(schema.payment_date, datetime)
        self.assertEqual(schema.payment_method, "Credit Card")

    def test_feedback_schema(self):
        data = {
            "id": 1,
            "customer": 123,
            "order": 1,
            "rating": 5,
            "review": "Great product and service!",
            "feedback_date": datetime.now()
        }
        schema = FeedbackSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.customer, 123)
        self.assertEqual(schema.order, 1)
        self.assertEqual(schema.rating, 5)
        self.assertEqual(schema.review, "Great product and service!")
        self.assertIsInstance(schema.feedback_date, datetime)

    def test_calc_points_schema(self):
        data = {
            "id": 1,
            "onepointforXdollar": 10
        }
        schema = CalcPointsSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.onepointforXdollar, 10)

    def test_loyalty_model_schema(self):
        data = {
            "id": 1,
            "CalcPoints": 10,
            "customer": 123,
            "points": 100,
            "tier": "Gold",
            "last_updated": datetime.now()
        }
        schema = LoyaltyModelSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.CalcPoints, 10)
        self.assertEqual(schema.customer, 123)
        self.assertEqual(schema.points, 100)
        self.assertEqual(schema.tier, "Gold")
        self.assertIsInstance(schema.last_updated, datetime)

    def test_promotion_schema(self):
        data = {
            "id": 1,
            "name": "Summer Sale",
            "description": "Big discounts for summer",
            "type": "discount",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=30),
            "discount_type": "percentage",
            "discount_value": 20.0,
            "expiration_date": datetime.now() + timedelta(days=60),
            "usage_limits": 100,
            "category": "Electronics"
        }
        schema = PromotionSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.name, "Summer Sale")
        self.assertEqual(schema.description, "Big discounts for summer")
        self.assertEqual(schema.type, "discount")
        self.assertIsInstance(schema.start_date, datetime)
        self.assertIsInstance(schema.end_date, datetime)
        self.assertEqual(schema.discount_type, "percentage")
        self.assertAlmostEqual(schema.discount_value, 20.0)
        self.assertIsInstance(schema.expiration_date, datetime)
        self.assertEqual(schema.usage_limits, 100)
        self.assertEqual(schema.category, "Electronics")

    def test_promotion_redemption_schema(self):
        data = {
            "id": 1,
            "promotion": 1,
            "customer": 123,
            "redemption_date": datetime.now()
        }
        schema = PromotionRedemptionSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.promotion, 1)
        self.assertEqual(schema.customer, 123)
        self.assertIsInstance(schema.redemption_date, datetime)

    def test_subscription_schema(self):
        data = {
            "id": 1,
            "types": ["Basic", "Premium"],
            "price": [10, 20],
            "discount": [12, 12],  # Correcting field name to 'discount'
            "duration": 30,
            "duration_unit": "Days"
        }
        schema = SubscriptionSchema(**data)
        self.assertEqual(schema.id, 1)
        self.assertListEqual(schema.types, ["Basic", "Premium"])
        self.assertListEqual(schema.price, [10, 20])
        self.assertListEqual(schema.discount, [12, 12])  # Correcting field name to 'discount'
        self.assertEqual(schema.duration, 30)
        self.assertEqual(schema.duration_unit, "Days")


    def test_subscribed_customer_schema(self):
    # Assuming data is wrapped in a Django Getter object
        data = {
            "id": 1,
            "customer_id": 123,
            "subscription": 1,  # Make sure this key is spelled correctly
            "subscription_type": "Basic",  # Make sure this key is spelled correctly
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=365),
            "status": "Active"
        }

        # Now create the schema
        schema = SubscribedCustomerSchema(**data)

        self.assertEqual(schema.id, 1)
        self.assertEqual(schema.customer_id, 123)
        self.assertEqual(schema.subscription, 1)
        self.assertEqual(schema.subscription_type, "Basic")
        self.assertIsInstance(schema.start_date, datetime)
        self.assertIsInstance(schema.end_date, datetime)
        self.assertEqual(schema.status, "Active")