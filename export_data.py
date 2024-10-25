from cassandra.cluster import Cluster, NoHostAvailable
import pandas as pd

def export_data_to_csv(batch_size=1000):
    try:
        # Kết nối tới Cassandra
        cluster = Cluster(['localhost'], port=9042)  # Thay 'localhost' bằng địa chỉ container nếu cần
        session = cluster.connect('spark_streams')  # Kết nối tới keyspace 'spark_streams'
        
        # Cấu hình paging để giới hạn số lượng bản ghi trong mỗi batch
        session.default_fetch_size = batch_size

        # Truy vấn dữ liệu từ bảng 'created_users'
        query = "SELECT * FROM created_users"
        result_set = session.execute(query)
        
        # Lấy tên cột từ schema của bảng
        column_names = result_set.column_names

        # Tạo file CSV và ghi header
        csv_file = 'created_users.csv'

        # Ghi dữ liệu và header vào file CSV
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            # Chỉ ghi header một lần
            f.write(','.join(column_names) + '\n')

            # Lặp qua các batch của Cassandra
            while True:
                print("loading")
                # Lấy dữ liệu theo từng trang
                page = result_set.current_rows
                if not page:
                    break  # Nếu không có dữ liệu, dừng lại

                # Chuyển thành DataFrame và ghi ra file CSV
                data = [list(row) for row in page]
                df = pd.DataFrame(data, columns=column_names)
                df.to_csv(f, header=False, index=False)  # Append dữ liệu không ghi header

                # Fetch trang tiếp theo
                if not result_set.has_more_pages:
                    break
                result_set = session.execute(query, paging_state=result_set.paging_state)

        print(f"Data exported to {csv_file}")

    except NoHostAvailable:
        print("Error: No host available. Please check if the Cassandra server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Đóng kết nối nếu đã mở
        if 'session' in locals():
            session.shutdown()
        if 'cluster' in locals():
            cluster.shutdown()

if __name__ == "__main__":
    export_data_to_csv(batch_size=1000)
