import discord
from discord.ext import commands
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ─────────────────────────────────────────
#  CONFIG — remplace ces IDs par les tiens
# ─────────────────────────────────────────
PAIRS = [
    {
        "voice_id": 1216030475777216624,   # ID de ╰『🏕』évent
        "text_id":  1216030117470670958,   # ID de ╭『🎊』chat-évent
    },
    # Tu peux en ajouter d'autres ici :
    # {
    #     "voice_id": 111111111111111111,
    #     "text_id":  222222222222222222,
    # },
]
# ─────────────────────────────────────────

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ── Health server pour UptimeRobot / Railway ──
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"EventBot OK")

    def log_message(self, *args):
        pass  # silence les logs HTTP


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# ── Événements Discord ──
@bot.event
async def on_ready():
    print(f"✅ EventBot connecté en tant que {bot.user}")
    print(f"   {len(PAIRS)} paire(s) vocal/texte configurée(s)")


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    guild = member.guild

    for pair in PAIRS:
        voice_ch = guild.get_channel(pair["voice_id"])
        text_ch  = guild.get_channel(pair["text_id"])

        if voice_ch is None or text_ch is None:
            continue

        # Quelqu'un rejoint CE salon vocal
        if after.channel and after.channel.id == pair["voice_id"]:
            members_in_voice = len([m for m in voice_ch.members if not m.bot])
            if members_in_voice >= 1:
                await text_ch.set_permissions(guild.default_role, send_messages=True)
                print(f"🔓 #{text_ch.name} déverrouillé ({members_in_voice} personne(s) dans #{voice_ch.name})")

        # Quelqu'un quitte CE salon vocal
        elif before.channel and before.channel.id == pair["voice_id"]:
            members_in_voice = len([m for m in voice_ch.members if not m.bot])
            if members_in_voice == 0:
                await text_ch.set_permissions(guild.default_role, send_messages=False)
                print(f"🔒 #{text_ch.name} verrouillé (plus personne dans #{voice_ch.name})")


# ── Lancement ──
if __name__ == "__main__":
    # Démarre le health server en arrière-plan
    t = threading.Thread(target=run_health_server, daemon=True)
    t.start()

    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise ValueError("❌ Variable d'environnement DISCORD_TOKEN manquante")

    bot.run(token)
