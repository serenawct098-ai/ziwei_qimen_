# Module 4：終局裁決輸出

> 來源：規格書第13節「模組4：終局裁決輸出」
> source_locator: 紫微奇門排盤起局系統架構規格書v3建置版/第13節
> 治理依據：紫微與奇門各自的五級評級依古籍判準語句與規則檔獨立完成，25格查表屬使用者裁定之解讀層合併陳述，非另一層加權仲裁。

## 13.1 各自單一輸出

紫微、奇門五級評級各自獨立完成，各自輸出：

```yaml
system: ziwei | qimen
grade: 大吉 | 小吉 | 平 | 小凶 | 大凶 | null
grade_status: ready | unavailable_pending_grade_rules
main_judgment: string
secondary_judgment: string
risk_conditions: []
time_window: string
recommended_actions: []
evidence_entries: []
contrary_signals: []
effective_rules_version: string
```

## 13.2 25格合併陳述啟動條件

僅於以下條件同時成立時執行：

```yaml
run_mode: dual
ziwei_grade_status: ready
qimen_grade_status: ready
ziwei_grade: 大吉 | 小吉 | 平 | 小凶 | 大凶
qimen_grade: 大吉 | 小吉 | 平 | 小凶 | 大凶
verdict_25_grid_version: string
```

禁止輸入分數、權重、百分比及加總結果。

## 13.3 25格為解讀層，非另一層仲裁

25格終局評級查表屬**解讀層**：紫微評級獨立運算，只計主星廟旺利陷、四化祿權科忌、格局成敗，代表命定之路，不受單次決策影響；奇門評級獨立運算，只計八門吉凶＞落宮旺衰＞十干格局＞神星助緣，按此優先序疊算，代表每次決策的因果反應。兩線各自完成後才交叉查表，查表本身不做加總、不重新計算、不覆蓋任一管線的古籍判準結論。

25格查表是把紫微「命定之路」與奇門「當下因果反應」兩個獨立古籍判準結論，並列合看後給出的白話解讀陳述，其性質等同於命理實務中「本命看格局、流年看奇門，兩者對照解讀」的通行做法，本身不是古籍逐字記載的公式，亦不是系統自行發明的加權裁決機制；查表文字由使用者定稿確認。

**強制附帶規則**：模組4每次輸出25格合併陳述時，必須同時附上：

1. 紫微該次評級所依據的古籍條目（`ziwei_evidence_entries`），包含主星廟旺利陷、四化祿權科忌、格局成敗之原文引用及 `source_locator`。
2. 奇門該次評級所依據的古籍條目（`qimen_evidence_entries`），包含八門吉凶、落宮旺衰、十干格局命中、神星助緣之原文引用及 `source_locator`。
3. 兩者的判準語句原文摘錄，不可只輸出25格那一句合併結論而省略雙方各自的古籍依據。

不可只輸出「combined_statement」一句話了事；使用者需能從輸出中直接回查該次紫微判斷與奇門判斷各自基於哪一條古籍原文。

紫微＼奇門交叉陳述表：

| 紫微＼奇門 | 大吉 | 小吉 | 平 | 小凶 | 大凶 |
|---|---|---|---|---|---|
| 大吉 | 極吉：命強運順，全力衝刺不留保留 | 順勢加速：命強運助，可加大力度執行原定計劃 | 穩健推進：命強運靜，按原定節奏走 | 命強運滯：行動謹慎，避開運勢卡住的具體時間點 | 命強運逆：延後行動待機，命底夠厚可以等 |
| 小吉 | 乘勢而上：命普通運強勁，抓緊此波機會 | 平順向好：兩邊皆可，慢慢累積 | 按部就班：照計劃走，無驚喜無風險 | 小心試探：細步進行，不可一次落重注 | 暫緩觀望：運勢明顯不配合，等過此段再動 |
| 平 | 借運突破：命普通但此刻運強，可借勢突破 | 小幅進展：慢慢行，不強求 | 維持現狀：兩邊皆無特別因素，原地踏步屬正常 | 收縮防守：減少新嘗試，守住已有 | 退守避險：兩邊皆無支撐，先避風頭 |
| 小凶 | 一線生機：命底偏弱但運強可撐一把，值得一試 | 借力緩解：壓力減輕，不可掉以輕心 | 艱難持平：無惡化亦無好轉，捱過去 | 雙重承壓：兩邊皆不助力，減少行動與曝露 | 停止擴張：全面防守，任何新計劃停止，保住底線 |
| 大凶 | 絕地逢生：命極弱但運極強，翻盤罕有窗口，須果斷抓住 | 一線生機：命弱運有得幫，仍需謹慎，不可貪心 | 命弱運平：守成待變，不動為主，等下一運勢窗口 | 雙弱交疊：高危，大幅收縮所有動作 | 命運皆凶：全面退守避害，最高風險組合，須提醒醫療或法律方向 |

## 13.4 25格輸出資料結構

```yaml
output_layer: interpretation
combined_cell: string
combined_statement: string
decision_band: exploit_now | prepare_execute | monitor | conserve | retreat
combined_actions: []
ziwei_evidence_entries:
  - entry_id: string
    original_quote: string
    source_locator: string
    judgment_basis: main_star_brightness | sihua_lu_quan_ke_ji | pattern_success_or_failure
qimen_evidence_entries:
  - entry_id: string
    original_quote: string
    source_locator: string
    judgment_basis: door_grade | palace_prosperity | pattern_priority | god_star_assistance
verdict_25_grid_version: string
```

`output_layer: interpretation` 標記本結構屬解讀層輸出，非原始評級運算層；`ziwei_evidence_entries`與`qimen_evidence_entries`為強制欄位，缺一即視為輸出不完整。

決策帶對應：

| 決策帶 | 對應格位 |
|---|---|
| exploit_now | 大吉×大吉、大吉×小吉、小吉×大吉、平×大吉 |
| prepare_execute | 小吉×小吉、小吉×平、平×小吉、小凶×大吉、小凶×小吉、大凶×大吉 |
| monitor | 大吉×平、平×平、小凶×平、大凶×小吉 |
| conserve | 大吉×小凶、小吉×小凶、平×小凶、小凶×小凶、大凶×平 |
| retreat | 大吉×大凶、小吉×大凶、平×大凶、小凶×大凶、大凶×小凶、大凶×大凶 |

「大凶×大吉」（絕地逢生）雖屬 `exploit_now` 之外的特殊攻擊窗口，輸出時必須強制附帶風險條件與反向訊號，不可只輸出鼓勵性陳述。

25格只整合已完成雙軌評級及行動建議，不覆蓋紫微或奇門原始證據，不反向改寫任一管線評級。任一管線五級規則未完成時，模組4只輸出各自單一推演，`combined_25_grid_status` 設為 `unavailable_pending_grade_rules`。

## 13.5 輸出安全邊界

健康只描述盤面風險象意及建議就醫，不作診斷預後或死亡預言。法律只描述程序爭議及風險象意，建議諮詢合資格法律專業人士。投資只描述財務風險及行動節奏，不保證收益不給買賣指令。事故血光疾病官非一律以風險提示、預防及專業協助方向輸出。
