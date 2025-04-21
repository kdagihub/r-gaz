from tabnanny import verbose
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.products'
    verbose_name = 'Produits'