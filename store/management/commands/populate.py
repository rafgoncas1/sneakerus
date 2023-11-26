# store/management(commands/populate.py)

from django.core.management.base import BaseCommand
from store.models import Brand, Color, Size, Status, Product, ProductColor, ProductSize, Order, OrderItem
import random

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        # Delete all brands, colors, sizes, products, productcolors and productsizes
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        ProductColor.objects.all().delete()
        ProductSize.objects.all().delete()
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Color.objects.all().delete()
        Size.objects.all().delete()
        Status.objects.all().delete()

        # Create 5 brands
        brand1, created = Brand.objects.get_or_create(name='Nike')
        brand2, created = Brand.objects.get_or_create(name='Adidas')
        brand3, created = Brand.objects.get_or_create(name='Puma')
        brand4, created = Brand.objects.get_or_create(name='Reebok')
        brand5, created = Brand.objects.get_or_create(name='New Balance')

        # Create 10 colors
        color1, created = Color.objects.get_or_create(name='Negro')
        color2, created = Color.objects.get_or_create(name='Blanco')
        color3, created = Color.objects.get_or_create(name='Rojo')
        color4, created = Color.objects.get_or_create(name='Azul')
        color5, created = Color.objects.get_or_create(name='Verde')
        color6, created = Color.objects.get_or_create(name='Amarillo')
        color7, created = Color.objects.get_or_create(name='Naranja')
        color8, created = Color.objects.get_or_create(name='Rosa')
        color9, created = Color.objects.get_or_create(name='Gris')
        color10, created = Color.objects.get_or_create(name='Marrón')

        # Create 10 sizes
        size1, created = Size.objects.get_or_create(name=44.0)
        size2, created = Size.objects.get_or_create(name=44.5)
        size3, created = Size.objects.get_or_create(name=45.0)
        size4, created = Size.objects.get_or_create(name=45.5)
        size5, created = Size.objects.get_or_create(name=42.0)
        size6, created = Size.objects.get_or_create(name=42.5)
        size7, created = Size.objects.get_or_create(name=43.0)
        size8, created = Size.objects.get_or_create(name=43.5)
        size9, created = Size.objects.get_or_create(name=40.0)
        size10, created = Size.objects.get_or_create(name=40.5)
        sizes = [size1, size2, size3, size4, size5, size6, size7, size8, size9, size10]

        # Create all Status
        status1, created = Status.objects.get_or_create(name='No realizado')
        status2, created = Status.objects.get_or_create(name='Realizado')
        status3, created = Status.objects.get_or_create(name='Gestionado')
        status4, created = Status.objects.get_or_create(name='Enviado')
        status5, created = Status.objects.get_or_create(name='En reparto')
        status6, created = Status.objects.get_or_create(name='Entregado')
        status7, created = Status.objects.get_or_create(name='Cancelado')
        status8, created = Status.objects.get_or_create(name='Devuelto')

        # Create 2 products per brand
        product1, created = Product.objects.get_or_create(name='Air Force 1', image='air-force-1.jpeg' , price=100.99, brand=brand1, description='Zapatillas de baloncesto', details="El fulgor sigue vivo en las Nike Air Force 1 '07, un modelo original de baloncesto que introduce un nuevo giro a sus ya característicos revestimientos con costuras duraderas, sus acabados impecables y la cantidad perfecta de reflectante.")
        product2, created = Product.objects.get_or_create(name='Air Max 90', image='air-max-90.jpeg', price=120.99, brand=brand1, description='Zapatillas de running', details="Las Nike Air Max 90 se renuevan con una parte superior de malla transpirable y revestimientos de piel sintética que le confieren un look moderno y una mayor comodidad. La unidad Max Air visible en el talón ofrece una amortiguación que se ha convertido en todo un icono.")
        product3, created = Product.objects.get_or_create(name='Superstar', image='adidas-superstar.jpg', price=90.99, brand=brand2, description='Zapatillas de baloncesto', details="Las adidas Superstar son un icono de la cultura urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color rojo. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        product4, created = Product.objects.get_or_create(name='Stan Smith', image='stan-smith.jpg', price=80.99, brand=brand2, description='Zapatillas de tenis', details="Las adidas Stan Smith son un icono de la moda urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color verde. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        product5, created = Product.objects.get_or_create(name='Suede Classic', image='suede-classic.jpeg', price=70.99, brand=brand3, description='Calzado urbano', details="Las zapatillas más emblemáticas de PUMA aparecieron por primera vez en 1968 y causaron un gran impacto en la cultura del calzado. Desde entonces, han acompañado a iconos de todas las generaciones. Las Suede Classic XXI tienen un empeine de ante y toques modernos que ofrecen una mejora en la calidad y la comodidad general de un clásico de todos los tiempos.")
        product6, created = Product.objects.get_or_create(name='Slipstream Lo Vintage', image='slipstream-lo-retro.jpg', price=60.99, brand=brand3, description='Zapatillas de baloncesto', details="Este modelo se presentó como una zapoatilla de baloncesto en los 80. En los 2000 estas zapatillas se relanzaron con un diseño más moderno y actual.")
        product7, created = Product.objects.get_or_create(name='Classic Leather', image='classic-leather.jpg', price=80.99, brand=brand4, description='Calzado urbano', details="Las Classic Leather son un icono de la moda urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color rojo. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        product8, created = Product.objects.get_or_create(name='Club C 85', image='club-c-85.jpg', price=70.99, brand=brand4, description='Calzado urbano', details="Las Club C 85 son un icono de la moda urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color rojo. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        product9, created = Product.objects.get_or_create(name='574', image='574.jpg', price=90.99, brand=brand5, description='Calzado urbano', details="Las 574 son un icono de la moda urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color rojo. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        product10, created = Product.objects.get_or_create(name='373', image='373.png', price=80.99, brand=brand5, description='Calzado urbano', details="Las 373 son un icono de la moda urbana. Esta versión se ha confeccionado en piel con las 3 bandas y el contrafuerte del talón en un llamativo color rojo. La puntera de goma y la suela cosida le confieren el auténtico estilo del modelo original.")
        products = [product1, product2, product3, product4, product5, product6, product7, product8, product9, product10]
        
        # Create ProductColor
        ProductColor.objects.get_or_create(product=product1, color=color1)
        ProductColor.objects.get_or_create(product=product1, color=color2)
        ProductColor.objects.get_or_create(product=product2, color=color1)
        ProductColor.objects.get_or_create(product=product2, color=color2)
        ProductColor.objects.get_or_create(product=product3, color=color2)
        ProductColor.objects.get_or_create(product=product3, color=color1)
        ProductColor.objects.get_or_create(product=product4, color=color1)
        ProductColor.objects.get_or_create(product=product4, color=color5)
        ProductColor.objects.get_or_create(product=product5, color=color1)
        ProductColor.objects.get_or_create(product=product5, color=color2)
        ProductColor.objects.get_or_create(product=product6, color=color1)
        ProductColor.objects.get_or_create(product=product6, color=color8)
        ProductColor.objects.get_or_create(product=product6, color=color3)
        ProductColor.objects.get_or_create(product=product7, color=color1)
        ProductColor.objects.get_or_create(product=product7, color=color3)
        ProductColor.objects.get_or_create(product=product7, color=color4)
        ProductColor.objects.get_or_create(product=product8, color=color10)
        ProductColor.objects.get_or_create(product=product9, color=color10)
        ProductColor.objects.get_or_create(product=product9, color=color8)
        ProductColor.objects.get_or_create(product=product9, color=color1)
        ProductColor.objects.get_or_create(product=product10, color=color6)
        ProductColor.objects.get_or_create(product=product10, color=color9)

        # Create ProductSize with different 5 random sizes and stocks between 0 and 30
        for product in products:
            choices = sizes.copy()
            for i in range(5):
                size = random.choice(choices)
                choices.remove(size)
                ProductSize.objects.get_or_create(product=product, size=size, stock=random.randint(0, 5))
        
        



