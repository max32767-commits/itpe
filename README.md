# ITPE 반복암기

정보관리기술사 토픽 920개를 두음 플래시카드·4지선다로 반복 암기하는 앱. 단일 HTML + data.js, 진도는 브라우저(localStorage)에 저장.

- 앱: https://max32767-commits.github.io/itpe/
- 원본 데이터: Google 시트 '토픽정리3_노션' (노션 「셀테기반 토픽정리」와 동일)

## 데이터 갱신
시트 범위 `'토픽정리3_노션'!A1:F` 를 JSON(`{"values":[[...],...]}`)으로 받은 뒤:

```
python3 tools/build_data.py sheet_values.json > data.js
```
