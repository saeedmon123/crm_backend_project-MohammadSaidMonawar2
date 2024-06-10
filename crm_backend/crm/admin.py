from django.contrib import admin
from .models import Customer, Profile,Lead, loyalRedemption,Interaction, Product, Order, OrderItem, Payment, Feedback, Subscription,SubscribedCustomer,LoyaltyThreshold, LoyaltyModel, Promotion, PromotionRedemption

admin.site.register(Customer)
admin.site.register(Lead)
admin.site.register(Interaction)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Subscription)
admin.site.register(LoyaltyModel)
admin.site.register(Promotion)
admin.site.register(PromotionRedemption)
admin.site.register(SubscribedCustomer)
admin.site.register(Profile)
admin.site.register(LoyaltyThreshold)
admin.site.register(loyalRedemption)
