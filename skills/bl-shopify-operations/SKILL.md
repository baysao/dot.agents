---
name: bl-shopify-operations
description: "Tổ chức fulfillment, đơn ngoại lệ, bản nháp chăm sóc khách, hoàn trả và đối soát dòng tiền Shopify sau khi có đơn."
---

# Vận hành đơn và dòng tiền

## Đầu vào
Orders, trạng thái payment/fulfillment/tracking, chính sách, supplier, payout và báo cáo chi phí; chỉ lấy dữ liệu cá nhân cần dùng.

## Cách thực hiện
1. Đối chiếu đơn/variant/địa chỉ/payment và nguy cơ ngoại lệ; lập hàng chờ xử lý có người phụ trách.
2. Đối chiếu supplier và tracking thực trước cập nhật; ưu tiên đơn quá hạn hoặc thiếu hàng theo cam kết giao.
3. Soạn trả lời khách dựa trên trạng thái thực và chính sách; phân biệt return, refund, cancellation và chargeback. Kiểm khoản đã hoàn trước đề xuất hoàn tiếp.
4. Lập dòng tiền: tiền nhận thực, payout đang chờ, supplier, ads, hoàn, phí và số dư dự kiến; phân biệt doanh thu kế toán và tiền khả dụng.
5. Review tuần, nguyên nhân gốc và việc sửa. Gửi tin, đặt hàng, refund hay đổi trạng thái đơn chỉ khi đúng phạm vi được người dùng ủy quyền; yêu cầu lập sổ hoặc soạn nháp không cấp quyền đó.

## Đầu ra và tiêu chí hoàn thành
M10 hàng chờ ngoại lệ + bản nháp CS; M11 đối soát/dòng tiền, vấn đề tuần và việc cải tiến. Ẩn thông tin khách không cần thiết trong báo cáo tổng hợp.
Chỉ đánh dấu hoàn thành phần có đầu ra và bằng chứng tương ứng; liệt kê việc còn chờ cùng đầu vào cần bổ sung.

## Điểm quyết định cần giữ
Không đánh dấu shipped khi chưa có bằng chứng. Không hứa ngày giao ngoài dữ liệu supplier. Không xem payout là doanh thu mới hoặc trừ refund hai lần. SOP 19–22 là phần biên tập bổ sung của giáo trình, không phải bài giảng gốc đầy đủ.

## Tài liệu theo nhu cầu
Đọc [quy trình và mẫu](references/quy-trinh.md) khi cần thực hiện chi tiết hoặc điền biểu mẫu. Đây là phần trích chọn theo nhiệm vụ từ giáo trình tổng hợp Binh Le, bản 05/11/2026; không phải quy định nền tảng hiện hành. Các mẫu do biên tập mới.

## Phạm vi và bằng chứng
Dùng nguồn người dùng cung cấp trước; hỏi phần thực sự thiếu và tiếp tục phần làm được. Tách dữ kiện, giả định và chưa kiểm chứng. Khi cần thông tin hiện hành về giao diện, điều kiện nền tảng hoặc thị trường, kiểm tra nguồn chính thức/nguồn trực tiếp và ghi ngày. Ưu tiên connector phù hợp nếu có; thiếu quyền hoặc công cụ thì bàn giao bản nháp/checklist và nêu giới hạn. Không báo đã thao tác khi chỉ mới hướng dẫn. Yêu cầu dùng skill không tự cấp quyền chi tiền, xuất bản, gửi tin hay thay đổi tài khoản. Tôn trọng quyền đã được cấp trong phiên, không xin lại máy móc.
