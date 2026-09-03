# Module 2B：奇門轉盤起局

> 來源：規格書第10節「模組2B：奇門轉盤起局」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第10節

## 10.1 B01：四柱、節氣、陰陽遁、符頭、三元及局數

輸入模組1B結果，產生：

```yaml
yin_yang_dun: yang | yin
ju_number: 1..9
symbol_head: string
three_yuan: upper | middle | lower
hour_pillar: string
```

## 10.2 B02：地盤三奇六儀（完整九局查表，逐字轉自《三奇六儀完整格局》）

規則：

1. 依 `yin_yang_dun` 及 `ju_number` 直接查 `data/qimen/earth_plate_9_ju_table.json` 完整九局地盤表，不得由摘要口訣即席拼接或推導九宮序列。
2. 表中「中5寄坤2」欄位表示該儀原應落中五宮，因中宮不參與飛佈占斷，一律轉記於坤二宮。
3. 地盤於同一局五日一元內固定不移。
4. 來源：《三奇六儀完整格局》〈陰陽遁九局（都寄坤二宮版）〉。

輸出：

```yaml
earth_plate:
  palace_1: stem
  palace_2: stem
  palace_3: stem
  palace_4: stem
  palace_5: stem
  palace_6: stem
  palace_7: stem
  palace_8: stem
  palace_9: stem
```

## 10.3 B03：旬首及值符本位

依時柱查六旬首（甲子、甲戌、甲申、甲午、甲辰、甲寅），對應六儀（甲子戊、甲戌己、甲申庚、甲午辛、甲辰壬、甲寅癸），找出旬首六儀於地盤所在宮，取該宮九星本位為值符星。

本步驟之六局×六旬首完整枚舉查表由 `data/qimen/xunshou_zhifu_table.json` 提供；該表現階段為骨架，內容標記待補，B03邏輯先依本節文字規則執行。

## 10.4 B04：值符加時干及天盤九星轉布

找出時干於地盤所在宮，將值符星加臨時干宮，依 `nine_palace_rotation_table.json` 轉布九星；該表定義九宮環行序列、起點、起點計數、陽遁方向、陰遁方向、中宮跳轉及寄宮處理；其餘九星隨值符同步平移。

`nine_palace_rotation_table.json` 現階段為骨架，B04依本節文字規則（值符隨時干飄轉，其餘八星依旬首原始順序同步平移）執行。

## 10.5 B05：值使本位及八門轉布

取值符星原始本位宮所對應八門為值使，從旬首所在宮起，依陽遁順行、陰遁逆行，數至時支所在宮，值使移至該宮，其餘七門依八門固定序列同步轉布。八門本位固定：坎休、坤死、震傷、巽杜、艮生、離景、兌驚、乾開，中五無門寄坤二死門統之。`zhishi_door_table.json` 保存值使起點、時支數法、方向及完整八門轉布結果。

`zhishi_door_table.json` 現階段為骨架，B05依本節文字規則執行。

## 10.6 B06：八神轉布

以值符加臨後所在宮為八神首宮，次序固定：值符、螣蛇、太陰、六合、白虎、玄武、九地、九天；陽遁順時針排佈，陰遁逆時針排佈；使用 `nine_palace_rotation_table.json`。

## 10.7 天禽及中宮資料模型

```yaml
star: 天禽
home_palace: 5
effective_base_palace: 2
display_with_star: 天芮
rotation_policy: follows_turning_heaven_plate
```

規則：天禽本位中五；天禽排盤、顯示及斷局寄坤二；坤二顯示天芮及天禽同宮；天禽按天盤轉布規則隨值符飄轉；本位、寄宮、顯示及旋轉分開保存；不可將寄坤二誤作天禽永遠不隨轉。

## 10.8 B07：旬空及驛馬

依時柱推算兩個空亡宮位；依時支推算驛馬宮位；使用 `void_horse_table.json`。

`void_horse_table.json` 現階段為骨架，規格書本節僅述規則文字，未提供完整六十甲子旬空及驛馬枚舉對照表，詳細缺口說明見該JSON檔待補欄位。

## 10.9 B08：內外盤

陽遁內盤：坎一、艮八、震三、巽四；外盤：離九、坤二、兌七、乾六。陰遁內盤：離九、坤二、兌七、乾六；外盤：坎一、艮八、震三、巽四。

## 10.10 B09：格局及狀態檢查（完整轉自《三奇六儀完整格局》〈六甲值符格局〉）

B09為模組2B最後一道判定步驟，須在B02至B08全部完成、天盤人盤神盤地盤四盤及天禽寄宮狀態皆已確定後才可執行。B09運作方式如下：

1. **呼叫方式**：B09讀取 `data/qimen/qimen_pattern_table.json`（18條十干剋應吉凶格局，來源《三奇六儀完整格局》〈六甲值符格局〉）逐條核對本局天盤干加地盤干的組合，找出所有命中條目。
2. **判定順序**：依 `qimen_pattern_table.json` 內條目原文順序（青龍返首與飛鳥跌穴→龍逃走與虎猖狂→騰蛇夭矯與朱雀投江→五不遇時與勃格→六儀擊刑→伏宮格飛宮格伏干格飛干格→大格與刑格→三奇得使與相佐）逐條核對，非任意順序，亦非依吉凶分類優先核對。
3. **命中標記方式**：每命中一條，輸出：

```yaml
pattern_id: string
pattern_type: string
palace: string
status: auspicious | neutral | inauspicious
source_entries: [string]
```

4. **與五級評級的關係**：B09輸出的格局命中結果，於模組3B（奇門推演及五級評級）第12.3節依 `pattern_priority`（major_auspicious／major_inauspicious／structural_risk）分類使用，B09本身不做吉凶加總，只負責枚舉命中條目。

