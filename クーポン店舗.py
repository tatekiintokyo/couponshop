import pandas as pd
from selenium import webdriver
import os
import time
import datetime

def search_coupon():

    #検索するためのURL
    url = "https://ranking.rakuten.co.jp/coupon/p="

    dt_now = datetime.datetime.now()
    dt_year = dt_now.year
    dt_month = dt_now.month
    dt_day = dt_now.day

    #２．リストを作成
    columns = ["Year", "Month", "day", "Rank", "itemName", "discount", "shop", "shopUrl"]
    # 配列名を指定する
    df = pd.DataFrame(columns=columns)

    # ブラウザを開く
    # 本pythonファイルと同じディレクトリにchromeriver.exeがある場合、
    # 引数空でも良い
    browser = webdriver.Chrome()
    
    # 起動時に時間がかかるため、5秒スリープ
    time.sleep(5)

    # 表示ページ
    page = 1
        
    try:
        while(True):
            # ブラウザで検索
            browser.get(url + str(page))
            # 商品ごとのHTMLを全取得
            posts = browser.find_elements_by_css_selector(".rnkRanking_after4box")
            # 何ページ目を取得しているか表示
            print(str(page) + "ページ取得中")
            
            # 商品ごとに情報取得
            for post in posts:
                # ランク

                try:
                    rank = post.find_element_by_css_selector(
                    ".rnkRanking_dispRank").text
                
                except:
                    rank = post.find_element_by_css_selector(
                    ".rnkRanking_dispRank_overHundred").text

                itemname = post.find_element_by_css_selector(
                ".rnkRanking_itemName").text

                discount = post.find_element_by_css_selector(
                ".rnkRanking_discount").text    

                shop = post.find_element_by_css_selector(
                ".rnkRanking_shop").text

                shopurl = post.find_element_by_css_selector(
                    ".rnkRanking_shop a").get_attribute("href")                       
                
                # スクレイピングした情報をリストに追加
                se = pd.Series([dt_year, dt_month, dt_day, rank, itemname, discount, shop, shopurl], columns)
                df = df.append(se, columns)
                print(rank + 'の情報取得完了')
            
            # ページ数をインクリメント
            page += 1
            # 次のページに進むためのURLを取得

            if page == 4:
                print("Finish scriping.")
                break

            print("Moving to next page ...")
    except:
        print("Next page is nothing.")

    # 最後に得たデータをCSVにして保存
    filename = "rakuten_coupon.csv"
    df.to_csv(filename, encoding="utf-8-sig", mode='a', header=False)
    print("Finish!")

# ------------------------------------------------------ #

search_coupon()