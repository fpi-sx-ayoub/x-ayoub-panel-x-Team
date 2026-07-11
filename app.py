import os, sys, json, time, ssl, asyncio, aiohttp, traceback, uuid, random
from datetime import datetime, timedelta
from threading import Thread
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, jsonify
from xC4 import *
from xHeaders import *
from byte import Encrypt_ID, encrypt_api
from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2

app = Flask(__name__)
bots = {}
user_sessions = {} # {uid: expiry_time}

Hr = {
    "User-Agent": "fadai/1.0 (Linux; Android 13; SM-S918B Build/TP1A.220.624.014)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54"
}

RIZERx = "1.126.9"

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "fadai/1.0 (Linux; Android 13; SM-S918B Build/TP1A.220.624.014)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("open_id"), data.get("access_token")
                elif response.status == 429:
                    return "429", "429"
    except Exception:
        pass
    return None, None

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = RIZERx
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_operator_a = "Verizon"
    major_login.network_type = "WIFI"
    major_login.network_type_a = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.unique_device_id = f"Google|{uuid.uuid4()}"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.login_open_id_type = 4
    major_login.access_token = access_token
    major_login.login_by = 3
    major_login.platform_sdk_id = 2
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.external_storage_total = 128512
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = 110731
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_total = 26628
    major_login.game_disk_storage_available = random.randint(18000, 25000)
    major_login.external_sdcard_total_storage = 119234
    major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.library_token = "hash|base.apk"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.supported_astc_bitset = 16383
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.channel_type = 3
    major_login.reg_avatar = 1
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.android_engine_init_flag = 110009
    string = major_login.SerializeToString()
    return await Encrypt_Proto(string)

async def Encrypt_Proto(payload):
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(payload, AES.block_size)
    return cipher.encrypt(padded)

async def MajorLogin(payload):
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr_copy = Hr.copy()
    Hr_copy["Authorization"] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr_copy, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = "0000000"
    elif uid_length == 8: headers = "00000000"
    elif uid_length == 10: headers = "000000"
    elif uid_length == 7: headers = "000000000"
    else: headers = "0000000"
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def create_craftland_room_latest(key, iv):
    fields = {
        1: 2,
        2: {
            1: 10, 2: 53, 3: 2, 4: "[B][C][FF0000]RIZER", 5: "777", 6: 6, 7: 10, 8: 1, 9: 8, 11: 1,
            14: 134217728,
            15: {1: "IDC4", 2: 282, 3: "ME"},
            16: "\u0001\u0007\t\n\u000b\u0012\u0019 '",
            27: 1,
            31: "651C8B8671A6A8360CCACEE764A3CCE64204",
            32: 1780933561, 33: 8,
            34: "\u0000\u0001", 35: 6, 40: "fr",
            42: "\n\u0010Craftland_Search\u0012/#FREEFIRE651C8B8671A6A8360CCACEE764A3CCE64204/1",
            46: 80, 49: "\b\u0015"
        }
    }
    proto_hex = (await CrEaTe_ProTo(fields)).hex()
    return await GeneRaTePk(proto_hex, "0E15", key, iv)

async def create_invite_packet(target_uid, key, iv):
    fields = {1: 22, 2: {1: int(target_uid)}}
    proto_hex = (await CrEaTe_ProTo(fields)).hex()
    return await GeneRaTePk(proto_hex, "0E15", key, iv)

async def send_keep_alive(key, iv):
    fields = {1: 99, 2: {1: int(time.time()), 2: 1}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), "0515", key, iv)

