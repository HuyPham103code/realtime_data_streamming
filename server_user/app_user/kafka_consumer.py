from kafka import KafkaConsumer
import json

def kafka_consumer():
    # Tạo Kafka Consumer, đọc dữ liệu từ topic 'users_created'
    print('***conecting with kafka')
    # consumer = KafkaConsumer(
    #     'users_created',
    #     bootstrap_servers=['localhost:9092'],  # Đổi địa chỉ nếu cần
    #     value_serializer=lambda v: json.loads(v.decode('utf-8')),
    #     auto_offset_reset='earliest',
    #     enable_auto_commit=True
    # )

    # for message in consumer:
    #     # Xử lý message (chuyển nó thành JSON chẳng hạn)
    #     data = message.value
    #     print("Received message:", data)

    #     # Ở đây bạn có thể lưu trữ data vào cache hoặc cơ sở dữ liệu nếu cần
    #     # Hoặc push data này tới phía client qua WebSocket hoặc SSE

