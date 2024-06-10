from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Customer, Lead, User, Interaction, Promotion, Order, Product, OrderItem, Payment, Feedback, Subscription, SubscribedCustomer, CalcPoints, LoyaltyModel, PromotionRedemption

class ModelTestCase(TestCase):
    def test_customer_creation(self):
        # Test customer creation with valid data
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        self.assertEqual(Customer.objects.count(), 1)

    def test_lead_creation(self):
        # Test lead creation with valid data
        lead = Lead.objects.create(first_name="Jane", last_name="Smith", email="jane@example.com", phone_number="9876543210", address="456 Elm St", city="Anycity", state="Anotherstate", country="USA", postal_code="54321", status="New", source="Website_Form")
        self.assertEqual(Lead.objects.count(), 1)

    def test_user_creation(self):
        # Test user creation with valid data
        user = User.objects.create(username="test_user", email="test@example.com", role="Sales_Representative")
        self.assertEqual(User.objects.count(), 1)

    def test_interaction_clean_method(self):
        # Test Interaction model's clean method
        lead = Lead.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        user = User.objects.create(username="test_user", email="test@example.com", role="Sales_Representative")
        interaction = Interaction(participant_type='Lead', participant_id=lead.id, interaction_type='Phone_Call', interaction_details='Called the lead.', responsible_user=user, interaction_date=timezone.now())
        interaction.full_clean()  # This should pass without raising any validation errors

  
    def test_promotion_usage_limits(self):
        # Test Promotion model's usage limits and expiration date handling
        promotion = Promotion.objects.create(name="Test Promotion", description="Test promotion description", type="Coupon", start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=7), discount_type="Percentage", discount_value=10, usage_limits=1)
        self.assertEqual(promotion.expiration_date, None)

        # Change usage_limits to trigger expiration_date update
        promotion.usage_limits -= 1
        promotion.save()

        # Call check_usage_limits method
        promotion.check_usage_limits(promotion.id)

        # Refresh promotion object to get updated data from the database
        promotion.refresh_from_db()
    
        # Assert expiration_date is not None
        self.assertIsNotNone(promotion.expiration_date)

    def test_order_creation(self):
        # Test order creation with valid data
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        order = Order.objects.create(customer=customer, total_amount=100, status="UnPaid")
        self.assertEqual(Order.objects.count(), 1)

    def test_product_creation(self):
        # Test product creation with valid data
        product = Product.objects.create(name="Test Product", description="Test product description", category="Electronics", unit_price=99.99, quantity_available=100, br_code="123456789", coin_type="US_Dollar")
        self.assertEqual(Product.objects.count(), 1)

    def test_payment_creation(self):
        # Test payment creation with valid data
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        order = Order.objects.create(customer=customer, total_amount=100, status="UnPaid")
        payment = Payment.objects.create(order=order, amount=100, payment_method="Credit_Card")
        self.assertEqual(Payment.objects.count(), 1)

    def test_feedback_creation(self):
        # Test feedback creation with valid data
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        order = Order.objects.create(customer=customer, total_amount=100, status="UnPaid")
        feedback = Feedback.objects.create(customer=customer, order=order, rating=5, review="Great service!")
        self.assertEqual(Feedback.objects.count(), 1)

    def test_subscription_creation(self):
        # Test subscription creation with valid data
        subscription = Subscription.objects.create(types=['Premium'], price=[10], discount=[2], duration=1, duration_unit='Months')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_subscribed_customer_end_date(self):
        # Test SubscribedCustomer model's end_date calculation
        subscription = Subscription.objects.create(types=['Premium'], price=[10], discount=[2], duration=1, duration_unit='Months')
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        subscribed_customer = SubscribedCustomer.objects.create(subscription=subscription, customer=customer, start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=30))
        subscribed_customer.save()
        self.assertEqual(subscribed_customer.status, 'Active')

        # Advance the end date to a past date
        subscribed_customer.end_date = timezone.now() - timezone.timedelta(days=1)
        subscribed_customer.save()
        self.assertEqual(subscribed_customer.status, 'Expired')

        # Test the auto-expiration of subscriptions
        subscription.duration_unit = 'Days'
        subscription.duration = 2
        subscription.save()
        subscribed_customer.refresh_from_db()
        self.assertEqual(subscribed_customer.status, 'Expired')

    def test_loyalty_model_upgrade_tier(self):
        # Test LoyaltyModel model's upgrade_tier method
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890", address="123 Main St", city="Anytown", state="Somestate", country="USA", postal_code="12345")
        calc_points = CalcPoints.objects.create(onepointforXdollar=10)
        loyalty_model = LoyaltyModel.objects.create(customer=customer,CalcPoints= calc_points,points=0, tier='Bronze')
        loyalty_model.points = 600
        loyalty_model.save()
        loyalty_model.refresh_from_db()

        loyalty_model.upgrade_tier(loyalty_model.id)
        loyalty_model.refresh_from_db()
        self.assertEqual(loyalty_model.tier, 'Silver')

if __name__ == '__main__':
    # This block allows you to run tests without using django's test runner

    import unittest
    unittest.main()
