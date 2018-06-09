# James Tate - https://github.com/james-tate/
# hwreblog.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import obspython as obs
import urllib.request
import urllib.error
import socket, string
import datetime
import time

source_name = ""
readbuffer = "".encode()
MODT = False
s = socket.socket()
# this gets all the scenes and puts in list
# when switching to another scene call obs.obs_frontend_set_current_scene(scenes[!scene number in list!]) 
scenes = obs.obs_frontend_get_scenes()

# ------------------------------------------------------------

# sends a message to the channel
# example "PRIVMSG #ninjahipst3r :"
def Send_message(message):
    s.send("PRIVMSG #"your_channel_name" :".encode() + message.encode() + "\r\n".encode())

def send_help():
	Send_message("Welcome to the stream! type !help for commands!")

def update_text():
	global source_name
	global readbuffer
	global MODT
	global sock_close

	recieve = "".encode()

	try:
		recieve = s.recv(1024)
		# uncomment if you want to see the recieved message
		# print(recieve)
	except:
		# I don't handle this, but you can if needed
		pass

	readbuffer = readbuffer + recieve
	temp = readbuffer.split("\n".encode())
	readbuffer = temp.pop()

	# this is setup to take 1 (the first) command every 5 seconds. Anything else it 'SHOULD' throw away.
	# not tested fully and more testing/optimization should be done
	for line in temp:
		parts = line.split(":".encode())
		if "QUIT".encode() not in parts[1] and "JOIN".encode() not in parts[1] and "PART".encode() not in parts[1]:
			try:
				message = parts[2][:len(parts[2]) - 1]
			except:
				message = ""
			usernamesplit = parts[1].split("!".encode())
			username = usernamesplit[0]
		if MODT:
			if message == "Hey".encode():
				Send_message("Welcome to the stream, " + str(username))
				obs.timer_remove(update_text)
				obs.timer_add(update_text, 1000 * 5)
			elif message == "!help".encode():
				Send_message("ENTER HELP INFO HERE\n")
				obs.timer_remove(update_text)
				obs.timer_add(update_text, 1000 * 5)
			elif message == "!change_view".encode():
				Send_message("Next switch available in 5 seconds\n")
				# this switches to scene 1
				obs.obs_frontend_set_current_scene(scenes[1])
				obs.timer_remove(update_text)
				obs.timer_add(update_text, 1000 * 5)
			#continue if needed
			break
				
		for l in parts:
			if "End of /NAMES list".encode() in l:
				MODT = True

# ------------------------------------------------------------

def script_description():
	return "Chat bot"

def script_update(settings):

	# see here to generate info needed below https://help.twitch.tv/customer/en/portal/articles/1302780-twitch-irc
	HOST = "irc.twitch.tv"
	# example "NICK ninjahipst3r :"
	NICK = "NICK "your_nickname"\r\n"
	PORT = 6667
	#example PASS = "PASS oauth:abcdefghijcklmnop\r\n
	PASS = "PASS oauth:"your_key"\r\n"
	# example "JOIN #ninjahipst3r :"
	JOIN= "JOIN #"your_channel_name" \r\n"

	#this makes the connection and sets it up to not block. Otherwise OBS will hangup
	s.connect((HOST, PORT))
	s.send(PASS .encode())
	s.send(NICK.encode())
	s.send(JOIN.encode())
	s.setblocking(0)
	sock_close = False

	obs.timer_remove(send_help)
	obs.timer_add(send_help, 1000 * 300)

	source_name = obs.obs_data_get_string(settings, "source")

	obs.timer_remove(update_text)
	obs.timer_add(update_text, 1)

	#bug here when first started, this can be taken out if needed
	obs.obs_frontend_set_current_scene(scenes[1])


def script_defaults(settings):
	pass

def script_properties():
	props = obs.obs_properties_create()

	return props
