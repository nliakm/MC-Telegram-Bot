#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import emoji
from kubernetes import client, config
from kubernetes.stream import stream

class TelegramBot:
    def __init__(self):
    	# login into kubernetes cluster
    	config.load_kube_config('/home/ansible/.kube/config')
    	self.v1 = client.CoreV1Api()
    	self.mc_namespace_pod = self.v1.list_namespaced_pod("minecraft")
    	self.name = self.mc_namespace_pod.items[0].metadata.name
    	self.namespace = "minecraft"
    	self.rcon_pw = "XXXXXXXXXX"

    # Enable logging
    #logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.INFO)
#----------------------------------------------------------------------
    def rescanNamespace(self):
        self.mc_namespace_pod = self.v1.list_namespaced_pod("minecraft")
        self.name = self.mc_namespace_pod.items[0].metadata.name 
#----------------------------------------------------------------------
    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi {}!\nBot zum verwalten des Minecraft Servers.\nSende /help für mehr Informationen.'.format(
            update.message.from_user.first_name))

#----------------------------------------------------------------------
    def help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('TG Bot v0.1\nFolgende Befehle implementiert \
                \n/server Infos zum Server \
                \n/restart Startet den Server neu \
                \n/say Nachricht \
                \n/msg Spielername Nachricht \
                \n/online')


#----------------------------------------------------------------------
    def server(self, update, context):
        """Give information about the server"""

        mc_version = ''
        difficulty = ''
        mc_server = 'XXXXXXXXXX:25565'
        mc_map = 'XXXXXXXXXX:32000'
        for i in self.mc_namespace_pod.items[0].spec.containers[0].env:
            if i.name == 'VERSION':
                mc_version = i.value
            if i.name == 'DIFFICULTY':
                difficulty = i.value
        update.message.reply_text('Server: ' + mc_server + '\nMap: ' + mc_map + '\nVersion: ' + mc_version + '\nSchwierigkeit: ' + difficulty)

#----------------------------------------------------------------------
    def recreate(self, update, context):
        """Delete the pod to force redeploy"""
        update.messge.reply_text('Server wird komplett neu erstellt und gestartet.')
        
#----------------------------------------------------------------------
    def say(self, update, context):
        """RCON say the user message."""
        update.message.reply_text('Sende Nachricht: ' + str(update.message.text).replace('/say', ''))
        msg_text = 'rcon-cli --password ' + self.rcon_pw + ' say ' + str(update.message.text).replace('/say', '')
        say_cmd = ['/bin/sh', '-c', msg_text ]
        say_exec = stream(self.v1.connect_get_namespaced_pod_exec,
                self.name, self.namespace, command=say_cmd,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False)

#----------------------------------------------------------------------
    def msg(self, update, context):
        """RCON say the user message."""
        update.message.reply_text('Sende Nachricht: ' + str(update.message.text).replace('/msg', ''))
        msg_text = 'rcon-cli --password ' + self.rcon_pw + ' msg ' + str(update.message.text).replace('/msg', '')
        msg_cmd = ['/bin/sh', '-c', msg_text ]
        say_exec = stream(self.v1.connect_get_namespaced_pod_exec,
                self.name, self.namespace, command=msg_cmd,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False)

#----------------------------------------------------------------------
    def online(self, update, context):
        """Show online players"""
        list_cmd = ['/bin/sh', '-c', 'rcon-cli --password ' + self.rcon_pw + ' list']
        online_exec = stream(self.v1.connect_post_namespaced_pod_exec,
                self.name, self.namespace,
		command=list_cmd,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False)
        update.message.reply_text(online_exec)

#----------------------------------------------------------------------
    def error(self, update, context):
        """Log Errors caused by Updates."""
        global logger
        logger.warning('Update "%s" caused error "%s"', update, error)

#----------------------------------------------------------------------
    def restart(self, update, context):
        """Restart the minecraft server."""
        update.message.reply_text('Server wird neugestartet...')
        restart_cmd = ['/bin/sh', '-c',  'rcon-cli --password ' + self.rcon_pw + ' restart']
        restart_exec = stream(self.v1.connect_get_namespaced_pod_exec,
		self.name, self.namespace, command=restart_cmd,
	        stderr=True,
        	stdin=False,
	        stdout=True,
	        tty=False)
        update.message.reply_text('Rückmeldung vom Server: {}', restart_exec)

#----------------------------------------------------------------------
    def main(self):
        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
        updater = Updater("XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("online", self.online))
        dp.add_handler(CommandHandler("restart", self.restart))
        dp.add_handler(CommandHandler("say", self.say))
        dp.add_handler(CommandHandler("msg", self.msg))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler("server", self.server))
        # on noncommand i.e message - echo the message on Telegram
        #dp.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


#----------------------------------------------------------------------
if __name__ == "__main__":
    tlgrmbt = TelegramBot()
    tlgrmbt.main()
