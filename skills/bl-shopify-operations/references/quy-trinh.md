# Quy trình và mẫu liên quan

Nguồn: bộ giáo trình tổng hợp Shopify Binh Le, cuốn 02 và 03, phiên bản 05/11/2026. Trích nguyên các mục liên quan; SOP 19–22 là phần biên tập bổ sung.

## SOP 19. Xử lý đơn và giao hàng mỗi ngày

**Bổ sung vận hành. Đầu vào:** đơn Shopify, payment, supplier. **Đầu ra:** mỗi đơn có trạng thái và người xử lý.

1. Lọc đơn mới; xác minh payment, đúng SKU/variant, địa chỉ và yêu cầu đặc biệt. Đơn chưa thanh toán hoặc cần kiểm tra không tự gửi supplier như đơn bình thường.
2. Gửi đơn qua app/quy trình đã duyệt. Đối chiếu số lượng, giá vốn và địa chỉ; chỉ chia sẻ dữ liệu cần thiết cho giao hàng.
3. Ghi mã đơn supplier, hạn xử lý và trạng thái tồn. Nếu thiếu hàng, dừng bán phần liên quan và liên hệ khách về lựa chọn thực tế.
4. Khi có tracking, kiểm hãng/URL và việc kiện đã vào luồng vận chuyển. Cập nhật khách theo sự kiện thật.
5. Mỗi ngày rà đơn quá hạn xử lý, chưa có scan, đứng tracking, phát không thành công, sai/thiếu/hỏng.
6. Escalate supplier theo SLA đã thỏa thuận. Ghi lần hỏi và hạn cập nhật tiếp theo, không để ticket trôi.
7. Khi giao lại/hoàn, cập nhật cả customer log và chi phí; không bỏ chi phí ngoại lệ khỏi lợi nhuận.

**Đạt khi:** mọi đơn có đường đi và ngoại lệ có deadline. **Không làm:** đánh dấu shipped chỉ để đẹp chỉ số, tự thay SKU, dùng tracking không liên quan.

## SOP 20. Chăm sóc khách, đổi trả và tranh chấp

**Bổ sung vận hành. Đầu vào:** email/ticket và dữ liệu đơn. **Đầu ra:** phương án xử lý rõ, lưu lịch sử.

1. Xác minh đơn qua thông tin tối thiểu cần thiết; xem payment, fulfillment, tracking và trao đổi trước đó.
2. Phân loại: hỏi trước mua; sửa/hủy; hỏi giao; lỗi/sai hàng; return/refund; tranh chấp. Ghi ưu tiên theo ảnh hưởng và thời hạn thực tế.
3. Trả lời đúng tình trạng, hành động đang làm và thời điểm sẽ cập nhật. Mục tiêu nội bộ có thể là trong một ngày làm việc nếu đội ngũ đáp ứng; không hứa phản hồi 24/7 nếu không làm được.
4. Với hủy, kiểm supplier đã xử lý chưa. Với hàng lỗi, lấy thông tin cần để giải quyết, tránh yêu cầu không cần thiết; chọn giao lại/hoàn theo chính sách và nghĩa vụ phù hợp.
5. Nếu có hàng trả về, thiết lập return trước refund theo luồng Shopify phù hợp. Kiểm số tiền, shipping, số lượng, tồn và phương thức hoàn; refund đã khởi tạo không thể hủy đơn giản. [Shopify: refund](https://help.shopify.com/en/manual/fulfillment/managing-orders/refunding-orders).
6. Với chargeback, ghi hạn phản hồi do cổng cung cấp và chuẩn bị hồ sơ thật: đơn, mô tả, tracking, trao đổi. Không hứa chắc chắn thắng hoặc coi chargeback là refund thông thường.
7. Đóng ticket khi đã hoàn tất hoặc có mốc theo dõi; gắn nguyên nhân để sửa supplier, page hoặc quảng cáo.

**Mẫu trả lời trễ giao:** “Em đã kiểm tra đơn [mã]. Hiện kiện hàng đang ở [trạng thái đã xác minh]. Bên em đang làm việc với đơn vị giao và sẽ cập nhật trước [mốc]. Nếu [điều kiện theo chính sách], bên em sẽ hỗ trợ [phương án thực].” Không điền trạng thái khi chưa kiểm được.

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

## SOP 22. Đánh giá tuần và cải tiến hệ thống

**Đầu vào:** daily log, creative log, supplier/CS log và tài chính. **Đầu ra:** kế hoạch tuần tới có ưu tiên.

1. Xem nhu cầu và cạnh tranh có thay đổi; nếu trì hoãn test, research lại thay vì dùng danh sách cũ.
2. Chọn 1–3 vấn đề ảnh hưởng lớn nhất: margin, conversion, creative, giao hàng hoặc hoàn. Gán người xử lý và hạn.
3. Phân loại creative: concept có tín hiệu, iteration cần thêm dữ liệu, đã đủ bằng chứng dừng. Giữ lịch sản xuất phù hợp ngân sách test.
4. Rà claim/offer với hàng thực, tình trạng supplier và phản hồi khách. Cập nhật Master File và các tài sản phụ thuộc.
5. Rà phí công cụ, quyền truy cập, backup, domain và app. Hủy công cụ không còn giá trị theo quy trình của chủ tài khoản.
6. Quyết định giữ, scale, mở thử nghiệm mới hoặc đóng sản phẩm. Ghi bài học để vòng research sau tốt hơn.

**Đạt khi:** có quyết định và người thực hiện; cuộc họp không chỉ xem dashboard.

## M10. Sổ đơn ngoại lệ và chăm sóc khách

| Mã đơn | Vấn đề | Trạng thái supplier/tracking | Việc đã làm | Hạn cập nhật | Chi phí thêm | Đã đóng? |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |

Tránh đưa dữ liệu khách không cần thiết vào bảng tổng hợp chung. Khi giao việc, người xử lý chỉ xem dữ liệu phù hợp nhiệm vụ.

## M11. Sổ dòng tiền và review tuần

| Ngày/kỳ | Tiền đầu kỳ | Payout dự kiến/đã nhận | Ads | Supplier | Phí/hoàn/khác | Tiền cuối kỳ |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |

Tiền cuối kỳ = đầu kỳ + tiền thực nhận − tiền thực chi. Payout dự kiến chưa cộng như tiền đã có. Review tuần trả lời: điều gì đã chứng minh; điều gì chưa biết; chỗ nào tốn tiền nhất; tuần sau sửa gì; ai làm; khi nào đánh giá.
