from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    # You can extend this regex to handle various phone number formats.
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_regex(value)

class Subscription(models.Model):
    DURATION_UNIT_CHOICES = [
        ("Days", "Days"),
        ("Months", "Months"),
        ("Years", "Years"),
    ]

    id = models.AutoField(primary_key=True)
    types = models.JSONField(default=list[str])  # Assuming types will be stored as a JSON list
    price = models.JSONField(default=list[int])
    discount=models.JSONField(default=list[int])  # Assuming prices will be stored as a JSON list
    duration = models.IntegerField(null=True)
    duration_unit = models.CharField(max_length=20, choices=DURATION_UNIT_CHOICES,default="Months")

class LoyaltyThreshold(models.Model):
    id = models.AutoField(primary_key=True)
    onepointforXdollar = models.IntegerField()  # Points earned per X dollars spent
    minimum_order_amount = models.FloatField()  # Minimum order amount to earn points
    min_points_to_redeem = models.IntegerField()  # Minimum points required to start redeeming
    points_expiry_days = models.IntegerField()  # Number of days before points expire
    tier_name = models.JSONField()  # List of tier names (e.g., ["Bronze", "Silver", "Gold"])
    points_for_next_tier = models.JSONField()  # List of points required to reach each tier
    tier_discount = models.JSONField()  # List of discount percentages for each tier

    def __str__(self):
        return f"#{self.id}{self.tier_name} Threshold"
    

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_contacted = models.DateTimeField(null=True)
    Subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, default=None)
    LoyaltyThreshold = models.ForeignKey(LoyaltyThreshold, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"Customer {self.pk}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Converted", "Converted")
    ]
    SOURCE_CHOICES = [
        ("Website_Form", "Website_Form"),
        ("Referral", "Referral"),
        ("Cold_Call", "Cold_Call"),
        ("Ads", "Ads"),
    ]

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    

    def __str__(self):
        return f"Lead {self.pk}"


    

class Profile(models.Model):
    ROLE_CHOICES = [
        ("Sales_Representative", "Sales Representative"),
        ("Customer_Support_Agent", "Customer Support Agent"),
        ("Account_Manager", "Account Manager"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ("Phone_Call", "Phone Call"),
        ("Email", "Email"),
        ("Meeting", "Meeting"),
    ]
    
    PARTICIPANT_TYPES_CHOICES = [
        ("Lead", "Lead"),
        ("Customer", "Customer")
    ]
    
    id = models.AutoField(primary_key=True)
    participant_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    participant_id = models.PositiveIntegerField(null=True)
    participant = GenericForeignKey('participant_type', 'participant_id')
    interaction_type = models.CharField(max_length=100, choices=INTERACTION_TYPE_CHOICES, null=True)
    interaction_details = models.TextField(null=True)
    outcome = models.CharField(max_length=100, blank=True)
    responsible_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    interaction_date = models.DateTimeField(null=True)
    follow_up_required=models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)  
    follow_up_notes = models.TextField(blank=True)  

    def schedule_follow_up(self, follow_up_date, follow_up_notes):
        self.follow_up_required = True
        self.follow_up_date = follow_up_date
        self.follow_up_notes = follow_up_notes
        self.save()

    def clear_follow_up(self):
        self.follow_up_required = False
        self.follow_up_date = None
        self.follow_up_notes = ""
        self.save()

    def clean(self):

        if self.participant_type and self.participant_id:
            try:
                participant_class = self.participant_type.model_class()
                participant = participant_class.objects.get(pk=self.participant_id)
            except participant_class.DoesNotExist:
                raise ValidationError("Participant does not exist.")

    def clean(self):
        if self.participant_type == 'Lead':
            try:
                # Fetch the Lead instance based on the provided participant_id
                lead_instance = Lead.objects.get(id=self.participant_id)
                self.participant_id = lead_instance.id  # Assign the ID of the Lead instance
            except Lead.DoesNotExist:
                raise ValidationError('Lead with the provided ID does not exist.')
        elif self.participant_type == 'Customer':
            try:
                # Fetch the Customer instance based on the provided participant_id
                customer_instance = Customer.objects.get(id=self.participant_id)
                self.participant_id = customer_instance.id  # Assign the ID of the Customer instance
            except Customer.DoesNotExist:
                raise ValidationError('Customer with the provided ID does not exist.')

