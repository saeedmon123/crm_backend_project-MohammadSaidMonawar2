from django.core.management.base import BaseCommand
from crm.models import Product
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Check inventory levels and send alerts if stock is low'

    def handle(self, *args, **kwargs):
        # Fetch products with quantity available less than 10
        low_stock_products = Product.objects.filter(quantity_available__lt=10)
        if low_stock_products.exists():
            for product in low_stock_products:
                send_mail(
                    'Low Stock Alert',
                    f'The product "{product.name}" is low on stock. Only {product.quantity_available} items left.',


                    
                    'mhmsaeed26@gmail.com',
                    ['mhmsaeed26@gmail.com'],
                )
            self.stdout.write(self.style.SUCCESS('Low stock alerts sent.'))
        else:
            self.stdout.write('No low stock products found.')