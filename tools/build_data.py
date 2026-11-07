"""시트 '토픽정리3_노션' 내보내기(JSON: {values:[[분류,토픽,두음,내용,인사이트,정렬키],...]})를 data.js로 변환.
사용: python3 tools/build_data.py <sheet_values.json> > data.js
"""
import json, re, sys

def parse(rows):
    items = []
    for r in rows[1:]:
        r = list(r) + [''] * (6 - len(r))
        g, t, du, body, ins, key = r[:6]
        if not t.strip():
            continue
        m = re.match(r'\s*"(.*?)"\s*(?:\n|$)', body, re.S)
        defn = m.group(1).strip() if m else ''
        rest = body[m.end():] if m else body
        lines = []
        for ln in rest.split('\n'):
            ln = ln.strip()
            mm = re.match(r'\[(.+?)\]\s*(.*)$', ln)
            if not mm:
                continue
            k, v = mm.group(1), mm.group(2)
            ds = re.findall(r'\(\*([^()]+?)\)', v)
            v = re.sub(r'\s*\(\*[^()]+?\)', '', v).strip()
            lines.append({'k': k, 'v': v, 'd': ' / '.join(ds)})
        try:
            key = int(str(key).strip())
        except ValueError:
            key = 0
        major = key // 1000; minor = key % 1000
        no = f'{major}' if minor == 0 else f'{major}-{minor}'
        items.append({
            'id': key, 'no': no, 'g': g.strip(), 't': t.strip(),
            'du': [x.strip() for x in du.split('\n') if x.strip()],
            'def': defn,
            'lines': lines,
            'ins': [x.strip() for x in ins.split('\n') if x.strip()],
        })
    # 같은 대분류 번호 안에서 분류명이 섞여 있으면 다수 표기로 통일
    from collections import Counter, defaultdict
    cnt = defaultdict(Counter)
    for it in items:
        cnt[it['id'] // 1000][it['g']] += 1
    for it in items:
        it['g'] = cnt[it['id'] // 1000].most_common(1)[0][0]
    items.sort(key=lambda x: x['id'])
    return items

if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    items = parse(d['values'])
    groups = []
    for it in items:
        if it['g'] not in groups:
            groups.append(it['g'])
    out = 'window.ITPE_GROUPS=' + json.dumps(groups, ensure_ascii=False) + ';\n'
    out += 'window.ITPE_TOPICS=' + json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ';\n'
    sys.stdout.write(out)
    sys.stderr.write(f'{len(items)} topics, {len(groups)} groups\n')
