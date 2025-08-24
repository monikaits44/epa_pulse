from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PolicyViewSet,
    ReminderViewSet,
    RecommendationViewSet,
    TestResultViewSet,
    PredictionViewSet,
    DashboardViewSet,
    MedicalBotAPIView,
    upload_patient_data,
    PatientDeleteView,
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'policy', PolicyViewSet, basename='policy')
router.register(r'reminders', ReminderViewSet, basename='reminders')
router.register(r'recommendations', RecommendationViewSet, basename='recommendations')
router.register(r'test-results', TestResultViewSet, basename='test-results')
router.register(r'predictions', PredictionViewSet, basename='predictions')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path("medical-bot/", MedicalBotAPIView.as_view(), name="medical-bot"),
    path('upload-patient-data/', upload_patient_data, name='upload_patient_data'),
    path('patients/delete/', PatientDeleteView.as_view(), name='delete_patient'),
]
