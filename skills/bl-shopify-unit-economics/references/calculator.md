# Máy tính kinh tế một đơn

Chạy `python3 scripts/calculate.py input.json` từ thư mục skill. Không cần cài thư viện ngoài. Tất cả số tiền phải cùng currency, cùng bundle và cùng cơ sở một đơn; helper không tự đổi tiền hoặc xác minh báo giá.

```json
{
  "revenue": 49,
  "landed": 13,
  "variable_fees": 3,
  "refund_loss": 2,
  "target_margin": 0.20,
  "actual_cpa": 25
}
```

- `revenue`: sản phẩm sau discount + ship khách trả, loại thuế thu hộ.
- `landed`: hàng + vận chuyển/fulfillment/bao bì và chi phí nhập hàng phân bổ, không trùng variable_fees.
- `variable_fees`: payment và chi phí biến đổi khác trước ads.
- `refund_loss`: tổn thất kỳ vọng một đơn; nếu dùng tổn thất thực phân bổ thì thay dự phòng, không cộng trùng.
- `target_margin`: tỷ lệ đóng góp sau ads trước cố định và thuế thu nhập, dạng 0–<1.
- `actual_cpa`: tùy chọn; các trường khác bắt buộc. Chỉ điền 0 khi đã xác minh khoản đó bằng 0.

Kết quả ví dụ: CM 31; BE ROAS 1.5806; target CPA 21.2000; target ROAS 2.3113; đóng góp sau CPA thực là 6. Khi CM/CPA mục tiêu không dương, ngưỡng tương ứng trả null; `feasible_paid_acquisition=false` nghĩa không còn ngân sách ads dương theo mục tiêu đó. Số được xuất thành chuỗi thập phân bốn chữ số để tránh sai số nhị phân.

Không gồm chi phí cố định, thuế thu nhập hoặc dòng tiền payout. Đối chiếu báo giá và lập kịch bản phí/hoàn thay đổi trước quyết định test.
