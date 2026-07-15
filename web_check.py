import requests
import os
import urllib3
from bs4 import BeautifulSoup

# 証明書エラーの警告を非表示にする
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# チェック対象の講義用URL
url = "https://dench.mklab.osakac.ac.jp/script-pg/"
cache_file = "last_script_pg.txt"

try:
    # Webサイトの情報を取得
    response = requests.get(url, verify=False)
    response.raise_for_status()
    
    # HTMLを解析して中身のテキストを取り出す
    soup = BeautifulSoup(response.text, "html.parser")
    current_content = soup.get_text().strip()

except requests.exceptions.RequestException as e:
    print(f"通信エラーが発生しました: {e}")
    exit(1)

# ===== 差分チェックの処理 =====
if not os.path.exists(cache_file):
    # 初回実行時：現在の状態を保存
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(current_content)
    print("【初回取得】現在の状態を保存しました。次回から差分をチェックします。")
else:
    # 2回目以降：前回の内容を読み込んで比較
    with open(cache_file, "r", encoding="utf-8") as f:
        last_content = f.read()
    
    if current_content == last_content:
        print("【差分なし】前回からWebサイトの更新はありません。")
    else:
        print("【★更新検知★】Webサイトが更新されました！")
        # 新しい状態に上書き
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(current_content)
# webhook test 1
