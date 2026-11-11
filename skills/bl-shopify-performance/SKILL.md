---
name: bl-shopify-performance
description: "Phân tích hiệu suất quảng cáo Shopify/Meta, chẩn đoán funnel và đề xuất dừng, sửa, tiếp tục hoặc scale dựa trên hiệu quả kinh tế."
---

# Đọc số liệu, dừng và scale

## Đầu vào
Báo cáo ads và đơn cùng kỳ/currency/timezone, attribution window, chi phí, refund, thay đổi gần đây và giới hạn test.

## Cách thực hiện
1. Kiểm phạm vi báo cáo, độ trễ và tracking; không gộp số khác currency hoặc cửa sổ attribution. Đối chiếu orders Shopify nhưng không coi UTM là toàn bộ attribution.
2. Tính CPA, AOV, ROAS tổng bằng tổng revenue/tổng spend, và đóng góp sau ads theo chi phí thực. Không lấy trung bình đơn giản ROAS các dòng.
3. Chẩn đoán tuần tự exposure → click → landing → cart → checkout → purchase → hoàn/giao. Tách lỗi kỹ thuật với vấn đề thông điệp/offer/traffic.
4. Đối chiếu target CPA và giới hạn lỗ đã chốt; ghi mức chắc chắn, sample size và yếu tố còn thiếu. Không ép ra kết luận khi dữ liệu chưa đủ.
5. Đề xuất dừng/sửa/tiếp tục/scale cùng mức thay đổi, thời điểm review và điều kiện rollback; ghi M09. Chỉ thay ngân sách hoặc tắt/mở ads trong phạm vi được ủy quyền.

## Đầu ra và tiêu chí hoàn thành
Báo cáo M08 + quyết định có lý do, bảng kinh tế, chẩn đoán theo bằng chứng và M09 cho các thay đổi.
Chỉ đánh dấu hoàn thành phần có đầu ra và bằng chứng tương ứng; liệt kê việc còn chờ cùng đầu vào cần bổ sung.

## Điểm quyết định cần giữ
CTR 2%, CR 3%, tăng 20% là ví dụ không phải luật. Chi tiêu không bằng lỗ. Không nâng stop-loss để gỡ. Scale 100→120→144; rollback 144→120 phải về mức cũ, không mặc định giảm 20%. Lỗi checkout/tracking cần sửa trước khi đánh giá creative.

## Tài liệu theo nhu cầu
Đọc [quy trình và mẫu](references/quy-trinh.md) khi cần thực hiện chi tiết hoặc điền biểu mẫu. Đây là phần trích chọn theo nhiệm vụ từ giáo trình tổng hợp Binh Le, bản 05/11/2026; không phải quy định nền tảng hiện hành. Các mẫu do biên tập mới.

## Phạm vi và bằng chứng
Dùng nguồn người dùng cung cấp trước; hỏi phần thực sự thiếu và tiếp tục phần làm được. Tách dữ kiện, giả định và chưa kiểm chứng. Khi cần thông tin hiện hành về giao diện, điều kiện nền tảng hoặc thị trường, kiểm tra nguồn chính thức/nguồn trực tiếp và ghi ngày. Ưu tiên connector phù hợp nếu có; thiếu quyền hoặc công cụ thì bàn giao bản nháp/checklist và nêu giới hạn. Không báo đã thao tác khi chỉ mới hướng dẫn. Yêu cầu dùng skill không tự cấp quyền chi tiền, xuất bản, gửi tin hay thay đổi tài khoản. Tôn trọng quyền đã được cấp trong phiên, không xin lại máy móc.
