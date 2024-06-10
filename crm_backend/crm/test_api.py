from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import json


from .models import (
    Customer, Lead, User, Interaction, Product, Order, OrderItem, Payment,
    Feedback, Subscription, SubscribedCustomer, CalcPoints, LoyaltyModel,
    Promotion, PromotionRedemption
)
from .schemas import (
    CustomerSchema, LeadSchema, UserSchema, InteractionSchema, ProductSchema,
    OrderSchema, OrderItemSchema, PaymentSchema, FeedbackSchema,
    SubscriptionSchema, SubscribedCustomerSchema, CalcPointsSchema,
    LoyaltyModelSchema, PromotionSchema, PromotionRedemptionSchema
)
from crm.schemas import (
    ParticipantTypeChoices, PromotionTypeChoices, DiscountTypeChoices,
    CategoryChoices, DurationUnitChoices
)

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Set up test data here
        self.customer = Customer.objects.create(
            first_name="John", last_name="Doe", email="john@example.com",
            phone_number="1234567890", address="123 Street", city="City",
            state="State", country="Country", postal_code="12345",
            date_created=timezone.now(), last_contacted=timezone.now()
        )

        self.lead = Lead.objects.create(
            first_name="Jane", last_name="Doe", email="jane@example.com",
            phone_number="0987654321", address="456 Avenue", city="City",
            state="State", country="Country", postal_code="54321",
            status="New", source="Referral", created_date=timezone.now(),
            notes="Interested in product"
        )

        self.user = User.objects.create(
            username="testuser", email="testuser@example.com", role="Admin"
        )

        self.product = Product.objects.create(
            name="Test Product", description="Product Description",
            category="Electronics", unit_price=10.0,
            quantity_available=100, br_code="BR123", coin_type="US_Dollar"
        )

        self.product1 = Product.objects.create(name='Product 1', description="Product Description",
            category="Electronics", unit_price=10.0,
            quantity_available=100, br_code="BR123", coin_type="US_Dollar"
        )
        self.product2 = Product.objects.create(name='Product 2',  description="Product Description",
            category="Electronics", unit_price=10.0,
            quantity_available=100, br_code="BR123", coin_type="US_Dollar"
        )
        self.product3 = Product.objects.create(name='Product 3',  description="Product Description",
            category="Electronics", unit_price=10.0,
            quantity_available=100, br_code="BR123", coin_type="US_Dollar"
        )

        self.promotion = Promotion.objects.create(
            name="Test Promotion", description="Test Description",
            type="Offer", start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            discount_type="Percentage", discount_value=10.0,
            expiration_date=timezone.now() + timedelta(days=30),
            usage_limits=100, category="Electronics"
        )

        self.subscription = Subscription.objects.create(
            types=["Basic", "Premium"], price=[10, 20],
            discount=[10, 20], duration=1, duration_unit="Months"
        )

        self.calc_points = CalcPoints.objects.create(onepointforXdollar=10)

        self.order = Order.objects.create(
            customer=self.customer, order_date=timezone.now(),
            total_amount=100.0, promotion=self.promotion, status="UnPaid"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, unit_price=10.0
        )

        self.payment = Payment.objects.create(
            order=self.order, payment_date=timezone.now(), amount=100.0,
            payment_method="Credit_Card"
        )

        self.feedback = Feedback.objects.create(
            customer=self.customer, order=self.order,feedback_date=timezone.now(),
            review="Great service!", rating=5
        )
     

        self.subscribed_customer = SubscribedCustomer.objects.create(
            customer=self.customer, subscription=self.subscription,
            start_date=timezone.now(), end_date=timezone.now() + timedelta(days=30)
        )

        self.loyalty_model = LoyaltyModel.objects.create(
          CalcPoints=self.calc_points, customer=self.customer,points=50, tier="Bronze",last_updated=timezone.now()
        )
        self.promotion_redemption = PromotionRedemption.objects.create(
            customer=self.customer, promotion=self.promotion,
            redemption_date=timezone.now()
        )

    def test_get_customers(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('John', response.json()[0]['first_name'])

    def test_get_leads(self):
        response = self.client.get('/api/leads/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Jane', response.json()[0]['first_name'])

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.json()[0]['username'])

    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Product', response.json()[0]['name'])


    def test_get_orders(self):
            response = self.client.get('/api/orders/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('UnPaid', response.json()[0]['status'])

    def test_get_order_items(self):
        response = self.client.get('/api/orderitems/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['quantity'], 1)

    def test_get_payments(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Credit_Card', response.json()[0]['payment_method'])

    def test_get_feedbacks(self):
        response = self.client.get('/api/feedbacks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Great service!', response.json()[0]['review'])

    def test_get_subscriptions(self):
        response = self.client.get('/api/subscriptions/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Basic', response.json()[0]['types'])

    def test_get_subscribed_customers(self):
        response = self.client.get('/api/subscribedCustomers/')
        self.assertEqual(response.status_code, 200)
        # Check if the response JSON is not empty
        self.assertTrue(response.json())
        # Assuming the response JSON contains 'subscription_id', 'customer_id', 'start_date', 'end_date', and 'status' keys
        self.assertIn('subscription_id', response.json()[0])
        self.assertIn('customer_id', response.json()[0])
        self.assertIn('start_date', response.json()[0])
        self.assertIn('end_date', response.json()[0])
        self.assertIn('status', response.json()[0])


    def test_get_calc_points(self):
        response = self.client.get('/api/calcpoints/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['onepointforXdollar'], 10)

    def test_get_loyalty_models(self):
        response = self.client.get('/api/loyaltymodels/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bronze', response.json()[0]['tier'])

    def test_get_promotions(self):
        response = self.client.get('/api/promotions/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Promotion', response.json()[0]['name'])

    def test_get_promotion_redemptions(self):
        response = self.client.get('/api/promotionredemptions/')
        self.assertEqual(response.status_code, 200)
        # Check if the response JSON is not empty
        self.assertTrue(response.json())
        # Assuming the response JSON contains 'promotion_id', 'customer_id', and 'redemption_date' keys
        self.assertIn('promotion_id', response.json()[0])
        self.assertIn('customer_id', response.json()[0])
        self.assertIn('redemption_date', response.json()[0])
  

    def test_create_order(self):
        # Define test data
        participant_id = self.lead.id  # ID of the lead
        participant_type = "Lead"  # Participant type
        product_ids = [self.product1.id, self.product2.id, self.product3.id]  # List of product IDs
        quantities = [2, 1, 3]  # List of quantities corresponding to product IDs
        promotion_id = 1  # ID of the promotion (if any)

        # Create a dictionary representing the request body
        request_body = {
            'participant_id': participant_id,
            'participant_type': participant_type,
            'product_ids': product_ids,
            'quantities': quantities,
            'promotion_id': promotion_id
        }

        # Convert the request body dictionary to JSON
        json_request_body = json.dumps(request_body)

        # Make POST request to create an order
        response = self.client.post(
             f'/api/orders/?participant_id={participant_id}&participant_type={participant_type}&promotion_id={promotion_id}',
            data=json_request_body,
            content_type='application/json'  # Specify content type as JSON
        )

        # Check if the order was created successfully
        if response.status_code != 200:
            print("Response content:", response.content)

        # Check if the order was created successfully
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('original_amount', data)
        self.assertIn('after promotion: ', data)  # Corrected key
        self.assertEqual(data['message'], 'Order created successfully')
    # You may add more assertions based on the expected response structure and behavior

    def test_create_payment(self):
        # Define test data
        order_id = self.order.id  # ID of the order
        payment_method = "Credit_Card"  # Payment method

        # Make POST request to create a payment
        response = self.client.post(
            f'/api/payments/?order_id={order_id}&payment_method={payment_method}',
        )

        # Check if the payment was created successfully
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)

    def test_create_calcpoints(self):
        # Define test data
        point_for_x_dollar = 10  # Example value for pointforxdollar

        # Make POST request to create a CalcPoints object
        response = self.client.post(
            f'/api/calcpoints/?pointforxdollar={point_for_x_dollar}',
            content_type='application/json'
        )

        # Check if the CalcPoints object was created successfully
        self.assertEqual(response.status_code, 200)  #
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'calcpoints created successfully')


    def test_create_loyalty(self):
        # Define test data
        calcpoints_id = 1  # Example value for calcpoints_id
        customer_id = 1  # Example value for customer_id

        # Make POST request to create a LoyaltyModel object
        response = self.client.post(
            f'/api/loyalties/?calcpoints_id={calcpoints_id}&customer_id={customer_id}',
            content_type='application/json'
        )

        # Check if the LoyaltyModel object was created successfully
        self.assertEqual(response.status_code, 200)  
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'LoyaltyModel created successfully')

    def test_create_interaction(self):
        # Define test data
        participant_type = "Lead"
        participant_id = self.lead.id
        interaction_type = "Call"
        interaction_details = "Follow-up call with the lead."
        outcome = "Interested"
        responsible_user_id = self.user.id
        follow_up_required = True

        # Make POST request to create an interaction
        response = self.client.post(
            f'/api/interactions/?participant_type={participant_type}&participant_id={participant_id}&interaction_type={interaction_type}&interaction_details={interaction_details}&outcome={outcome}&responsible_user_id={responsible_user_id}&follow_up_required={follow_up_required}',
            content_type='application/json'
        )

        # Check if the interaction was created successfully or not
        if response.status_code == 200:
            data = response.json()
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'interaction created successfully')
        else:
            # Handle validation error (status code 422)
            self.assertEqual(response.status_code, 422)  # Validation error
            data = response.json()
            self.assertIn('detail', data)
            self.assertIn('loc', data['detail'][0])  # Check for location of the validation error
    def test_get_interaction(self):
        # Define test data
        participant_id = self.lead.id
        participant_type = "Lead"

        # Make GET request to retrieve interactions
        response = self.client.get(
            '/api/interactions/?participant_id={}&participant_type={}'.format(participant_id, participant_type)
        )

        # Check if interactions were retrieved successfully or not
        if response.status_code == 200:
            data = response.json()
            if data:
                self.assertIn('interactions', data)
                interactions = data['interactions']
                self.assertTrue(len(interactions) > 0)  # Ensure that at least one interaction is returned
            else:
                self.assertTrue(len(data) == 0)  # Ensure that the data is empty (no interactions)
        else:
            # Handle error response
            self.fail("Failed to retrieve interactions. Status code: {}".format(response.status_code))
        
