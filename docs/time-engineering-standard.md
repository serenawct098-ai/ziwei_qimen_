# 時間工程標準

## 支援範圍

```text
1901-01-01 至 2100-12-31
```

超出範圍回傳：

```text
unsupported_date_range
```

## 地點邊界

```text
birth_location
→ 紫微出生地真太陽時
→ 紫微本命盤

question_location
→ 問事者提出問題時的實際所在城市或座標
→ 奇門問事地真太陽時
→ 奇門四柱、節氣、陰陽遁、局數與九宮盤

primary_residence_location
→ 完成奇門九宮盤後的住宅風水方位映射
→ 結合住宅坐向、平面圖與實際方向
```

`primary_residence_location` 不參與奇門真太陽時、四柱、節氣、陰陽遁、符頭、三元、局數、地盤、天盤、人盤或神盤。

## 時間鏈

```text
civil_datetime + iana_timezone
→ UTC
→ 天文時間尺度
→ 經度時差 + 均時差
→ true_solar_datetime
```

內部時間保存微秒精度；晚子時與節氣交界以秒判定。

## 固定工具鏈

| 責任 | 固定資產 |
|---|---|
| 民用時區與夏令時間 | Python `zoneinfo` + `tzdata==2025.2` |
| 天文計算 | Batch 2B 固定 Skyfield 版本 |
| 星曆 | Batch 2B 固定 JPL `de440s.bsp` |
| Earth orientation | Batch 2B 固定 IERS snapshot |
| 城市解析 | Batch 2B 受控 `city_coordinates.json` |

不允許 runtime 自動下載、更新或改用第二資料來源。

## Batch 2A

Batch 2A 完成：

```text
日期範圍驗證
IANA timezone 驗證
DST ambiguous local time 停止
DST nonexistent local time 停止
座標邊界驗證
時間 provenance 資料契約
無星曆資產時停止
```

城市名稱解析在正式受控城市資料集未入庫前回傳：

```text
location_resolution_failed
```

真太陽時計算在 Skyfield、JPL 星曆與 IERS snapshot 未入庫前回傳：

```text
astronomy_asset_unavailable
```

## Batch 2B

Batch 2B 只可在下列資產完成受控納入後開始：

```text
固定 Skyfield package version
JPL de440s.bsp 實體檔案
de440s.bsp SHA-256
固定 IERS snapshot 實體檔案
IERS snapshot 版本與 SHA-256
city_coordinates.json
城市資料來源、授權、版本與 SHA-256
```

未完成時不得建立空檔、範例城市、估算均時差、固定 UTC offset 或 fallback。
