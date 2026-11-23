# Checklist chạy & phân tích data KLTN

Đề tài: Tác động phi tuyến của đa dạng hóa xuất khẩu đến tăng trưởng (128 quốc gia, 2000–2024).
Biến: GDPG ~ HHI / THEIL + CAP, FDI, GOV, LAB (+ GFC, COVID).

## A. Chạy dữ liệu (mỗi bước ra 1 bảng)

- [ ] **1. Thống kê mô tả**: mean, SD, min, max của GDPG, HHI, THEIL, CAP, FDI, GOV, LAB → *Bảng thống kê mô tả*
- [ ] **2. Tương quan + VIF**: không cặp biến độc lập nào tương quan quá cao, VIF < 10 → *Bảng ma trận tương quan + VIF*
- [ ] **3. Tuyến tính cơ sở**: Pooled OLS, FE, RE (HHI, rồi THEIL) → *Bảng hồi quy tuyến tính*
- [ ] **4. Chọn mô hình panel**: F-test (Pooled vs FE), Breusch–Pagan LM (Pooled vs RE), Hausman (FE vs RE) → ghi rõ chọn mô hình nào
- [ ] **5. Bậc hai**: thêm HHI² / THEIL² → xác định dạng U hay U ngược; nếu có thì tính điểm ngoặt = −β₁ / (2β₂)
- [ ] **6. Threshold regression**: kiểm định có ngưỡng hay không → giá trị ngưỡng + hệ số từng regime
- [ ] **7. Developed vs Developing**: chạy riêng 2 nhóm (hoặc dùng biến tương tác) → hệ số + ngưỡng mỗi nhóm
- [ ] **8. Khủng hoảng**: EDI×GFC, EDI×COVID → hệ số tương tác
- [ ] **9. Kiểm định độ vững**: thay HHI ↔ THEIL; robust/clustered SE; kiểm tra outlier khi cần

## B. Đọc kết quả (trả lời đủ 5 câu, không cần diễn giải từng con số)

- [ ] **HHI/THEIL có ý nghĩa không?** p < 0,05 thì có ý nghĩa ở mức 5%
- [ ] **Chiều tác động?** HHI/THEIL cao nghĩa là tập trung cao (ít đa dạng). Hệ số âm thường hàm ý tập trung cao hơn làm giảm tăng trưởng, tức đa dạng hóa cao hơn hỗ trợ tăng trưởng
- [ ] **Có phi tuyến không?** Xem đồng thời hệ số EDI và EDI². EDI² có ý nghĩa thì quan hệ không còn tuyến tính; tính điểm ngoặt để biết vị trí tác động đổi chiều
- [ ] **Có ngưỡng không?** Kiểm định threshold có ý nghĩa thì so sánh hệ số trước và sau ngưỡng
- [ ] **Hai nhóm nước khác nhau không?** So sánh dấu, độ lớn, mức ý nghĩa, ngưỡng. Khác biệt phải có ý nghĩa thống kê

## C. So sánh bắt buộc

- [ ] HHI vs THEIL: kết luận có nhất quán không
- [ ] Tuyến tính vs bậc hai: mô hình tuyến tính có bỏ sót phi tuyến không
- [ ] Điểm ngoặt (bước 5) vs ngưỡng (bước 6): có gần nhau không
- [ ] Developed vs Developing: tác động và ngưỡng có khác nhau không
- [ ] Bình thường vs khủng hoảng (GFC/COVID): tác động có đổi không
- [ ] Cơ sở vs robustness: kết luận chính có giữ nguyên không

## D. Viết chương kết quả (đúng thứ tự)

- [ ] Thống kê mô tả
- [ ] Tương quan / VIF
- [ ] Lựa chọn mô hình panel
- [ ] Hồi quy tuyến tính
- [ ] Mô hình bậc hai
- [ ] Threshold regression
- [ ] So sánh Developed / Developing
- [ ] GFC / COVID
- [ ] Kiểm định độ vững
