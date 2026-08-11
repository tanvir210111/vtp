import os
import sys
import pathlib
sys.path.insert(0, r'd:\Office Work\vtp\vtp\ai-engine')
sys.path.insert(0, r'd:\Office Work\vtp\vtp\backend')
from google import genai

env_path = pathlib.Path(r'd:\Office Work\vtp\vtp\backend\.env')
key = ''
for line in env_path.read_text(encoding='utf-8').splitlines():
    if line.startswith('GEMINI_API_KEY='):
        key = line.split('=', 1)[1].strip()
        break

print('KEY_PRESENT', bool(key))
client = genai.Client(api_key=key)
print('CLIENT_OK')
try:
    models = list(client.models.list())
    print('MODEL_COUNT', len(models))
    for model in models[:50]:
        name = getattr(model, 'name', None)
        display = getattr(model, 'display_name', None)
        supported = getattr(model, 'supported_actions', None)
        print(name, '|', display, '|', supported)
except Exception as e:
    import traceback
    print(type(e).__name__, e)
    traceback.print_exc()

for model_name in ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-2.0-flash-lite', 'gemini-2.0-flash-thinking-exp', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-001', 'gemini-2.0-flash-preview-image-generation']:
    try:
        resp = client.models.generate_content(model=model_name, contents='hi')
        print('MODEL', model_name, 'OK', getattr(resp, 'text', None))
    except Exception as e:
        print('MODEL', model_name, 'ERR', type(e).__name__, e)