class Bot:
    def __init__(self, uid, password):
        self.uid = uid
        self.password = password
        self.online_writer = None
        self.online_reader = None
        self.whisper_writer = None
        self.whisper_reader = None
        self.key = None
        self.iv = None
        self.tarGeT = None
        self.token = None
        self.timestamp = None
        self.auth_token = None
        self.region = "BD"
        self.online_ip = None
        self.online_port = None
        self.chat_ip = None
        self.chat_port = None
        self.account_name = ""
        self.connected = False
        self.spamming = False
        self.spam_target = None
        self.spam_count = 10
        self.keep_alive_task = None
        self.read_task = None
        self.login_data = None
        self.payload = None
        self.open_id = None
        self.access_token = None
        self.room_opened = False
        self._lock = asyncio.Lock()

    async def do_login(self):
        for attempt in range(5):
            try:
                self.open_id, self.access_token = await GeNeRaTeAccEss(self.uid, self.password)
                if self.open_id == "429" or self.access_token == "429":
                    await asyncio.sleep(0.5)
                    continue
                if not self.open_id or not self.access_token:
                    await asyncio.sleep(1)
                    continue
                self.payload = await EncRypTMajoRLoGin(self.open_id, self.access_token)
                ml_response = await MajorLogin(self.payload)
                if not ml_response:
                    await asyncio.sleep(1)
                    continue
                ml_auth = await DecRypTMajoRLoGin(ml_response)
                self.tarGeT = ml_auth.account_uid
                self.token = ml_auth.token
                if not self.token:
                    await asyncio.sleep(1)
                    continue
                self.region = getattr(ml_auth, "region", "BD")
                url = ml_auth.url
                self.key = ml_auth.key
                self.iv = ml_auth.iv
                self.timestamp = ml_auth.timestamp
                login_data_enc = await GetLoginData(url, self.payload, self.token)
                if not login_data_enc:
                    await asyncio.sleep(1)
                    continue
                self.login_data = await DecRypTLoGinDaTa(login_data_enc)
                self.online_ip, self.online_port = self.login_data.Online_IP_Port.split(":")
                self.chat_ip, self.chat_port = self.login_data.AccountIP_Port.split(":")
                self.account_name = getattr(self.login_data, "AccountName", "Bot")
                self.auth_token = await xAuThSTarTuP(int(self.tarGeT), self.token, int(self.timestamp), self.key, self.iv)
                print(f"Bot {self.uid}: Login OK | UID={self.tarGeT} | Region={self.region} | Name={self.account_name}")
                return True
            except Exception as e:
                print(f"Bot {self.uid}: Login attempt {attempt+1} error: {e}")
                await asyncio.sleep(1)
        return False

    async def reconnect_auth(self):
        try:
            if not self.payload:
                return await self.do_login()
            ml_response = await MajorLogin(self.payload)
            if not ml_response:
                self.open_id, self.access_token = await GeNeRaTeAccEss(self.uid, self.password)
                if not self.open_id or not self.access_token:
                    return False
                self.payload = await EncRypTMajoRLoGin(self.open_id, self.access_token)
                ml_response = await MajorLogin(self.payload)
                if not ml_response:
                    return False
                ml_auth = await DecRypTMajoRLoGin(ml_response)
                self.tarGeT = ml_auth.account_uid
                self.token = ml_auth.token
                self.region = getattr(ml_auth, "region", "BD")
                url = ml_auth.url
                self.key = ml_auth.key
                self.iv = ml_auth.iv
                self.timestamp = ml_auth.timestamp
                login_data_enc = await GetLoginData(url, self.payload, self.token)
                if not login_data_enc:
                    return False
                self.login_data = await DecRypTLoGinDaTa(login_data_enc)
                self.online_ip, self.online_port = self.login_data.Online_IP_Port.split(":")
                self.chat_ip, self.chat_port = self.login_data.AccountIP_Port.split(":")
                self.account_name = getattr(self.login_data, "AccountName", "Bot")
                self.auth_token = await xAuThSTarTuP(int(self.tarGeT), self.token, int(self.timestamp), self.key, self.iv)
            else:
                ml_auth = await DecRypTMajoRLoGin(ml_response)
                self.token = ml_auth.token
                self.timestamp = ml_auth.timestamp
                self.key = ml_auth.key
                self.iv = ml_auth.iv
                self.auth_token = await xAuThSTarTuP(int(self.tarGeT), self.token, int(self.timestamp), self.key, self.iv)
            return True
        except Exception as e:
            print(f"Bot {self.uid}: Reconnect auth error: {e}")
            return False

    async def connect_tcp(self):
        await self.disconnect_tcp()
        for attempt in range(10):
            try:
                self.online_reader, self.online_writer = await asyncio.wait_for(
                    asyncio.open_connection(self.online_ip, int(self.online_port)), timeout=15
                )
                self.online_writer.write(bytes.fromhex(self.auth_token))
                await self.online_writer.drain()
                print(f"Bot {self.uid}: Online connected to {self.online_ip}:{self.online_port}")
                try:
                    self.whisper_reader, self.whisper_writer = await asyncio.wait_for(
                        asyncio.open_connection(self.chat_ip, int(self.chat_port)), timeout=15
                    )
                    self.whisper_writer.write(bytes.fromhex(self.auth_token))
                    await self.whisper_writer.drain()
                    print(f"Bot {self.uid}: Chat connected to {self.chat_ip}:{self.chat_port}")
                except Exception as e:
                    print(f"Bot {self.uid}: Chat connection skipped: {e}")
                    self.whisper_reader = None
                    self.whisper_writer = None
                self.connected = True
                self.read_task = asyncio.create_task(self.read_loop())
                self.keep_alive_task = asyncio.create_task(self.keep_alive_loop())
                return True
            except Exception as e:
                print(f"Bot {self.uid}: TCP connect attempt {attempt+1} failed: {e}")
                await asyncio.sleep(0.5)
        return False

    async def disconnect_tcp(self):
        self.connected = False
        for task_attr in ["read_task", "keep_alive_task"]:
            task = getattr(self, task_attr, None)
            if task and not task.done():
                try:
                    task.cancel()
                except Exception:
                    pass
        for writer_attr in ["online_writer", "whisper_writer"]:
            writer = getattr(self, writer_attr, None)
            if writer:
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass
        self.online_writer = None
        self.online_reader = None
        self.whisper_writer = None
        self.whisper_reader = None
        await asyncio.sleep(0.1)

    async def read_loop(self):
        try:
            while self.connected:
                try:
                    data = await asyncio.wait_for(self.online_reader.read(8192), timeout=60)
                    if not data:
                        print(f"Bot {self.uid}: Connection closed by server (read 0)")
                        asyncio.create_task(self.handle_disconnect())
                        break
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    if self.connected:
                        print(f"Bot {self.uid}: Read error: {e}")
                        asyncio.create_task(self.handle_disconnect())
                    break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if self.connected:
                print(f"Bot {self.uid}: Read loop error: {e}")
                asyncio.create_task(self.handle_disconnect())

    async def keep_alive_loop(self):
        try:
            while self.connected:
                try:
                    await asyncio.sleep(25)
                    if not self.connected:
                        break
                    ka_packet = await send_keep_alive(self.key, self.iv)
                    if self.online_writer and self.connected:
                        self.online_writer.write(ka_packet)
                        await self.online_writer.drain()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    if self.connected:
                        print(f"Bot {self.uid}: Keep-alive error: {e}")
        except asyncio.CancelledError:
            pass

    async def handle_disconnect(self):
        async with self._lock:
            if not self.connected:
                return
            self.connected = False
            print(f"Bot {self.uid}: Handling disconnect, reconnecting...")
            await self.disconnect_tcp()
            await asyncio.sleep(0.5)
            for attempt in range(20):
                try:
                    if not self.auth_token:
                        ok = await self.do_login()
                        if not ok:
                            await asyncio.sleep(1)
                            continue
                    ok = await self.reconnect_auth()
                    if not ok:
                        ok = await self.do_login()
                        if not ok:
                            await asyncio.sleep(1)
                            continue
                    ok = await self.connect_tcp()
                    if ok:
                        print(f"Bot {self.uid}: Reconnected successfully")
                        await self.open_craftland_room()
                        if self.spam_target:
                            self.spamming = True
                            asyncio.create_task(self.spam_loop())
                        return
                except Exception as e:
                    print(f"Bot {self.uid}: Reconnect attempt {attempt+1} error: {e}")
                await asyncio.sleep(1)
            print(f"Bot {self.uid}: Failed to reconnect after 20 attempts")

    async def open_craftland_room(self):
        try:
            if not self.connected or not self.online_writer:
                return False
            packet = await create_craftland_room_latest(self.key, self.iv)
            self.online_writer.write(packet)
            await self.online_writer.drain()
            self.room_opened = True
            print(f"Bot {self.uid}: Craftland room opened")
            await asyncio.sleep(0.1)
            return True
        except Exception as e:
            print(f"Bot {self.uid}: Error opening room: {e}")
            return False

    async def send_invite(self, target_uid):
        try:
            if not self.connected or not self.online_writer:
                return False
            packet = await create_invite_packet(int(target_uid), self.key, self.iv)
            self.online_writer.write(packet)
            await self.online_writer.drain()
            return True
        except Exception:
            return False

    async def spam_loop(self):
        self.spamming = True
        sent = 0
        try:
            if not getattr(self, "room_opened", False):
                await self.open_craftland_room()
            while self.spamming and self.spam_target:
                # Check session validity
                expiry = user_sessions.get(self.spam_target)
                if not expiry or datetime.now() > expiry:
                    print(f"Session for {self.spam_target} expired or not found.")
                    break

                if not self.connected:
                    await asyncio.sleep(0.1)
                    continue
                
                # Optimized sending: faster batching
                for _ in range(20):
                    if not self.spamming or not self.connected:
                        break
                    ok = await self.send_invite(self.spam_target)
                    if ok:
                        sent += 1
                    # Minimal sleep for continuous flow
                    await asyncio.sleep(0.005)
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Bot {self.uid}: Spam loop error: {e}")
        self.spamming = False
        print(f"Bot {self.uid}: Spam stopped for {self.spam_target}, total sent: {sent}")

