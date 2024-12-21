import bs4
import traceback
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
 
# ドライバーのフルパス
CHROMEDRIVER = "chromedriver.exeのパス"
# 改ページ（最大）
PAGE_MAX = 2
# 遷移間隔（秒）
INTERVAL_TIME = 3
# 対象カテゴリー
#CATEGORY = ["top-picks", "domestic", "world", "business","entertainment", "sports", "it", "science", "local"]
CATEGORY = ["business"]
 
 
# ドライバー準備
def get_driver():
    # ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
 
    # ブラウザーを起動
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
 
    return driver
 
 
# 対象ページのソース取得
def get_source_from_page(driver, page):
    try:
        # ターゲット
        driver.get(page)
        page_source = driver.page_source
 
        return page_source
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None
 
 
# ソースからスクレイピングする
def get_data_from_source(src):
    # スクレイピングする
    soup = bs4.BeautifulSoup(src, features='lxml')
 
    try:
        info = []
        base = soup.find(class_="newsFeed")
 
        if base:
 
            a_elems = base.find_all("a", class_="newsFeed_item_link")
 
            for elem in a_elems:
                item = {}
                href = elem.attrs['href']
                pickup_id = href.replace('https://news.yahoo.co.jp/pickup/', '')
 
                title = elem.find(class_="newsFeed_item_title").text
 
                item["pickup_id"] = pickup_id
                item["title"] = title
 
                info.append(item)
 
        return info
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None
 
 
# 次のページへ遷移
def next_btn_click(driver):
    try:
        # 次へボタン
        elem_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'pagination_item-next'))
        )
 
        class_value = elem_btn.get_attribute("class")
        if class_value.find('pagination_item-disabled') > 0:
            return False
        else:
            # クリック処理
            actions = ActionChains(driver)
            actions.move_to_element(elem_btn)
            actions.click(elem_btn)
            actions.perform()
            # 間隔を設ける(秒単位）
            time.sleep(INTERVAL_TIME)
 
            return True
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return False
 
if __name__ == "__main__":
 
    # ブラウザのdriver取得
    driver = get_driver()
 
    # ページカウンター制御
    page_counter = 0
 
    for category in CATEGORY:
 
        page_counter = page_counter + 1
 
        # 対象ページURL
        page = "https://news.yahoo.co.jp/topics/" + str(category)
 
        # ページのソース取得
        source = get_source_from_page(driver, page)
        result_flg = True
 
        while result_flg:
 
            # ソースからデータ抽出
            data = get_data_from_source(source)
 
            # データ保存
            print(data)
 
            # 改ページ処理を抜ける
            if page_counter == PAGE_MAX:
                page_counter = 0
                break
 
            # 改ページ処理
            result_flg = next_btn_click(driver)
            source = driver.page_source
 
            page_counter = page_counter + 1
 
    # 閉じる
    driver.quit()
