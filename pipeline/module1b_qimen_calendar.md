# Module 1B：奇門曆法轉換

> 來源：規格書第8節「模組1B：奇門曆法轉換」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第8節

輸入：`question_effective_true_solar_datetime`。

輸出：

```yaml
ganzhi_year: string
ganzhi_month: string
ganzhi_day: string
ganzhi_hour: string
solar_term_name: string
solar_term_start: datetime
solar_term_end: datetime
yin_yang_dun: yang | yin
symbol_head: string
three_yuan: upper | middle | lower
calendar_algorithm_version: string
```
執行順序：

1. 以effective真太陽時取得精確節氣區間。
2. 冬至後至夏至前使用陽遁；夏至後至冬至前使用陰遁。
3. 依日干支追溯甲己符頭。
4. 符頭地支子、午、卯、酉定上元；寅、申、巳、亥定中元；辰、戌、丑、未定下元。
5. 依節氣、陰陽遁、三元查拆補法局數表。
6. 產生四柱、陰陽遁、符頭、三元、局數。
