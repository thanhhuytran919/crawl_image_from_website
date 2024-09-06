import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import base64

# URL trang web muốn cào
url = "https://hongduchonda.com.vn/products/cb150r-the-streetster-1"

# Thư mục lưu ảnh
output_folder = "downloaded_images"
os.makedirs(output_folder, exist_ok=True)

# Gửi yêu cầu đến trang web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả các thẻ ảnh <img> trên trang
images = soup.find_all('img')


# Hàm xử lý tên file hợp lệ
def valid_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '.', '_')).rstrip()


# Hàm lưu ảnh từ Data URL
def save_base64_image(data_url, output_path):
    # Tách phần MIME type và dữ liệu base64
    header, encoded = data_url.split(',', 1)
    # Giải mã dữ liệu base64
    image_data = base64.b64decode(encoded)
    # Lưu ảnh
    with open(output_path, 'wb') as f:
        f.write(image_data)


# Lặp qua các thẻ ảnh và tải về
for img in images:
    # Lấy URL của ảnh
    img_url = img.get('src')

    # Nếu URL ảnh là tương đối, chuyển thành URL tuyệt đối
    img_url = urljoin(url, img_url)

    # Nếu ảnh là Data URL (bắt đầu với 'data:image/')
    if img_url.startswith('data:image/'):

        mime_type = img_url.split(';')[0].split(
            '/')[1]
        img_name = f"image_{images.index(img)}.{mime_type}"

        img_name = valid_filename(img_name)

        # Lưu ảnh base64
        save_base64_image(img_url, os.path.join(output_folder, img_name))
        print(f"Tải về từ Data URL: {img_name}")

    # Nếu ảnh là URL thông thường
    else:
        # Tách phần path của URL và bỏ qua query string
        parsed_url = urlparse(img_url)
        img_name = os.path.basename(parsed_url.path)

        # Xử lý tên ảnh hợp lệ
        img_name = valid_filename(img_name)

        # Nếu img_name không có đuôi, gán tên mặc định
        if not img_name:
            img_name = "image_default.jpg"

        # Tải ảnh về nếu img_name không rỗng
        img_response = requests.get(img_url)

        # Lưu ảnh vào thư mục
        with open(os.path.join(output_folder, img_name), 'wb') as f:
            f.write(img_response.content)

        print(f"Tải về từ URL: {img_name}")
