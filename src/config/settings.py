from pathlib import Path

# Xác định thư mục gốc của dự án (DO_AN_KTLT_RIELL)
# Cấu trúc: DO_AN_KTLT_RIELL / src / config / settings.py -> Lùi ra ngoài 3 cấp
BASE_DIR = Path(__file__).resolve().parent.parent.parent