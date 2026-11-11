---
name: bl-shopify-unit-economics
description: "Tính landed cost, giá/bundle, CPA và ROAS hòa vốn hoặc mục tiêu cho sản phẩm Shopify; kiểm tra hiệu quả một đơn trước test quảng cáo."
---

# Tính giá và biên lợi nhuận

## Đầu vào
Doanh thu sau discount chưa thuế thu hộ, landed, phí biến đổi, tổn thất hoàn dự kiến, tỷ lệ đóng góp mục tiêu; cùng currency.

## Cách thực hiện
1. Chuẩn hóa doanh thu R và chi phí C theo từng bundle; không lấy chi phí gói một cho gói ba. Chi phí thiếu phải ghi thiếu, không mặc định bằng 0.
2. Tính CM=R−C, CPA hòa vốn=CM, ROAS hòa vốn=R/CM khi CM>0. Với m là tỷ lệ đóng góp sau ads: target CPA=CM−mR; target ROAS=R/target CPA khi dương.
3. Dùng scripts/calculate.py với JSON theo references/calculator.md để tính nhất quán; có thể tính trực tiếp theo công thức nếu không chạy được Python.
4. Lập kịch bản cơ sở, phí vận chuyển tăng và hoàn tăng; chọn mức test có khoảng dự phòng, chỉ rõ giả định.
5. Nếu CPA mục tiêu không dương, ghi không khả thi với các đầu vào hiện tại và đề xuất kiểm tra giá/chi phí.

## Đầu ra và tiêu chí hoàn thành
Bảng M04 theo bundle, giả định/nguồn báo giá, CPA/ROAS hòa vốn và mục tiêu, đóng góp sau ads nếu có CPA thực; kết luận khả thi có điều kiện.
Chỉ đánh dấu hoàn thành phần có đầu ra và bằng chứng tương ứng; liệt kê việc còn chờ cùng đầu vào cần bổ sung.

## Điểm quyết định cần giữ
ROAS không phải lợi nhuận ròng. Chưa trừ chi phí cố định và thuế thu nhập. Không trừ dự phòng và cùng khoản hoàn thực hai lần. Mức 3–5 lần landed hay 20 USD trước ads trong bài là heuristic, không phải chuẩn lợi nhuận bắt buộc.

## Tài liệu theo nhu cầu
Đọc [quy trình và mẫu](references/quy-trinh.md) khi cần thực hiện chi tiết hoặc điền biểu mẫu. Đây là phần trích chọn theo nhiệm vụ từ giáo trình tổng hợp Binh Le, bản 05/11/2026; không phải quy định nền tảng hiện hành. Các mẫu do biên tập mới.

## Phạm vi và bằng chứng
Dùng nguồn người dùng cung cấp trước; hỏi phần thực sự thiếu và tiếp tục phần làm được. Tách dữ kiện, giả định và chưa kiểm chứng. Khi cần thông tin hiện hành về giao diện, điều kiện nền tảng hoặc thị trường, kiểm tra nguồn chính thức/nguồn trực tiếp và ghi ngày. Ưu tiên connector phù hợp nếu có; thiếu quyền hoặc công cụ thì bàn giao bản nháp/checklist và nêu giới hạn. Không báo đã thao tác khi chỉ mới hướng dẫn. Yêu cầu dùng skill không tự cấp quyền chi tiền, xuất bản, gửi tin hay thay đổi tài khoản. Tôn trọng quyền đã được cấp trong phiên, không xin lại máy móc.

Xem [định dạng máy tính](references/calculator.md) khi chạy helper.
