"# student_manager" 
DONE: 
- Tự gender user sinh viên => DONE!
- Update avatar, thông tin user => DONE!
- Create giảng viên => DONE!
- Ấn vào tên sinh viên hiển thị thông tin => DONE!
* Giờ muốn cho sinh viên đăng kí được lớp thì phải có lớp => Tạo lớp
* Thời khóa biểu trống vì chưa đăng kí lớp => Đăng kí lớp
* Đăng kí học lại trống vì chưa có môn phải học lại ( Điểm tổng kết < 4.0 )
- PHIÊN 1: GIÁO VIÊN - HỌC SINH

- Tạo lớp
- Tạo thêm 5 sinh viên có cùng một ngành
- Nếu ngày đăng kí còn khả dụng => Cho phép đăng kí, còn không thì ngược lại => FAILED! ( Đã làm trong chức năng đăng kí học lại )
   + Đăng kí lớp => DONE!
   + Hủy lớp  => DONE !
   + Đăng kí lớp đã đăng kí rồi thì báo lỗi  => DONE!
   + Sau khi đăng kí 1 ngày thì không được quyền hủy lớp => DONE !
   + Quá hạn đăng kí lớp ( cải thiện ) => DONE!
   + Khi sinh viên kết thúc lớp đó, giáo viên sẽ cập nhật lại điểm, nếu qua thì khi hủy lớp thì sẽ không thấy lớp đó trong danh sách học lại ( Vì môn đấy sinh viên đã học qua ) => DONE!
   + Xử lý trường hợp lớp đã full => DONE!
- Học phí: Đăng kí lớp thành công thì số tiền tự động tăng ( 1 tín chỉ 300k ), hủy lớp thì số tiền cũng sẽ trừ đi => DONE!
- Giáo viên có thể thấy lớp đang giảng dạy của mình => DONE!
- Đăng kí lớp thành công => Giáo viên có thể thấy sinh viên đó trong lớp của mình => DONE!
* Giáo viên cập nhật điểm cho sinh viên => Hệ thống tự động tính điểm :
  + Cập nhật điểm bằng file excel:
    _ input: .xlsx file. Nếu danh sách sinh viên trong file có mã sinh viên trung với mã sinh viên của lớp đó => Cập nhật điểm những sinh viên đó => DONE!

  + Ấn xuất phiếu điểm => Xuất file excel => DONE
  + Khi sinh viên học lại xong, giáo viên cập nhật điểm cho sinh viên tại lớp mới thì sẽ cập nhật lại luôn điểm ban đầu của sinh viên => DONE!
  + >= 4.0 => Sinh viên qua môn  => DONE!
  + < 4.0 => Sinh viên học lại : 
        _ Nếu có lớp trùng với môn cho sinh viên đăng kí học lại thì hiển thị lớp đó => DONE!
        _ Nếu lớp đó đã hết hạn đăng kí thì sẽ không cho đăng kí => DONE!   

* Chức năng tạo lịch sử khi cập nhật điểm

- PHIÊN 2: ADMIN - HỌC SINH
 * Nhập danh sách sinh viên từ file excel:
	+ Thiếu thông tin tên và ngày sinh thì sẽ không được nhập vào => DONE!
 * Quản lý học phí: 
	+ Chuẩn hóa input thành chữ hoa => DONE !
	+ Tìm kiếm thông tin học phí theo mã sinh viên => DONE !
	+ Trường hợp còn phải đóng thêm => DONE !
        + Trường hợp đóng dư => DONE!

	- LỊCH SỬ GIAO DỊCH => DONE!

 * Gửi tin nhắn đến sinh viên
	+ Lọc người nhận theo lớp => DONE!
	+ Xử lý nếu chưa chọn người nhận thì hiện thông báo => DONE!
	+ Gửi tới 1 người => DONE!
	+ Gửi tới nhiều người => DONE!
	+ Thống báo có tin nhắn mới => DONE!
	+ Xử lý tin nhắn chưa đọc và tin nhắn đã đọc => DONE!

 * Tìm kiếm thông tin của sinh viên
	+ Tìm kiếm theo lớp => DONE!
	+ Tìm kiếm theo mã sinh viên, họ tên  => DONE!

* TÀI LIỆU: 
	+ THANG ĐIỂM ( ĐỂ SAU )
	+ CÁCH TÍNH ĐIỂM TÍCH LŨY ( ĐỂ SAU )
"# student_manager" 
