from tabnanny import verbose
from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.reviews'
    verbose_name = 'Avis'