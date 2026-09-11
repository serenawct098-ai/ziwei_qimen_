# Astronomy Provisioning Design (Batch 3B-1A)

## 現況（已核實）

- de440s.bsp、finals2000A.all 只存在 Release `astronomy-assets-2026-09-06`，未落地於 repo 檔案樹。
- asset_manifest.json 為 size 與 SHA-256 的唯一真值，provisioner 與 loader 皆須以此為核對依據，不建立第二來源。
- true_solar_time() 現為無條件 raise ErrorCode.ASTRONOMY_ASSET_UNAVAILABLE，尚無天文計算路徑。

## Provisioning（人手觸發，不在 runtime 執行）

流程：
1. 人手從 Release 下載 de440s.bsp、finals2000A.all。
2. 人手執行 provisioner，寫入固定本地資產根目錄（非 Python package 內）。
3. Provisioner 對照 asset_manifest.json 核對 size 與 SHA-256，任一不符即中止，不寫入。
4. Provisioner 完成後不留副本、不留 cache、不建立 alias 路徑。

固定本地資產根目錄由環境變數 ZIWEI_QIMEN_ASSET_ROOT 指定。程式不得自行猜測路徑、不得 fallback 到 package 內建路徑。

## Runtime Loader

職責：
- 只從 ZIWEI_QIMEN_ASSET_ROOT 指定路徑讀取已存在檔案。
- 讀取前重算 SHA-256，與 asset_manifest.json 比對；不符即 raise ErrorCode.ASTRONOMY_ASSET_UNAVAILABLE。
- 呼叫 Skyfield 時必須明確指定本地 Loader(directory=...)，且僅在確認檔案已存在後才呼叫 load.timescale(builtin=False)。
- 任何觸發網路下載的路徑一律視為資產不可用，不得重試、不得使用近似值代替。

不得：
- runtime 自動下載。
- 放入 Python package 內建資產。
- 使用第二 binary 來源。
- 使用 fallback、alias 或 path search。
- 把本地 cache 當作正式 SSOT；SSOT 只能是 asset_manifest.json。

## 與既有 contract 的對齊

TrueSolarTimeProvenance 現有欄位不變：
civil_datetime, iana_timezone, timezone_data_version,
true_solar_datetime, precision, ephemeris_id, ephemeris_version,
iers_data_version, calculation_status

本設計不新增 longitude_correction_seconds、mean_solar_datetime、
equation_of_time_seconds 等欄位；均時差不作獨立輸出，
已於使用者確認裁定。

ephemeris_id / ephemeris_version 於 loader 成功時填入
asset_manifest.json 記錄之名稱與版本；
iers_data_version 填入 finals2000A.all 對應版本標記。

## 驗收條件（供 3B-1B 承接）

- Loader 在資產缺失或雜湊不符時必須 raise ASTRONOMY_ASSET_UNAVAILABLE，
  並附帶缺失原因（missing / hash_mismatch）。
- Loader 必須在無網路環境下可通過測試（模擬資產已存在本地）。
- Loader 不得引入任何新的 ErrorCode；沿用既有 ASTRONOMY_ASSET_UNAVAILABLE。
