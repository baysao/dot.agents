---
name: bl-shopify-launch-check
description: "Kiểm tra store Shopify, Markets, shipping, payment, tracking và đơn thử trước mở bán; lập biên bản sẵn sàng/chưa sẵn sàng có bằng chứng."
---

# Kiểm tra trước mở bán

## Đầu vào
URL/quyền đọc store hoặc ảnh cấu hình, thị trường, SKU/offer, payment, shipping, pixel và phạm vi kiểm thử được phép.

## Cách thực hiện
1. Kiểm tài sản/domain, chủ thể kinh doanh thực và payment hợp lệ; đối chiếu tài liệu Shopify hiện hành khi cần yêu cầu theo quốc gia.
2. Kiểm Markets, shipping profile/location, giá và currency, chính sách, variant và bundle từ mobile đến checkout. Kiểm ngưỡng miễn ship ngay dưới/đúng/trên ngưỡng và sau discount.
3. Kiểm đường đo lường Pixel/CAPI, dedup, Purchase value/currency, consent phù hợp và UTM. PageView/ATC thành công chưa chứng minh Purchase đúng.
4. Thực hiện đơn thử trong phạm vi người dùng đã cho; ghi test mode hay giao dịch thật và giới hạn sự kiện. Không tự thực hiện thanh toán thật từ yêu cầu audit.
5. Đánh dấu Đạt/Không đạt/Chưa kiểm chứng từng mục; nêu blocker và cách xác minh lại.

## Đầu ra và tiêu chí hoàn thành
Biên bản M07 gồm môi trường, bước thử, kết quả mong đợi/thực tế, bằng chứng, blocker, người xử lý và quyết định readiness.
Chỉ đánh dấu hoàn thành phần có đầu ra và bằng chứng tương ứng; liệt kê việc còn chờ cùng đầu vào cần bổ sung.

## Điểm quyết định cần giữ
Không dùng địa chỉ giả/giấy tờ mượn để mở payment. Không mặc định mỗi SKU cần pixel mới. Tên mục Shopify có thể đổi, không báo đã kiểm chứng từ checklist lý thuyết. Không coi thiếu quyền đọc là đạt.

## Tài liệu theo nhu cầu
Đọc [quy trình và mẫu](references/quy-trinh.md) khi cần thực hiện chi tiết hoặc điền biểu mẫu. Đây là phần trích chọn theo nhiệm vụ từ giáo trình tổng hợp Binh Le, bản 05/11/2026; không phải quy định nền tảng hiện hành. Các mẫu do biên tập mới.

## Phạm vi và bằng chứng
Dùng nguồn người dùng cung cấp trước; hỏi phần thực sự thiếu và tiếp tục phần làm được. Tách dữ kiện, giả định và chưa kiểm chứng. Khi cần thông tin hiện hành về giao diện, điều kiện nền tảng hoặc thị trường, kiểm tra nguồn chính thức/nguồn trực tiếp và ghi ngày. Ưu tiên connector phù hợp nếu có; thiếu quyền hoặc công cụ thì bàn giao bản nháp/checklist và nêu giới hạn. Không báo đã thao tác khi chỉ mới hướng dẫn. Yêu cầu dùng skill không tự cấp quyền chi tiền, xuất bản, gửi tin hay thay đổi tài khoản. Tôn trọng quyền đã được cấp trong phiên, không xin lại máy móc.
