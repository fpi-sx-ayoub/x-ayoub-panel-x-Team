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
user_sessions = {}  # {uid: expiry_time (datetime)}
loop = None  # will be set inside main()

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


# ============================================================
#                  LOW-LEVEL LOGIN / CRYPTO
# ============================================================
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
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
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
    timeout = aiohttp.ClientTimeout(total=20)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.read()
                return None
    except Exception:
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
    timeout = aiohttp.ClientTimeout(total=20)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=payload, headers=Hr_copy, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.read()
                return None
    except Exception:
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


# ============================================================
#                          BOT
# ============================================================
class Bot:
    """
    Persistent Free-Fire bot.

    Architecture (fixed):
      • supervisor()  : runs FOREVER. It restarts the login/connection whenever
                        the socket dies, no matter the reason. Never gives up.
      • spam_loop()   : runs FOREVER while the bot object exists. It only sends
                        invites when (a) socket is up AND (b) a spam_target exists
                        AND (c) that target's 30-minute session is still valid.
                        It NEVER exits on socket drop – it just waits and resumes.
    So calling /xAyOuB just sets spam_target + expiry and the loop takes care
    of the rest, including through unlimited disconnections.
    """

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
        self.spam_target = None    # current target uid (str) or None
        self.account_name = ""
        self.login_data = None
        self.payload = None
        self.open_id = None
        self.access_token = None
        self.room_opened = False
        self.total_sent = 0
        self.total_failed = 0
        self.last_send_ts = 0
        # Tasks
        self.supervisor_task = None
        self.spam_task = None
        self.read_task = None
        self.keep_alive_task = None
        # Event: set whenever we are fully connected and ready to send
        self.ready_event = asyncio.Event()
        self._lock = asyncio.Lock()

    # ---------------- LOGIN ----------------
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
                print(f"[{self.uid}] LOGIN OK  uid={self.tarGeT} region={self.region} name={self.account_name}")
                return True
            except Exception as e:
                print(f"[{self.uid}] Login attempt {attempt+1} error: {e}")
                await asyncio.sleep(1)
        return False

    async def refresh_auth(self):
        """Refresh MajorLogin (short) to get a new session-key without full oauth re-fetch."""
        try:
            if not self.payload:
                return await self.do_login()
            ml_response = await MajorLogin(self.payload)
            if not ml_response:
                # full re-login
                return await self.do_login()
            ml_auth = await DecRypTMajoRLoGin(ml_response)
            if not getattr(ml_auth, "token", None):
                return await self.do_login()
            self.tarGeT = ml_auth.account_uid or self.tarGeT
            self.token = ml_auth.token
            self.timestamp = ml_auth.timestamp
            self.key = ml_auth.key
            self.iv = ml_auth.iv
            self.region = getattr(ml_auth, "region", self.region)
            # refresh IP:port too when server gives one
            try:
                url = ml_auth.url
                login_data_enc = await GetLoginData(url, self.payload, self.token)
                if login_data_enc:
                    self.login_data = await DecRypTLoGinDaTa(login_data_enc)
                    self.online_ip, self.online_port = self.login_data.Online_IP_Port.split(":")
                    self.chat_ip, self.chat_port = self.login_data.AccountIP_Port.split(":")
                    self.account_name = getattr(self.login_data, "AccountName", self.account_name)
            except Exception:
                pass
            self.auth_token = await xAuThSTarTuP(int(self.tarGeT), self.token, int(self.timestamp), self.key, self.iv)
            return True
        except Exception as e:
            print(f"[{self.uid}] refresh_auth error: {e}")
            return await self.do_login()

    # ---------------- TCP ----------------
    async def connect_tcp(self):
        await self.disconnect_tcp()
        try:
            self.online_reader, self.online_writer = await asyncio.wait_for(
                asyncio.open_connection(self.online_ip, int(self.online_port)), timeout=15
            )
            self.online_writer.write(bytes.fromhex(self.auth_token))
            await self.online_writer.drain()
            print(f"[{self.uid}] Online connected {self.online_ip}:{self.online_port}")
            try:
                self.whisper_reader, self.whisper_writer = await asyncio.wait_for(
                    asyncio.open_connection(self.chat_ip, int(self.chat_port)), timeout=15
                )
                self.whisper_writer.write(bytes.fromhex(self.auth_token))
                await self.whisper_writer.drain()
                print(f"[{self.uid}] Chat connected {self.chat_ip}:{self.chat_port}")
            except Exception as e:
                print(f"[{self.uid}] Chat connection skipped: {e}")
                self.whisper_reader = None
                self.whisper_writer = None
            self.connected = True
            self.room_opened = False
            # Spawn per-connection helpers
            self.read_task = asyncio.create_task(self.read_loop())
            self.keep_alive_task = asyncio.create_task(self.keep_alive_loop())
            self.ready_event.set()
            return True
        except Exception as e:
            print(f"[{self.uid}] TCP connect failed: {e}")
            self.connected = False
            self.ready_event.clear()
            return False

    async def disconnect_tcp(self):
        self.connected = False
        self.room_opened = False
        self.ready_event.clear()
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
                    try:
                        await asyncio.wait_for(writer.wait_closed(), timeout=3)
                    except Exception:
                        pass
                except Exception:
                    pass
        self.online_writer = None
        self.online_reader = None
        self.whisper_writer = None
        self.whisper_reader = None
        await asyncio.sleep(0.05)

    async def read_loop(self):
        try:
            while self.connected:
                try:
                    data = await asyncio.wait_for(self.online_reader.read(8192), timeout=90)
                    if not data:
                        # peer closed
                        print(f"[{self.uid}] read: peer closed")
                        break
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"[{self.uid}] read error: {e}")
                    break
        except asyncio.CancelledError:
            pass
        finally:
            # Signal the supervisor: socket is dead.
            self.connected = False
            self.ready_event.clear()

    async def keep_alive_loop(self):
        try:
            while self.connected:
                try:
                    await asyncio.sleep(20)
                    if not self.connected or not self.online_writer:
                        break
                    ka_packet = await send_keep_alive(self.key, self.iv)
                    self.online_writer.write(ka_packet)
                    await self.online_writer.drain()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"[{self.uid}] keep-alive error: {e}")
                    self.connected = False
                    self.ready_event.clear()
                    break
        except asyncio.CancelledError:
            pass

    # ---------------- HIGH-LEVEL ----------------
    async def open_craftland_room(self):
        try:
            if not self.connected or not self.online_writer:
                return False
            packet = await create_craftland_room_latest(self.key, self.iv)
            self.online_writer.write(packet)
            await self.online_writer.drain()
            self.room_opened = True
            print(f"[{self.uid}] Craftland room opened")
            await asyncio.sleep(0.15)
            return True
        except Exception as e:
            print(f"[{self.uid}] open room error: {e}")
            self.room_opened = False
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
            self.connected = False
            self.ready_event.clear()
            return False

    # ---------------- SUPERVISOR ----------------
    async def supervisor(self):
        """
        FOREVER loop that keeps this bot logged in and TCP-connected.
        If the socket ever dies (peer close, keep-alive fail, send fail, timeout)
        it immediately re-logs in and reconnects. Never gives up.
        The spam loop is running independently and will resume as soon as
        `ready_event` is set again.
        """
        backoff = 1.0
        while True:
            try:
                # 1) Make sure we have a valid auth
                if not self.auth_token:
                    ok = await self.do_login()
                else:
                    ok = await self.refresh_auth()
                if not ok:
                    await asyncio.sleep(min(backoff, 5))
                    backoff = min(backoff * 1.5, 5)
                    continue

                # 2) Open TCP
                ok = await self.connect_tcp()
                if not ok:
                    await asyncio.sleep(min(backoff, 5))
                    backoff = min(backoff * 1.5, 5)
                    continue

                # 3) Open craftland room once (best-effort)
                try:
                    await self.open_craftland_room()
                except Exception:
                    pass

                backoff = 1.0  # reset

                # 4) Sit here as long as we stay connected
                while self.connected:
                    await asyncio.sleep(1)

                # If we exit the inner while, socket died. Loop reconnects.
                print(f"[{self.uid}] supervisor: socket lost, reconnecting immediately...")
                await self.disconnect_tcp()
                await asyncio.sleep(0.3)

            except asyncio.CancelledError:
                print(f"[{self.uid}] supervisor cancelled")
                await self.disconnect_tcp()
                return
            except Exception as e:
                print(f"[{self.uid}] supervisor error: {e}")
                traceback.print_exc()
                await asyncio.sleep(1)

    # ---------------- SPAM ----------------
    async def spam_loop_forever(self):
        """
        FOREVER loop for the whole life of this bot.
        Sends invites whenever:
          - self.spam_target is set
          - user_sessions[spam_target] is in the future
          - self.connected is True
        Otherwise, it just waits (never exits). This guarantees that:
          1. A /xAyOuB call causes continuous spam for 30 minutes.
          2. If the socket drops mid-session, the loop pauses briefly
             and RESUMES automatically once the supervisor reconnects.
          3. When the 30 minute window ends, sending stops – but the loop
             stays alive, ready for the NEXT /xAyOuB call.
        """
        print(f"[{self.uid}] spam_loop_forever started (idle, waiting for target)")
        while True:
            try:
                target = self.spam_target
                if not target:
                    await asyncio.sleep(0.5)
                    continue
                expiry = user_sessions.get(target)
                if not expiry or datetime.now() >= expiry:
                    # session ended; clear target so we don't spin
                    if self.spam_target == target:
                        self.spam_target = None
                    await asyncio.sleep(0.5)
                    continue

                # Wait for a ready connection (never exit)
                if not self.connected or not self.online_writer:
                    try:
                        await asyncio.wait_for(self.ready_event.wait(), timeout=2)
                    except asyncio.TimeoutError:
                        continue

                # Ensure the craftland room is open
                if not self.room_opened:
                    try:
                        await self.open_craftland_room()
                    except Exception:
                        pass

                # Fast batch send
                batch_ok = 0
                for _ in range(20):
                    if self.spam_target != target:
                        break
                    exp2 = user_sessions.get(target)
                    if not exp2 or datetime.now() >= exp2:
                        break
                    if not self.connected or not self.online_writer:
                        break
                    ok = await self.send_invite(target)
                    if ok:
                        self.total_sent += 1
                        batch_ok += 1
                        self.last_send_ts = time.time()
                    else:
                        self.total_failed += 1
                        break
                    await asyncio.sleep(0.005)

                if batch_ok == 0:
                    # small backoff while disconnected / server rate-limits
                    await asyncio.sleep(0.2)
                else:
                    await asyncio.sleep(0.03)

            except asyncio.CancelledError:
                print(f"[{self.uid}] spam_loop_forever cancelled")
                return
            except Exception as e:
                print(f"[{self.uid}] spam_loop_forever error: {e}")
                await asyncio.sleep(0.5)


