# 時間工程標準

## 日期範圍

```text
1901-01-01 至 2100-12-31
```

超出範圍回傳 `unsupported_date_range`。

## 工具鏈

| 責任 | 工具或資料 |
|---|---|
| 民用時區與夏令時間 | Python `zoneinfo` + 固定版本 `tzdata` |
| 城市解析 | 受控 `city_coordinates.json` |
| 天文計算 | 固定版本 Skyfield |
| 星曆 | JPL `de440s.bsp` |
| 農曆轉換基準 | 香港天文台 1901–2100 公曆—農曆資料 |

## 紫微

```text
出生民用時間 + birth_location
→ 出生地真太陽時
→ 原始農曆年月日與生年干支
→ 晚子時與閏月有效月
→ 紫微本命盤
```

## 奇門

```text
問事民用時間 + question_location
→ 問事地真太陽時
→ 年月日時干支
→ 節氣
→ 陰陽遁
→ 符頭、三元、局數
→ 時家轉盤奇門九宮盤
```

`primary_residence_location` 不參與奇門真太陽時、四柱、節氣、陰陽遁、局數或起局。

## 風水

```text
完成奇門九宮盤 + primary_residence_location + 空間方向資料
→ 九宮方位映射
→ 風水建議
```

風水映射不重新起局，不改寫奇門盤。

## 城市

```text
city
optional country_code
```

解析結果：

```text
canonical_city_id
city_display_name
country_code
latitude_degrees_north
longitude_degrees_east
iana_timezone
city_dataset_version
```

城市無法唯一解析時回傳 `location_resolution_failed`。
