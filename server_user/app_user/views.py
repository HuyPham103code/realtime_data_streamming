from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer
import pandas as pd
import numpy as np
from .models import Employee
import joblib  
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

kmeans_model_path = os.path.join(base_dir, 'kmeans_model.pkl')
label_encoder_path = os.path.join(base_dir, 'label_encoders.pkl')
# Tải model KMeans và LabelEncoder đã lưu
kmeans_model = joblib.load(kmeans_model_path)
label_encoder = joblib.load(label_encoder_path)

class EmployeeAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        # kmeans_model = joblib.load(r'D:\Data_Engineer\projects\spark\data_pipeline_ai\train_model\kmeans_model.pkl')
        # label_encoder = joblib.load(r'D:\Data_Engineer\projects\spark\data_pipeline_ai\train_model\label_encoders.pkl')
        if serializer.is_valid():
            user_data = serializer.validated_data
            data = pd.DataFrame([user_data])
            
            # Kiểm tra và đảm bảo các thuộc tính có trong LabelEncoder
            try:
                first_name_encoded = label_encoder['first_name'].transform(data['first_name'].astype(str))
            except ValueError:
                first_name_encoded = 1
            try:
                last_name_encoded = label_encoder['last_name'].transform(data['last_name'].astype(str))
            except ValueError:
                last_name_encoded = -1
            try:
                phone_encoded = label_encoder['phone'].transform(data['phone'].astype(str))
            except ValueError:
                phone_encoded = -1
            try:
                post_code_encoded = label_encoder['post_code'].transform(data['post_code'].astype(str))
            except ValueError:
                post_code_encoded = 1
            gender_encoded = np.where(data['gender'] == 'male', 0, 1)

            
            encoded_data = pd.DataFrame({
                'first_name': first_name_encoded,
                'gender': gender_encoded,
                'last_name': last_name_encoded,
                'phone': phone_encoded,
                'post_code': post_code_encoded
            })
            # Dự đoán cụm
            cluster = kmeans_model.predict(encoded_data)
            return Response({'cluster': int(cluster[0])}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