# ============================================================
#                        FLASK API
# ============================================================
@app.route("/", methods=["GET"])
def root_endpoint():
    return jsonify({"status": "active", "api_name": "x-ayoub-panel-x-Team"}), 200


@app.route("/ping", methods=["GET"])
def ping_endpoint():
    return jsonify({"status": "alive", "ts": datetime.now().isoformat()}), 200


@app.route("/x-ayoub-panel-x-Team", methods=["GET"])
def x_ayoub_panel_x_Team_endpoint():
    return jsonify({"status": "active", "api_name": "x-ayoub-panel-x-Team"}), 200


@app.route("/xAyOuB", methods=["GET"])
def x_ayoub_endpoint():
    target_uid = request.args.get("uid")
    if not target_uid:
        return jsonify({"status": "error", "message": "Missing uid parameter"}), 400

    # Set/refresh 30 minutes session
    user_sessions[target_uid] = datetime.now() + timedelta(minutes=30)

    online_bots = [b for b in bots.values() if b.connected]

    # Assign target to ALL bots (both connected and reconnecting).
    # Their spam_loop_forever will pick it up whenever their socket comes back.
    for bot in bots.values():
        bot.spam_target = target_uid

    return jsonify({
        "status": "ok",
        "message": "Started for 30 minutes (bots will send continuously; auto-reconnect if disconnected)",
        "target_uid": target_uid,
        "total_bots": len(bots),
        "online_bots": len(online_bots),
        "session_expires": user_sessions[target_uid].isoformat()
    }), 200


