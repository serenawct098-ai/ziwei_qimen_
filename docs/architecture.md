# 系統架構

## 目的

本系統將紫微斗數與時家轉盤奇門遁甲建立為兩條獨立、可追溯、可驗證的計算管線。

唯一算法裁定來源為《紫微×奇門傳統算法作業規格書》。

本文件只定義工程責任、資料邊界、程式模組與依賴方向。它不重寫任何排盤、起局、格局或評級算法。

## 分層

| 層級 | 名稱 | 唯一責任 |
|---|---|---|
| L1 | Source corpus | 保存古籍原文、口訣、已鎖定裁定及官方日曆來源條目 |
| L2 | Canonical tables | 保存完整、可機讀、具 `source_ref` 的唯一正式資料表 |
| L3 | Compute engine | 真太陽時、曆法、紫微排盤、限運、奇門起局與九宮全盤 |
| L4 | Independent inference | 紫微與奇門各自推演、條目化證據與五級輸出 |
| L5 | Integration | 只讀兩邊已完成評級，讀 25 格，輸出行動策略 |

## 資料流

```text
ZiweiBirthInput
→ 真太陽時
→ 紫微曆法
→ 紫微本命排盤
→ 紫微限運
→ 紫微推演
→ 紫微五級

QimenQueryInput
→ 真太陽時
→ 奇門四柱與節氣
→ 奇門起局
→ 奇門九宮全盤
→ 奇門推演
→ 奇門五級

紫微五級 + 奇門五級
→ 25 格
→ 行動策略
```

## 不可混用

- 紫微本命只讀出生民用時間、出生城市與性別。
- 紫微限運只讀紫微本命結果與分析時間。
- 奇門只讀問事民用時間、問事城市與問題類型。
- 紫微本命不讀奇門城市或問事時間。
- 奇門起局不讀出生資料。
- L4 推演不改寫 L3 排盤結果。
- L5 整合不改寫 L3 排盤結果或 L4 的任一獨立推演與評級。

## 城市解析責任

外部請求可直接提交城市名稱；可選 ISO 3166-1 alpha-2 國家／地區代碼作消歧。

```text
city + optional country_code
→ controlled city dataset
→ canonical city_id
→ latitude + longitude + IANA timezone
→ true solar time
```

城市解析只可使用本地、受控的城市資料集。不得在 runtime 呼叫外部地理編碼服務。

城市無法唯一解析時，系統回傳 `location_resolution_failed`。不得猜測座標或時區。

## 資料夾責任

```text
src/ziwei_qimen/domain/
  穩定枚舉、資料模型、來源及計算 provenance。

src/ziwei_qimen/contracts/
  請求與輸出的 JSON Schema；只檢查結構與資料邊界。

src/ziwei_qimen/time/
  民用時間、時區、地點、天文時間、真太陽時、節氣。

src/ziwei_qimen/ziwei/
  紫微曆法、本命、限運、關係宮、推演、五級。

src/ziwei_qimen/qimen/
  奇門四柱、節氣、起局、九宮、推演、五級。

src/ziwei_qimen/integration/
  25 格整合，禁止計算或改寫任一單軌盤面。

data/sources/
  原文與裁定來源條目。原文只保存一次。

data/tables/
  唯一正式機器表。每張表必有 `table_id` 與 `source_refs`。

data/astronomy/
  受控版本的星曆、Earth-orientation 資料與城市座標資料。
```

## 中五資料模型

奇門中五不可被壓縮成單一宮位欄位。

地盤干必保存：

```text
original_palace
effective_palace
is_lodged_from_center
```

天禽必保存：

```text
original_home_palace = 5
static_lodged_palace = 2
dynamic_palace = tianrui_dynamic_palace
interpretation_palace = tianrui_dynamic_palace
```

天禽不可成為獨立外圈星。中五不可設獨立八門或八神。

## 評級與 25 格

紫微與奇門必先完成獨立推演與獨立五級。

- 紫微基礎五級只讀主星亮度、有效四化、格局成敗。
- 奇門五級優先序：八門吉凶 ＞ 落宮旺衰 ＞ 十干格局 ＞ 神星助緣。
- 兩邊不得使用數值、權重、百分比或加總公式。
- 評級條件不足時，只輸出條目化推演。
- 任一單軌評級未完成時，不可讀取 25 格。
- 25 格只輸出行動策略、決策帶、風險條件與雙方證據集合。

## 不可建立的結構

- 兼容欄位、deprecated 欄位、alias、redirect、fallback、dual-read。
- 同功能的第二張正式資料表。
- 0 byte JSON 或半成品 placeholder。
- 把古籍原文複製到多份表。
- 以外部萬年曆、未受控網頁或未鎖定線上資料作 runtime 算法來源。
