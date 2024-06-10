from django.test import TestCase
from django.utils import timezone
from .models import Customer, Subscription, SubscribedCustomer

class SubscribedCustomerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="123456789",
            address="123 Main St",
            city="Anytown",
            state="Somestate",
            country="Somecountry",
            postal_code="12345"
        )
        self.subscription = Subscription.objects.create(
            types=["Type1", "Type2"],
            price=[100, 200],
            discount=[10, 20],
            duration=30,
            duration_unit="Days"
        )
        self.active_subscription = SubscribedCustomer.objects.create(
            customer=self.customer,
            subscription=self.subscription,
            subscription_type="Type1",
            end_date=timezone.now() + timezone.timedelta(days=10)
        )

    def test_subscription_expiry(self):
        # Ensure that an active subscription with an end date in the past gets marked as expired
        self.active_subscription.end_date = timezone.now() - timezone.timedelta(days=1)
        self.active_subscription.save()
        self.assertEqual(self.active_subscription.status, "Expired")

    def test_subscription_not_expired(self):
        # Ensure that an active subscription with an end date in the future remains active
        self.assertEqual(self.active_subscription.status, "Active")

    def test_subscription_creation(self):
        # Ensure that a new subscription with an end date in the past gets marked as expired upon creation
        expired_subscription = SubscribedCustomer.objects.create(
            customer=self.customer,
            subscription=self.subscription,
            subscription_type="Type1",
            end_date=timezone.now() - timezone.timedelta(days=1)
        )
        self.assertEqual(expired_subscription.status, "Expired")

        # Ensure that a new subscription with an end date in the future remains active upon creation
        future_subscription = SubscribedCustomer.objects.create(
            customer=self.customer,
            subscription=self.subscription,
            subscription_type="Type1",
            end_date=timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(future_subscription.status, "Active")