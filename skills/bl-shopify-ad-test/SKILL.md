---
name: bl-shopify-ad-test
description: "Lập kế hoạch thử nghiệm Meta Ads cho Shopify với cấu trúc campaign/ad set/ad, giả thuyết, ngân sách và điều kiện dừng rõ ràng."
---

# Thiết kế test quảng cáo

## Đầu vào
Readiness, kinh tế đơn, creative, thị trường/currency/timezone, ngân sách test và lỗ tối đa đã chốt.

## Cách thực hiện
1. Kiểm đầu vào và blocker của store/measurement; thiếu dữ liệu vẫn lập bản nháp và đánh dấu phần chưa thể mở.
2. Nêu giả thuyết test, biến thay đổi và KPI ra quyết định. Sales/Website/Purchase, broad một thị trường và CBO là mẫu khởi đầu trong bài, điều chỉnh theo mục tiêu và tính năng hiện hành.
3. Lập bảng campaign/ad set/ad cùng creative, URL, UTM, identity, event, currency/timezone.
4. Chốt ngân sách, cách tính lỗ tối đa và lịch review theo dữ liệu; tách daily budget với billing threshold, card limit và account spending limit.
5. Kiểm preview, URL/event, trùng bản nháp và quyền thực thi. Chỉ mở chiến dịch khi người dùng đã yêu cầu/ủy quyền đúng phạm vi; không xin lại nếu đã có quyền và cấu hình nằm trong phạm vi đó.

## Đầu ra và tiêu chí hoàn thành
Kế hoạch M08, cấu trúc setup có thể duyệt, checklist trước publish và quy tắc tiếp tục/sửa/dừng; nói rõ trạng thái nháp hay đã thực thi.
Chỉ đánh dấu hoàn thành phần có đầu ra và bằng chứng tương ứng; liệt kê việc còn chờ cùng đầu vào cần bổ sung.

## Điểm quyết định cần giữ
50 USD/ngày, lỗ 150 USD hay warmup 1 USD trong bài không phải yêu cầu mặc định. Daily budget có thể là mức trung bình theo nền tảng. CBO chia tiền không đều; ad ít exposure chưa đủ kết luận thua. Warmup không bảo đảm tránh khóa tài khoản.

## Tài liệu theo nhu cầu
Đọc [quy trình và mẫu](references/quy-trinh.md) khi cần thực hiện chi tiết hoặc điền biểu mẫu. Đây là phần trích chọn theo nhiệm vụ từ giáo trình tổng hợp Binh Le, bản 05/11/2026; không phải quy định nền tảng hiện hành. Các mẫu do biên tập mới.

## Phạm vi và bằng chứng
Dùng nguồn người dùng cung cấp trước; hỏi phần thực sự thiếu và tiếp tục phần làm được. Tách dữ kiện, giả định và chưa kiểm chứng. Khi cần thông tin hiện hành về giao diện, điều kiện nền tảng hoặc thị trường, kiểm tra nguồn chính thức/nguồn trực tiếp và ghi ngày. Ưu tiên connector phù hợp nếu có; thiếu quyền hoặc công cụ thì bàn giao bản nháp/checklist và nêu giới hạn. Không báo đã thao tác khi chỉ mới hướng dẫn. Yêu cầu dùng skill không tự cấp quyền chi tiền, xuất bản, gửi tin hay thay đổi tài khoản. Tôn trọng quyền đã được cấp trong phiên, không xin lại máy móc.
