# 時間工程標準

## 適用範圍

本文件只規定民用時間、時區、城市解析、天文時間、真太陽時、節氣資料的工程選型與資料責任。

紫微與奇門的傳統排盤、起局與推演規則，仍以《紫微×奇門傳統算法作業規格書》為唯一裁定來源。

## 正式產品日期範圍

```text
1901-01-01 至 2100-12-31
```

日期超出此範圍時，系統回傳：

```text
unsupported_date_range
```

不可改用第二份星曆、固定 UTC offset、第三方網頁萬年曆或未受控估算法。

## 正式工具鏈

| 責任 | 正式工具或資料 | 規則 |
|---|---|---|
| 民用時區與夏令時間 | Python `zoneinfo` + 固定版本 `tzdata` | 由受控城市資料取得 IANA timezone；不可只使用固定 UTC offset |
| 城市解析 | 本地受控 `city_coordinates.json` | 輸入城市名稱，可選國家／地區代碼消歧；不可 runtime 呼叫外部地理編碼 |
| 天文計算 | Skyfield | production 唯一天文 Python 套件 |
| 正式星曆 | JPL `de440s.bsp` | 本地受控資產，不得 runtime 自動下載 |
| 星曆覆蓋 | 1849–2150 | 覆蓋產品 1901–2100 範圍 |
| Earth orientation | 固定版本 IERS 資料快照 | 不得 runtime 自動更新 |
| 農曆轉換基準 | 香港天文台 1901–2100 公曆—農曆資料 | 只在完成來源、授權與本地封裝核實後加入 |
| 外部驗證 | 香港天文台年曆、Overview 香港萬年曆 | 只作測試及人工抽樣，不可 runtime 讀取 |
| Swiss Ephemeris | 隔離的開發驗證工具 | 不可列入 production dependency |
| Astropy | 可選開發驗證工具 | 不可列入第一版 production dependency |

## 時間處理次序

```text
本地民用日期時間
→ 城市解析為經緯度與 IANA timezone
→ IANA timezone 解析
→ UTC
→ UT1、TT、ΔT 與太陽視位置所需天文量
→ 經度時差
→ 均時差
→ 真太陽時
→ 紫微或奇門各自的曆法分流
```

## 城市輸入與解析

外部輸入只要求：

```text
city
optional country_code
```

城市解析結果必保存：

```text
canonical_city_id
city_display_name
country_code
latitude_degrees_north
longitude_degrees_east
iana_timezone
city_dataset_version
resolution = controlled_city_dataset
```

不得以城市名稱文字本身直接計算真太陽時。

如城市無法在受控資料集中唯一解析，回傳：

```text
location_resolution_failed
```

不得猜測座標或 IANA timezone。

## 民用時間問題

當本地民用時間落在夏令時間切換的重複或不存在區間時：

| 狀態 | 錯誤碼 | 行為 |
|---|---|---|
| 重複的本地時間 | `ambiguous_local_time` | 要求呼叫端提供可消歧的資料 |
| 不存在的本地時間 | `nonexistent_local_time` | 拒絕計算，要求修正輸入 |
| IANA timezone 不存在或無效 | `invalid_iana_timezone` | 拒絕計算 |
| 日期超出 1901–2100 | `unsupported_date_range` | 拒絕計算 |

不可在上述情況自動選取夏令時間前後任一 offset。

## 真太陽時輸出

時間核心輸出不可只有最終字串。至少保存：

```text
civil_datetime
canonical_city_id
city_display_name
country_code
iana_timezone
timezone_data_version
utc_datetime
ut1_datetime
tt_datetime
delta_t_seconds
latitude_degrees_north
longitude_degrees_east
location_resolution
longitude_correction_seconds
equation_of_time_seconds
true_solar_datetime
precision = second
ephemeris_id = jpl_de440s
ephemeris_version
iers_data_version
calculation_status
```

這些欄位是不同時間尺度與計算事實，不是 compatibility 欄位。

## 紫微分流

紫微只使用出生民用時間與出生城市計算真太陽時。

```text
birth true solar datetime
→ 原始農曆年月日、原始時支、生年干支
→ 晚子時判定
→ 閏月有效月判定
→ 紫微本命盤
```

晚子時規則：

```text
23:00:00–23:59:59：排盤日期加一日，時支維持子。
00:00:00–00:59:59：排盤日期不加日，時支為子。
```

閏月規則：

```text
初一至十五：有效月取原月。
十六至月末：有效月取下一月。
```

原始農曆事實與排盤有效事實都必須保存，不得互相覆蓋。

## 奇門分流

奇門只使用問事民用時間與問事城市計算真太陽時。

```text
question true solar datetime
→ 年月日時干支
→ 節氣瞬時與所在節氣
→ 陰陽遁
→ 符頭、三元、局數
→ 時家轉盤奇門九宮全盤
```

冬至後至夏至前為陽遁；夏至後至冬至前為陰遁。節氣切換以真太陽時的秒級時間判定，不可只按萬年曆顯示日期。

## 資料版本與可重現性

每次時間運算必輸出所使用的：

```text
tzdata version
JPL ephemeris identifier and version
IERS snapshot version
ΔT model identifier
city dataset version
calculation precision
```

正式 runtime 不可下載「最新」星曆、時區資料、IERS 資料或城市資料。資料更新只能透過一個明確版本升級批次完成，並重跑所有 golden cases。

## 歷史資料限制

IANA 時區資料是民用時間資料來源，適合處理歷史時區與夏令時間；較早年代或特定地點的歷史民用時間資料可能存在不確定性。

系統應如實輸出採用的 IANA timezone、城市資料版本與時區資料版本。當受控城市資料不能對應輸入城市，或 IANA timezone 不能代表輸入地點的歷史民用時間時，必須要求補充資料，不得以固定 UTC offset 猜補。
