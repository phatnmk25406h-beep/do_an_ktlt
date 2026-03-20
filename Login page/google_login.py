from google_auth_oauthlib.flow import InstalledAppFlow #Thư viện xử lý luồng đăng nhập OAuth
from googleapiclient.discovery import build #gọi Google API để lấy thông tin user
import os # tìm đường dẫn đến client_sceret

#Các quyền xin từ Google như đọc mail, đọc profile 
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def login_with_google():
    """
    Mở trình duyệt để user chọn tài khoản Google.
    Trả về dict chứa thông tin user, hoặc None nếu thất bại.
    """
    try:
        # Tìm file client_secret.json cùng thư mục
        base_dir = os.path.dirname(os.path.abspath(__file__))
        secret_path = os.path.join(base_dir, 'client_secret.json')
        #Đọc file Json lấy từ Gg để cbi data cho luồng login
        flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)

        # Mở trình duyệt → hiện popup "Choose an account" -> Nhận token trả về từ google rồi lưu vào creds
        #Token là một đoạn ký tự ngẫu nhiên, đóng vai trò như thẻ tạm thời mà Google cấp cho app sau khi user đồng ý đăng nhập.
        creds = flow.run_local_server(port=0)

        # Lấy thông tin user từ Google
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        #Trả về dict chứa thông tin user
        return {
            "name":    user_info.get('name', ''),
            "email":   user_info.get('email', ''),
            "picture": user_info.get('picture', ''),
            "google_id": user_info.get('id', '')
        }

    except Exception as e:
        print(f"[Google Login] Lỗi: {e}")
        return None
