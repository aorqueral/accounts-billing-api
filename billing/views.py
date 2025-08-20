from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
import csv

from .models import Plan, Subscription, Invoice
from .serializers import PlanSerializer, SubscriptionSerializer, InvoiceSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related("customer", "plan").all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        sub = self.get_object()
        if sub.status == "canceled":
            return Response({"detail": "Subscription already canceled"}, status=status.HTTP_400_BAD_REQUEST)
        sub.status = "canceled"
        sub.canceled_at = timezone.now()
        sub.save(update_fields=["status", "canceled_at"])
        return Response(SubscriptionSerializer(sub).data)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related("subscription", "customer").all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Emitir factura (mock): body requiere `subscription`
        - amount lo toma del plan de la suscripción
        - customer lo toma de la suscripción
        """
        subscription_id = request.data.get("subscription")
        if not subscription_id:
            return Response({"detail": "subscription is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sub = Subscription.objects.select_related("plan", "customer").get(pk=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        inv = Invoice.objects.create(
            subscription=sub,
            customer=sub.customer,
            amount=sub.plan.price,
            currency="USD",
            status="issued",
            note=request.data.get("note", ""),
        )
        return Response(InvoiceSerializer(inv).data, status=status.HTTP_201_CREATED)


def invoices_export_csv_view(_request):
    """
    /api/v1/invoices/export.csv
    """
    rows = Invoice.objects.select_related("customer", "subscription__plan").order_by("-id")
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="invoices.csv"'
    writer = csv.writer(resp)
    writer.writerow(["id", "customer_email", "amount", "currency", "status", "issued_at", "subscription_id", "plan"])
    for i in rows:
        writer.writerow([
            i.id,
            i.customer.email,
            str(i.amount),
            i.currency,
            i.status,
            i.issued_at.isoformat(),
            i.subscription_id,
            str(i.subscription.plan),
        ])
    return resp
