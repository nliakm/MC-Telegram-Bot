# MC-Telegram-Bot
Telegram-Bot zum Managen des Minecraft-Servers in Kubernetes. Läuft als systemd-Dienst

## Installation
1. Python-Pakete installieren
2. Skript anpassen (Telegram-Token und RCON Passwort anpassen)
3. Systemd-Dienst nach /etc/systemd/system/system/multi-user.target.wants/ kopieren
4. systemctl daemon-reload ausführen
5. Dienst starten
