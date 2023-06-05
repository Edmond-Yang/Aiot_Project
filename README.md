# Aiot Project


## 分工事項

* 庭毅： 硬體
* 建維： 爬蟲
* 世宇： API, 資料庫, APP
* 峻豪： 機器學習


## 檔案

### ./

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| main.py                                    | 執行 fastapi 後端程式                                         |
| DockerFile                                 | Container 環境所需執行的指令                                   |
| README.md                                  | 紀錄要務                                                       |


### service/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| sql.py                                     | 連接 Cloud SQL                                                |
| webCrawl.py                                | 爬蟲 天氣資訊                                                  |
| example.txt                                | SQL 指令函式 例子                                              |


### settings/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| requirements.txt                           | python 環境所需套件 (任何需要透過 pip 下載的套件)               |
| root_ca.txt                                | esp32 連接 api 時所需憑證                                      |
| southern-tempo-387713-d30e2f27945c.json    | Cloud SQL Proxy 所需密鑰                                       |

### hardware/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| ESP32_code.txt                             | ESP32的code                                                   |
| wiring & note.txt                          | 接線與程式的說明                                               |
| 地獄繪圖.jpg                               | 接線圖片                                               |

### templates/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| index.html                                 | 觀看 Plants 資料庫的簡易網頁                                   |

### static/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| icon.PNG                                   | 櫻花 Image 用於網頁的 Icon                                     |

### LSTM/
| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| main.py                                    | 預測天氣使用 function: Predict_watering_amount()               |
| requirements.txt                           | 使用packages                                                  |

## Message

> **楊世宇** 大家加油\
> **林庭毅** 大氣溫溼度跟土壤溼度都用int就好
