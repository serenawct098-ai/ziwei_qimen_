# Time Engineering Standard

## Location responsibilities

```text
birth_location
  -> required only for a Ziwei birth chart
  -> civil time to UTC and true solar time

question_location
  -> required only for a Qimen question chart
  -> civil time to UTC and true solar time

primary_residence_location
  -> required only for residential feng shui mapping after Qimen chart completion
  -> does not affect Qimen chart construction
```

`primary_residence_location` 不參與奇門真太陽時、四柱、節氣、陰陽遁、符頭、三元、局數、地盤、天盤、人盤或神盤。

## 地點解析

- 優先輸入為 `latitude`、`longitude` 與 `iana_timezone`。系統只驗證座標範圍與 `tzdata==2025.2` 的 IANA identifier。
- 便利輸入為受控 `city` 與 `country_code`。系統只讀 `src/ziwei_qimen/data/astronomy/city_coordinates.json` 的 package resource，且必須唯一命中。
- 未收錄、重複或資料不完整時回傳 `location_resolution_failed`。不進行全球城市時區推斷或網路查詢。

## 時間鏈

```text
civil_datetime + iana_timezone
  -> validated local civil time
  -> UTC
  -> true solar time (astronomy asset required)
  -> solar-term instant (astronomy asset required)
  -> Ziwei / Qimen downstream engine
```

## 固定依賴

| 責任 | 固定資產 |
|---|---|
| 民用時區與夏令時間 | Python `zoneinfo` + `tzdata==2025.2` |
| 天文計算 | Skyfield `1.55` |
| 星曆 | JPL `de440s.bsp` Release asset |
| Earth orientation | IERS `finals2000A.all` Release asset |
| 城市解析 | `ziwei_qimen` package resource 的受控 `city_coordinates.json` |

不允許 runtime 自動下載、更新或改用第二資料來源。

## Time output states

```text
valid
ambiguous_local_time
nonexistent_local_time
invalid_timezone
unsupported_date_range
invalid_coordinates
location_resolution_failed
astronomy_asset_unavailable
```

## Batch 2A

Batch 2A 已建立民用時間邊界：輸入必須為 naïve civil datetime，加明確 IANA timezone；系統拒絕 DST ambiguous／nonexistent local time，並限制 1901-01-01 至 2100-12-31。

## Batch 2B

Batch 2B 已固化 Skyfield `1.55`、JPL `de440s.bsp` 與 IERS `finals2000A.all`。正式檔名、版本、大小與 SHA-256 以 `src/ziwei_qimen/data/astronomy/asset_manifest.json` 為唯一真值。

## Batch 2C

Batch 2C 的城市 registry 只可在全部已審核主要城市均由 Natural Earth `5.1.2` 唯一取值、每筆 IANA timezone 可由 `tzdata==2025.2` 載入、city table 的 canonical SHA-256 已寫入 manifest，且 wheel 安裝後能以 package resource 讀取時完成。

- Runtime SSOT：`src/ziwei_qimen/data/astronomy/city_coordinates.json`。
- Runtime metadata SSOT：`src/ziwei_qimen/data/astronomy/asset_manifest.json`。
- `tools/build_city_coordinates.py` 是固定 Natural Earth input 的 build recipe；`tools/verify_city_coordinates.py` 是驗證器。兩者不在 runtime 讀取路徑。
- 每次修改城市 registry，必須重建 city table、驗證 canonical JSON、SHA-256 與唯一鍵，並同步更新 package manifest 的城市資產 metadata 與 self-hash。
- 每次修改後，必須以乾淨 venv 安裝 wheel，確認 package resource 可讀取城市表，且 city + country_code 與直接座標兩條輸入路徑均通過。
- runtime 不可使用網路查詢、城市別名、時區推斷、fallback、alias 或 dual-read。

## HKO 公農曆日期

`hong_kong_lunar_calendar_1901_2100.json` 是 1901-01-01 至 2100-12-31 的固定離線 Gregorian date 到 Lunar date 資料。runtime 只接受 `date` lookup，並以 package resource 讀取；不使用網路、raw TXT、演算法 fallback、lunar-to-Gregorian reverse lookup 或 coverage 外日期推算。1900 年十一月與 2100 年十二月是 coverage boundary partial month，`month_length` 為 `null`；晚子時規則屬後續命理輸入正規化，不屬本表。
