# Module 0：輸入正規化與真太陽時校正

> 來源：規格書第6節「模組0：輸入正規化與真太陽時校正」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第6節

## 6.1 紫微流程

輸入：`birth_datetime_local`、`birth_place`。

1. 驗證出生地、時區及時間格式。
2. 使用出生地IANA時區及歷史夏令時間，將民用時間轉UTC。
3. 取得出生地經度。
4. 取得星曆日期所需儒略日、ΔT及均時差。
5. 計算經度時差及均時差。
6. 產生出生地effective真太陽時。
7. 保存完整轉換鏈。

輸出：

```yaml
birth_civil_local_datetime: string
birth_utc_datetime: string
birth_julian_day_ut: number
birth_julian_day_tt: number
delta_t_seconds: number
equation_of_time_seconds: number
longitude_correction_seconds: number
birth_effective_true_solar_datetime: string
birth_location_precision: exact_coordinate | city_centroid
birth_timezone_source: iana_timezone
tzdb_version: string
ephemeris_provider: string
ephemeris_version: string
delta_t_model: string
```

`current_residence` 不參與紫微本命盤真太陽時校正，不改變命宮、身宮、五行局、主星、輔曜、四化或大限順逆。

## 6.2 奇門流程

輸入：`question_datetime_local`、`current_residence`。

1. 驗證現居地是否居住滿兩年以上或已指定主要長居基地。
2. 驗證現居地、時區及時間格式。
3. 使用現居地IANA時區及歷史夏令時間，將問事民用時間轉UTC。
4. 取得現居地經度。
5. 取得星曆日期所需儒略日、ΔT及均時差。
6. 計算經度時差及均時差。
7. 產生現居地effective真太陽時。
8. 保存完整轉換鏈。

輸出：

```yaml
question_civil_local_datetime: string
question_utc_datetime: string
question_julian_day_ut: number
question_julian_day_tt: number
delta_t_seconds: number
equation_of_time_seconds: number
longitude_correction_seconds: number
question_effective_true_solar_datetime: string
current_residence_location_precision: exact_coordinate | city_centroid
current_residence_timezone_source: iana_timezone
residence_qualified: boolean
tzdb_version: string
ephemeris_provider: string
ephemeris_version: string
delta_t_model: string
```

## 6.3 晚子時及中月分界

1. 真太陽時23:00–23:59：紫微排盤日期加一日，時支維持子。
2. 真太陽時00:00–00:59：紫微排盤日期不加日，時支為子。
3. 真太陽時完成後才換算農曆日月。
4. 閏月採中月分界法：1–15日歸本月；16日至月底歸下月。
5. 29日及30日均歸後半月，按下月處理。
