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
| example.txt                                | SQL 指令函式 例子                                              |


### settings/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| requirements.txt                           | python 環境所需套件 (任何需要透過 pip 下載的套件)               |
| southern-tempo-387713-d30e2f27945c.json    | Cloud SQL Proxy 所需密鑰                                       |

### hardware/

| File Name                                  | Description                                                   |
| ------------------------------------------ | --------------------------------------------------------------|
| ESP32_code.txt                             | ESP32的code                                                   |
| wiring & note.txt                          | 接線與程式的說明                                               |



## Message

> **楊世宇** 大家加油\
> **林庭毅** 大氣溫溼度跟土壤溼度都用int就好
