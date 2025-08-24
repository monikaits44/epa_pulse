from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Policy, Appointment, TestResult, Prediction, Watchlist, Recommendation, Patient
from .serializers import (
    PolicySerializer,
    AppointmentSerializer,
    TestResultSerializer,
    PredictionSerializer,
    WatchlistSerializer,
)

import re
import pandas as pd
from openai import OpenAI

# Policy-Based Health Coverage Insights
class PolicyViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Change 'patient_id' to 'pk'
        try:
            policy = Policy.objects.get(patient__id=pk)  # Get policy using 'pk'
            serializer = PolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Policy.DoesNotExist:
            return Response({"detail": "Policy not found."}, status=status.HTTP_404_NOT_FOUND)


# Automated Health Reminders
class ReminderViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Change 'patient_id' to 'pk'
        appointments = Appointment.objects.filter(patient__id=pk)
        if not appointments.exists():
            return Response({"detail": "No upcoming appointments found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointments, many=True)
        reminders = [
            {
                "date": appointment.date,
                "type": appointment.appointment_type,
                "status": appointment.status,
                "message": f"Reminder: Your {appointment.appointment_type} is scheduled."
            }
            for appointment in appointments if appointment.status == "Scheduled"
        ]

        return Response({"reminders": reminders, "appointments": serializer.data}, status=status.HTTP_200_OK)


# Personalized Preventive Recommendations
class RecommendationViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Change 'patient_id' to 'pk'
        try:
            watchlist_apps = Watchlist.objects.get(patient__id=pk)  # Get the watchlist for the patient
            watchlist_serializer = WatchlistSerializer(watchlist_apps)

            recommendations = []

            # Generate recommendations based on app usage
            for app_data in watchlist_apps.apps_used:
                if app_data.get("name") == "Hypertension Monitor":
                    recommendations.append({
                        "type": "Lifestyle Change",
                        "message": "Consider reducing salt intake to manage blood pressure."
                    })
                elif app_data.get("name") == "Healthy Lifestyle Tips":
                    recommendations.append({
                        "type": "App Usage",
                        "message": "Use the 'Healthy Lifestyle Tips' app weekly for diet advice."
                    })

            return Response({"recommendations": recommendations, "watchlist": watchlist_serializer.data},
                            status=status.HTTP_200_OK)
        except Watchlist.DoesNotExist:
            return Response({"detail": "Watchlist not found."}, status=status.HTTP_404_NOT_FOUND)


# Test Results Visualization
class TestResultViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Change 'patient_id' to 'pk'
        test_results = TestResult.objects.filter(patient__id=pk)
        if not test_results.exists():
            return Response({"detail": "No test results found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TestResultSerializer(test_results, many=True)

        # Prepare trends for visualization
        trends = {
            "blood_pressure": [],
            "dates": []
        }
        for result in test_results:
            trends["dates"].append(result.date)
            if result.test_type == "Blood Pressure":
                trends["blood_pressure"].append(result.result)

        return Response({
            "test_results": serializer.data,
            "trends": trends
        }, status=status.HTTP_200_OK)


# Disease Prediction and Risk Scoring
class PredictionViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Change 'patient_id' to 'pk'
        predictions = Prediction.objects.filter(patient__id=pk)
        if not predictions.exists():
            return Response({"detail": "No predictions found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PredictionSerializer(predictions, many=True)
        return Response({
            "predictions": serializer.data
        }, status=status.HTTP_200_OK)


class DashboardViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):  # Use 'pk' to refer to patient ID
        try:
            patient = Patient.objects.all().first()
            if patient is None:
                return Response({}, status=status.HTTP_200_OK)
            pk = patient.id
            # Get the patient's policy
            policy = Policy.objects.filter(patient__id=pk).first()
            if policy:
                policy_serializer = PolicySerializer(policy)

            # Get the patient's upcoming appointments
            appointments = Appointment.objects.filter(patient__id=pk, status="Scheduled")
            appointment_serializer = AppointmentSerializer(appointments, many=True)

            # Get the patient's test results
            test_results = TestResult.objects.filter(patient__id=pk)
            test_result_serializer = TestResultSerializer(test_results, many=True)

            # Get the patient's watchlist apps
            watchlist_apps = Watchlist.objects.filter(patient__id=pk).first()
            if watchlist_apps:
                watchlist_serializer = WatchlistSerializer(watchlist_apps)

            # Get health alerts with specific recommendations
            health_alerts_with_recommendations = self.get_health_alerts_and_recommendations(pk)

            # Prepare the dashboard data
            dashboard_data = {
                "patient_name": patient.name,
                "policy_details": policy_serializer.data if policy else {},
                "upcoming_appointments": appointment_serializer.data,
                "test_results": test_result_serializer.data,
                "apps_used": watchlist_serializer.data['apps_used'] if watchlist_apps else [],
                "health_alerts_with_recommendations": health_alerts_with_recommendations
            }

            return Response(dashboard_data, status=status.HTTP_200_OK)

        except Policy.DoesNotExist:
            return Response({"detail": "Policy not found."}, status=status.HTTP_404_NOT_FOUND)
        except Watchlist.DoesNotExist:
            return Response({"detail": "Watchlist not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_health_alerts_and_recommendations(self, patient_id):
        alerts_with_recommendations = []

        # Fetch predictions for the patient
        predictions = Prediction.objects.filter(patient_id=patient_id)
        print(predictions)

        for prediction in predictions:
            # Generate alerts based on test result types and their values
            alert = f"You are at the risk of {prediction.disease}. Your risk score is {prediction.risk_score}"
            recommendations = Recommendation.objects.filter(
                patient_id=patient_id, recommendation_type=prediction.disease
            ).values("content")
            # Only add to the list if an alert and recommendations were created
            if alert and recommendations:
                alerts_with_recommendations.append({
                    "alert": alert,
                    "disease": prediction.disease,
                    "risk_score": prediction.risk_score,
                    "recommendations": list(recommendations)  # Convert queryset to list
                })

        return alerts_with_recommendations


# Configure the NVIDIA OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)


class MedicalBotAPIView(APIView):
    """
    API endpoint to handle user questions with a medical chatbot.
    """

    def post(self, request):
        user_question = request.data.get("question", "")

        if not user_question:
            return Response(
                {"error": "Question field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate response using NVIDIA's medical LLM
        try:
            # Set up the chat completion parameters
            completion = client.chat.completions.create(
                model="writer/palmyra-med-70b-32k",
                messages=[{"role": "user", "content": user_question}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )

            response_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content

            return Response({"response": response_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def parse_disease_risk(data):
    # Initialize variables to hold extracted data
    disease = None
    risk_score = None
    predictions = []
    recommendations = []
    # Regular expression patterns for extracting information
    disease_pattern = r'Disease:\s*(.*)'
    risk_score_pattern = r'Risk Score:\s*(.*)'
    recommendation_pattern = r'Preventive Recommendation:\s*(.*)'
    # Extract Disease
    disease_match = re.search(disease_pattern, data)
    if disease_match:
        disease = disease_match.group(1).strip()  # Strip whitespace
        disease = re.sub(r'[^a-zA-Z0-9\s]', '', disease)  # Remove special characters
    # Extract Risk Score
    risk_score_match = re.search(risk_score_pattern, data)
    if risk_score_match:
        risk_score_text = risk_score_match.group(1).strip()
        # Extract the numeric part and convert to float
        score_match = re.search(r'(\d+)', risk_score_text)
        if score_match:
            risk_score = float(score_match.group(1)) / 10.0  # Normalize to a float between 0 and 1
    # Extract Preventive Recommendation
    recommendation_match = re.search(recommendation_pattern, data, re.DOTALL)
    if recommendation_match:
        recommendation = recommendation_match.group(1).strip()
        recommendation = re.sub(r'[^a-zA-Z0-9\s:,.]', '', recommendation).strip()  # Remove special characters
        # Add prediction
        predictions.append({"disease": disease, "risk_score": risk_score})
        # Add single recommendation
        recommendations.append({"type": disease, "content": recommendation})
    return predictions, recommendations



class PatientDeleteView(APIView):
    def delete(self, request):
        try:
            # Fetch the patient by ID
            patient = Patient.objects.all().first()

            # Delete related records
            Policy.objects.filter(patient=patient).delete()
            Appointment.objects.filter(patient=patient).delete()
            TestResult.objects.filter(patient=patient).delete()
            Prediction.objects.filter(patient=patient).delete()
            Recommendation.objects.filter(patient=patient).delete()
            Watchlist.objects.filter(patient=patient).delete()

            patient.delete()

            return Response({"message": "Patient data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Configure the NVIDIA client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

@api_view(['POST'])
def upload_patient_data(request):
    # Ensure we accept multi-part data for file uploads
    parser_classes = (MultiPartParser, FormParser)

    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if not file_obj:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # Read the CSV file
        df = pd.read_csv(file_obj)

        # Process each row in the DataFrame
        for index, row in df.iterrows():
            patient_data = {
                "name": row.get("name"),
                "age": row.get("age"),
                "gender": row.get("gender"),
                "weight": row.get("weight"),
                "height": row.get("height"),
                "medical_history": {
                    "hypertension": row.get("hypertension") == 'True',
                    "diabetes": row.get("diabetes") == 'True'
                },
                "wearable_data": {
                    "steps": row.get("steps"),
                    "heart_rate": row.get("heart_rate"),
                    "sleep": row.get("sleep")
                },
                "policy": {
                    "policy_id": row.get("policy_id"),
                    "coverage_details": {
                        "mammogram_coverage": row.get("mammogram_coverage") == 'True',
                        "deductible": row.get("deductible"),
                        "last_claim": row.get("last_claim"),
                        "total_premium_paid": row.get("total_premium_paid")
                    }
                },
                "appointments": [],  # Will fill this
                "apps_used": [],     # Will fill this
                "test_results": []    # Will fill this
            }

            # Populate appointments
            appointments_data = row.get("appointments")
            if isinstance(appointments_data, str):
                try:
                    appointments = eval(appointments_data)  # Convert string representation of list to actual list
                    for appointment in appointments:
                        patient_data["appointments"].append({
                            "date": appointment.get("date"),
                            "type": appointment.get("type"),
                            "status": appointment.get("status"),
                            "doctor": appointment.get("doctor")
                        })
                except Exception as e:
                    return JsonResponse({'error': f'Invalid appointments format: {str(e)}'}, status=400)

            # Populate apps used
            apps_used_data = row.get("apps_used")
            if isinstance(apps_used_data, str):
                try:
                    apps = eval(apps_used_data)  # Convert string representation of list to actual list
                    for app in apps:
                        patient_data["apps_used"].append({
                            "name": app.get("name"),
                            "description": app.get("description"),
                            "usage_frequency": app.get("usage_frequency")
                        })
                except Exception as e:
                    return JsonResponse({'error': f'Invalid apps_used format: {str(e)}'}, status=400)

            # Populate test results
            test_results_data = row.get("test_results")
            if isinstance(test_results_data, str):
                try:
                    test_results = eval(test_results_data)  # Convert string representation of list to actual list
                    for test_result in test_results:
                        patient_data["test_results"].append({
                            "test_type": test_result.get("test_type"),
                            "date": test_result.get("date"),
                            "result": test_result.get("result"),
                            "doctor": test_result.get("doctor")
                        })
                except Exception as e:
                    return JsonResponse({'error': f'Invalid test_results format: {str(e)}'}, status=400)

            # Now we will create the patient and associated data
            create_patient_with_data(patient_data)

        return JsonResponse({'message': 'Patient data uploaded successfully!'}, status=201)


def create_patient_with_data(patient_info):
    # Create Policy
    policy_info = patient_info.pop("policy")
    policy = Policy.objects.create(
        policy_id=policy_info["policy_id"],
        coverage_details=policy_info["coverage_details"]
    )

    Patient.objects.all().delete()
    # Create Patient
    patient = Patient.objects.create(
        name=patient_info["name"],
        age=patient_info["age"],
        gender=patient_info["gender"],
        weight=patient_info["weight"],
        height=patient_info["height"],
        medical_history=patient_info["medical_history"],
        wearable_data=patient_info["wearable_data"],
        policy=policy
    )

    # Create Appointments
    for appointment in patient_info["appointments"]:
        Appointment.objects.create(
            patient=patient,
            date=appointment["date"],
            appointment_type=appointment["type"],
            status=appointment["status"],
            doctor=appointment["doctor"]
        )

    # Create Watchlist
    Watchlist.objects.create(
        patient=patient,
        apps_used=patient_info["apps_used"]
    )

    # Create Test Results
    for result in patient_info["test_results"]:
        TestResult.objects.create(
            patient=patient,
            test_type=result["test_type"],
            date=result["date"],
            result=result["result"],
            doctor=result["doctor"]
        )

    # Fetch Predictions using the classifier for disease risk
    predictions, recommendations = parse_disease_risk(classify_disease_risk(patient_info))

    # Save Predictions in the Database
    for prediction in predictions:
        Prediction.objects.create(
            patient=patient,
            disease=prediction["disease"],
            risk_score=prediction["risk_score"]
        )

    # Save Recommendations in the Database
    for recommendation in recommendations:
        Recommendation.objects.create(
            patient=patient,
            recommendation_type=recommendation["type"],
            content=recommendation["content"]
        )

def classify_disease_risk(patient_data):
    """
    Use NVIDIA BioNemo to classify and predict disease risk based on patient data.
    """
    prompt = (
        f"Classify a disease risk based on the following patient data: "
        f"Age: {patient_data['age']}, Gender: {patient_data['gender']}, "
        f"Medical history: {patient_data['medical_history']}, "
        f"Wearable data: {patient_data['wearable_data']}. "
        f"Output the disease with risk score and 1 preventive recommendation. Keep it short and concise."
    )

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=300
    )

    response_text = completion.choices[0].message.content
    print(response_text)

    return response_text




