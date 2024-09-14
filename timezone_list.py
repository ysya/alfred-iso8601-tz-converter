import sys
import csv
from datetime import datetime
from zoneinfo import ZoneInfo

# 檢查是否有輸入的時間參數
if len(sys.argv) < 2 or not sys.argv[1].strip():
    print('{"items": [{"title": "Please input ISO 8601 time", "subtitle": "", "arg": ""}]}')
    sys.exit(0)

iso8601_time = sys.argv[1].strip()

# 檢查 CSV 文件是否存在
csv_file = "timezones.csv"
flag_path = "./flags/png"  # 國旗文件存放的目錄

try:
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # 使用 DictReader 來讀取每一行作為字典
        output = []

        # 解析 UTC ISO 8601 時間
        try:
            parsed_time = datetime.fromisoformat(iso8601_time)
        except Exception as e:
            print(f'{{"items": [{{"title": "Error: {e}", "subtitle": "無法解析時間", "arg": "Error"}}]}}')
            sys.exit(1)

        # 遍歷 CSV 文件中的每個時區，並轉換時間
        for row in reader:
            timezone = row["TimeZone"]
            country_code = row["CountryCode"]

            try:
                # 轉換為當前時區
                local_time = parsed_time.astimezone(ZoneInfo(timezone))

                # 國旗圖標路徑
                flag_path_full = f"{flag_path}/{country_code}.png"

                output.append({
                    "title": local_time.isoformat(),
                    "subtitle": f"Timezone: {timezone} ({country_code.upper()})",
                    "arg": local_time.isoformat(),
                    "icon": {
                        "path": flag_path_full
                    }
                })
            except Exception as e:
                continue  # 如果某個時區轉換失敗，跳過

        # 輸出結果給 Alfred
        print('{"items": ' + str(output).replace("'", '"') + '}')

except FileNotFoundError:
    print('{"items": [{"title": "Error: CSV file not found", "subtitle": "找不到 default_timezones.csv", "arg": "Error: CSV file not found"}]}')
    sys.exit(0)