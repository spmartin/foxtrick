#!/usr/bin/env python

if __name__ == '__main__':
	from Hattrick.CHPP import Client
	from Hattrick.CHPP import Credentials
	from Hattrick.CHPP import AccessToken

	import xml.etree.ElementTree as ET

	CONSUMER_KEY = Credentials.KEY
	CONSUMER_SECRET = Credentials.SECRET

	ACCESS_TOKEN_KEY = AccessToken.KEY
	ACCESS_TOKEN_SECRET = AccessToken.SECRET

	chpp = Client.ChppClient(CONSUMER_KEY, CONSUMER_SECRET)
	chpp.setAccessToken((AccessToken.KEY, AccessToken.SECRET))

	# in case no access token is present
	#auth_url = chpp.getAuthorizeUrl()
	#print auth_url
	#verifier = raw_input('Verifier:')
	#accessToken = chpp.getAccessToken(verifier)
	#print accessToken

	session = chpp.getSession()

	def getCoaches(id):
		#no get started
		response = chpp.getFile('nationalteams', params={'version':'1.5', 'LeagueOfficeTypeID': id })
		dom = ET.fromstring(response.content)

		teams = []
		iTeams =  dom.iter("NationalTeam")
		for iTeam in iTeams:
			team = {}
			team['TeamId'] = int(iTeam.find('NationalTeamID').text)
			team['LeagueId'] = int(iTeam.find('LeagueId').text)
			team['TeamName'] = iTeam.find('NationalTeamName').text
			teams.append(team)

		for t in teams:
			response = chpp.getFile('nationalteamdetails', params={'version':'1.8', 'teamID':t['TeamId']})
			dom = ET.fromstring(response.content)
			iCoaches =  dom.iter("NationalCoach")
			for iCoach in iCoaches:
				t['CoachId'] = int(iCoach.find('NationalCoachUserID').text)
				t['CoachName'] = iCoach.find('NationalCoachLoginname').text

		return teams

	def saveCoaches(coaches, filename):
		file = open( filename, "w")
		file.write('{\n')
		file.write('\t"type": "%s",\n' % "coach")
		file.write('\t"internal": "true",\n')
		file.write('\t"list": [\n')
		file.write('\t\t' + ',\n\t\t'.join(map(lambda a: '{ "LeagueId": %d, "TeamId": %d, "TeamName": "%s", "CoachId": %d, "CoachName": "%s" }' % (a["LeagueId"], a["TeamId"], a["TeamName"].encode('utf-8'), a["CoachId"], a["CoachName"].encode('utf-8')), coaches)))
		file.write('\n\t]\n}')
		file.close()
		print filename, 'written'

	u20 = getCoaches(4);
	nt = getCoaches(2);

	saveCoaches(u20, '/home/foxtrick/trunk/res/staff/u20coaches.json')
	saveCoaches(nt, '/home/foxtrick/trunk/res/staff/ntcoaches.json')