依序檢查以下十干剋應與吉凶格局，逐條記錄命中結果：

```yaml
pattern_qinglong_fanshou:
  condition: 天盤甲子戊加地盤丙奇（戊加丙）
  status: auspicious
  meaning: 青龍返首，木生火子顧其母，丙火剋庚金救護值符，宜就職訴訟遷移求財建造
  source_locator: 三奇六儀完整格局/二、青龍返首與飛鳥跌穴

pattern_feiniao_dieqxue:
  condition: 天盤丙奇加地盤甲子戊（丙加戊）
  status: auspicious
  meaning: 飛鳥跌穴，火歸木源如鳥歸巢，宜就職求財訴訟建造婚姻
  source_locator: 三奇六儀完整格局/二、青龍返首與飛鳥跌穴

pattern_long_taozou:
  condition: 乙木加辛金（乙遇辛）
  status: inauspicious
  meaning: 龍逃走，青龍受剋，身殘財損
  source_locator: 三奇六儀完整格局/三、龍逃走與虎猖狂

pattern_hu_changkuang:
  condition: 辛金加乙木（辛遇乙）
  status: inauspicious
  meaning: 虎猖狂，白虎受沖，財物虛耗
  source_locator: 三奇六儀完整格局/三、龍逃走與虎猖狂

pattern_tengshe_yaojiao:
  condition: 癸水加丁火或丁火加癸水
  status: inauspicious
  meaning: 騰蛇夭矯，虛驚怪異，心神不寧，夢魅纏擾
  source_locator: 三奇六儀完整格局/四、騰蛇夭矯與朱雀投江

pattern_zhuque_toujiang:
  condition: 丁火遇癸水剋制
  status: inauspicious
  meaning: 朱雀投江，文書失誤，口舌是非，謀事不成
  source_locator: 三奇六儀完整格局/四、騰蛇夭矯與朱雀投江

pattern_wubuyu_shi:
  condition: 時干剋日干
  status: inauspicious
  meaning: 五不遇時，諸事不宜，宜靜不宜動
  source_locator: 三奇六儀完整格局/五、五不遇時與勃格

pattern_bo_ge:
  condition: 丙奇加臨時干之上
  status: inauspicious
  meaning: 勃格，躁動生禍，急躁招災
  source_locator: 三奇六儀完整格局/五、五不遇時與勃格

pattern_liuyi_jixing:
  condition: 六甲直符加臨其所刑之地支宮位，共六種對應：甲子戊加震三宮（子刑卯）、甲戌己加坤二宮（戌刑未）、甲申庚加艮八宮（申刑寅）、甲午辛加離九宮（午自刑）、甲辰壬加巽四宮（辰自刑）、甲寅癸加巽四宮（寅刑巳）
  status: greatly_inauspicious
  meaning: 六儀擊刑，極凶，百凶俱集，即使值符亦不可用，一動必有災傷
  source_locator: 三奇六儀完整格局/六、六儀擊刑

pattern_fugong_ge:
  condition: 天盤六庚加地盤六甲值符所在之宮（庚加戊）
  status: greatly_inauspicious
  meaning: 伏宮格，賊星剋值符，主客皆不利，求人不在，出行遇盜賊
  source_locator: 三奇六儀完整格局/七、伏宮格飛宮格伏干格飛干格

pattern_feigong_ge:
  condition: 天盤六甲值符加地盤六庚（戊加庚）
  status: greatly_inauspicious
  meaning: 飛宮格，值符遇庚金，尤不利客，作戰主敗亡
  source_locator: 三奇六儀完整格局/七、伏宮格飛宮格伏干格飛干格

pattern_fugan_ge:
  condition: 天盤六庚加地盤日干
  status: greatly_inauspicious
  meaning: 伏干格，日干受剋，不利主事，百事宜隱伏不可聲張
  source_locator: 三奇六儀完整格局/七、伏宮格飛宮格伏干格飛干格

pattern_feigan_ge:
  condition: 天盤日干加地盤六庚
  status: greatly_inauspicious
  meaning: 飛干格，主客兩傷皆不利；若得三奇吉門則可用兵
  source_locator: 三奇六儀完整格局/七、伏宮格飛宮格伏干格飛干格

pattern_da_ge:
  condition: 庚金加臨六癸
  status: greatly_inauspicious
  meaning: 大格，出行遠征大凶，主帥有殞命之危
  source_locator: 三奇六儀完整格局/八、大格與刑格

pattern_xing_ge:
  condition: 庚金加臨六己
  status: inauspicious
  meaning: 刑格，刑傷官訟，牢獄之災
  source_locator: 三奇六儀完整格局/八、大格與刑格

pattern_sanqi_deshi:
  condition: 三奇乙丙丁得其所值之門與宮相輔相成
  status: auspicious
  meaning: 三奇得使，眾善皆臻，百事順遂
  source_locator: 三奇六儀完整格局/九、三奇得使與相佐

pattern_sanqi_xiangzuo:
  condition: 本旬直符加地盤三奇之上
  status: auspicious
  meaning: 三奇相佐，調兵派弁軍士效力吉
  source_locator: 三奇六儀完整格局/九、三奇得使與相佐
```

其餘必跑檢查依序：三奇入墓、旬空、驛馬、門迫（人盤門剋地盤宮）、宮迫（地盤宮剋人盤門）、星生宮、星剋宮、九星八門旺相休囚廢、十干十二長生、伏吟、反吟、三詐、五假、九遁、坤二天芮天禽同宮特例。

每項輸出：

```yaml
pattern_id: string
pattern_type: string
palace: string
status: auspicious | neutral | inauspicious
source_entries: [string]
```
