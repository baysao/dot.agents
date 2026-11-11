# Quy trình và mẫu liên quan

Nguồn: bộ giáo trình tổng hợp Shopify Binh Le, cuốn 02 và 03, phiên bản 05/11/2026. Trích nguyên các mục liên quan; SOP 19–22 là phần biên tập bổ sung.

## SOP 06. Lập Master File và sổ kiểm chứng nội dung

**Đầu vào:** hồ sơ sản phẩm, báo giá, ảnh, nghiên cứu khách. **Đầu ra:** Master File phiên bản có ngày.

1. Ghi tên nội bộ, SKU, supplier, ảnh chuẩn, thông số, vật liệu/thành phần, kích thước, hướng dẫn và giới hạn sử dụng.
2. Ghi thị trường, avatar giả thuyết, vấn đề, mong muốn, phản đối, ngôn ngữ khách. Phân biệt lời khách thật và suy luận của người viết.
3. Ghi giá/offer, các bundle, shipping, thời gian giao, điều kiện return/refund và email hỗ trợ.
4. Tạo bảng claim: câu muốn viết → nguồn → áp dụng đúng SKU không → giới hạn → được dùng/chờ/không dùng.
5. Tạo bảng quyền tài sản: file, nguồn, chủ quyền, phạm vi dùng quảng cáo, thời hạn, bằng chứng cho phép.
6. Đưa vào AI chỉ những dữ kiện được phép dùng. Yêu cầu trả “thiếu dữ kiện” khi không biết; không cho tự tạo review, % hiệu quả, chứng nhận hoặc ảnh trước/sau.
7. Khóa phiên bản dùng cho lần test. Thay supplier/claim/offer phải cập nhật phiên bản và những trang/ads phụ thuộc.

**Đạt khi:** người viết web/video có thể tra mọi khẳng định quan trọng về nguồn. **Chưa đạt:** Master File chỉ là ảnh chụp trang đối thủ với nhãn thương hiệu đã đổi.

## SOP 08. Tạo listing, trang sản phẩm và bundle

**Đầu vào:** Master File đã duyệt, ảnh có quyền, bảng giá. **Đầu ra:** trang sản phẩm hoàn chỉnh trên bản preview.

1. Tạo product với title, mô tả, media, SKU, biến thể và giá chính xác. Chỉ bật bán khi có phương án tồn hàng/cung ứng rõ.
2. Nếu cần layout riêng, tạo template và gán cho product. Mở URL product thực để kiểm, không chỉ xem template trong editor.
3. Viết hero: sản phẩm gì, dành cho nhu cầu nào, lợi ích có chứng cứ gì. Thêm 3 điểm nổi bật, thông số và hướng dẫn dễ đọc.
4. Xếp gallery và block ảnh–chữ theo câu hỏi của khách: đây là gì → dùng thế nào → phù hợp không → vì sao tin → nhận hàng/đổi trả thế nào.
5. Chỉ thêm comparison, số liệu hoặc review đã có nguồn phù hợp. Nếu chưa có thì bỏ block, không dùng placeholder có vẻ thật.
6. Cài bundle nếu bài toán cho phép. Chọn SKU áp dụng, số lượng, giá, nhãn gói và app embed. Kiểm quà tặng/discount có cộng dồn với mã khác không.
7. Giữ chức năng giá/variant/cart chuẩn. Nếu dùng Custom Liquid, dùng cho body khi phù hợp; không để code AI thay nhầm luồng mua hàng.
8. Rà mobile và desktop: chữ, ảnh, vùng bấm, lỗi tràn, video, FAQ, sticky cart, ảnh sai mẫu, tên cũ và đường dẫn.
9. Thêm từng biến thể và từng bundle vào giỏ; đối chiếu số lượng, giá, giảm giá, currency và SKU. Kiểm tăng/giảm số lượng rồi xóa sản phẩm.
10. Lưu ảnh preview và phiên bản trang, sẵn sàng cho kiểm thử tổng thể.

**Đạt khi:** quảng cáo, trang, giỏ và checkout nói cùng một sản phẩm/offer. **Dừng:** sai giá hoặc biến thể; hai widget làm giảm hai lần; còn nội dung mẫu “xxxx reviews”, tên sản phẩm khác hoặc số liệu bịa.

## M05. Master File và sổ claim

Mục lục Master File: nhận diện SKU; dữ kiện kỹ thuật; sử dụng/giới hạn; ảnh/video chuẩn; khách hàng; offer; supplier; shipping/returns; bằng chứng; quyền tài sản; lịch sử thay đổi.

| Claim dự định dùng | Nguồn và ngày | Đúng SKU/đối tượng? | Giới hạn cần nói | Trạng thái |
|---|---|---|---|---|
| … | … | … | … | Được dùng / chờ / bỏ |

| Asset | Nguồn/chủ quyền | Quyền quảng cáo ở đâu, đến khi nào | Bằng chứng cho phép | Phiên bản |
|---|---|---|---|---|
| … | … | … | … | … |

Ảnh supplier gửi không tự bảo đảm có đủ quyền dùng mọi hình người/nhãn trong ảnh. Không ghi “đã chứng minh” nếu chỉ có AI tóm tắt trang bán hàng khác.

## P02. Prompt Master File và unique mechanism

“Chỉ dùng tài liệu tôi đính kèm để lập hồ sơ cho SKU [mã]. Tách dữ kiện có nguồn, lời bên bán tuyên bố và suy luận. Với mỗi claim ghi nguồn, giới hạn và trạng thái có thể dùng/chưa đủ chứng cứ. Giải thích cơ chế thật bằng tối đa 5 câu; không tạo tên khoa học, tỷ lệ hiệu quả, review hoặc chứng nhận. Nếu thiếu thông tin, ghi rõ câu hỏi cần hỏi supplier.”

## P03. Prompt trang sản phẩm

“Dựa trên Master File phiên bản [mã], viết trang sản phẩm cho [nhóm khách/thị trường]. Xuất title, hero, 3 lợi ích có căn cứ, 3 block feature-benefit, cách dùng, thông số, shipping/returns theo chính sách đã cho và FAQ. Không thêm số liệu, review, before/after, sale hoặc guarantee chưa có. Đánh dấu phần thiếu dữ liệu thay vì điền giả. Nếu đề xuất hình, ghi hình cần tự sản xuất hay hình đã có quyền. Giữ offer [nội dung] chính xác.”