@app.route("/xSToP", methods=["GET"])
def x_stop_endpoint():
    target_uid = request.args.get("uid")
    if target_uid in user_sessions:
        del user_sessions[target_uid]
    for bot in bots.values():
        if bot.spam_target == target_uid:
            bot.spam_target = None
    return jsonify({"status": "ok", "message": f"Stopped for {target_uid}"}), 200


@app.route("/status", methods=["GET"])
def status_endpoint():
    now = datetime.now()
    sessions = {k: {"expires": v.isoformat(), "remaining_seconds": max(0, int((v - now).total_seconds()))}
                for k, v in user_sessions.items()}
    result = {"sessions": sessions, "bots": {}}
    for uid, bot in bots.items():
        result["bots"][uid] = {
            "connected": bot.connected,
            "target": bot.spam_target,
            "name": bot.account_name,
            "sent": bot.total_sent,
            "failed": bot.total_failed,
            "last_send_ago_s": (int(time.time() - bot.last_send_ts) if bot.last_send_ts else None),
        }
    return jsonify(result), 200


# ============================================================
#                     ORCHESTRATION
# ============================================================
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


def run_flask():
    from werkzeug.serving import make_server
    port = int(os.environ.get("PORT", 5000))
    srv = make_server("0.0.0.0", port, app, threaded=True)
    print(f"Flask API running on port {port}")
    srv.serve_forever()


def keep_alive_worker():
    """Self-ping every 50 seconds to prevent Render free tier from sleeping."""
    import requests as _rq
    time.sleep(15)
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

    # Start Flask + self-ping ASAP so Render sees the port bound quickly
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    Thread(target=keep_alive_worker, daemon=True).start()

    accounts = await load_accs("accs.txt")
    if not accounts:
        print("No accounts found in accs.txt, staying alive as web service.")
        while True:
            await asyncio.sleep(3600)
        return

    # Instantiate bots and start their supervisor + spam loops
    for uid, password in accounts:
        bot = Bot(uid, password)
        bots[uid] = bot
        # The supervisor keeps the bot logged-in & connected FOREVER
        bot.supervisor_task = asyncio.create_task(bot.supervisor())
        # The spam loop runs FOREVER too, but only actually sends when
        # spam_target + valid session + connected.
        bot.spam_task = asyncio.create_task(bot.spam_loop_forever())

    print(f"Launched {len(bots)} bots with permanent supervisors + spam loops.")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
