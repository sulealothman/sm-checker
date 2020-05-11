import requests
import json
import sys
import re
import argparse

# Author Suleiman Al-Othman (@sulealothman)
# sm-cheker script ( social media checker )
# Matching and checking available for username Github, Twitter, Instagram and Snapchat
# version v0.1

class smchecker:

	patterns = {
		'Github' : r'^(?!.*\-\-|.*\-$|.*\_)[a-zA-Z0-9][\w-]+[a-zA-Z0-9]{0,39}$',
		'Twitter' : r'^[A-z0-9]{0,15}$',
		'Instagram' : r'^(?!.*\.\.|.*\.$)[A-z0-9][\w.]+[A-z0-9]{0,30}$',
		'Snapchat' : r'^(?!.*\.\.|.*\_\_|.*\-\-)(?!.*\.$|.*\_$|.*\-$)(?!.*\.\-|.*\-\.|.*\-\_|.*\_\-|.*\.\_|.*\_\.)[a-zA-Z]+[\w.-][0-9A-z]{0,15}$'
	}

	def __init__(self, username, options = 'default'):
		self.username = username
		self.options = options
		for appName, pattern in self.patterns.items():
			print('# ', appName, ' : ', self.username)
			if self.options == 'regex':
				print('=> ', self.check_pattern(pattern, self.username))
			elif self.options == 'check':
				print('=> ', eval('self.' + appName)(self.username))
			else:
				print('=> ', self.check_pattern(pattern, self.username))
				print('=> ', eval('self.' + appName)(self.username))


	def check_pattern(self, pattern, text):
		if(re.match(pattern, text)):
			return 'Yes, is matched .'
		return 'No, is not matched .'


	def Github(self, username):
		request_url = 'https://api.github.com/users/' + username
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/75.0'
		}

		response = requests.get(request_url, headers=headers)
		data = response.json()
		status = data.get('message')
		if status == 'Not Found':
			return 'Username available'
		else:
			return 'Username unavailable'


	def Instagram(self, username):
		request_url = 'https://www.instagram.com/' + username + '?__a=1'
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/75.0'
		}

		response = requests.get(request_url, headers=headers)

		try:
			data = response.json()
			return 'Username unavailable'
		except:
			return 'Username available'

	def Snapchat(self, username):
		request_url = 'https://accounts.snapchat.com/accounts/get_username_suggestions?requested_username=' + username + '&xsrf_token=wRrADebNRCvxaHmdRtVTzQ'

		headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/75.0',
            'Cookie': 'xsrf_token=wRrADebNRCvxaHmdRtVTzQ; sc-cookies-accepted=true; web_client_id=6b6145f7-a747-41ba-92d6-b37c8ad38d03; oauth_client_id=c25hcC1jb25uZWN0LS1wcm9k',
		}
		response = requests.post(request_url, headers=headers)
		data = response.json()
		status = data.get('reference').get('status_code')

		if status == 'TAKEN':
			return 'Username unavailable'
		else:
			return 'Username available'
        
	def Twitter(self, username):
		request_url = 'https://api.twitter.com/graphql/E4iSsd6gypGFWx2eUhSC1g/UserByScreenName?variables={"screen_name":"' + username + '","withHighlightedLabel":true}'
		headers = {
			'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/75.0',
		}

		response = requests.get(request_url, headers=headers)
		data = response.json()

		try:
			status = data.get('errors')[0].get('message')
			if status != 'Not Found':
				return 'Username available'
		except:
			return 'Username unavailable'


parser = argparse.ArgumentParser(
	description="Script name : Social Media Checker (sm-cheker), Ver. : 0.1, Author : SuleAlOthman",
	usage=""" Example #1 : python3 sm-checker.py -l list.txt \r\n
	Example #2 : python3 sm-checker.py -l list.txt -o regex \r\n
	Example #3 : python3 sm-checker.py -u username \r\n
	Example #3 : python3 sm-checker.py -u username -o checker \r\n""")
parser.add_argument('-l', '--list_file',type=str,help='Text file for users')
parser.add_argument('-u', '--username',type=str,help='username')
parser.add_argument('-o', '--options',nargs='?',default="default",type=str,help='options : default - regex - check')
args = parser.parse_args()


if __name__ == '__main__':
	if args.list_file != None:
		try:
			path = args.list_file
			user_list = open(path, 'r').read().split('\n')
			for username in user_list:
				smchecker(username, args.options.strip())
		except:
			print('Directory is wrong, please check your list file directory is correct/')
	elif args.username != None:
		username = args.username
		try:
			smchecker(username, args.options.strip())
		except:
			print('Something is wrong, please try again.')
			
	else:

		print('Options :', '\n 1 => Check available and matched', '\n 2 => Check username available', '\n 3 => Check username is matched', '\n 4 => Exit !')

		while True:
			options = input('Select your option : ')
			try:
				if int(options) == 4:
					break
				username = input('Enter your username : ')
				if int(options) == 1:
					smchecker(username)
				elif int(options) == 2:
					smchecker(username, 'check')
				elif int(options) == 3:
					smchecker(username, 'regex')
				else:
					print("Your insert number not found, please select correct select options number.")
			except:
				print("Please enter select options number.")











