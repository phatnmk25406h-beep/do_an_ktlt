import os
from datetime import datetime
import pandas as pd


class VocabRepository:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def load(self):
        if not os.path.exists(self.data_file_path):
            return []

        try:
            # THÊM dtype={"Set_ID": str} VÀO ĐÂY:
            # Lệnh này ép Pandas ngay từ đầu phải đọc cột Set_ID dưới dạng Text (chuỗi)
            df = pd.read_excel(self.data_file_path, dtype={"Set_ID": str}) 
            df = df.fillna("")

            sets_dict = {}
            for _, row in df.iterrows():
                sid = str(row["Set_ID"])
                if sid not in sets_dict:
                    sets_dict[sid] = {
                        "id": sid,
                        "title": str(row["Title"]),
                        "topic": str(row["Topic"]),
                        "created": str(row["Created"]),
                        "updated": str(row["Updated"]),
                        "last_studied": str(row["Last_Studied"]),
                        "progress_pct": int(row["Progress_Pct"]) if str(row["Progress_Pct"]).isdigit() else 0,
                        "cards": [],
                    }

                if str(row["Term"]).strip():
                    sets_dict[sid]["cards"].append({
                        "term": str(row["Term"]),
                        "definition": str(row["Definition"]),
                    })

            return list(sets_dict.values())
        except Exception:
            return []

    def save(self, sets):
        rows = []
        for vocab_set in sets:
            base_info = {
                "Set_ID": vocab_set.get("id", ""),
                "Title": vocab_set.get("title", ""),
                "Topic": vocab_set.get("topic", ""),
                "Created": vocab_set.get("created", ""),
                "Updated": vocab_set.get("updated", ""),
                "Last_Studied": vocab_set.get("last_studied", ""),
                "Progress_Pct": vocab_set.get("progress_pct", 0),
            }

            cards = vocab_set.get("cards", [])
            if not cards:
                row = base_info.copy()
                row["Term"] = ""
                row["Definition"] = ""
                rows.append(row)
            else:
                for card in cards:
                    row = base_info.copy()
                    row["Term"] = card.get("term", "")
                    row["Definition"] = card.get("definition", "")
                    rows.append(row)

        df = pd.DataFrame(rows, columns=[
            "Set_ID",
            "Title",
            "Topic",
            "Created",
            "Updated",
            "Last_Studied",
            "Progress_Pct",
            "Term",
            "Definition",
        ])
        try:
            df.to_excel(self.data_file_path, index=False)
        except PermissionError as exc:
            raise PermissionError(
                f"Cannot write to '{self.data_file_path}'. Close the Excel file if it is open and try again."
            ) from exc

    @staticmethod
    def generate_id():
        return "ID_"+ datetime.now().strftime("%Y%m%d%H%M%S%f")
    