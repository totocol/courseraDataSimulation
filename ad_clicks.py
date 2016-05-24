import global_vars
import random
import numpy as np
import datetime

def writeAdClicksCSV(startTime, dayDuration	):
	#get users who are playing and their ad probabilities
	teamAssignments =global_vars.globalTeamAssignments
	userSessions	= global_vars.globalUSessions
	totalUsers 		= []
	adProbabilities = []

	numberOfAds = 30

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE ad database if global variable is None
	if(global_vars.adDatabase is None):
		adCategories = ['sports', 'fashion', 'hardware', 'electronics', 'clothing', 'games', 'automotive', 'computers', 'movies']
		pickCategories=np.random.choice(adCategories, numberOfAds)
		adDatabase = zip(range(0,numberOfAds), pickCategories) #each member is a tuple (adID, category)
		global_vars.adDatabase = adDatabase
	else:
		adDatabase = global_vars.adDatabase

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GET list1= (teamid,userid) list2=adfactor for each user currently playing
	addition = 0
	for s in userSessions:
		userid = teamAssignments[s['assignmentid']]['userid']
		teamid = teamAssignments[s['assignmentid']]['teamid']
		adfactor = global_vars.globalUsers[userid]['tags']['adbeh']
		totalUsers.append((teamid, userid)) #list
		adProbabilities.append(adfactor) #list
		addition += adfactor

	adProbabilities = [x/addition for x in adProbabilities]

	#pick 30% users for clicking based on their click probabilities
	factor = random.uniform(0, 0.3)
	#print factor
	adUsers = np.random.choice(range(0, len(totalUsers)), factor*len(totalUsers), replace=True, p=adProbabilities).tolist()
	adclicks = []

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE adclicks from these users
	for indx in adUsers:
		adEvent = {}
		adEvent['timeStamp'] = startTime + datetime.timedelta(hours=random.uniform(0, dayDuration.seconds // 3600))
		adEvent['teamid'] = totalUsers[indx][0]
		adEvent['userid'] = totalUsers[indx][1]
		pickAnAd 				= np.random.choice(len(adDatabase), 1)[0]
		adEvent['adID']   		= adDatabase[pickAnAd][0]
		adEvent['adCategory'] 	= adDatabase[pickAnAd][1]
		adclicks.append(adEvent)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~APPEND to file
	assignLog = open("ad-clicks.log", "a")
	for a in sorted(adclicks, key=lambda a: a['timeStamp']):
		assignLog.write("%s, team=%s, userid=%s, adID=%s, adCategory=%s\n" %
			(a['timeStamp'], a['teamid'], a['userid'], a['adID'], a['adCategory']))
	assignLog.close()
