import os
os.environ['BRAPI_API_KEY'] = 'tky3Vocipoj9ZocxEumbCe'
os.environ['ELEVENLABS_API_KEY'] = 'sk_2e12b95dc92a231055f4e9d4f275ae9fab83940d59b26a3e'
os.environ['ELEVENLABS_VOICE_ID'] = '0r2zCQO0vO1jOfWbm7N7'
os.environ['HEYGEN_API_KEY'] = 'sk_V2_hgu_kkX2jmyuQzW_9R8ocwO4rBLzHX0mrIyQwKAJWLAGrJjW'
os.environ['HEYGEN_AVATAR_ID'] = '351538dd8eea417882a312681f2168d9'
os.environ['ZAPI_INSTANCE_ID'] = '3F11BDD3D23071C40CFC9EED2DF277BD'
os.environ['ZAPI_API_TOKEN'] = 'D06BC58B1E9B2833DB10EBF3'
os.environ['TELEGRAM_BOT_TOKEN'] = '8371953023:AAH8zJBO9hc0n_Z0x5D_f630piy31brCGXc'
os.environ['TELEGRAM_CHAT_ID'] = '7686120986'
os.environ['MANYCHAT_API_KEY'] = '11058963:93a19ff0c8e75129c2d9303960e974dd'

from orchestrator import NinePillaOrchestrator
orch = NinePillaOrchestrator()
result = orch.run_full_cycle()
import json
print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
