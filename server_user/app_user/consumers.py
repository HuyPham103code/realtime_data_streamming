from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from kafka import KafkaConsumer as KafkaPyConsumer
import joblib
import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
connection = False
class KafkaConsumer(AsyncWebsocketConsumer):
    connection = False
    async def connect(self):
        await self.accept()
        self.connection = True
        ### kafka
        logger.info("*********** connecting")
        try:
            
            self.kafka_consumer = KafkaPyConsumer(
                'users_created',  
                bootstrap_servers='broker:29092',  
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),  
                auto_offset_reset='earliest', 
                enable_auto_commit=True, 
                consumer_timeout_ms=30000 
            )
            logger.info("*********** connected")
            #await asyncio.sleep(5)
            self.send_message_task = asyncio.create_task(self.send_messages())
        
        except Exception as e:
            print(f'Error connecting Kafka Consumer: {e}')



    async def disconnect(self, close_code):
        # Hủy nhiệm vụ khi ngắt kết nối
        self.send_message_task.cancel()
        ### kafka
        self.connection = True
        self.kafka_consumer.close()

 
    async def send_messages(self):
        logger.info("*********** do1")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kmeans_model = joblib.load(os.path.join(base_dir, 'kmeans_model.pkl'))
        label_encoder = joblib.load(os.path.join(base_dir, 'label_encoders.pkl'))
        # kmeans_model = joblib.load(r'D:\Data_Engineer\projects\spark\data_pipeline_ai\server_user\app_user\kmeans_model.pkl')
        # label_encoder = joblib.load(r'D:\Data_Engineer\projects\spark\data_pipeline_ai\server_user\app_user\label_encoders.pkl')
        # logger.info("*********** do2")
        await asyncio.sleep(5)
        
        try:
            # Chạy Kafka consumer trong một luồng riêng biệt
            await asyncio.to_thread(self.consume_kafka_messages, kmeans_model, label_encoder)
        except Exception as e:
            logger.error(f"Error during message processing: {e}")



    def consume_kafka_messages(self, kmeans_model, label_encoder):
        for message in self.kafka_consumer:
            message_data = message.value

            if self.connection == False:
                logger.warning("out connect")
                break
            # Kiểm tra nếu message_data là null hoặc rỗng
            if not message_data:
                logger.warning("Received empty or null message.")
                continue  

            logger.info(f"Received message: {message_data}")
            
            try:
                cluster = asyncio.run(asyncio.to_thread(self.get_cluster_sync, message_data, kmeans_model, label_encoder))
                message_data['cluster'] = cluster
            except Exception as e:
                logger.error(f"Error in get_cluster: {e}")
                message_data['cluster'] = None

            print(message_data)
            # Kiểm tra nếu WebSocket còn mở và gửi message
            asyncio.run(self.send_message_to_frontend(message_data))

            # Thêm độ trễ trước khi tiếp tục xử lý thông điệp tiếp theo
            asyncio.run(asyncio.sleep(30))

    async def send_message_to_frontend(self, message_data):
        # Kiểm tra xem WebSocket có còn mở không
        if self.connection == True:  # WebSocket vẫn đang mở nếu close_code là None
            try:
                # Gửi dữ liệu lên frontend
                await self.send(text_data=json.dumps(message_data))
            except Exception as e:
                logger.error(f"Error sending message to WebSocket: {e}")
                await self.close()  # Đóng kết nối nếu gặp lỗi khi gửi tin nhắn
        else:
            logger.warning("WebSocket connection closed. Stopping message sending.")
            await self.close()

    def get_cluster_sync(self, message_data, kmeans_model, label_encoder):
        data = pd.DataFrame([message_data])

        first_name_encoded = self.encode_with_label_encoder(label_encoder, 'first_name', data)
        last_name_encoded = self.encode_with_label_encoder(label_encoder, 'last_name', data)
        phone_encoded = self.encode_with_label_encoder(label_encoder, 'phone', data)
        post_code_encoded = self.encode_with_label_encoder(label_encoder, 'post_code', data)
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
        return int(cluster[0])
        


    def encode_with_label_encoder(self, label_encoder, column_name, data):
        try:
            return label_encoder[column_name].transform(data[column_name].astype(str))
        except ValueError:
            return 1  

 
