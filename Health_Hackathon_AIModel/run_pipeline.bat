@echo off
python src/01_clean_text.py
python src/02_extract_signals.py
python src/03_build_city_day_features.py
python src/04_outbreak_zscore.py
python src/05_outbreak_report.py
python src/08_export_map_data.py
python src/09_build_explanations_json.py
echo Pipeline finished!
pause
