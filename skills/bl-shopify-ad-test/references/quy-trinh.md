# Quy trình và mẫu liên quan

Nguồn: bộ giáo trình tổng hợp Shopify Binh Le, cuốn 02 và 03, phiên bản 05/11/2026. Trích nguyên các mục liên quan; SOP 19–22 là phần biên tập bổ sung.

## SOP 01. Chốt phạm vi, quyền tài sản và ngân sách

**Đầu vào:** thị trường dự kiến, chủ thể kinh doanh thật, tiền có thể sử dụng, thời gian làm việc. **Đầu ra:** phiếu dự án và danh sách tài sản.

1. Chọn một thị trường test đầu tiên. Bài gốc ưu tiên US; nếu chọn nơi khác, thay ngôn ngữ, giá, vận chuyển và bằng chứng nhu cầu tương ứng.
2. Xác định ai sở hữu store, domain, Page, ad account, dataset, tài khoản ngân hàng và nguồn hàng. Lưu ID và email quản trị; không lưu mật khẩu/token vào bảng chia sẻ.
3. Kiểm eligibility thanh toán theo quốc gia và loại hình thực. Không lấy quốc gia khách hàng làm quốc gia đăng ký kinh doanh.
4. Lập bốn ngăn chi phí: cố định; tiền test ads; tiền ứng hàng trước payout; dự phòng hoàn/đổi. Ghi mức lỗ tối đa của một test và của toàn đợt.
5. Chọn cách ghi số liệu: cùng currency, múi giờ báo cáo, doanh thu có/không thuế và phương pháp tính lỗ.
6. Bật bảo mật, lưu mã khôi phục riêng, cấp quyền theo công việc. Nếu thuê agency, ghi điều kiện bàn giao và thu hồi quyền.

**Đạt khi:** có chủ tài sản rõ, phương án thanh toán phù hợp và đủ tiền giao các đơn có thể phát sinh. **Dừng khi:** chưa xác minh được quyền hoặc nguồn tiền nhận; vẫn có thể nghiên cứu sản phẩm, nhưng chưa mở bán trả phí.

**Ghi chú bài gốc:** mốc 10 sản phẩm và 150 USD/test là ví dụ quản trị kỳ vọng. Không phải lịch buộc tiêu hết 1.500 USD và không bảo đảm có winner.

## SOP 15. Tạo và mở chiến dịch thử

**Đầu vào:** SOP 14 đạt, creative duyệt, ngân sách cho phép. **Đầu ra:** một test có giả thuyết, hạn mức và thời điểm bắt đầu rõ.

1. Ghi test ID, SKU, angle, ngày, phiên bản page/offer, CPA/ROAS mục tiêu và mức lỗ tối đa.
2. Theo cấu trúc bài: tạo Sales campaign, dùng campaign budget/CBO. Đặt tên có thị trường/SKU/ngày.
3. Tạo ad set: Website, dataset đúng, Purchase, đúng thị trường và nhóm phù hợp. Broad là cách khởi đầu trong lớp, không phải lý do bỏ kiểm country/age hoặc điều kiện ngành hàng.
4. Chọn ngân sách phù hợp bảng tiền. Nếu dùng ví dụ 50 USD/ngày, phải đủ sức chi và ứng tiền hàng; đọc thông báo mức chi tối đa trên giao diện.
5. Đặt ngày giờ theo timezone ad account. Ghi cửa sổ attribution đang dùng để đọc số nhất quán.
6. Tạo từng ad với một creative để dễ đọc; chọn đúng Page, text, CTA, URL và UTM. Kiểm các tiện ích auto/AI không làm đổi lời hứa hoặc trang đích.
7. Duplicate để tạo biến thể nhưng giữ draft/off trong lúc sửa. Rà từng hàng, không chỉ ad đầu.
8. Review cuối campaign/ad set/ad; sau khi duyệt mới publish. Ghi thời điểm approved/delivering; lịch “2–3 ngày test” tính theo thời gian thực sự phân phối có ý nghĩa.
9. Theo dõi lỗi delivery, URL và checkout sớm. Không sửa liên tục nếu chưa có sự cố hoặc giả thuyết rõ.

