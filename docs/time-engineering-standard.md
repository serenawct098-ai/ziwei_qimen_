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

## 地點解析

- 優先輸入為 `latitude`、`longitude` 與 `iana_timezone`。系統只驗證座標範圍與 `tzdata==2025.2` 的 IANA identifier。
- 便利輸入為受控 `city` 與 `country_code`。系統只讀 `src/ziwei_qimen/data/astronomy/city_coordinates.json` 的 package resource，且必須唯一命中。
- 未收錄、重複或資料不完整時回傳 `location_resolution_failed`。不進行全球城市時區推斷或網路查詢。

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
| 天文計算 | Skyfield `1.55` |
| 星曆 | JPL `de440s.bsp` Release asset |
| Earth orientation | IERS `finals2000A.all` Release asset |
| 城市解析 | `ziwei_qimen` package resource 的受控 `city_coordinates.json` |

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

Batch 2B 已固化 Skyfield `1.55`、JPL `de440s.bsp` 與 IERS `finals2000A.all`。正式檔名、版本、大小與 SHA-256 以 `src/ziwei_qimen/data/astronomy/asset_manifest.json` 為唯一真值。

## Batch 2C

Batch 2C 的城市 registry 只可在全部已審核主要城市均由 Natural Earth `5.1.2` 唯一取值、每筆 IANA timezone 可由 `tzdata==2025.2` 載入、city table 的 canonical SHA-256 已寫入 manifest，且 wheel 安裝後能以 package resource 讀取時完成。

## 城市 registry 後續 batch 驗收

- `tools/build_city_coordinates.py` 是唯一 build recipe；它不可進入 runtime 讀取路徑。
- `src/ziwei_qimen/data/astronomy/city_coordinates.json` 是唯一 runtime SSOT；runtime 只可經 package resource 讀取此檔。
- 每次修改城市 registry，必須重建 city table、驗證 canonical JSON、SHA-256 與唯一鍵，並同步更新 package manifest 的城市資產 metadata 與 self-hash。
- 每次修改後，必須以乾淨 venv 安裝 wheel，確認 package resource 可讀取城市表，且 city + country_code 與直接座標兩條輸入路徑均通過。
- runtime 不可使用網路查詢、城市別名、時區推斷、fallback、alias 或 dual-read。
