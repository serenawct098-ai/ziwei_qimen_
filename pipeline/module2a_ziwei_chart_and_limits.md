# Module 2A：紫微本命起盤與限運疊盤

> 來源：規格書第9節「模組2A：紫微本命起盤與限運疊盤」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第9節

## 9.1 本命盤骨架

### A01：定命宮及身宮

- 寅宮起正月，順數至有效農曆生月。
- 自生月宮起子時逆數至生時定命宮。
- 自生月宮起子時順數至生時定身宮。

輸出：

```yaml
life_palace_branch: string
body_palace_branch: string
```

### A02：安十二宮

以命宮為起點，逆時針固定排列：命宮、兄弟、夫妻、子女、財帛、疾厄、遷移、交友、官祿、田宅、福德、父母。

輸出：十二宮名稱、地支、宮位索引、對宮、三方關係。

### A03：起十二宮天干

依生年天干五虎遁起寅宮干，順布十二宮干：

```text
甲己年丙寅起
乙庚年戊寅起
丙辛年庚寅起
丁壬年壬寅起
戊癸年甲寅起
```

輸出：各宮宮干。

### A04：定五行局

以命宮干支查六十甲子納音，歸入水二局、木三局、金四局、土五局、火六局。

輸出：`five_element_bureau`。

### A05：起紫微星及安十四主星

1. 依五行局及農曆生日查《紫微星定位表》定紫微落宮。
2. 依紫微天機逆行旁、天府太陰順行等主星序列安十四主星。
3. 記錄每顆主星所落宮位、星系及亮度。

輸出：十四主星完整落宮表。

## 9.2 輔曜、煞曜、神煞及流曜

### A06：年干系安星

依生年天干安：生年四化（祿權科忌）、祿存、擎羊、陀羅、天魁天鉞（辛年固定魁寅鉞午）。

輸出：年干系星曜及四化標記。

### A07：年支系安星

依生年地支安：天馬、紅鸞、天喜、歲前十二神、將前十二神。

輸出：年支系星曜及神煞落宮。

### A08：生月系安星

依有效農曆生月安：左輔右弼、天刑天姚、三台八座及其他知識庫月系條目定義星曜。

輸出：月系星曜落宮。

### A09：生時系安星

依生時安：文昌文曲、火星鈴星、地空地劫、天傷天使及其他知識庫時系條目定義星曜。

輸出：時系星曜落宮。

### A10：博士十二神

由祿存起點，陽男陰女順行、陰男陽女逆行，安博士、力士、青龍、小耗、將軍、奏書、蜚廉、喜神、病符、大耗、伏兵、官府。

輸出：博士十二神落宮。

## 9.3 本命格局及飛星四化

### A11：主盤格局

建立三方四正（命財官遷）、對宮、三合宮、會照、夾宮、主星格局（紫府朝垣、殺破狼、機月同梁、府相朝垣等）、吉煞會照、主星亮度。

### A12：宮干飛化、自化、向心及離心

對每一宮：讀取本宮宮干，依十干四化表取得化祿化權化科化忌目標星，尋找目標星所在宮建立飛化記錄。飛化目標宮等於來源宮標記 `self_transform`；來源宮及目標宮互為對宮標記 `outward_transform`；對宮宮干飛化目標落入本宮標記 `inward_transform`。

每筆飛化記錄：

```yaml
source_palace: string
source_stem: string
transform_type: lu | quan | ke | ji
target_star: string
target_palace: string
relation: normal_fly | self_transform | inward_transform | outward_transform
time_layer: natal | decade | annual | monthly | daily | hourly
```

演算層只保存飛化方向及落點；解讀層依宮位主題、祿權科忌類型及時間層轉譯象意。

### A13：忌煞交沖判定

依《忌煞交沖格局》原文轉表：

```yaml
pattern_horse_head_arrow:
  condition: 擎羊坐命午宮，與天同或貪狼同宮，丙年戊年生人
  effect: 富貴可許但不耐久，須防意外血光
  source_locator: 忌煞交沖格局/二、馬頭帶箭格

pattern_xingqiu_jiayin:
  condition: 廉貞天相同宮坐命子宮或午宮，並有擎羊同宮
  effect: 官非訴訟牢獄刑杖，終身難以發達
  worst_case: 丙年生人廉貞於午宮化忌
  source_locator: 忌煞交沖格局/三、刑囚夾印格

pattern_fengliu_caizhang:
  condition: 貪狼獨坐命宮寅宮，與陀羅同宮
  effect: 因色致禍，桃花糾紛，甚而官非訟事
  source_locator: 忌煞交沖格局/四、風流彩杖格

pattern_chenxu_chouwei_weiquan:
  condition: 擎羊火星入坐辰戌丑未四墓宮，或貪狼武曲遇火旺地
  effect: 文武雙全，兵權萬里
  source_locator: 忌煞交沖格局/五、擎羊火星同宮異格

pattern_yangtuo_jiaji:
  condition: 化忌坐守之宮，左右鄰宮為擎羊陀羅所夾或火星鈴星所夾
  effect: 凶性倍增
  distinction: 相夾非同宮，須與刑囚夾印格三星同宮嚴格區分
  source_locator: 忌煞交沖格局/六、羊陀夾忌與火鈴夾忌之通則
```

## 9.4 限運疊盤

### A14：大限

依五行局定起限歲數，陽男陰女順行、陰男陽女逆行，每十年一限，標定大限命宮，讀取大限宮干飛出大限祿權科忌。

### A15：小限

依生年地支及性別，逐年順行或逆行一宮，標定小限宮。

### A16：流年

以流年地支所在本命宮為流年命宮，以流年天干飛流年四化，對齊本命宮、大限宮、小限宮、流年宮。

### A17：流月

定斗君，順布流月命宮，以農曆月份原月干飛流月四化，跨節氣不改月干。

### A18：流日

以流月命宮起初一順行定流日命宮，以日干五鼠遁定流日時干飛流日四化。

### A19：流時

以流日宮起子時順布定流時命宮，依日干五鼠遁定時干飛流時四化。

## 9.5 重忌判定

```yaml
natal_ji_target_palace: string
decade_ji_target_palace: string
annual_ji_target_palace: string
heavy_ji: boolean
```

```text
若 natal_ji_target_palace = decade_ji_target_palace
且 decade_ji_target_palace = annual_ji_target_palace：
    heavy_ji = true
否則：
    heavy_ji = false
```

流月、流日、流時化忌只作附加壓力條件，不改寫三重忌定義。

重忌、自化、向心、離心、忌煞交沖、限運疊盤屬盤面推演、風險條件、時間窗口及行動修正之用，不直接改寫紫微基礎五級評級（基礎評級只計主星廟旺利陷、四化祿權科忌、格局成敗，見effective_rules.md「紫微脈絡資料」條目及module3a_ziwei_inference.md）。
