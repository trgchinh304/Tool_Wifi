# WiFi Speed & Password Tool | Get nation data & weather data tool

## Giới thiệu

Đây là một bộ công cụ Python đa năng gồm 4 chức năng chính:
Kiểm tra tốc độ mạng WiFi
Xem mật khẩu của các mạng WiFi đã từng kết nối
Tra cứu thông tin thời tiết tại một khu vực cụ thể
Xem thông tin tổng quát về các quốc gia trên thế giới
Phù hợp để sử dụng cá nhân, kiểm tra hệ thống hoặc tích hợp vào các công cụ hỗ trợ kỹ thuật

## Chức năng

- Kiểm tra tốc độ mạng
  + Đo tốc độ tải xuống (Download), tải lên (Upload) và độ trễ (Ping) bằng speedtest.
- Hiển thị mật khẩu WiFi đã lưu
  + Liệt kê tên các mạng WiFi đã từng kết nối và hiển thị mật khẩu tương ứng.
  + Yêu cầu chạy với quyền quản trị (Admin/sudo).
- Tra cứu thời tiết theo khu vực
  + Hiển thị nhiệt độ, độ ẩm, tình trạng thời tiết, thời gian mặt trời mọc/lặn,...
  + Tích hợp API thời tiết và hỗ trợ dịch tên khu vực sang tiếng Việt.
- Xem thông tin quốc gia
  + Bao gồm thủ đô, dân số, diện tích, đơn vị tiền tệ, ngôn ngữ, múi giờ,...
  + Hỗ trợ tìm kiếm theo tên quốc gia tiếng Việt.
 
## Yêu cầu

- Python 3.x
- Thư viện `speedtest-cli` để đo tốc độ mạng.
- Chức năng xem mật khẩu chạy với quyền `Administrator` (Windows) hoặc `sudo` (Linux) để hiển thị mật khẩu WiFi.

## Cài đặt

Cài đặt thư viện cần thiết bằng lệnh:

```sh
pip install speedtest-cli
pip install requests
pip install deep_translator
```

## Cách sử dụng

Chạy tập tin Python:

```sh
python ten_file.py
```

# Screenshot

## Speedtest 
![image](https://github.com/user-attachments/assets/0103122f-bdc7-4757-9437-64af08c3dfda)

## Get Password
![image](https://github.com/user-attachments/assets/debd9d4d-fa0a-411c-ae58-2ccc943a9b18)

## Get weather data
![image](https://github.com/user-attachments/assets/f556306e-da34-4838-a64f-f4fcb1e03601)

## Get nation data
![image](https://github.com/user-attachments/assets/cd5f66a2-6e16-4a4f-be2e-36af2dbbb0ac)


