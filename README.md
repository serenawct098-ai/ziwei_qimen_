# 紫微×奇門系統

紫微斗數與時家轉盤奇門遁甲系統。

## 算法基準

《紫微×奇門傳統算法作業規格書》是唯一算法裁定來源。

- 紫微：南派三合十二宮骨架，加已鎖定北派四化飛星。
- 奇門：時家、轉盤、拆補、寄坤二隨芮派。
- 真太陽時先於紫微曆法、奇門四柱與節氣。
- 紫微與奇門各自完成推演與五級後，才讀取 25 格。

## 日期範圍

```text
1901-01-01 至 2100-12-31
```

超出範圍回傳 `unsupported_date_range`。

## 輸入邊界

```text
birth_location
→ 紫微出生地真太陽時
→ 紫微本命盤

question_location
→ 奇門問事地真太陽時
→ 奇門起局

primary_residence_location
→ 已完成奇門九宮盤的風水方位映射
```

`primary_residence_location` 不影響奇門四柱、節氣、陰陽遁、局數、地盤、天盤、人盤或神盤。

## 開發

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
