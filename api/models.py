from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    medical_history = models.JSONField()  # stores diagnoses, conditions, etc.
    wearable_data = models.JSONField()    # stores real-time metrics like steps, heart rate, sleep
    policy = models.OneToOneField('Policy', on_delete=models.SET_NULL, null=True, blank=True)  # Linking policy

    def __str__(self):
        return self.name


class Policy(models.Model):
    policy_id = models.CharField(max_length=50)
    coverage_details = models.JSONField()  # details like mammogram coverage, deductible, etc.

    def __str__(self):
        return f"{self.policy_id} - {self.patient.name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    appointment_type = models.CharField(max_length=100)  # e.g., "Breast Cancer Screening"
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Missed', 'Missed')])
    doctor = models.CharField(max_length=100)  # Name of the doctor

    def __str__(self):
        return f"{self.appointment_type} on {self.date} for {self.patient.name}"


class Watchlist(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    apps_used = models.JSONField()  # e.g., [{"name": "Hypertension Monitor", ...}]

    def __str__(self):
        return f"Watchlist for {self.patient.name}"


class TestResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)  # e.g., "Blood Pressure", "Blood Sugar"
    date = models.DateField()
    result = models.CharField(max_length=100)  # e.g., "Normal", "High"
    doctor = models.CharField(max_length=100)  # Name of the doctor

    def __str__(self):
        return f"{self.test_type} result for {self.patient.name} on {self.date}"


class Prediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)  # e.g., "Hypertension"
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease} risk score of {self.risk_score} for {self.patient.name}"


class Recommendation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=100)  # e.g., "Lifestyle", "App"
    content = models.TextField()  # e.g., description of the recommendation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.patient.name} - {self.recommendation_type}"
