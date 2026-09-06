# 系統架構

| 層級 | 責任 |
|---|---|
| Source corpus | 原文、口訣、鎖定裁定、官方日曆來源 |
| Canonical tables | 完整、可機讀、具 `source_ref` 的唯一正式資料表 |
| Compute engine | 真太陽時、曆法、紫微排盤、限運、奇門起局、九宮全盤 |
| Independent inference | 紫微與奇門各自推演、條目化證據、五級 |
| Integration | 完成五級後讀取 25 格與行動策略 |

```text
出生時間 + birth_location + 性別
→ 出生地真太陽時
→ 紫微本命排盤
→ 紫微限運
→ 紫微推演與五級

問事時間 + question_location
→ 問事地真太陽時
→ 奇門起局
→ 奇門九宮盤
→ 奇門事件推演與五級

完成奇門九宮盤 + primary_residence_location + 空間方向資料
→ 奇門風水方位映射

紫微五級 + 奇門五級
→ 25 格
→ 行動策略
```

## 邊界

- `birth_location` 只用於紫微本命真太陽時。
- `question_location` 只用於奇門真太陽時與起局。
- `primary_residence_location` 只用於完成奇門起局後的風水方位映射。
- `primary_residence_location` 不進奇門四柱、節氣、陰陽遁、局數、地盤、天盤、人盤、神盤。
- 推演層不改寫排盤層結果。
- 整合層不改寫任何單軌結果。

## 中五

```text
earth_plate:
  original_palace
  effective_palace
  is_lodged_from_center

tianqin:
  original_home_palace = 5
  static_lodged_palace = 2
  dynamic_palace = tianrui_dynamic_palace
  interpretation_palace = tianrui_dynamic_palace
```

## 評級

- 紫微：主星亮度、有效四化、格局成敗。
- 奇門：八門吉凶 ＞ 落宮旺衰 ＞ 十干格局 ＞ 神星助緣。
- 不使用數值、權重、百分比或加總公式。
- 任一單軌評級未完成時，不讀取 25 格。
