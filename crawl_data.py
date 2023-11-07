from selenium import webdriver
import json
import csv
import pandas as pd
from selenium.webdriver.common.by import By


def site_click(XPATH, driver):
    search_box = driver.find_element(By.XPATH,XPATH)
    search_box.click()
    driver.implicitly_wait(5)

def send_keys(XPATH,driver,str):
    search_box = driver.find_element(By.XPATH,XPATH)
    search_box.clear()
    search_box.send_keys(str)
    search_box.send_keys('\n')


def crawl_data(hscode_list, driver):
    for code in hscode_list:
        #search hscode
        send_keys('//*[@id="srchDtrmHsSgn"]',driver,code)
        items = driver.find_element(By.XPATH,'//*[@id="ULS0203002S_T1_container"]/aside/div/span[1]/strong')
        driver.implicitly_wait(5)
        print(items.text)
        print('@'*100)
        print(code)
        
        #check table
        is_table = driver.find_element(By.XPATH,'//*[@id="ULS0203002S_T1_container"]/div[1]')
        driver.implicitly_wait(5)
        is_tbody = is_table.find_element(By.TAG_NAME,"tbody")
        is_rows = is_tbody.find_elements(By.TAG_NAME, "tr")
        if is_rows[0].text == '조회결과가 존재하지 않습니다.':
            continue
        
        #crawl table data
        item_num = int(items.text.replace(',',''))
        ix = 2
        next = 1
        while True:
            table = driver.find_element(By.XPATH,'//*[@id="ULS0203002S_T1_container"]/div[1]')
            driver.implicitly_wait(5)
            tbody = table.find_element(By.TAG_NAME,"tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            new_data_list = []
            for value in rows:
                item_name = value.find_elements(By.TAG_NAME, "td")[5].text
                new_data = [str(code), str(item_name)]
                print(new_data)
                new_data_list.append(new_data)

            with open('./data/dataset.csv', mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(new_data_list)
            f.close()
            if item_num//10 < (next-1)*10+ix :
                break
            if ix == 11:
                ix = 1
                next += 1
                xpath = '//*[@id="ULS0203002S_T1_container"]/div[2]/ul['+str(min(next,3))+']/li['+str(ix)+']/a'
                print(xpath)
                page_box = driver.find_element(By.XPATH, xpath)
            else:
                page_box = driver.find_element(By.XPATH,'//*[@id="ULS0203002S_T1_container"]/div[2]/ul['+str(min(next,2))+']/li['+str(ix)+']/a' )            
            page_box.click()
            ix += 1
        driver.implicitly_wait(5)

if __name__ == '__main__':

    dic = {'hscode':[], 'name':[]}
    df = pd.DataFrame(dic)
    df.to_csv('./data/dataset.csv',encoding='utf-8-sig',index=False)

    with open('./data/hscode.pickle' , 'r') as f:
        hscode = json.load(f)
    f.close()
    hscode_list = list(hscode.keys())


    driver = webdriver.Chrome()
    driver.get('https://unipass.customs.go.kr/clip/index.do')
    driver.implicitly_wait(5)

    #분류사례
    site_click('//*[@id="mainbanner"]/ul/li[3]/a',driver)

    #국내사례
    site_click('//*[@id="mainbanner"]/ul/li[3]/div/div[2]/ul/li[5]/a',driver)

    #품목분류사례
    site_click('//*[@id="mainarea"]/div/ul/li[4]/a',driver)

    crawl_data(hscode_list,driver)