@app.route("/", methods=["GET"])
def root_endpoint():
    return jsonify({"status": "active", "api_name": "x-ayoub-panel-x-Team"}), 200

@app.route("/ping", methods=["GET"])
def ping_endpoint():
    return jsonify({"status": "alive", "ts": datetime.now().isoformat()}), 200

@app.route("/x-ayoub-panel-x-Team", methods=["GET"])
def x_ayoub_panel_x_Team_endpoint():
    # Placeholder for general info or status
    return jsonify({"status": "active", "api_name": "x-ayoub-panel-x-Team"}), 200

@app.route("/xAyOuB", methods=["GET"])
def x_ayoub_endpoint():
    global loop
    target_uid = request.args.get("uid")
    if not target_uid:
        return jsonify({"status": "error", "message": "Missing uid parameter"}), 400
    
    # Set 30 minutes session
    user_sessions[target_uid] = datetime.now() + timedelta(minutes=30)
    
    online_bots = [b for b in bots.values() if b.connected]
    if not online_bots:
        return jsonify({"status": "error", "message": "No bots online"}), 503
    
    for bot in bots.values():
        bot.spam_target = target_uid
        if not bot.spamming and bot.connected:
            bot.spamming = True
            asyncio.run_coroutine_threadsafe(bot.spam_loop(), loop)
            
    return jsonify({
        "status": "ok",
        "message": "Started for 30 minutes",
        "target_uid": target_uid,
        "online_bots": len(online_bots)
    }), 200

