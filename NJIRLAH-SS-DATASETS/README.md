# NJIRLAH-SS Dataset Collection

## 🚀 Quick Start
```bash
# Validasi semua dataset
python scripts/validator.py

# Generate statistik
python scripts/compute_stats.py

# Cek duplikasi
python scripts/dedup_check.py
```

## 📊 Dataset Summary
- **Total Records:** 11,400+
- **Domains:** 24
- **Format:** JSONL
- **Quality Score:** 0.94 avg

## 🔧 Maintenance
### Menambahkan Dataset Baru
1. Buat file `gen_dataset_XX.py` di `scripts/`
2. Gunakan template dari dataset existing
3. Jalankan validator sebelum merge

### Update Dataset
1. Edit file di `raw/`
2. Jalankan `python scripts/validator.py`
3. Pindahkan ke `final/` jika valid

## 📈 Benchmark Alignment
| Dataset | Primary Benchmark | Secondary Benchmark |
|---------|-------------------|---------------------|
| 1-3     | MMLU, GPQA        | -                   |
| 4       | BrowseComp        | MMLU                |
| 5       | MCP-Atlas         | OSWorld             |
| 6       | Finance-Agent     | -                   |
| 7       | CharXiv-R         | -                   |
| 8       | Humanities-Last-Exam | MMLU            |
| 9       | BrowseComp        | -                   |

## 🛡️ Quality Control
- Minimal quality score: 0.90
- Duplikasi: 0% toleransi
- Validasi otomatis via `scripts/validator.py`

## 📝 Documentation
- `dataset-card.md` - Detail lengkap
- `CHANGELOG.md` - Riwayat perubahan
- `CONTRIBUTING.md` - Panduan kontribusi
