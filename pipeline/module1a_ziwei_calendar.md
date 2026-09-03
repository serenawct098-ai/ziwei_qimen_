# Module 1A：紫微曆法轉換

> 來源：規格書第7節「模組1A：紫微曆法轉換」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第7節

輸入：`birth_effective_true_solar_datetime`。

輸出：

```yaml
lunar_year: integer
lunar_month_raw: integer
lunar_day: integer
is_leap_month: boolean
effective_lunar_month: integer
ganzhi_year: string
ganzhi_month: string
ganzhi_day: string
hour_branch: 子 | 丑 | 寅 | 卯 | 辰 | 巳 | 午 | 未 | 申 | 酉 | 戌 | 亥
zi_hour_day_shift_applied: boolean
calendar_algorithm_version: string
```

執行順序：

1. 以effective真太陽時換算農曆年月日。
2. 套用晚子時日界。
3. 若屬閏月，套用中月分界法，產生 `effective_lunar_month`。
4. 產生生年、生月、生日、生時干支。
5. 將 `effective_lunar_month`、農曆日、時支送交紫微起盤。
