from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Avg
from .models import Delivery
from .serializers import DeliverySerializer, DeliveryCreateSerializer, DeliveryUpdateSerializer


class DeliveryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeliveryCreateSerializer
        return DeliverySerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()
        return Delivery.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class DeliveryDetailView(generics.RetrieveAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()
        return Delivery.objects.filter(customer=user)


class DeliveryUpdateView(generics.UpdateAPIView):
    serializer_class = DeliveryUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()
        return Delivery.objects.filter(customer=user, status='pending')


class DeliveryCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            if request.user.is_staff:
                delivery = Delivery.objects.get(pk=pk)
            else:
                delivery = Delivery.objects.get(pk=pk, customer=request.user)
                
            if delivery.status not in ['pending', 'in_progress']:
                return Response({"error": "Impossible d'annuler une livraison terminée ou déjà annulée"}, 
                                status=status.HTTP_400_BAD_REQUEST)
                
            delivery.status = 'cancelled'
            delivery.save()
            return Response({"success": "Livraison annulée avec succès"}, status=status.HTTP_200_OK)
            
        except Delivery.DoesNotExist:
            return Response({"error": "Livraison non trouvée"}, status=status.HTTP_404_NOT_FOUND)


class DeliveryTrackingView(generics.RetrieveAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        tracking_number = self.kwargs.get('tracking_number')
        try:
            return Delivery.objects.get(id=tracking_number)
        except Delivery.DoesNotExist:
            return Response({"error": "Livraison non trouvée"}, status=status.HTTP_404_NOT_FOUND)


class DeliveryStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        total_deliveries = Delivery.objects.count()
        pending_deliveries = Delivery.objects.filter(status='pending').count()
        in_progress_deliveries = Delivery.objects.filter(status='in_progress').count()
        completed_deliveries = Delivery.objects.filter(status='completed').count()
        cancelled_deliveries = Delivery.objects.filter(status='cancelled').count()
        
        stats = {
            'total_deliveries': total_deliveries,
            'pending_deliveries': pending_deliveries,
            'in_progress_deliveries': in_progress_deliveries,
            'completed_deliveries': completed_deliveries,
            'cancelled_deliveries': cancelled_deliveries,
        }
        
        return Response(stats, status=status.HTTP_200_OK)


class DeliveryReportsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Exemple de rapport simple
        monthly_deliveries = Delivery.objects.extra(
            select={'month': "EXTRACT(month FROM created_at)"}
        ).values('month').annotate(
            count=Count('id'),
            total_quantity=Sum('quantity')
        ).order_by('month')
        
        return Response(monthly_deliveries, status=status.HTTP_200_OK)


class DeliveryZoneListView(generics.ListAPIView):
    # Ceci est un exemple - vous devrez créer un modèle Zone
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Exemple de zones de livraison
        zones = [
            {"id": 1, "name": "Zone Nord", "price": 1000},
            {"id": 2, "name": "Zone Sud", "price": 1200},
            {"id": 3, "name": "Zone Est", "price": 1100},
            {"id": 4, "name": "Zone Ouest", "price": 1300},
        ]
        return Response(zones, status=status.HTTP_200_OK)


class DeliveryZoneDetailView(generics.RetrieveAPIView):
    # Ceci est un exemple - vous devrez créer un modèle Zone
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        # Exemple de détail d'une zone
        zones = {
            1: {"id": 1, "name": "Zone Nord", "price": 1000, "description": "Couvre les quartiers nord de la ville"},
            2: {"id": 2, "name": "Zone Sud", "price": 1200, "description": "Couvre les quartiers sud de la ville"},
            3: {"id": 3, "name": "Zone Est", "price": 1100, "description": "Couvre les quartiers est de la ville"},
            4: {"id": 4, "name": "Zone Ouest", "price": 1300, "description": "Couvre les quartiers ouest de la ville"},
        }
        
        if int(pk) in zones:
            return Response(zones[int(pk)], status=status.HTTP_200_OK)
        return Response({"error": "Zone non trouvée"}, status=status.HTTP_404_NOT_FOUND)