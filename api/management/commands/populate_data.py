import random
from django.core.management.base import BaseCommand
from api.models import Patient, Policy, Appointment, Watchlist, TestResult, Prediction, Recommendation
from openai import OpenAI
from django.conf import settings

# Configure the NVIDIA client
client = OpenAI(
    base_url="xx",
    api_key="xx"
)

import re


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

class Command(BaseCommand):
    help = 'Populate the database with test data for patients'

    def classify_disease_risk(self, patient_data):
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

    def handle(self, *args, **options):
        # Sample patient data
        patient_data = [
            {
                "name": "Anna Smith",
                "age": 63,
                "gender": "Female",
                "weight": 70,
                "height": 165,
                "medical_history": {"hypertension": True, "diabetes": False},
                "wearable_data": {"steps": 5000, "heart_rate": 72, "sleep": 7},
                "policy": {
                    "policy_id": "AOK_7826345",
                    "coverage_details": {
                        "mammogram_coverage": True,
                        "deductible": "€200",
                        "last_claim": "06/15/2023",
                        "total_premium_paid": "€1500"
                    }
                },
                "appointments": [
                    {"date": "2023-09-15", "type": "Breast Cancer Screening", "status": "Completed",
                     "doctor": "Dr. Linda Monroe"},
                    {"date": "2024-09-15", "type": "Breast Cancer Screening", "status": "Scheduled",
                     "doctor": "Dr. Linda Monroe"},
                ],
                "apps_used": [
                    {"name": "Hypertension Monitor", "description": "Tracks daily blood pressure readings.",
                     "usage_frequency": "Daily"},
                    {"name": "Healthy Lifestyle Tips", "description": "Provides diet and exercise plans.",
                     "usage_frequency": "Weekly"},
                ],
                "test_results": [
                    {"test_type": "Mammogram", "date": "2023-09-15", "result": "Normal", "doctor": "Dr. Linda Monroe"},
                    {"test_type": "Blood Pressure", "date": "2023-06-15", "result": "Normal",
                     "doctor": "Dr. Linda Monroe"},
                    {"test_type": "Blood Pressure", "date": "2024-06-15", "result": "High",
                     "doctor": "Dr. Linda Monroe"},
                    {"test_type": "Diabetes", "date": "2023-06-15", "result": "Normal", "doctor": "Dr. Linda Monroe"},
                    {"test_type": "Diabetes", "date": "2024-06-15", "result": "Normal", "doctor": "Dr. Linda Monroe"},
                ],
                "predictions": [
                    {"disease": "Diabetes", "risk_score": random.uniform(0.5, 0.9)},
                ],
                "recommendations": [
                    {"type": "Diabetes", "content": "Limit sugar intake to manage Diabetes levels."},
                    {"type": "Diabetes", "content": "Use the 'Diabetes Tracker' app daily to monitor glucose levels."}
                ]
            }

        ]

        # Create patients and associated data
        for patient_info in patient_data:
            # Create Policy
            policy_info = patient_info.pop("policy")
            policy = Policy.objects.create(
                policy_id=policy_info["policy_id"],
                coverage_details=policy_info["coverage_details"]
            )

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
                predictions, recommendations = parse_disease_risk(self.classify_disease_risk(patient_info))

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

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with test data including dynamic predictions and recommendations!'))
