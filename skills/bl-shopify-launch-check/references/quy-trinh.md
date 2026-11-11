# Quy trình và mẫu liên quan

Nguồn: bộ giáo trình tổng hợp Shopify Binh Le, cuốn 02 và 03, phiên bản 05/11/2026. Trích nguyên các mục liên quan; SOP 19–22 là phần biên tập bổ sung.

## SOP 07. Tạo store, domain và cấu hình nền

**Đầu vào:** tài khoản hợp lệ, Master File, tên thương hiệu. **Đầu ra:** store có nhận diện, quyền quản trị và domain hoạt động.

1. Tạo/đăng nhập store bằng email anh kiểm soát. Điền thông tin doanh nghiệp đúng thực tế, tiền tệ và múi giờ phù hợp kế hoạch.
2. Chọn gói theo chức năng cần; kiểm giá đang hiển thị, chu kỳ và gia hạn. Không lấy giá khuyến mại trong PDF làm báo giá hiện tại.
3. Mua/kết nối domain hợp lệ; làm theo bản ghi DNS Shopify cung cấp tại thời điểm cấu hình. Kiểm cả tên chính, chuyển hướng và HTTPS.
4. Đặt tên store, email hỗ trợ, sender email và thông tin liên hệ nhất quán. Thử nhận/gửi email cần thiết.
5. Chọn theme hợp lệ; tạo bản sao trước sửa. Nếu dùng ZIP, đó phải là file theme được quyền sử dụng; không có ZIP gốc trong bộ học này.
6. Tạo navigation tối thiểu: trang chủ, sản phẩm/collection liên quan, liên hệ, shipping, returns/refunds, privacy và terms theo hoạt động thật.
7. Ghi quyền truy cập và cách khôi phục. Chỉ publish giao diện sau SOP 14.

**Đạt khi:** mở được domain đúng, nhận diện đúng, email hoạt động, có bản sao theme. **Xử lý lỗi:** DNS/HTTPS chưa ổn thì kiểm trạng thái kết nối; upload theme lỗi thì kiểm cấu trúc ZIP/giấy phép và hỗ trợ theme, không cài thêm app ngẫu nhiên.

## SOP 09. Cấu hình Markets, shipping, payment và chính sách

**Đầu vào:** thị trường test, báo giá ship, payment hợp lệ, chính sách đã chốt. **Đầu ra:** checkout có thể nhận đơn đúng điều kiện.

