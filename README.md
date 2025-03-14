# AUTOMATION HARPIE + METAMASK WALLET với Selenium Python

## ⚠ Lưu ý quan trọng

🔴 **Dự án này có chứa code hint.** Vui lòng tìm đến **bài ghim** trong kênh [Telegram Channel](https://t.me/+8o9ebAT9ZSFlZGNl) để kiểm tra trước khi sử dụng.

---

## 📖 Mục lục
1. [Giới thiệu](#-giới-thiệu)
2. [Video demo](#-video-demo)
3. [Chức năng chính](#-chức-năng-chính)
4. [Yêu cầu ban đầu](#-yêu-cầu-ban-đầu)
5. [Cấu trúc file](#-cấu-trúc-file)
6. [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
7. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
8. [Tùy chỉnh cấu hình](#-tùy-chỉnh-cấu-hình)
9. [Thông tin liên hệ](#-thông-tin-liên-hệ)

## 🔔 Bật thông báo để theo dõi mã nguồn khi có update

1. Đăng nhập vào GitHub.
2. Nhấn vào biểu tượng 🔔 **Watch** (góc trên bên phải của repository này).
3. Chọn **"All Activity"** để nhận tất cả thông báo hoặc **"Custom" > "Pull Requests"** để nhận thông báo khi có thay đổi trong mã nguồn.

---

## 🌐 Giới thiệu

**AUTOMATION HARPIE + METAMASK WALLET** là một công cụ tự động hóa hoạt động ví điện tử dựa trên Selenium, giúp tự động quét và thực hiện giao dịch trên mạng **Polygon**.

📌 **Trang dự án**: [Harpie.io](https://harpie.io/)

<p align="center">
    <img src="intro.jpg" alt="Giới thiệu">
</p>

---

## 🎬 Video demo

<p align="center">
    <a href="https://www.youtube.com/watch?v=GJn3SSoGSK8">
        <img src="https://img.youtube.com/vi/GJn3SSoGSK8/0.jpg" alt="Xem video demo">
    </a>
</p>

---


## 🚀 Chức năng chính

- **Quét ví (Scan Wallet)**: Tự động quét ví hàng ngày.
- **Chuyển POL trên Polygon**: Tự động gửi **POL (MATIC)** từ ví chính sang ví khác trên mạng **Polygon (Polygon Harpie RPC)**.

---

## 🔧 Yêu cầu ban đầu

- **Số lượng profile**: chạy tối thiểu 2 profile, để thực hiện gửi token đến ví của các profile khác
- **Gmail**: Cần để thiết lập ban đầu.
- **Metamask Wallet**: Phải được đăng nhập sẵn.
- **Số dư Polygon Mainnet**: Tối thiểu **2-3 POL/ví**, cần nạp thêm khi hết.

---

## 📂 Cấu trúc file

| File                           | Mô tả                                    |
| ------------------------------ | ---------------------------------------- |
| `extensions/meta-wallet-*.crx` | Tiện ích mở rộng Metamask Wallet.        |
| `browser_automation.py`        | Code tự động hóa trình duyệt.            |
| `utils.py`                     | Các hàm hỗ trợ chung.                    |
| `harpie.py`                    | Chương trình chính thực hiện automation. |
| `requirements.txt`             | Danh sách các thư viện cần thiết.        |
| `intro.jpg`                    | Hình ảnh giới thiệu.                     |

---

## 📌 Hướng dẫn cài đặt

### 1️ Tạo file `data.txt`

- Mỗi dòng chứa thông tin một profile theo cấu trúc:
  ```plaintext
  [tên_profile]|[mật_khẩu_ví_meta]|[địa_chỉ_ví_của_profile]
  ```
- Ví dụ:
  ```plaintext
  profile1|12345678|0x23fb68d805ebb9d18e8d2e3a07f85ba5416eb2ed
  profile2|12345678|0x23fb68d805ebb9d18e8d2e3a07f85ba5416eb2ed
  ```

### 2️ (Tùy chọn) Tạo file `token_tele.txt`

- Lưu **Telegram Bot Token** để chương trình gửi thông báo lỗi qua Telegram khi gặp sự cố.
- Nếu không có file này, ảnh lỗi sẽ lưu vào thư mục **snapshot**.
- File có cấu trúc:
  ```plaintext
  [Id_bot_tele]|[Token_bot_tele]
  ```
- Ví dụ:
  ```plaintext
  123456789|7934583453:AAFcOebukTPfkL6dfg4_PH_ahBA0lU36xyc
  ```

### 3️ Cài đặt Python & thư viện

Trước tiên, cần cài đặt Python (phiên bản 3.8 trở lên). Nếu chưa có, hãy tải và cài đặt từ [Python Official Site](https://www.python.org/downloads/).

- Kiểm tra phiên bản Python bằng lệnh:
  ```sh
  python --version
  ```
- Cài đặt thư viện yêu cầu:
  ```sh
  pip install -r requirements.txt
  ```

---

## ▶ Hướng dẫn sử dụng

### 1️ Chạy chương trình

```sh
python harpie.py
```

### 2️ Các chế độ hoạt động

- **1. Set up**: Chạy chế độ cài đặt ban đầu và chọn profile.
- **2. Chạy Auto**: Chạy chế độ tự động theo cấu hình đã thiết lập.
- **3. Thoát**: Dừng chương trình.

**💡 Lưu ý:**

- **Lần đầu:** Chạy **Set up (1)** để thiết lập cấu hình ví, thực hiện như trong video.
- **Những lần sau:** Chạy **Auto (2)** để thực hiện automation.

---

## ⚙ Tùy chỉnh cấu hình

Mở **`harpie.py`** và tìm dòng sau:

### 🔹 **Thay đổi số lần thực hiện send token**

Tìm dòng sau, thay đổi số `15` thành số bất kì.

```python
times = 15
```

Nên đặt max 15. Mình thấy rằng, khi gửi liên tiếp đến 15 lần, lần 16 sẽ bị gián đoạn hiển thị popup "Approve" trên web harpie

### 🔹 **Thay đổi số lượng token random sẽ gửi**
Tìm dòng sau, thay đổi `(0.00001, 0.0001)` thành `(min, max)`

```python
random_token_amount = str(round(random.uniform(0.00001, 0.0001),6))
```

### 🔹 **Bật chế độ Auto không cần chọn menu**

```python
manager.run_terminal(
    profiles=PROFILES,
    auto=False,
    max_concurrent_profiles=4
)
```

Đổi `auto=False` thành `auto=True`:

```python
manager.run_terminal(
    profiles=PROFILES,
    auto=True,
    max_concurrent_profiles=4
)
```

### 🔹 **Thay đổi số lượng profile chạy cùng lúc**

Đổi số `4` thành số bất kì

```python
max_concurrent_profiles=4  
```

---

### **Ẩn duyệt trinh khi đang hoạt động**

Đổi `False` hành `True`

```python
headless=False
```

---

## 🔗 Thông tin liên hệ

📢 **Telegram Channel:** [Airdrop Automation](https://t.me/+8o9ebAT9ZSFlZGNl)

💰 **Ủng hộ tác giả:**

- **EVM:** `0x3b3784f7b0fed3a8ecdd46c80097a781a6afdb09`
- **SOL:** `4z3JQNeTnMSHYeg9FjRmXYrQrPHBnPg3zNKisAJjobSP`
- **TON:** `UQDKgC6TesJJU9TilGYoZfj5YYtIzePhdzSDJTctJ-Z27lkR`
- **SUI:** `0x5fb56584bf561a4a0889e35a96ef3e6595c7ebd13294be436ad61eaf04be4b09`
- **APT (APTOS):** `0x557ea46189398da1ddf817a634fa91cfb54a32cfc22cadd98bb0327c880bac19`

🙏 Nếu ủng hộ, vui lòng gửi token chính của mạng đó. Cảm ơn anh em đã hỗ trợ!

