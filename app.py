#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from telethon import TelegramClient, sync
from telethon.tl.types import Chat, Channel, UserStatusOffline
import json, time, datetime

api_id = ''
api_hash = ''

with TelegramClient('session_name', api_id, api_hash) as client:
	client.start()

	## TIMESTAMPS WITH USERNAME (SLOWER)

	user_file = 'users.json'
	with open('users.json') as data_file:
		users = json.load(data_file)

	usernames = [users[id]['username'] for id in users]

	for key, username in enumerate(usernames):
		try:
			member = client.get_entity(username)
		except ValueError:
			continue
		if (member.username != None and member.bot == False):
			if isinstance(member.status, UserStatusOffline):
				print(key, username, datetime.datetime.now(datetime.timezone.utc) - member.status.was_online)

	## TIMESTAMPS WITH SCRAPED USERS (FASTER)

	groupList = list(dialog.entity for dialog in client.get_dialogs(limit=100) if (isinstance(dialog.entity, Chat) or isinstance(dialog.entity, Channel)) and hasattr(dialog.entity, 'username'))

	for key, group in enumerate(groupList):
		print("[{}]".format(key), group.title, "-", group.username)

	try:
		option   = int(input("Please type the number of the group where users will be scraped: "), 10)
		username = groupList[option].username
		for key, member in enumerate(client.get_participants(username, aggressive=False)):
			if (member.username != None and member.bot == False):
				if isinstance(member.status, UserStatusOffline):
					print(key, member.username, datetime.datetime.now(datetime.timezone.utc) - member.status.was_online, "ago")
	except Exception as e:
		print("An error has ocurred.", e)

