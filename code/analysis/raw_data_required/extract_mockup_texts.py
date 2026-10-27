"""Extracts the texts shown in the chat mock-ups (after shortening and redaction) into JSON.
Run: python -X utf8 extract_mockup_texts.py -> examples/mockup_texts_en.json (needs the raw response log, not published)."""
import os, re, json, runpy, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make_chat_examples.py'), encoding='utf-8').read()
# run only the definitions (before the generation loop), without starting the browser
cut = src.index('made = []')
g = {'__file__': os.path.join(HERE, 'make_chat_examples.py'), '__name__': 'mockups'}
exec(compile(src[:cut], 'make_chat_examples.py', 'exec'), g)
PAIRS = {'1.3': g['MODELS'], '3.1': g['MODELS'], '6.4': g['MODELS'], '8.2': ['GPT-5.6 Sol', 'Claude Opus 5']}
out = {'requests': {}, 'cuts': {}, 'texts': {}}
for sid, ms in PAIRS.items():
    out['requests'][sid] = g['SC'][sid]['text']
    for m in ms:
        r, t, omitted = g['prepare'](sid, m)
        shown = t if omitted else g['truncate'](t)
        out['texts'][f'{sid}|{m}'] = shown
        if omitted:
            out['cuts'][f'{sid}|{m}'] = omitted
os.makedirs(os.path.join(HERE, 'examples'), exist_ok=True)
json.dump(out, open(os.path.join(HERE, 'examples', 'mockup_texts_en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out['texts']), 'texts;', sum(len(v) for v in out['texts'].values()), 'chars;', len(out['cuts']), 'cuts')