@app.route("/xSToP", methods=["GET"])
def x_stop_endpoint():
    target_uid = request.args.get("uid")
    if target_uid in user_sessions:
        del user_sessions[target_uid]
    
    for bot in bots.values():
        if bot.spam_target == target_uid:
            bot.spamming = False
            
    return jsonify({"status": "ok", "message": f"Stopped for {target_uid}"}), 200

@app.route("/status", methods=["GET"])
def status_endpoint():
    result = {}
    for uid, bot in bots.items():
        result[uid] = {
            "connected": bot.connected,
            "spamming": bot.spamming,
            "target": bot.spam_target,
            "name": bot.account_name
        }
    return jsonify(result), 200

async def load_accs(filename="accs.txt"):
    accounts = []
    try:
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                parts = line.split(":", 1)
                if len(parts) == 2:
                    uid = parts[0].strip()
                    password = parts[1].strip()
                    if uid and password:
                        accounts.append((uid, password))
    except Exception as e:
        print(f"Error loading accs.txt: {e}")
    return accounts

async def start_bot(bot):
    try:
        print(f"Starting bot {bot.uid}")
        ok = await bot.do_login()
        if not ok:
            return False
        ok = await bot.connect_tcp()
        if not ok:
            return False
        await asyncio.sleep(0.1)
        await bot.open_craftland_room()
        return True
    except Exception as e:
        print(f"Bot {bot.uid}: Start error: {e}")
        return False

async def ensure_all_bots_online():
    while True:
        offline_bots = [bot for bot in bots.values() if not bot.connected]
        if not offline_bots:
            break
        tasks = [start_bot(bot) for bot in offline_bots]
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(10)

def run_flask():
    from werkzeug.serving import make_server
    port = int(os.environ.get("PORT", 5000))
    srv = make_server("0.0.0.0", port, app, threaded=True)
    print(f"Flask API running on port {port}")
    srv.serve_forever()

def keep_alive_worker():
    """Self-ping every 50 seconds to prevent Render free tier from sleeping."""
    import requests as _rq
    time.sleep(15)  # wait for server to boot
    port = int(os.environ.get("PORT", 5000))
    external_url = os.environ.get("RENDER_EXTERNAL_URL", f"http://127.0.0.1:{port}")
    ping_url = external_url.rstrip("/") + "/ping"
    while True:
        try:
            r = _rq.get(ping_url, timeout=10)
            print(f"[keep-alive] {ping_url} -> {r.status_code}")
        except Exception as e:
            print(f"[keep-alive] error: {e}")
        time.sleep(50)

async def main():
    global loop
    loop = asyncio.get_running_loop()
    accounts = await load_accs("accs.txt")
    if not accounts:
        print("No accounts found")
        # still start flask so the web service stays alive on Render
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        Thread(target=keep_alive_worker, daemon=True).start()
        while True:
            await asyncio.sleep(3600)
        return
    for uid, password in accounts:
        bot = Bot(uid, password)
        bots[uid] = bot

    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    Thread(target=keep_alive_worker, daemon=True).start()
    
    await ensure_all_bots_online()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
