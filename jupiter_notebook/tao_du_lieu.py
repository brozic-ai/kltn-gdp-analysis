"""Tạo file dữ liệu cuối cho KLTN: data/input/KLTN_du_lieu.xlsx (sheet DATA + README).

Nguồn:
- data/input/KLTN_Tong_hop_hoan_chinh.xlsx: các sheet *_clean (WDI: GDPG, CAP, FDI, GOV, LAB; UNCTAD: THEIL)
  và COUNTRY_REGION (128 nước, DEV, khu vực).
- data/input/bulk_files_Herfindahl-Hirschman_Market_Concentration_Index_Mirrored_Export.xlsx: link World Bank
  WITS cho HHI tập trung thị trường xuất khẩu (file ed_hhpci_mrkt_<năm>, có 1988-2022).

Giai đoạn 2000-2022 vì HHI chỉ có đến 2022. Chạy: python jupiter_notebook/tao_du_lieu.py (tải ~400MB, vài phút).
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "input" / "KLTN_Tong_hop_hoan_chinh.xlsx"
LINKS = ROOT / "data" / "input" / "bulk_files_Herfindahl-Hirschman_Market_Concentration_Index_Mirrored_Export.xlsx"
OUT = ROOT / "data" / "input" / "KLTN_du_lieu.xlsx"
NAM = range(2000, 2023)

# 1. HHI thị trường: dòng tổng cấp quốc gia (Partner = All, Product = Total) của từng năm
links = pd.read_excel(LINKS)
links = links[links.Path.str.contains("ed_hhpci_mrkt_")]
links = dict(zip(links.Path.str.extract(r"ed_hhpci_mrkt_(\d{4})_")[0].astype(int), links.Path))
hhi = []
for nam in NAM:
    d = pd.read_csv(links[nam], dtype={"Product": str})
    hhi.append(d[(d.Partner == "All") & (d.Product == "Total")][["ReporterISO3", "Year", "Indicator"]])
    print("HHI", nam, len(hhi[-1]), "nước")
hhi = (pd.concat(hhi).rename(columns={"ReporterISO3": "Code", "Indicator": "HHI"})
       .replace({"Code": {"ROM": "ROU", "ZAR": "COD"}}))  # WITS dùng mã ISO cũ của Romania, CHDC Congo

# 2. Ghép các biến của 128 nước theo Code-Year
nuoc = pd.read_excel(SRC, sheet_name="COUNTRY_REGION", usecols=["ID", "Country", "Code", "Region", "DEV"]).dropna(subset=["Code"])
df = nuoc.merge(pd.DataFrame({"Year": NAM}), how="cross")
lab = pd.read_excel(SRC, sheet_name="LAB_clean")
lab["LAB"] = (lab.LF_total / lab.LF_total_lag1 - 1) * 100  # sheet gốc là công thức, tính lại giá trị
nguon = {"GDPG_clean": ["GDPG"], "CAP_clean": ["CAP"], "FDI_clean": ["FDI"], "GOV_clean": ["GOV"],
         "THEIL_clean": ["THEIL", "THEIL_PROD"]}
for sheet, cols in nguon.items():
    df = df.merge(pd.read_excel(SRC, sheet_name=sheet)[["Code", "Year", *cols]], on=["Code", "Year"], how="left")
df = df.merge(lab[["Code", "Year", "LAB"]], on=["Code", "Year"], how="left").merge(hhi, on=["Code", "Year"], how="left")
df["GFC"] = df.Year.isin([2008, 2009]).astype(int)
df["COVID"] = df.Year.isin([2020, 2021]).astype(int)
df = df[["ID", "Country", "Code", "Year", "Region", "DEV", "GFC", "COVID",
         "GDPG", "HHI", "THEIL", "THEIL_PROD", "CAP", "FDI", "GOV", "LAB"]].sort_values(["ID", "Year"])

thieu = df.isna().sum()
assert len(df) == 128 * len(NAM) and not thieu.any(), f"Thiếu số liệu:\n{thieu[thieu > 0]}"

# 3. README
bien = [
    ("ID, Country, Code", "Mã thứ tự, tên nước, mã ISO3", "COUNTRY_REGION"),
    ("Region", "Khu vực và nhóm phát triển", "COUNTRY_REGION"),
    ("DEV", "1 = nước phát triển (37 nước), 0 = đang phát triển (91 nước)", "Đề cương; nước bổ sung tự phân loại"),
    ("GFC", "1 nếu năm 2008-2009", "Tính theo Year"),
    ("COVID", "1 nếu năm 2020-2021", "Tính theo Year"),
    ("GDPG", "Tăng trưởng GDP thực bình quân đầu người, %/năm", "WDI NY.GDP.PCAP.KD.ZG"),
    ("HHI", "Herfindahl-Hirschman tập trung thị trường xuất khẩu (0-1, càng cao càng tập trung vào ít đối tác)",
     "World Bank WITS, HH Market Concentration Index, Mirrored Export"),
    ("THEIL", "Chỉ số Theil tổng, luồng xuất khẩu", "UNCTAD series 1412"),
    ("THEIL_PROD", "Thành phần Theil theo sản phẩm, luồng xuất khẩu", "UNCTAD series 1413"),
    ("CAP", "Tích lũy vốn gộp, % GDP", "WDI NE.GDI.TOTL.ZS"),
    ("FDI", "FDI ròng đổ vào, % GDP", "WDI BX.KLT.DINV.WD.GD.ZS"),
    ("GOV", "Tiêu dùng cuối cùng của chính phủ, % GDP", "WDI NE.CON.GOVT.ZS"),
    ("LAB", "Tăng lực lượng lao động, %/năm = (LF_t / LF_t-1 - 1) x 100", "WDI SL.TLF.TOTL.IN"),
]
readme = pd.DataFrame(bien, columns=["Biến", "Mô tả", "Nguồn"])

with pd.ExcelWriter(OUT) as w:
    df.to_excel(w, sheet_name="DATA", index=False)
    pd.DataFrame({"Ghi chú": [
        f"Panel cân bằng {df.Code.nunique()} nước x {len(NAM)} năm (2000-2022) = {len(df)} quan sát, không thiếu ô nào, không nội suy.",
        "Dừng ở 2022 vì HHI thị trường (World Bank WITS) chỉ công bố đến 2022.",
        "HHI là dòng tổng cấp quốc gia (Partner = All, Product = Total). WITS ghi Romania là ROM, CHDC Congo là ZAR; đã đổi sang ROU, COD.",
        "Tạo bằng jupiter_notebook/tao_du_lieu.py từ KLTN_Tong_hop_hoan_chinh.xlsx (dữ liệu gốc WDI, UNCTAD) và file link HHI.",
    ]}).to_excel(w, sheet_name="README", index=False)
    readme.to_excel(w, sheet_name="README", index=False, startrow=7)
print(f"Đã lưu {len(df)} dòng vào {OUT}")
