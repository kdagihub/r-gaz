import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.payments.models import Payment

User = get_user_model()

@pytest.mark.django_db
def test_payment_list_authenticated():
    user = User.objects.create_user(username='testuser', password='testpass')
    Payment.objects.create(user=user, amount=100)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('payment-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_payment_detail_authenticated():
    user = User.objects.create_user(username='testuser2', password='testpass')
    payment = Payment.objects.create(user=user, amount=200)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('payment-detail', args=[payment.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['amount'] == 200

@pytest.mark.django_db
def test_payment_list_unauthenticated():
    url = reverse('payment-list')
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED