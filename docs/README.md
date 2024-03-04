# Tải eBook từ VNU-LIB

## 1. Cách chạy tool

> [!IMPORTANT]
>
> Tool yêu cầu windows có cài đặt Python 3.x. Phiên bản hiện tại chưa hỗ trợ linux và macOS 

> Để đảm bảo không có đột biến với các dự án khác trên máy của bạn, tool này tạo một môi trường ảo và tải những packages cần thiết trong đó.

+ Điền username và password vào file `authorization.json`.
+ Chạy `run.bat`.
+ Nhập tên đường dẫn (dạng `https://ir.vnulib.edu.vn/handle/VNUHCM/31319`). Có thể nhập nhiều đường dẫn cách nhau bằng space.
+ Tuỳ chọn sử dụng đa luồng (tốn CPU) `fast mode`.
+ Tuỳ chọn gộp các mục thành 1 file `merge sections`.
+ Tuỳ chọn xoá các file ảnh khi xuất xong pdf (nếu cần) `clean up`.
+ Đợi script chạy và hoàn thành. Các file ảnh sẽ được lưu tại `imgs/` và các file pdf sẽ được lưu tại `pdfs/`

## 2. Bugs

- Nếu bạn phát hiện bugs, hãy đăng issues! Thanks!!!
