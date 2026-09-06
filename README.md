# 紫微×奇門系統

此 repository 建立一個可重現、可驗證、可封裝為 Skill 的紫微斗數與時家轉盤奇門遁甲系統。

## 算法基準

《紫微×奇門傳統算法作業規格書》是本系統唯一算法裁定來源。

系統採用：

- 紫微斗數：南派三合十二宮骨架，加已鎖定北派四化飛星。
- 奇門遁甲：時家、轉盤、拆補、寄坤二隨芮派。
- 共同時間前置：先校正真太陽時，再進入紫微曆法或奇門四柱與節氣。
- 雙軌原則：紫微本命與限運、奇門起局與推演先各自完成；兩邊完成評級後，才可讀取 25 格行動策略。

## 正式支援範圍

- 日期：1901-01-01 至 2100-12-31
- 地點輸入：城市名稱；可選 ISO 3166-1 alpha-2 國家／地區代碼作消歧
- 民用時區：由受控城市資料映射至 IANA Time Zone Database
- 正式星曆：JPL DE440S
- 真太陽時規則判定：秒級

超出正式日期範圍時，系統回傳 `unsupported_date_range`，不使用替代星曆、網頁萬年曆、固定 UTC offset 或估算方式。

無法從受控城市資料唯一解析城市、經緯度或 IANA 時區時，系統回傳 `location_resolution_failed`，不使用外部地理編碼服務或猜測結果。

## 資料邊界

紫微本命只使用：

- 出生民用時間
- 出生城市
- 性別
- 分析時間

奇門起局只使用：

- 問事民用時間
- 問事城市
- 問題類型

問事時間與問事城市不可改寫紫微本命盤。出生資料不可直接起時家奇門局。

現居資格、居住年期、旅遊地排除、酒店排除、出差地排除等規則不在本系統內。

## 系統狀態

目前處於 Batch 1：Repository 骨架與時間標準。

本批次不包含：

- 星曆檔與 IERS 資料快照
- 城市座標與時區資料
- 紫微與奇門機器表
- 排盤與起局實作
- 五級判定表
- 25 格整合表

未有完整、可核實資料的功能不得以空 JSON、placeholder、fallback 或替代資料表形式建立。

## 專案結構

```text
src/ziwei_qimen/
  domain/        枚舉、資料模型、證據與計算 provenance
  contracts/     請求與輸出 JSON Schema
  repositories/  受控來源與資料表讀取
  time/          民用時間、地點、天文時間、真太陽時、節氣
  ziwei/         紫微曆法、排盤、限運、推演、評級
  qimen/         奇門曆法、起局、九宮、推演、評級
  integration/   雙軌 25 格行動策略

data/
  astronomy/     固定版本星曆、IERS、城市座標資料
  sources/       原文與裁定來源條目
  tables/        唯一正式機器可讀資料表

docs/            架構、時間標準、來源政策、缺口登錄
tests/           unit、integration、acceptance、golden cases
```

## 開發原則

- 一個規則概念只可有一個正式來源。
- 一個功能只可有一份正式檔案。
- 一張資料表只可有一份正式算法來源。
- 一個算法結果只可有一個正式值。
- 不建立 alias、redirect、deprecated 欄位、compatibility 欄位、fallback、dual-read 或雙正式來源。
- 原文條目只保存一次；資料表以 `source_ref` 引用原文。
- 推演層不得改寫排盤層已確定的星曜、干支、宮位、門、星、神或局數。
- 25 格只作行動策略，不可回寫紫微或奇門任何結果。
- 未核實的資料不填入正式 JSON；以 `docs/source-gap-register.md` 登錄。

## 開發環境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

目前尚未建立可執行排盤 API。API 與排盤模組會在後續 Batch 建立。
