from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    # Gestion des livraisons
    path('', views.DeliveryListCreateView.as_view(), name='delivery_list_create'),
    path('<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery_detail'),
    path('<int:pk>/update/', views.DeliveryUpdateView.as_view(), name='delivery_update'),
    path('<int:pk>/cancel/', views.DeliveryCancelView.as_view(), name='delivery_cancel'),
    
    # Suivi des livraisons
    path('tracking/<str:tracking_number>/', views.DeliveryTrackingView.as_view(), name='delivery_tracking'),
    
    # Statistiques et rapports
    path('stats/', views.DeliveryStatsView.as_view(), name='delivery_stats'),
    path('reports/', views.DeliveryReportsView.as_view(), name='delivery_reports'),
    
    # Gestion des zones de livraison
    path('zones/', views.DeliveryZoneListView.as_view(), name='zone_list'),
    path('zones/<int:pk>/', views.DeliveryZoneDetailView.as_view(), name='zone_detail'),
]