**Đạt khi:** đúng test đang phân phối, không có bản sao thừa, có log baseline. **Nếu không chi:** kiểm review/restriction, payment, lịch, audience, quyền và giới hạn; không quy ngay cho sản phẩm thua.

## SOP 17. Dừng, sửa hoặc tiếp tục test

**Đầu vào:** daily log và giới hạn đã đặt. **Đầu ra:** quyết định có ngày và lý do.

1. Nếu có lỗi payment, checkout, sai hàng hoặc supplier không giao: tạm dừng phần ads liên quan ngay; sửa trước khi tiêu thêm.
2. Nếu tracking sai: dùng đơn thật để đánh giá tạm, sửa đo lường, không kết luận sản phẩm chỉ từ event lỗi.
3. Nếu đã chạm mức lỗ tối đa: dừng test theo quy tắc đã chốt. Lỗ dự kiến sau ads = spend − phần đóng góp trước ads của các đơn, cộng khoản test riêng nếu đã quy định; không lẫn với tổng spend.
4. Nếu chưa có ATC sau khoảng 2 ngày hoặc chưa có Purchase sau khoảng 3 ngày ở bối cảnh test lớp, rà dữ liệu và phễu; đây là mốc xem xét, không định luật áp cho mọi mức chi.
5. Nếu có đơn, chưa quá giới hạn và có nguyên nhân sửa được: ghi một vòng test tiếp theo với thay đổi cụ thể và giới hạn còn lại. Không tự gia hạn vô hạn.
6. Nếu hòa vốn/đi ngang lâu: tính thời gian nội dung và cơ hội sản phẩm khác; có thể kết thúc dù chưa lỗ lớn.
7. Lưu bài học: nhu cầu, hook, offer, supplier, lỗi và tài sản có thể tái sử dụng hợp lệ.

**Đạt khi:** test được đóng hoặc tiếp tục có điều kiện rõ. **Không làm:** tăng ngân sách chỉ để “gỡ”, gọi mọi ad không có đơn là TOF cần giữ, hoặc thay mọi biến số cùng lúc rồi không lưu kết quả.

## M01. Phiếu dự án

| Trường | Nội dung cần điền |
|---|---|
| Mã dự án / ngày / người phụ trách | … |
| Thị trường / ngôn ngữ / currency / timezone | … |
| Chủ thể kinh doanh / phương án payment đã xác minh | … |
| Ngân sách cố định / ads / ứng hàng / dự phòng | Tách bốn khoản |
| Lỗ tối đa một test / cả đợt | Ghi cách tính, không chỉ số tiền |
| Thời gian có thể làm / người hỗ trợ | … |
| Điều kiện không mở bán | Ví dụ thiếu payment, sai SKU, thiếu bằng chứng |
| Ngày review và người quyết định | … |

## M08. Nhật ký test và báo cáo ngày

| Trường cấu hình test | Giá trị |
|---|---|
| Test ID / SKU / angle / page version | … |
| Campaign/ad set/ad IDs | … |
| Ngày giờ thực bắt đầu phân phối | … |
| Currency/timezone/attribution | … |
| Ngân sách ngày / giới hạn khác | … |
| CPA/ROAS mục tiêu và mức lỗ tối đa | … |
| Điều kiện dừng/sửa/tăng | … |

| Ngày | Spend | Đơn thật | Doanh thu cùng cơ sở | CM trước ads | Sau ads | Hành động |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |

Lưu thêm snapshot Meta campaign/ad set/ad và Shopify funnel cùng ngày. Phần doanh thu Meta attributed để riêng khỏi tổng doanh thu shop; không cộng các nguồn attribution trùng nhau.

**Ví dụ tránh bình quân ROAS:** ngày 1 chi 50, thu 150 → ROAS 3; ngày 2 chi 150, thu 150 → ROAS 1. ROAS gộp = 300/200 = 1,5, không phải (3+1)/2 = 2.
