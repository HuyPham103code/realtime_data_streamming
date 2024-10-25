// ===================== Form Control Functions =====================

// Hiển thị hoặc ẩn form
const toggleForm = (show) => {
    const display = show ? 'block' : 'none';
    document.getElementById('overlay').style.display = display;
    document.getElementById('formContainer').style.display = display;
};

// Xử lý mở và đóng form khi nhấn nút
document.getElementById('showFormBtn').addEventListener('click', () => toggleForm(true));
document.getElementById('closeFormBtn').addEventListener('click', () => toggleForm(false));

// ===================== Form Submission Functions =====================

// Xử lý sự kiện submit form
const handleSubmit = (event) => {
    console.log("Form submitted.");
    event.preventDefault();  // Ngăn form reload trang  preventDefault

    const formData = getFormData();
    if (!validateFormData(formData)) {
        toggleForm(false);
        console.log("Please fill in all fields.");
        return;
    }

    // Gửi yêu cầu POST tới server và xử lý kết quả
    postFormData(formData).then((result) => {
        const dataWithCluster = { ...formData, cluster: result.cluster };
        insertRow(dataWithCluster);
        toggleForm(false);
        resetForm();
    }).catch((error) => console.error('Error:', error));
};

// Lấy dữ liệu từ form
const getFormData = () => ({
    first_name: document.getElementById('first_name').value,
    gender: document.getElementById('gender').value,
    last_name: document.getElementById('last_name').value,
    phone: document.getElementById('phone').value,
    address: document.getElementById('address').value,
    email: document.getElementById('email').value,
    picture: document.getElementById('picture').value,
    post_code: document.getElementById('post_code').value,
    registered_date: document.getElementById('registered_date').value,
    username: document.getElementById('username').value
});

// Kiểm tra dữ liệu form có đầy đủ không
const validateFormData = (data) => Object.values(data).every(value => value.trim());

// Gửi yêu cầu POST đến server
// const postFormData = (data) => {
//     return fetch('http://192.168.1.3:8000/employees/', {  // URL server
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
// };

const postFormData = async (data) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/employees/', {  // URL server
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error:', error);
    }
};

// Reset form sau khi gửi thành công
const resetForm = () => document.getElementById('dataForm').reset();

// ===================== Table Functions =====================

// Thêm dòng mới vào bảng từ kết quả server
const insertRow = (data) => {
    const tableBody = document.getElementById('employeeTable').querySelector('tbody');
    const newRow = tableBody.insertRow();

    newRow.style.backgroundColor = data.cluster === 1 ? 'lightgreen' : (data.cluster === 0 ? 'lightcoral' : '');

    ['first_name', 'gender', 'last_name', 'phone', 'address', 'email', 'picture', 'post_code', 'registered_date', 'username', 'cluster']
        .forEach((key, index) => {
            newRow.insertCell(index).textContent = data[key];
        });
};

// Xử lý sự kiện submit form
document.getElementById('dataForm').addEventListener('submit', handleSubmit);

// ===================== WebSocket Realtime Streaming =====================

let socket = null;
let isStreaming = false;

document.getElementById('streaming').addEventListener('click', function() {
    const button = this;  // Tham chiếu trực tiếp đến button
    console.log('zo')

    if (!isStreaming) {
        // Kết nối WebSocket
        socket = new WebSocket('ws://127.0.0.1:8000/ws/kafka/');

        socket.onopen = () => {
            console.log('WebSocket connection opened.');
            button.textContent = "Stop";
            isStreaming = true;
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received message:', data);
            insertRow(data);  // Thêm dữ liệu mới vào bảng
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed.');
            button.textContent = "Streaming Kafka";
            isStreaming = false;
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    } else {
        // Đóng kết nối WebSocket nếu đã streaming
        if (socket) {
            socket.close();
        }
    }
});



// // ======================realtime streaming=========================
// // create consumer to receive data from kafka
// let socket = null;
// let isStreaming = false;
// let url = ws://${window.location.host}/ws/kafka/
// document.getElementById('streaming').addEventListener('click', function() {
//     const button = document.getElementById('streaming');
    
//     if (!isStreaming) {
//         // Kết nối WebSocket 'ws://127.0.0.1:8000/ws/kafka/'
//         console.log('zo')
//         socket = new WebSocket('ws://localhost:8000/ws/kafka/');
//         console.log('zo2')


//         socket.onopen = function(event) {
//             console.log('WebSocket connection opened.');
//             button.textContent = "Stop";
//             isStreaming = true;
//         };

//         socket.onmessage = function(event) {
//             const data = JSON.parse(event.data);
//             console.log('Received message:', data);
//             insertRow(data)
//         };

//         socket.onclose = function(event) {
//             console.log('WebSocket connection closed.');
//             button.textContent = "Streaming Kafka";
//             isStreaming = false;
//         };

//         socket.onerror = function(error) {
//             console.log('WebSocket error:', error);
//         };
//     } else {
//         // Đóng kết nối WebSocket
//         if (socket) {
//             socket.close();
//         }
//     }
// });