class Promotion(models.Model):
    TYPE_CHOICES = [
        ("Coupon", "Coupon"),
        ("Offer", "Offer"),
        ("Discount_Code", "Discount_Code"),
        # Add more types here if needed
    ]
    DISCOUNT_TYPE_CHOICES = [
        ("Percentage", "Percentage"),
        ("Fixed_Amount", "Fixed_Amount"),
    ]
    CATEGORY_CHOICES = [
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Books", "Books"),
        ("Furniture", "Furniture"),
        ("Food", "Food"),
        ("Toys", "Toys"),
        ("Tools", "Tools"),
        ("Healthcare", "Healthcare"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    start_date = models.DateTimeField()
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Electronics")
    end_date = models.DateTimeField()
    discount_type = models.CharField(max_length=100, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.FloatField()
    expiration_date = models.DateTimeField(null=True,blank=True)
    expired = models.BooleanField(default=False)
    usage_limits = models.IntegerField()

    @classmethod
    def check_usage_limits(cls,promotion_id):
        promotion = cls.objects.get(id = promotion_id)
        if promotion.usage_limits == 0:
            promotion.expiration_date=timezone.now()
            promotion.expired=True
            promotion.save()


class Order(models.Model):
    STATUS_CHOICES = [
        ("UnPaid", "UnPaid"),
        ("Paid", "Paid"),

    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    order_message=models.JSONField(default=dict)
    loyalty_point_used = models.IntegerField(null=True,blank=True,default=0)
    promotion = models.ForeignKey(Promotion,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)


class Product(models.Model):

    COIN_CHOICES = [
        ("US_Dollar", "US_Dollar"),
        ("Euro", "Euro"),
        ("British_Pound", "British_Pound"),
        ("Japanese_Yen", "Japanese_Yen"),
        # Add more coin types here if needed
    ]
    CATEGORY_CHOICES = [
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Books", "Books"),
        ("Furniture", "Furniture"),
        ("Food", "Food"),
        ("Toys", "Toys"),
        ("Tools", "Tools"),
        ("Healthcare", "Healthcare"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Electronics")
    unit_price = models.FloatField()
    quantity_available = models.IntegerField()
    br_code = models.CharField(max_length=100)
    coin_type = models.CharField(max_length=50, choices=COIN_CHOICES,default="US_Dollar")



class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("Credit_Card", "Credit_Card"),
        ("Debit_Card", "Debit_Card"),
        ("PayPal", "PayPal"),
        ("Bank_Transfer", "Bank_Transfer"),
        # Add more payment methods here if needed
    ]

    id = models.AutoField(primary_key=True)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)




class SubscribedCustomer(models.Model):
    SUBSCRIBED_STATUS_CHOICES= [
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
    ]

    id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE,null=True)
    subscription_type=models.CharField(max_length=500,null=True)
    customer= models.ForeignKey(Customer,on_delete=models.CASCADE) # Foreign key referencing Customer
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SUBSCRIBED_STATUS_CHOICES,default="Active")

    def save(self, *args, **kwargs):
        if self.end_date <= timezone.now():
            self.status = "Expired"
        super().save(*args, **kwargs)





class LoyaltyModel(models.Model):
    id = models.AutoField(primary_key=True)
    loyaltyThreshold=models.ForeignKey(LoyaltyThreshold,on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tier = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.loyaltyThreshold:
            # Check if points_expiry_days is set for the associated threshold
            if self.loyaltyThreshold.points_expiry_days:
                expiry_date = self.last_updated + timezone.timedelta(days=self.loyaltyThreshold.points_expiry_days)
                if expiry_date < timezone.now():
                    self.points = 0  # Set points to 0 if expired

        super().save(*args, **kwargs)  # Call the original save method to save the object
        
    
    @classmethod
    def upgrade_tier(cls, loyalty_model_id):
        loyalty_model = LoyaltyModel.objects.get(id=loyalty_model_id)
        current_points = loyalty_model.points
   
        # Ensure loyaltyThreshold is not None
        if loyalty_model.loyaltyThreshold:
            # Iterate over points_for_next_tier and tier_name together
            for points, tier_name in zip(loyalty_model.loyaltyThreshold.points_for_next_tier, loyalty_model.loyaltyThreshold.tier_name):
                if current_points >= points:
                    loyalty_model.tier = tier_name
                    loyalty_model.save()


class loyalRedemption(models.Model):
    id = models.AutoField(primary_key=True)
    LoyaltyModel = models.ForeignKey(LoyaltyModel,on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    points_used = models.IntegerField(blank=True,null=True,default=0)
    redemption_date=models.DateTimeField(auto_now_add=True)


class PromotionRedemption(models.Model):
    id = models.AutoField(primary_key=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    redemption_date = models.DateTimeField(auto_now_add=True)

