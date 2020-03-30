# MC-Telegram-Bot
Telegram-Bot zum Managen des Minecraft-Servers in Kubernetes. Läuft als systemd-Dienst

## Installation
1. Python-Pakete installieren
2. Skript anpassen (Telegram-Token und RCON Passwort anpassen)
3. Systemd-Dienst nach /etc/systemd/system/system/multi-user.target.wants/ kopieren
4. systemctl daemon-reload ausführen
5. Dienst starten

## Funktionen implementiert
/restart Startet den Server per rcon-cli command neu<br>
/say <Nachricht> Sendet Nachricht per RCON<br>
/msg <Spielername> <Nachricht> sendet Nachricht per RCON an gewünschten Spieler<br>
/online Gibt aus, welche Spieler online sind (nutzt rcon-cli list command)<br>

## ToDo
/recreate<br>
Command, der den Pod löscht, statt rcon-cli restart zu benutzen. Soll die seltenen Fälle abdecken, wenn der Pod bspw. im Crashloop ist.
