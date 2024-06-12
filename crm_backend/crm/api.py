from .models import Customer, Lead, Profile,Interaction, Product, Order, OrderItem, Payment, Feedback, Subscription,SubscribedCustomer, LoyaltyModel,LoyaltyThreshold,loyalRedemption,Promotion, PromotionRedemption
from .schemas import  CustomerSchema, LeadSchema,LoyaltyModelSchema, InteractionSchema,  ProductSchema, DurationUnitChoices, OrderSchema,  OrderItemSchema, PaymentSchema, LoyaltyThresholdSchema,FeedbackSchema, loyaltyRedepmtionSchema, SubscriptionSchema,SubscribedCustomerSchema, PromotionSchema,  PromotionRedemptionSchema
from crm.schemas import (
    StatusChoices,
    SourceChoices,
    RoleChoices,
    InteractionTypeChoices,
    ParticipantTypeChoices,
    CoinChoices,
    OrderStatusChoices,
    PaymentMethodChoices,
    SubscriptionStatusChoices,
    PromotionTypeChoices,
    DiscountTypeChoices,
    CategoryChoices,
    DurationUnitChoices,
    PromotionRedemptionFilterSchema
    
)
from crm.schemas import(
    SortingSchema,
    CustomerFilterSchema,
    LeadFilterSchema,
    InteractionFilterSchema,
    ProductFilterSchema,
    OrderFilterSchema,
    OrderItemFilterSchema,
    PaymentFilterSchema,
    FeedbackFilterSchema,
    SubscriptionFilterSchema,
    SubscribedCustomerFilterSchema,
    LoyaltyThresholdFilterSchema,
    LoyaltyModelFilterSchema,
    PromotionFilterSchema,
)
from crm.schemas import(
    CreateOrderSchema,
    update_loyalty,
    update_subscription
)
from typing import List
from django.db import models  
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import  NinjaAPI
from datetime import datetime,timedelta
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import logging
from django.conf import settings
from ninja.errors import HttpError
from ninja import Query
logger = logging.getLogger(__name__)
api = NinjaAPI(title="CRM_BACKEND_PROJECT")

# # lsit of models

# Define the get_data function
def get_data(queryset):
    data = list(queryset.values())  # Convert QuerySet to list of dictionaries
    return data

# Define the get_resource function to handle common retrieval logic
def get_resource(queryset, filters, sorting):
    queryset = filters.filter(queryset)
    if sorting.sort_by:
        sort_order = '' if sorting.sort_order == 'asc' else '-'
        sort_by_field = sorting.sort_by
        queryset = queryset.order_by(f'{sort_order}{sort_by_field}')
    return queryset

