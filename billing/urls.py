from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet, InvoiceViewSet, invoices_export_csv_view

router = DefaultRouter()
router.register(r"plans", PlanViewSet, basename="plan")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")
router.register(r"invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    # export CSV (tolerante a slash y a endpoint sin .csv)
    path("invoices/export.csv", invoices_export_csv_view, name="invoices_export_csv"),
    path("invoices/export.csv/", invoices_export_csv_view),  # por si APPEND_SLASH redirige
    path("invoices/export/", invoices_export_csv_view),

    # router al final para evitar conflictos
    path("", include(router.urls)),
]
