## Tôi đã xây dựng tool này như thế nào?

- Theo lời đề nghị từ một người bạn, tôi đã dành 1 tiếng để nghiên cứu cách 1 trang sách render như thế nào. Sau đó tôi dành tận **1 NGÀY** để code nên cái tool sơ xài này.

- Nếu để ý cách 1 mục render ra các trang sách, thì url của các trang có cùng 1 format `https://ir.vnulib.edu.vn/flowpaper/services/view.php?doc={}&format=jpg&page={}&subfolder={}`. Do đó, chỉ cần biết tổng số trang là có thể truy cập được tất cả ảnh.

- Tuy nhiên, những mục chia của sách chỉ khả dụng cho những người dùng đã đăng nhập.

    ![](readme_imgs/1.png)

    Do đó, tôi lại phải mất công làm công đoạn đăng nhập dài dòng này.

- Khi mày mò thì tôi đã tìm ra trang đăng nhập, ban đầu tôi chỉ nghĩ khi ấn `submit`, client sẽ chỉ gửi đi form-data là `username` và `password`. Nhưng không! Nó còn kèm theo cả `formToken`

    ![](readme_imgs/2.png)

    Nên việc sử dụng `requests` để POST có lẽ là không khả dụng.

- Vì vậy, tôi chuyển qua `selenium` để thao tác thủ công và nó hoạt động rất ổn áp. 

- Nhưng trước tiên là tôi phải cần 1 cái `chromedriver.exe`. Do đó, tôi đã viết một file ngắn để tự động kiểm tra và cập nhật driver mỗi lần chạy script (dùng `wget`)

- Sau một lúc inspect element, tôi đã rõ cấu trúc của các file ảnh và cuối cùng là thu thập hết chúng và lại dùng `requests` để lưu ảnh về local.

- Cuối cùng thì chỉ cần merge hết ảnh lại và xuất ra pdf thôi (dùng `img2pdf`).

> [!WARNING]
>
> Để đẩy nhanh quá trình tải ảnh và chuyển thành pdf, tôi đã sử dụng `multithreading`. Chức năng này có thể gây ngốn CPU nếu dung lượng sách quá lớn

- **Khá đơn giản nhỉ?**