1. Bật đúng thị trường bán. Kiểm sản phẩm có được bán ở market đó, currency và ngôn ngữ hiển thị.
2. Vào cấu hình shipping của cửa hàng. Nếu đang dùng profiles, kiểm sản phẩm/location/profile/zone; nếu đã chuyển sang shipping options by market, cấu hình trong market tương ứng. Shopify đang triển khai hai kiểu giao diện. [Hướng dẫn shipping](https://help.shopify.com/en/manual/fulfillment/setup/shipping-rates/setting-up-shipping-rates).
3. Tạo rate theo chi phí thực và offer. Ví dụ biên tập: 3,99 USD dưới 40 USD; miễn phí từ 40 USD. Kiểm 39,99 / 40 / 40,01 và sau khi giảm giá. Đây không phải mức bắt buộc của bài.
4. Đặt tên dịch vụ và thời gian đúng khả năng giao. Tách thời gian xử lý khỏi vận chuyển. Không gọi “Express” nếu không có dịch vụ khác tương ứng.
5. Kết nối payment bằng thông tin thật; xác minh trạng thái kích hoạt và tài khoản nhận payout. Kiểm phí của phương thức dự định dùng.
6. Kiểm cấu hình thuế/nhập khẩu theo hoạt động thực và thị trường; không coi “not collecting” trong ảnh mẫu là đáp án chung. Chưa xác định nghĩa vụ thì phải làm rõ trước bán thật.
7. Điền chính sách theo khả năng thực: thời gian giao, xử lý trễ, điều kiện return, địa chỉ/luồng trả, ai trả phí, cách liên hệ và quyền riêng tư.
8. Kiểm policy ở footer, product và checkout nhất quán; không hứa hoàn 120 ngày chỉ vì đối thủ dùng con số đó.

**Đạt khi:** market, sản phẩm, rate và payment khớp. **Lỗi không có rate:** kiểm địa chỉ, profile/location, cân nặng nếu dùng weight rate, khoảng giá sau discount và market active. **Lỗi payment:** kiểm provider/test mode/eligibility trước khi sửa giao diện.

## SOP 10. Chuẩn bị Meta và cài đo lường

**Đầu vào:** store, tài sản Meta hợp lệ, quyền quản trị. **Đầu ra:** bản đồ tài sản và luồng event được kiểm.

1. Trong business, kiểm đúng Page, ad account và người quản trị. Nếu nhận lời mời, xác minh đúng doanh nghiệp/người gửi và phạm vi tài sản được cấp.
2. Kiểm tiền tệ, múi giờ, billing và giới hạn chi. Phân biệt số dư/thẻ, ngưỡng thu tiền, giới hạn chi tài khoản và ngân sách chiến dịch.
3. Tạo hoặc chọn dataset phù hợp; gán quyền với ad account. Lưu ID trong sổ tài sản; token để riêng trong nơi bảo mật.
4. Chọn một tích hợp chính. Bài dùng Omega/1Pixel; lựa chọn khác là kênh Facebook & Instagram trong Shopify. Không bật đồng thời nhiều đường gửi cùng sự kiện khi chưa hiểu deduplication.
5. Với tích hợp native, vào Settings của kênh để kết nối pixel và mức chia sẻ dữ liệu phù hợp; với app, cấu hình theo app và bật embed nếu cần. Kiểm chính sách dữ liệu của store. [Shopify: chia sẻ dữ liệu Meta](https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/meta-data-sharing).
6. Mở Test Events/Diagnostics, thao tác có kiểm soát trên site: xem trang, sản phẩm, add to cart, checkout. Kiểm ID đúng và tham số hợp lý.
7. Hoàn tất Purchase trong SOP 14; kiểm browser/server được hợp nhất thay vì đếm hai lần cho một giao dịch.
8. Gỡ test event code sau kiểm theo yêu cầu tích hợp; giữ log kết quả. Đối chiếu có đơn trong Shopify và event tương ứng, đồng thời hiểu rằng test mode có thể được các tích hợp xử lý khác nhau.

**Đạt khi:** có log test, không chỉ ảnh “pixel connected”. **Chờ:** không kiểm được Purchase/value/currency hoặc có event trùng. Không tự tạo Pixel mới để “reset” một lỗi chưa chẩn đoán.

## SOP 14. Kiểm thử trước mở bán

**Đầu vào:** store gần hoàn tất, payment và tracking đã kết nối. **Đầu ra:** biên bản pass/fail có ảnh/log.

1. Mở URL từ góc nhìn khách, cả mobile/desktop. Kiểm đúng tên miền, sản phẩm, currency, giá, ảnh, chính sách và liên hệ.
2. Kiểm tất cả biến thể bán và từng bundle. Thay số lượng, add/remove, áp discount. Giá giỏ phải đúng bảng tính.
3. Thử địa chỉ hợp lệ trong vùng nhận giao và ngoài vùng. Không tạo đơn thật gửi tới người không liên quan.
4. Kiểm phí giao sát ngưỡng và sau giảm giá; kiểm giỏ gồm nhiều sản phẩm/profile nếu có.
5. Thực hiện đơn thử bằng chế độ test của provider/Shopify theo khả năng hỗ trợ. Shopify khuyến nghị test trong quá trình setup và sau đổi payment; test mode không nhận đơn live và cần tắt khi xong. [Shopify: đặt đơn thử](https://help.shopify.com/en/manual/checkout-settings/test-orders).
6. Kiểm đơn được tạo, SKU/giá/tax/ship đúng, email xác nhận, tồn kho và fulfillment không gửi hàng thật ngoài ý muốn. Có thể test thất bại thanh toán theo hướng dẫn provider.
7. Kiểm Purchase, value/currency và trùng sự kiện theo tích hợp. Nếu test mode không phát sự kiện live, ghi rõ và dùng phương án kiểm được provider hỗ trợ; không coi việc không hiện trong báo cáo payout là lỗi.
8. Sau test, tắt chế độ test, khôi phục provider thật, kiểm trạng thái cửa hàng và password nếu chuẩn bị mở. Đánh dấu/hủy đơn thử theo luồng để không gửi supplier.
9. Kiểm ad preview: Page, creative, text, URL, UTM, country, event, budget, lịch và timezone.

**Điều kiện mở bán:** không còn lỗi giá/variant/payment/shipping; đo lường được kiểm; supplier sẵn; chi phí và mức lỗ đã chốt. **Lỗi nghiêm trọng:** giữ quảng cáo off, sửa và test lại đúng đường lỗi.

## M07. Biên bản QA và đơn thử

| Kiểm tra | Kết quả | Bằng chứng / lỗi / người xử lý |
|---|---|---|
| Mobile/desktop, domain, HTTPS | … | … |
| Product/variant/ảnh/claim đúng | … | … |
| Giá, bundle, discount, currency | … | … |
| Add/remove cart, quantity | … | … |
| Shipping dưới/đúng/trên ngưỡng | … | … |
| Market nhận giao / ngoài vùng | … | … |
| Payment thành công/thất bại thử | … | … |
| Đơn tạo đúng, email đúng | … | … |
| Purchase/value/currency/dedup | … | … |
| Không gửi supplier đơn thử | … | … |
| Đã tắt test mode, sẵn live | … | … |
| Page/dataset/URL/UTM/budget/timezone | … | … |

Mỗi lỗi có bước tái hiện. “Đã bấm thử” không đủ nếu chưa kiểm kết quả trong đơn và hệ thống event.
