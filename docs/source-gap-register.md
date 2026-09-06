# Source Gap Register

| ID | 範圍 | 缺口 | 阻塞功能 | 狀態 |
|---|---|---|---|---|
| GAP-TIME-001 | 天文時間 | Skyfield `1.55` 已鎖定並由 asset manifest 核驗 | Batch 2B 天文 runtime | closed_by_batch_2b |
| GAP-TIME-002 | 天文時間 | JPL `de440s.bsp` 已在 `astronomy-assets-2026-09-06` Release 固化並由 asset manifest 核驗 | 真太陽時與節氣 | closed_by_batch_2b |
| GAP-TIME-003 | 天文時間 | IERS `finals2000A.all` 已在 `astronomy-assets-2026-09-06` Release 固化並由 asset manifest 核驗 | UT1、ΔT 與節氣邊界 | closed_by_batch_2b |
| GAP-TIME-004 | 城市解析 | 受控主要城市表已由 62 筆已審核 Natural Earth 城市座標與明確 IANA timezone 建立 | 城市輸入解析 | closed_by_batch_2c |
| GAP-ZW-001 | Z02 | 香港天文台 1901–2100 公農曆逐日轉換表已以固定 package asset 入庫；只提供 Gregorian date 到 Lunar date 的查詢；不提供 2101、lunar-to-Gregorian 或跨 coverage 推算。 | 紫微原始農曆轉換 | closed_by_batch_3a_4 |
| GAP-ZW-002 | Z08 | 六十甲子納音與五行局完整表未建立 | 命宮五行局 | open |
| GAP-ZW-003 | Z09 | 五局 × 三十日紫微定位表未完成 | 紫微星定位 | open |