@api.get("/customers", response=List[CustomerSchema],tags=["customer"])
@paginate
def get_customers(request, filters: CustomerFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        customers = Customer.objects.all()
        customers = get_resource(customers, filters, sorting)
        return get_data(customers)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/leads", response=List[LeadSchema],tags=["lead"])
@paginate
def get_leads(request, filters: LeadFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        leads = Lead.objects.all()
        leads = get_resource(leads, filters, sorting)
        return get_data(leads)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/interactions", response=List[InteractionSchema],tags=["interaction"])
@paginate
def get_interactions(request, filters: InteractionFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        interactions = Interaction.objects.all()
        interactions = get_resource(interactions, filters, sorting)
        return get_data(interactions)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/products", response=List[ProductSchema],tags=["product"])
@paginate
def get_products(request, filters: ProductFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        products = Product.objects.all()
        products = get_resource(products, filters, sorting)
        return get_data(products)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/orders", response=List[OrderSchema],tags=["order"])
@paginate
def get_orders(request, filters: OrderFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        orders = Order.objects.all()
        orders = get_resource(orders, filters, sorting)
        
        # Ensure that each order has the required fields populated
        orders_data = []
        for order in orders:
            order_data = {
                "id": order.id,  # Add the id field
                "customer_id": order.customer_id,  # Assuming customer is a ForeignKey field
                "loyalty_point_used": order.loyalty_point_used,
                "promotion_id": order.promotion_id,
                "order_date": order.order_date.strftime("%Y-%m-%d"),  # Convert to string format
                "total_amount": order.total_amount,
                "status": order.status,
                # Include other fields from OrderSchema as needed
            }
            orders_data.append(order_data)
        
        return orders_data

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HttpError(500, error_message)
    
@api.get("/orderitems", response=List[OrderItemSchema],tags=["order"])
@paginate
def get_order_items(request, filters: OrderItemFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        order_items = OrderItem.objects.all()
        order_items = get_resource(order_items, filters, sorting)
        
        # Ensure that each order item has the required fields populated
        order_items_data = []
        for item in order_items:
            item_data = {
                "id": item.id,  # Add the id field
                "order_id": item.order_id,  # Assuming order is a ForeignKey field
                "product_id": item.product_id,  # Assuming product is a ForeignKey field
                "quantity": item.quantity,
                "unit_price": item.unit_price,
              
            }
            order_items_data.append(item_data)
        
        return order_items_data

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HttpError(500, error_message)

@api.get("/payments", response=List[PaymentSchema],tags=["payment"])
@paginate
def get_payments(request, filters: PaymentFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        payments = Payment.objects.all()
        payments = get_resource(payments, filters, sorting)
        
        # Ensure that each payment has the required fields populated
        payments_data = []
        for payment in payments:
            payment_data = {
                "id": payment.id,  # Add the id field
                "order_id": payment.order_id,  # Assuming order_id is a ForeignKey field
                "amount": payment.amount,
                "payment_date": payment.payment_date.strftime("%Y-%m-%d"),  # Convert to string format
                "payment_method": payment.payment_method,
                # Include other fields from PaymentSchema as needed
            }
            payments_data.append(payment_data)
        
        return payments_data

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HttpError(500, error_message)

@api.get("/feedbacks", response=List[FeedbackSchema],tags=["order"])
@paginate
def get_feedbacks_order(request, filters: FeedbackFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        feedbacks = Feedback.objects.all()
        feedbacks = get_resource(feedbacks, filters, sorting)
        
        # Ensure that each feedback has the required fields populated
        feedbacks_data = []
        for feedback in feedbacks:
            feedback_data = {
                "id":feedback.id,
                "customer_id": feedback.customer_id,  # Assuming customer_id is a ForeignKey field
                "order_id": feedback.order_id,  # Assuming order_id is a ForeignKey field
                "rating": feedback.rating,
                "review": feedback.review,
                "feedback_date": feedback.feedback_date,  # Convert to string format
                # Include other fields from FeedbackSchema as needed
            }
            feedbacks_data.append(feedback_data)
        
        return feedbacks_data


    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HttpError(500, error_message)

@api.get("/subscriptions", response=List[SubscriptionSchema],tags=["subscription"])
@paginate
def get_subscriptions(request, filters: SubscriptionFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        subscriptions = Subscription.objects.all()
        subscriptions = get_resource(subscriptions, filters, sorting)
        return get_data(subscriptions)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/subscribedCustomers", response=List[SubscribedCustomerSchema],tags=["subscription"])
@paginate
def get_subscribed_customers(request, filters: SubscribedCustomerFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        subscribed_customers = SubscribedCustomer.objects.all()
        subscribed_customers = get_resource(subscribed_customers, filters, sorting)
        return get_data(subscribed_customers)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/loyaltythresholds", response=List[LoyaltyThresholdSchema],tags=["loyalty"])
@paginate
def get_loyalty_thresholds(request, filters: LoyaltyThresholdFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        loyalty_thresholds = LoyaltyThreshold.objects.all()
        loyalty_thresholds = get_resource(loyalty_thresholds, filters, sorting)
        return get_data(loyalty_thresholds)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/loyaltymodels", response=List[LoyaltyModelSchema],tags=["loyalty"])
@paginate
def get_loyalty_models(request, filters: LoyaltyModelFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        loyalty_models = LoyaltyModel.objects.all()
        loyalty_models = get_resource(loyalty_models, filters, sorting)
        return get_data(loyalty_models)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")


@api.get("/promotions", response=List[PromotionSchema],tags=["promotion"])
@paginate
def get_promotions(request, filters: PromotionFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        promotions = Promotion.objects.all()
        promotions = get_resource(promotions, filters, sorting)
        return get_data(promotions)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")

@api.get("/promotionredemptions", response=List[PromotionRedemptionSchema],tags=["promotion"])
@paginate
def get_promotion_redemptions(request, filters: PromotionRedemptionFilterSchema = Query(...), sorting: SortingSchema = Query(...)):
    try:
        promotion_redemptions = PromotionRedemption.objects.all()
        promotion_redemptions = get_resource(promotion_redemptions, filters, sorting)
        return get_data(promotion_redemptions)

    except Exception as e:
        raise HttpError(500, "Internal Server Error, please try again later")



@api.get('/get_interactions_by_id',tags=["interaction"])
def IdInteraction(request, participant_id: int, participant_type: ParticipantTypeChoices):
    try:
        # Get the ContentType object for the provided participant type
        content_type = get_object_or_404(ContentType, model=participant_type.value.lower())

        # Filter interactions based on participant_id and participant_type
        interactions = Interaction.objects.filter(participant_id=participant_id, participant_type=content_type)

        if not interactions.exists():
            return JsonResponse({'message': f'No interactions found for the participant with ID {participant_id} and type {participant_type.value}'}, status=404)

        interaction_data = []
        for interaction in interactions:
            # Serialize responsible user
            responsible_user_data = {
                'username': interaction.responsible_user.username,
            }
            interaction_item = {
                'id': interaction.id,
                'participant_type':content_type.model
                ,
                'participant_id': interaction.participant_id,
                'interaction_type': interaction.interaction_type,
                'interaction_details': interaction.interaction_details,
                'outcome': interaction.outcome,
                'responsible_user': responsible_user_data,  # Serialize responsible user
                'interaction_date': interaction.interaction_date.isoformat(),
                'follow_up_required': interaction.follow_up_required,
            }
            interaction_data.append(interaction_item)

        return JsonResponse({'interactions': interaction_data}, safe=False)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': f'Invalid participant type: {participant_type.value}'}, status=400)

@api.get('/customerprofiles',tags=["customer"])
def get_customer_profiles(request, customer_id: int):
    try:
        # Retrieve customer details
        customer = get_object_or_404(Customer,pk=customer_id)
        customer_data = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone_number': customer.phone_number,
            'address': customer.address,
            'city': customer.city,
            'state': customer.state,
            'country': customer.country,
            'postal_code': customer.postal_code,
            'date_created': customer.date_created.isoformat(),
            'last_contacted': customer.last_contacted.isoformat() if customer.last_contacted else None
        }

        # Retrieve orders for the customer
        orders = Order.objects.filter(customer=customer)
        order_data = []
        for order in orders:
            order_item = {
                'id': order.id,
                'order_date': order.order_date.isoformat(),
                'total_amount': order.total_amount,
                'promotion_id': order.promotion_id,
                'status': order.status,
            }
            order_data.append(order_item)

        # Retrieve interactions for the customer
        interactions = Interaction.objects.filter(participant_id=customer_id)
        interaction_data = []
        for interaction in interactions:
            # Serialize responsible user
            responsible_user_data = {
                'username': interaction.responsible_user.username,
            }
            interaction_item = {
                'id': interaction.id,
                'participant_type': 'Customer',
                'participant_id': interaction.participant_id,
                'interaction_type': interaction.interaction_type,
                'interaction_details': interaction.interaction_details,
                'outcome': interaction.outcome,
                'responsible_user': responsible_user_data,  # Serialize responsible user
                'interaction_date': interaction.interaction_date.isoformat(),
                'follow_up_required': interaction.follow_up_required,
            }
            interaction_data.append(interaction_item)
        return JsonResponse({
            'customer_data': customer_data,
            'order_data': order_data,
            'interaction_data': interaction_data
        }, safe=False)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@api.get('/activesubscriptions/',tags=["subscription"])
def get_active_subscriptions(request):
    try:
        active_subscriptions = SubscribedCustomer.objects.filter(status='Active')
        return get_data(active_subscriptions)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
   



@api.get("/interaction-analysis/",tags=["interaction"])
def interaction_analysis(request):
    try:
        # Example: Count interactions by type
        interaction_type_count = list(Interaction.objects.values('interaction_type').annotate(count=Count('interaction_type')))

        # Example: Count interactions by outcome
        outcome_count = list(Interaction.objects.values('outcome').annotate(count=Count('outcome')))

        # Example: Count interactions by responsible user
        user_count = list(Interaction.objects.values('responsible_user__username').annotate(count=Count('responsible_user')))

        return {
            "interaction_type_count": interaction_type_count,
            "outcome_count": outcome_count,
            "user_count": user_count
        }
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#-----------------------------------------------
#creation:
@api.patch("/customers/{customer_id}/loyalty", tags=["customer"])
def update_customer_loyalty(request, data: update_loyalty):
    '''  update the customer loyalty based on the customer_id  '''
    try:
        # Retrieve the existing customer object
        customer = Customer.objects.get(pk=data.customer_id)

        if data.LoyaltyThreshold_id != 0 and customer.LoyaltyThreshold is None:
            loyalty_model_info = create_loyalty_model(data.LoyaltyThreshold_id, customer.id)
            if 'error' in loyalty_model_info:
                return JsonResponse(loyalty_model_info, status=loyalty_model_info['status'])
            
            customer.LoyaltyThreshold = LoyaltyThreshold.objects.get(pk=data.LoyaltyThreshold_id)
            customer.save()

        elif data.LoyaltyThreshold_id != 0 and customer.LoyaltyThreshold is not None:
            loyalty_model=LoyaltyModel.objects.get(customer = customer)
            loyalty_model.delete()
            customer.save()
            loyalty_model_info = create_loyalty_model(data.LoyaltyThreshold_id, customer.id)
            if 'error' in loyalty_model_info:
                return JsonResponse(loyalty_model_info, status=loyalty_model_info['status'])

            customer.LoyaltyThreshold = LoyaltyThreshold.objects.get(pk=data.LoyaltyThreshold_id)
            customer.save()

        # Save the updated customer object
        customer.save()

        return JsonResponse({'message': 'Customer loyalty updated successfully', 'customer_id': customer.id}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.patch("/customers/{customer_id}/subscription", tags=["customer"])
def update_customer_subscription(request, data: update_subscription):
    '''  update the customer subscription based on the customer_id  '''
    try:
        # Retrieve the existing customer object
        customer = Customer.objects.get(pk=data.customer_id)

        # Handle Subscription
        if data.Subscription_id != 0:
            if data.Subscription_type == "string":
                return JsonResponse({"error": "please check that you put suitable subscription id as well"}, status=404)
            subscription_info = create_customer_subscription(customer.id, data.Subscription_id, data.Subscription_type)
            if 'error' in subscription_info:
                return JsonResponse(subscription_info, status=subscription_info['status'])
            customer.Subscription = Subscription.objects.get(pk=data.Subscription_id)
        else:
            if customer.Subscription is not None:
                subscribed_customer = SubscribedCustomer.objects.get(customer=customer)
                subscribed_customer.delete()

        # Save the updated customer object
        customer.save()

        return JsonResponse({'message': 'Customer subscription updated successfully', 'customer_id': customer.id}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api.post("/customers/", tags=["customer"])
def create_customer(request, data: CustomerSchema):
    "creation of customer: can create without loyalty and subscription"
    try:
        # Extract the data dictionary from the schema
        customer_data = data.dict()

        # Check and replace 0 values with None for foreign key fields
        if customer_data['LoyaltyThreshold_id'] == 0:
            customer_data['LoyaltyThreshold_id'] = None
        if customer_data['Subscription_id'] == 0:
            customer_data['Subscription_id'] = None
        if customer_data['Subscription_type'] == "string":
            customer_data['Subscription_type'] = None
        if customer_data['Subscription_id'] is None and customer_data['Subscription_type'] is not None:
            return JsonResponse({'error': 'Both Subscription ID and subscription type must be provided or both must be None'}, status=400)
        
        subscription_type = customer_data.pop('Subscription_type', None)
 
        # Create a new customer using the validated data
        customer = Customer.objects.create(**customer_data)
        
        # Create loyalty model if LoyaltyThreshold_id is provided
        if customer_data['LoyaltyThreshold_id'] is not None:
            loyalty_model_info = create_loyalty_model(data.LoyaltyThreshold_id, customer.id)
            if 'error' in loyalty_model_info:
                # Delete the customer if an error occurs
                customer.delete()
                return JsonResponse(loyalty_model_info, status=loyalty_model_info['status'])
            
        if customer_data['Subscription_id'] is not None:
            if subscription_type is None:
                # Delete the customer if subscription type is not found
                customer.delete()
                return JsonResponse({'error': 'subscription type not found'}, status=404)
          
            subscription_info = create_customer_subscription(customer.id,data.Subscription_id,subscription_type)
            if 'error' in subscription_info:
                # Delete the customer if an error occurs
                customer.delete()
                return JsonResponse(subscription_info, status=subscription_info['status'])

        return JsonResponse({'message': 'Customer created successfully', 'customer_id': customer.id}, status=201)
    except Exception as e:
       customer.delete()
       return JsonResponse({'error': str(e)}, status=500)
    

@api.post("/orders/", tags=["order"])
def create_order(request, payload: CreateOrderSchema):
    ''' creat_order: if lead create the order the lead status become converted and all his data turn to customer with no subscription and no loyalty'''
    try:
        # Extract data from the payload
        participant_id = payload.participant_id
        participant_type = payload.participant_type
        product_ids = payload.product_ids
        quantities = payload.quantities
        promotion_id = payload.promotion_id
        UseLoyalty = payload.UseLoyalty
        RedeemPoints = payload.RedeemPoints

        

        # Check product availability before starting the transaction
        for product_id, quantity in zip(product_ids, quantities):
            product = Product.objects.filter(id=product_id).first()
            if quantity == 0:
                return JsonResponse({'error': f"can't order product witht 0 quantity"}, status=404)
            if not product:
                return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=404)
            if product.quantity_available < quantity:
                return JsonResponse({'error': f'The product {product.id} with the name {product.name} currently has only {product.quantity_available} units available in stock.'}, status=404)

        with transaction.atomic():
            if UseLoyalty == False and RedeemPoints != 0:
                return JsonResponse({'message': 'Cannot redeem points without using loyalty.'}, status=400)

            # Check if the provided promotion exists
            promotion = None
            if promotion_id:
                promotion = Promotion.objects.filter(id=promotion_id, expired=False).first()
                if not promotion:
                    return JsonResponse({'error': 'Promotion not found or expired'}, status=404)

            # Check if the participant is a lead or a customer
            if participant_type == ParticipantTypeChoices.Lead:
                lead = Lead.objects.filter(id=participant_id).first()
                if not lead:
                    return JsonResponse({'error': 'Lead not found'}, status=404)
                if lead.status != "Converted":
                    # Create a customer based on lead data if not already converted
                    customer = Customer.objects.create(
                        first_name=lead.first_name,
                        last_name=lead.last_name,
                        email=lead.email,
                        phone_number=lead.phone_number,
                        address=lead.address,
                        city=lead.city,
                        state=lead.state,
                        country=lead.country,
                        postal_code=lead.postal_code,
                        Subscription=None,
                        LoyaltyThreshold=None
                    )
                    customer.date_created = timezone.now()
                    customer.last_contacted = timezone.now()
                    lead.status = "Converted"
                    lead.save()
                else:
                    return JsonResponse({'message': 'The lead is already converted'})
            else:
                # Retrieve the customer if participant is not a lead
                customer = Customer.objects.filter(id=participant_id).first()
                if not customer:
                    return JsonResponse({'error': 'Customer not found'}, status=404)

            # Create a dictionary
            order_message_dict = {"key": "value"}

            # Serialize the dictionary to JSON
            order_message_json = json.dumps(order_message_dict)

            # Create the order with the serialized JSON as the order_message
            order = Order.objects.create(
                customer=customer,
                order_date=timezone.now(),
                total_amount=0,
                order_message=order_message_json,  # Assign the serialized JSON
                promotion=promotion,
                loyalty_point_used=RedeemPoints,
                status="UnPaid"
            )

            # Initialize total_amount and discount_amount
            total_amount = 0
            discount_amount = 0

            # Create order items and calculate total amount
            for product_id, quantity in zip(product_ids, quantities):
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=404)
                total_amount += quantity * product.unit_price

                # Apply promotion discount if applicable
                if promotion and promotion.category == product.category:
                    discount = calculate_discount(product.unit_price, promotion.discount_type, promotion.discount_value)
                    discount_amount += min(discount * quantity, product.unit_price * quantity)

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.unit_price
                )

            # Calculate total amount after discounts
            original_amount = total_amount
            total_amount -= discount_amount

            # Apply subscription discount if applicable
            subscribed_customer = SubscribedCustomer.objects.filter(customer=customer, status="Active").first()
            if subscribed_customer:
                subscription = subscribed_customer.subscription
                subscription_index = subscription.types.index(subscribed_customer.subscription_type)
                subscription_discount = subscription.discount[subscription_index]
                total_amount -= total_amount * (subscription_discount / 100)

            # Update total amount in the order
            order.total_amount = total_amount
            order.save()

            if UseLoyalty:
                loyaltymodel = get_object_or_404(LoyaltyModel, customer=customer)
                if loyaltymodel.loyaltyThreshold.minimum_order_amount > total_amount:
                    return JsonResponse({"message": f"you don't reach the minimum order amount to use loyal points the minimum order points is {loyaltymodel.loyaltyThreshold.minimum_order_amount}"})

            # Return response
            response_data = {'message': 'Order created successfully', 'original_amount': original_amount}
            if promotion_id and not subscribed_customer:
                response_data['after_promotion'] = total_amount
            elif subscribed_customer and not promotion_id:
                response_data['after_subscription_discount'] = total_amount
            elif subscribed_customer and promotion_id:
                response_data['after_promotion_and_subscription_discount'] = total_amount

            if UseLoyalty:
                loyaltymodel = get_object_or_404(LoyaltyModel, customer=customer)

                min_point_to_redeem = loyaltymodel.loyaltyThreshold.min_points_to_redeem
                # Check if the points to redeem are valid
                if RedeemPoints >= min_point_to_redeem:
                    total_amount = redeem_points(loyaltymodel.id, RedeemPoints, total_amount)
                else:
                    return JsonResponse({"message": f"you don't reach the minimum point to redeem {min_point_to_redeem}"})

                # Update the total amount in the order
                order.total_amount = total_amount
                order.save()

                # Include the total amount after loyalty in the response data
                response_data['after_loyalty'] = total_amount

            order.order_message = response_data
            order.save()
            return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.post('/loyaltythresholds/',tags=["loyalty"])
def create_loyalty_threshold(request, payload: LoyaltyThresholdSchema):
    '''Creates roles for loyalty program.

    Attributes:
        onepointforXdollar (int): Determines points earned per dollar spent.
        minimum_order_amount (float): Sets minimum spend to earn points.
        min_points_to_redeem (int): Minimum points required for redemption.
        points_expiry_days (int): Points expiration period in days.
        tier_name (list): Names of loyalty tiers.
        points_for_next_tier (list): Points needed for next loyalty tier.
        tier_discount (list): Discount percentage for each loyalty tier.
    '''
    try:
        # Create LoyaltyThreshold
        loyalty_threshold = LoyaltyThreshold.objects.create(
            onepointforXdollar=payload.onepointforXdollar,
            minimum_order_amount=payload.minimum_order_amount,
            min_points_to_redeem=payload.min_points_to_redeem,
            points_expiry_days=payload.points_expiry_days,
            tier_name=payload.tier_name,
            points_for_next_tier=payload.points_for_next_tier,
            tier_discount=payload.tier_discount,

        )
        return {'message': 'LoyaltyThreshold created successfully', 'id': loyalty_threshold.id}
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def create_loyalty_model(loyalty_threshold_id: int, customer_id: int):
    try:
        # Fetch the LoyaltyThreshold and Customer instances
        loyalty_threshold = get_object_or_404(LoyaltyThreshold, id=loyalty_threshold_id)
        customer = get_object_or_404(Customer, id=customer_id)

        # Create LoyaltyModel
        loyalty_model = LoyaltyModel.objects.create(
            loyaltyThreshold=loyalty_threshold,
            customer=customer,
            tier=loyalty_threshold.tier_name[0],  # Set initial tier to the first tier name
            points=0,
            last_updated=timezone.now()
        )
        return {'message': 'LoyaltyModel created successfully', 'id': loyalty_model.id}
    
    except LoyaltyThreshold.DoesNotExist:
        return {"error": "LoyaltyThreshold not found", 'status': 404}
    
    except Customer.DoesNotExist:
        return {"error": "Customer not found", 'status': 404}

@api.post('/payments/',tags=["payment"])
def create_payment(request, order_id: int, payment_method: PaymentMethodChoices):
    ''' create payment of the order created '''
    try:
        with transaction.atomic():
            order = get_object_or_404(Order, id=order_id)
            if order.status == 'Paid':
                return JsonResponse({'message': 'The order is already paid'})

            order.status = "Paid"
            order.save()

            loyalty_model = LoyaltyModel.objects.filter(customer=order.customer).first()
            if loyalty_model:
                if order.loyalty_point_used:
                    if loyalty_model.points >= order.loyalty_point_used:
                        loyalty_model.points -= order.loyalty_point_used
                        loyalty_model.save()

                        loyalRedemption.objects.create(
                            LoyaltyModel=loyalty_model,  # Use the LoyaltyModel instance directly
                            Customer=order.customer,  # Use the Customer instance directly
                            points_used=order.loyalty_point_used,
                            redemption_date=timezone.now()
                        )
                    else:
                        return JsonResponse({'message': f'Not enough loyalty points. You have only {loyalty_model.points} points'}, status=400)

                total_amount = order.total_amount

                loyalty_model.points += total_amount // loyalty_model.loyaltyThreshold.onepointforXdollar
                loyalty_model.save()
                loyalty_model.last_updated = timezone.now()
                loyalty_model.save()
                loyalty_model.upgrade_tier(loyalty_model_id=loyalty_model.id)

            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.quantity_available -= item.quantity
                product.save()

            promotion = order.promotion
            if promotion:
                promotion.usage_limits -= 1
                promotion.save()
                Promotion.check_usage_limits(promotion.id)

                PromotionRedemption.objects.create(
                    promotion=promotion,  # Use the promotion instance directly
                    customer=order.customer,  # Use the customer instance directly
                    redemption_date=timezone.now()
                )

            Payment.objects.create(
                order=order,
                amount=order.total_amount,
                payment_date=timezone.now(),
                payment_method=payment_method.value,
            )
            
            try:
                send_payment_notification(order.customer, order, loyalty_model, order.order_message)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            return JsonResponse({'message': 'Payment created successfully, loyalty points updated, order items quantity updated'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.post('/interactions/',tags=["interaction"])
def create_interaction(request, participant_type: ParticipantTypeChoices, participant_id: int, interaction_type: InteractionTypeChoices, interaction_details: str, outcome: str, responsible_user: str):
    ''' create the interaction if lead make interaction-> lead.status = contacted and if customer update last_contacted'''
    participant_type_str = participant_type.value
    participant_model = None
    if participant_type_str == 'Lead':
        participant_model = Lead
    elif participant_type_str == 'Customer':
        participant_model = Customer
    else:
        # Handle invalid participant type
        return JsonResponse({'message': 'Invalid participant type'}, status=400)

    try:
        participant_content_type = ContentType.objects.get_for_model(participant_model)
    except ContentType.DoesNotExist:
        return JsonResponse({'message': 'Participant content type not found'}, status=400)

    try:
        user = User.objects.get(username=responsible_user)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Responsible user not found'}, status=400)

    try:
        # Create the interaction
        interaction = Interaction.objects.create(
            participant_type=participant_content_type,
            participant_id=participant_id,
            interaction_type=interaction_type.value,
            interaction_details=interaction_details,
            outcome=outcome,
            responsible_user=user,
            interaction_date=timezone.now(),
        )

        # Update lead status or customer last_contacted based on participant type
        if participant_type_str == 'Lead':
            # Update lead status
            try:
                lead = get_object_or_404(Lead,pk=participant_id)
                lead.status = "Contacted"
                lead.save()
            except Lead.DoesNotExist:
                return JsonResponse({'message': 'Lead not found'}, status=400)
        elif participant_type_str == 'Customer':
            # Update customer last_contacted
            try:
                customer = get_object_or_404(Customer,pk=participant_id)
                customer.last_contacted = timezone.now()
                customer.save()
            except Customer.DoesNotExist:
                return JsonResponse({'message': 'Customer not found'}, status=400)

        return JsonResponse({'message': 'Interaction created successfully'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@api.post('/followup/',tags=["interaction"])
def need_followup(request, interaction_id: int, follow_up_date: datetime, follow_up_note: str):
    ''' if the interaction need follow up '''
    try:
        interaction = get_object_or_404(Interaction, id=interaction_id)
        interaction.schedule_follow_up(follow_up_date, follow_up_note)
        return JsonResponse({'message': 'Follow-up created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.delete('/clearfollowup',tags=["interaction"])
def clear_followup(request, interaction_id: int):
    ''' delete the follow up when it's done '''
    try:
        interaction = get_object_or_404(Interaction, id=interaction_id)
        interaction.clear_follow_up()
        return JsonResponse({'message': 'Follow-up cleared successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.post('/promotions/',tags=["promotion"])
def create_promotion(request, name: str, description: str, type: PromotionTypeChoices, start_date: datetime, end_date: datetime, discount_type: DiscountTypeChoices, discount_value: float, usage_limits: int, category: CategoryChoices):
    ''' create promtion to give discount for each product the customer pay based on it's category '''
    try:
        promotion = Promotion.objects.create(
            name=name,
            description=description,
            type=type.value,  
            start_date=start_date,
            end_date=end_date,
            discount_type=discount_type.value,  
            discount_value=discount_value,
            expiration_date=None,
            usage_limits=usage_limits,
            category=category.value  
        )
        return JsonResponse({'message': 'Promotion created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api.post('/subscriptions/',tags=["subscription"])
def create_subscription(request,types:list[str],prices:list[int],discounts:list[int],duration:int,duration_unit:DurationUnitChoices):
    '''Create a subscription.

    Args:
        types (list[str]): List of subscription types.
        prices (list[int]): List of prices corresponding to each subscription type.
        discounts (list[int]): List of discounts corresponding to each subscription type.
        duration (int): Duration of the subscription.
        duration_unit (DurationUnitChoices): Unit of the subscription duration (e.g., days, months).

    Explanation:
        - `types`, `prices`, and `discounts` are parallel lists where each type is followed by its price and discount.
        - The discount is deducted from the total amount of the order.
    '''
    try:
        Subscription.objects.create(
            types=types,
            price=prices,
            discount=discounts,
            duration=duration,
            duration_unit=duration_unit.value
        )
        return JsonResponse({'message': 'Subscription created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def create_customer_subscription(customer_id:int,subscription_id:int,subscription_type:str):
    '''Subscribe a customer to a specific subscription.

    Args:
        customer_id (int): The ID of the customer to subscribe.
        subscription_id (int): The ID of the subscription to subscribe the customer to.
        subscription_type (str): The type of subscription to subscribe the customer to.

    Explanation:
        - The subscription type must be one of the types associated with the given subscription ID.
        - Checks if the customer is already subscribed to the subscription. If yes, returns an error.
        - Calculates the end date of the subscription based on the subscription's duration and duration unit.
        - Creates a new subscription record for the customer with the specified details.
    '''
    try:
        
        try:
            customer = get_object_or_404(Customer,id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        try:
            subscription = get_object_or_404(Subscription,id=subscription_id)
        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'Subscription not found'}, status=404)

        if subscription_type not in subscription.types:
            return JsonResponse({'error': f'the subscription type you inserted is not existed in the types of the subscription of id {subscription_id}'}, status=404)
   
        # Check if the customer is already subscribed to this subscription
        existing_subscription = SubscribedCustomer.objects.filter(customer=customer, subscription=subscription, subscription_type=subscription_type, status="Active").exists()
        if existing_subscription:
            return JsonResponse({'error': 'Customer is already subscribed to this subscription'}, status=400)
    
        if subscription.duration_unit == DurationUnitChoices.Days.value:
            end_date = timezone.now() + timedelta(days=subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Months.value:
            end_date = timezone.now() + timedelta(days=30 * subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Years.value:
            end_date = timezone.now() + timedelta(days=365 * subscription.duration)
        else:
            return JsonResponse({'error': 'Invalid duration unit for subscription'}, status=400)
       
        SubscribedCustomer.objects.create(
            customer = customer,
            subscription=subscription,
            subscription_type=subscription_type,
            start_date=timezone.now(),
            end_date=end_date,
            status="Active"
        )

        return JsonResponse({'message': 'customer subscribed  successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    

@api.post('/feedbacks/',tags=["order"])
def create_feedback_order(request, customer_id: int, order_id: int, rating: int, review: str):
    '''Create feedback for a paid order.

    Args:
        customer_id (int): The ID of the customer providing the feedback.
        order_id (int): The ID of the order to provide feedback for.
        rating (int): The rating given for the order (should be between 1 and 5).
        review (str): The review or comment provided for the order.

    Explanation:
        - Validates if the rating provided is between 1 and 5.
        - Retrieves the customer and order objects based on the provided IDs.
        - Verifies if the order belongs to the customer.
        - Creates a new feedback object for the order with the provided rating and review.
    '''
    # Validation: Check if rating is between 1 and 5
    if not 1 <= rating <= 5:
        return JsonResponse({'error': 'Rating should be between 1 and 5'}, status=400)
    
    try:
        # Retrieve Customer and Order objects
        customer = get_object_or_404(Customer, id=customer_id)
        order = get_object_or_404(Order, id=order_id)
        
        # Verify if the order belongs to the customer
        if order.customer != customer:
            return JsonResponse({'error': 'The order does not belong to this customer'}, status=404)

        # Create Feedback object
        feedback = Feedback.objects.create(
            customer=customer,
            order=order,
            rating=rating,
            review=review
        )

        return JsonResponse({'message': 'Feedback created successfully', 'feedback_id': feedback.id})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer does not exist'}, status=404)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order does not exist'}, status=404)




@api.post('/profiles')
def create_profile(request,    username: str,role: RoleChoices):
    '''Create a profile and assign a role to a Django built-in user.

    Args:
        username (str): The username of the Django built-in user.
        role (RoleChoices): The role to assign to the user.

    Explanation:
        - Retrieves the Django built-in user instance based on the provided username.
        - Creates a new profile instance for the user with the specified role.
    '''
    try:
        # Get the admin User instance
        admin_user = get_object_or_404(User,username=username)
        
        # Create the Profile instance with the provided role for the admin user
        Profile.objects.create(user=admin_user, role=role.value)
        
        return JsonResponse({'message': 'Profile created successfully'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Admin user not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



#update

@api.patch('/renewals/',tags=["subscription"])
def renew_subscription(request, customer_id: int, subscription_id: int):
    '''Reactivate a subscription if it's deactivated.

    Args:
        customer_id (int): The ID of the customer whose subscription needs to be renewed.
        subscription_id (int): The ID of the subscription to be renewed.

    Explanation:
        - Retrieves the customer and subscription instances based on the provided IDs.
        - Checks if the customer is subscribed to the subscription.
        - Updates the subscription status to "Active" and recalculates the subscription end date.
    '''
    try:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'Subscription not found'}, status=404)


        try:
            subscribedCustomer = SubscribedCustomer.objects.get(customer=customer)
        except SubscribedCustomer.DoesNotExist:
            return JsonResponse({'error':'customer is not susbscribed'})
        
        subscribedCustomer.status="Active"
        subscribedCustomer.start_date=timezone.now()
        if subscription.duration_unit == DurationUnitChoices.Days.value:
            end_date = timezone.now() + timedelta(days=subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Months.value:
            end_date = timezone.now() + timedelta(days=30 * subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Years.value:
            end_date = timezone.now() + timedelta(days=365 * subscription.duration)
        
        subscribedCustomer.end_date=end_date
        subscribedCustomer.save()



        return JsonResponse({'message': 'Subscription renewed successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#New Function 
#=========================

#1-Adjust Pricing
           
@api.get("/adjust-pricing/")
def adjust_pricing(request,lt_quantity:int,increased_percnetage:float):
    '''Adjust pricing based on quantity of products.

    Args:
        lt_quantity (int): The threshold quantity. If the quantity of any product is less than this threshold, its price will be adjusted.
        increased_percentage (float): The percentage increase in price as a decimal (e.g., 0.1 for 10% increase).

    Explanation:
        - Checks if the quantity of any product is less than the threshold quantity.
        - If so, increases the price of the product by the specified percentage.
    '''
    response_data = {'message': 'product updated successfully'}

    products = Product.objects.all()
    for product in products:
        if product.quantity_available < lt_quantity:
            product.unit_price *= increased_percnetage
            product.save()
            response_data[f'{product.name} price updated to'] = product.unit_price

    return JsonResponse(response_data)

#2 function Product Recommendation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@api.get("/recommend-products",tags=["customer"])
def recommend_products(request, customer_id: int):
    '''Recommend products to a customer based on their past purchases.

    Args:
        customer_id (int): The ID of the customer for whom product recommendations are generated.

    Returns:
        A JSON response containing a list of recommended products.

    Explanation:
        - Retrieve the customer's past orders.
        - Extract product IDs from the order items of the customer's past orders.
        - Generate recommendations based on the customer's past purchases.
        - Construct a list of dictionaries containing recommended product information (ID and name).
        - Return the list of recommended products in a JSON response.
    '''
    customer = get_object_or_404(Customer, id=customer_id)
    customer_orders = Order.objects.filter(customer=customer)
    product_ids = OrderItem.objects.filter(order__in=customer_orders).values_list('product', flat=True)
    
    # Vectorize all products
    product_vectors = get_all_product_vectors()
    
 # Generate recommendations based on the customer's past purchases
    recommendations = generate_recommendations(product_vectors, product_ids)
    
    # Construct a list of dictionaries containing recommended product information
    recommended_products = []
    for recommendation in recommendations:
        product = get_object_or_404(Product, id=recommendation)
        recommended_products.append({
            "id": recommendation,
            "name": product.name
        })
        
    # Return the list of recommended products in a JSON response
    return JsonResponse({"Recommendations": recommended_products})

def get_all_product_vectors():
    '''Get vectors for all products.

    Returns:
        A dictionary where keys are product IDs and values are product vectors containing product information.
    '''
    products = Product.objects.all()
    product_vectors = {}
    
    for product in products:
        product_vector = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'unit_price': product.unit_price,
            'quantity_available': product.quantity_available,
            'br_code': product.br_code,
            'coin_type': product.coin_type
        }
        product_vectors[product.id] = product_vector

    return product_vectors

def generate_recommendations(product_vectors, purchased_product_ids):
    '''Generate product recommendations based on past purchases.

    Args:
        product_vectors (dict): Dictionary containing vectors for all products.
        purchased_product_ids (list): List of product IDs purchased by the customer.

    Returns:
        A list of recommended product IDs.

    Explanation:
        - Extract features for vectorization (category and description).
        - Combine all features into a single feature vector for each product.
        - Calculate similarity scores between products.
        - Generate recommendations based on similarity scores, excluding already purchased products.
    '''
    product_data = list(product_vectors.values())
    
    # Extract features for vectorization
    categories = [p['category'] for p in product_data]
    descriptions = [p['description'] for p in product_data]
    
    category_encoder = OneHotEncoder()
    category_features = category_encoder.fit_transform([[cat] for cat in categories]).toarray()
    
    description_vectorizer = TfidfVectorizer()
    description_features = description_vectorizer.fit_transform(descriptions).toarray()
    
    # Combine all features
    all_features = []
    for i, product in enumerate(product_data):
        numerical_features = [product['unit_price'], product['quantity_available']]
        combined_features = numerical_features + list(category_features[i]) + list(description_features[i])
        all_features.append(combined_features)
    
    # Convert to dictionary for easier indexing
    feature_dict = {product_data[i]['id']: all_features[i] for i in range(len(product_data))}

    recommendations = []
    for product_id in feature_dict:
        if product_id in purchased_product_ids:
            continue

        similarity_scores = calculate_similarity(feature_dict[product_id], feature_dict)
        
        # Get recommendations excluding already purchased products
        recommend_products = [(id, score) for id, score in similarity_scores.items() if id not in purchased_product_ids]

        recommend_products.sort(key=lambda x: x[1], reverse=True)
        recommendations.extend(recommend_products[:10])

    # Deduplicate recommendations
    unique_recommendations = list({rec[0]: rec for rec in recommendations}.values())
    
    return [rec[0] for rec in unique_recommendations[:10]]

def calculate_similarity(vector1, vectors):
    '''Calculate cosine similarity between two vectors.

    Args:
        vector1 (list): Feature vector of a product.
        vectors (dict): Dictionary containing feature vectors of products.

    Returns:
        Dictionary containing similarity scores between the given vector and all other vectors.
    '''
    similarities = cosine_similarity([vector1], list(vectors.values()))
    similarity_scores = {id: score for id, score in zip(vectors.keys(), similarities[0])}
    return similarity_scores


#3 Sales_forecase
from statsmodels.tsa.arima.model import ARIMA
from django.db.models import Sum

from django.core.exceptions import ValidationError
@api.get("/sales_forecase")
def sales_forecast(request,category:CategoryChoices):
    '''Generate sales forecast for a specific product category.

    Args:
        category (CategoryChoices): The category for which sales forecast is generated.

    Returns:
        A JSON response containing the forecasted sales data.

    Explanation:
        - Retrieve historical sales data for the specified category.
        - Calculate total sales for each date in the historical data.
        - Fit an ARIMA model to the historical sales data.
        - Generate sales forecast for the next 30 days.
        - Return the forecasted sales data in a JSON response.
    '''
    try:
            historical_sales = Order.objects.filter(
            order_date__lt=timezone.now(),
            orderitem__product__category=category
            ).distinct()
    
            sales_data = historical_sales.values('order_date').annotate(total_sales=Sum('total_amount'))

            if len(sales_data) <= 0:
                    return JsonResponse({"error": "Insufficient historical sales data for forecasting"}, status=400)

            dates = [entry['order_date'] for entry in sales_data]
            sales = [entry['total_sales'] for entry in sales_data]

            model= ARIMA(sales,order=(5,1,0))
            model_fit=model.fit()
            forecast=model_fit.forecast(steps=30)

            future_dates=[max(dates) + timedelta(days=i) for i in range(1,31)]

            forecast_data = [{'date':date.strftime('%Y-%m-%d'), 'forecasted_sales':round(sales)}for date,sales in zip(future_dates,forecast)]

            return JsonResponse({"category: ":category,"forecast:":forecast_data})
        
    except ValidationError as ve:
        return JsonResponse({"error": str(ve)}, status=400)

    except Exception as e:
        return JsonResponse({"error": "An error occurred while processing the request"}, status=500)







#function to used
#---------------------------------
def calculate_discount(total_amount: float, discount_type: str, discount_value: float) -> float:
    if discount_type == "Percentage":
        discount_amount = total_amount * (discount_value / 100)
    elif discount_type == "Fixed_Amount":
        discount_amount = discount_value
    else:
        raise ValueError("Invalid discount type")
    
    return discount_amount


def redeem_points(loyalty_model_id: int, points_to_redeem: int, total_amount: float) -> float:
    try:
        # Get the LoyaltyModel instance
        loyalty_model = LoyaltyModel.objects.get(id=loyalty_model_id)

        # Check if the loyalty model exists
        if loyalty_model:
            current_points = loyalty_model.points
       
            # Check if the points to redeem are valid
            if points_to_redeem <= current_points:
                tier_index = loyalty_model.loyaltyThreshold.tier_name.index(loyalty_model.tier)
                discount = loyalty_model.loyaltyThreshold.tier_discount[tier_index]

                discounted_amount = points_to_redeem*discount


                # Calculate the discounted total amount
                total_amount -= discounted_amount
           
                return total_amount
             
            else:
                raise ValueError(f"You don't have enough points to redeem {points_to_redeem} points.")
        else:
            raise ValueError("Loyalty model not found.")
    except LoyaltyModel.DoesNotExist:
        raise ValueError("Loyalty model not found.")
    except Exception as e:
        raise ValueError(str(e))
    



from django.core.mail import EmailMessage
from django.conf import settings
import logging


def send_payment_notification(customer, order, loyalty_model=None,order_message=dict):
    try:
        subject = 'Payment Confirmation'

        # Format order items
        order_items = OrderItem.objects.filter(order=order)
        item_details = "\n".join([
            f"<tr><td>{item.product.name}</td><td>{item.quantity}</td><td>${item.unit_price:.2f}</td></tr>"
            for item in order_items
        ])

        message = f"""
        <html>
        <body>
        <p>Dear {customer.first_name} {customer.last_name},</p>

        <p>Thank you for your payment.</p>

        <p>Here are the details of your purchase:</p>

        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Order ID</th>
                <td>{order.id}</td>
            </tr>
            <tr>
                <th>Date</th>
                <td>{order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>
        </table>

        <h3>Items:</h3>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Product Name</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
            {item_details}
        </table>

        """
        if order_message:
            message += "<h3>Order Details:</h3>"
            for key, value in order_message.items():
                if key != "message":
                    message += f"<p><strong>{key.capitalize()}:</strong> {value}</p>"
                
        # Add loyalty points information if available
        if loyalty_model:
            loyalty_points_earned = order.total_amount // loyalty_model.loyaltyThreshold.onepointforXdollar
            message += f"""
            <p><strong>Loyalty Points Used:</strong> {order.loyalty_point_used}</p>
            <p><strong>Loyalty Points Earned:</strong> {loyalty_points_earned}</p>
            """

        message += """
        <p>If you have any questions, please contact our support team.</p>

        <p>Best regards,<br>Your Company Name</p>
        </body>
        </html>
        """
    
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer.email]
        )
        email_message.content_subtype = "html"  # Main content is now text/html

        # Set SMTP server settings
        email_message.extra_headers = {'X-SMTPAPI': '{"category": "PaymentNotification"}'}
        email_message.send()

        logger.info(f"Payment notification sent to {customer.email} successfully.")

    except Exception as e:
        logger.error(f"Failed to send payment notification to {customer.email}: {str(e)}")
        raise  # Re-raise the exception for the caller to handle