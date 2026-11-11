# Quy trình và mẫu liên quan

Nguồn: bộ giáo trình tổng hợp Shopify Binh Le, cuốn 02 và 03, phiên bản 05/11/2026. Trích nguyên các mục liên quan; SOP 19–22 là phần biên tập bổ sung.

## SOP 05. Xác minh supplier và chọn một sản phẩm test

**Đầu vào:** shortlist; yêu cầu về SKU, tuyến giao và offer. **Đầu ra:** một SKU được duyệt, báo giá và phương án dự phòng.

1. Gửi yêu cầu báo giá cùng ảnh, mã mẫu, size/màu/dung lượng, quốc gia giao, số lượng từng bundle, loại bao bì và tracking.
2. Hỏi rõ tiền hàng, pick/pack, shipping, khoản nhập khẩu bên bán chịu, phụ phí vùng xa, thời gian xử lý và thời gian giao. Yêu cầu ngày hiệu lực báo giá.
3. Xác minh tồn và khả năng bổ sung. Hỏi lịch nghỉ và cách xử lý nếu hết SKU; không cho tự thay mẫu.
4. Lấy mẫu hoặc bằng chứng kiểm tra đủ để xác nhận chức năng, thông số và hình hàng thực. Với mặt hàng có yêu cầu riêng, chưa đủ hồ sơ thì chưa bán.
5. Thống nhất hàng lỗi, thất lạc, sai địa chỉ, tracking chậm, đổi trả và phí giao lại. Ghi ai xử lý và trong bao lâu.
6. Điền bảng unit economics cho từng gói. Dùng chi phí bảo thủ nếu còn bất định; không giấu phí để làm biên đẹp.
7. So 5 tiêu chí chính và 2 điểm cộng của lớp. Nếu còn thiếu điều kiện cốt lõi, để pending; chỉ xếp hạng các ứng viên đủ điều kiện.
8. Chọn một SKU và một angle ban đầu; lưu lý do loại/chờ các món khác để nghiên cứu sau.

**Đạt khi:** đúng hàng, đủ thông tin, margin khả thi và có người chịu trách nhiệm cung ứng. **Dừng:** nguồn chỉ gửi ảnh tương tự, báo giá thiếu ship, không có quyền hàng hóa/tư liệu hoặc không đáp ứng cam kết khách.

**Mẫu tin nhắn supplier:** “Please quote the exact item in the attached reference, including variant, unit cost, packing, tracked shipping to [country], processing time, delivery range, available stock, and the policy for defects/lost parcels. Please quote 1/2/3 units separately and confirm that no substitute SKU will be shipped without approval.”

## SOP 21. Đối soát tài chính và dòng tiền

**Bổ sung vận hành. Đầu vào:** đơn, chi phí supplier, ads, phí cổng, refund và payout. **Đầu ra:** báo cáo lãi/lỗ quản trị và dự báo tiền mặt.

1. Chốt kỳ báo cáo, currency và cơ sở doanh thu. Tách thuế thu hộ khỏi doanh thu quản trị; dùng tỷ giá thực hoặc phương pháp nhất quán khi quy đổi.
2. Ghi doanh thu sau discount, refund thực, phí ship khách trả và chi phí giao bên bán. Không ghi refund vừa trừ doanh thu vừa trừ chi phí thêm lần nữa.
3. Gắn COGS/ship/fulfillment từng đơn hoặc mức ước tính có căn cứ. Cập nhật khi có hóa đơn thật; kiểm đơn giao lại và hàng mất.
4. Ghi spend ads, payment fees, app, editor, công cụ và chi phí cố định. Báo rõ lợi nhuận trước/sau các khoản nào.
5. Đối chiếu payout: doanh thu phát sinh khác với tiền đang chờ/đã nhận; giải thích chênh do phí, reserve, refund hoặc lịch chuyển.
6. Lập dự báo tiền ra trước payout cho 7–14 ngày theo kịch bản nội bộ. Giữ quỹ cho các đơn còn phải phục vụ, không xem toàn bộ payout là tiền có thể rút dùng cá nhân.
7. Tổng hợp CM, CPA, lợi nhuận sau ads, lợi nhuận sau cố định, tỷ lệ hoàn và lý do. Kết quả này là cơ sở scale của SOP 18.

**Đạt khi:** số dư tiền và lợi nhuận được giải thích riêng. **Chờ:** chỉ có screenshot ROAS hoặc doanh thu gross mà chưa biết phí và tiền hàng.

## M04. Bảng kinh tế đơn hàng

| Khoản USD/đơn | Gói 1 | Gói 2 | Gói 3 |
|---|---|---|---|
| Giá sản phẩm sau discount | … | … | … |
| Ship khách trả | … | … | … |
| R: doanh thu, không thuế thu hộ | … | … | … |
| Tiền hàng | … | … | … |
| Ship/fulfillment/bao bì bên bán | … | … | … |
| Payment và chi phí biến đổi khác | … | … | … |
| Dự phòng tổn thất hoàn/đổi | … | … | … |
| C: tổng chi phí biến đổi trước ads | … | … | … |
| CM = R − C | … | … | … |
| CPA hòa vốn = CM | … | … | … |
| ROAS hòa vốn = R/CM | … | … | … |
| Tỷ lệ đóng góp mục tiêu sau ads m | … | … | … |
| CPA mục tiêu = CM − m×R | … | … | … |
| ROAS mục tiêu = R/CPA mục tiêu | … | … | … |

Chỉ tính ROAS nếu mẫu số dương. Lợi nhuận đóng góp chưa trừ chi phí cố định và thuế thu nhập. Khi chuyển từ dự phòng sang dữ liệu hoàn thực, thay phương pháp rõ ràng để không trừ cùng tổn thất hai lần.

**Bài tập mẫu:** R=49; landed=13; payment/khác=3; hoàn dự phòng=2; m=20%. Kết quả: C=18; CM=31; BE ROAS≈1,58; target CPA=21,20; target ROAS≈2,31. CPA thực 25 thì còn 6 USD/đơn trước cố định.
