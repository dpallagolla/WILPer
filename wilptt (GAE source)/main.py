#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import ndb
import json
import logging
from google.appengine.ext import db
import requests
from bs4 import BeautifulSoup
import sys
import re
from google.appengine.api import urlfetch
import html5lib


class TimeTable(ndb.Model):
	
	courseCode = ndb.StringProperty(indexed=True)
	subjectString = ndb.StringProperty(indexed=True)
	day = ndb.StringProperty(indexed=True)
	time = ndb.StringProperty(indexed=True)

def gql_json_parser(query_obj):
		timeTableDict = {}
		for timeTable in query_obj:
		    timeTableDict[timeTable.courseCode].append(timeTable.courseCode)
		    timeTableDict[timeTable.subjectCode].append(timeTable.subjectCode)
		    timeTableDict[timeTable.day].append(timeTable.day)
		    timeTableDict[timeTable.time].append(timeTable.time)
		return result

def doWriteOperation(sSubjects,time,day):
	subjects = {"SS","ES","BA","MBA","POM","MM","MATH","HHSM","QM","MEL","POMSS","ENGG","EEE","CS","BITS","ET","FIN","CSI","IS","DE","MGTS","EA","PE","TA","AAOC"}
	sSubjects = processText(sSubjects)



	for s in subjects:
		if(s=="MATH"):
			print "S:"+s+" sSubjects:"+sSubjects+"\n"
		if s in sSubjects:
			# logging.info(s+":"+sSubjects+":"+time+":"+day+"\n")
			# POM POMSS POM342 POMSS234
			
			if(s=="BA"):
				sChecker = sSubjects.replace("MBA","")
				if("BA" in sChecker):
					timeTable = TimeTable()
					timeTable.courseCode = s
					timeTable.subjectString = sSubjects
					timeTable.day = day
					timeTable.time = time
					timeTable.put()
			elif(s=="SS"):
				# print "code:"+s+" sSubjects:"+sSubjects
				sChecker = sSubjects.replace("POMSS","")
				# print "After replacing "+" code:"+s+" sSubjects:"+sChecker
				if("SS" in sChecker):
					timeTable = TimeTable()
					timeTable.courseCode = s
					timeTable.subjectString = sSubjects
					timeTable.day = day
					timeTable.time = time
					timeTable.put()
			elif(s=="POM"):
				sChecker = sSubjects.replace("POMSS","")
				if("POM" in sChecker):
					timeTable = TimeTable()
					timeTable.courseCode = s
					timeTable.subjectString = sSubjects
					timeTable.day = day
					timeTable.time = time
					timeTable.put()
			else:
				timeTable = TimeTable()
				timeTable.courseCode = s
				timeTable.subjectString = sSubjects
				timeTable.day = day
				timeTable.time = time
				timeTable.put()
	
def findTheDay(day):
	day = str(day)
	theDay = re.match('(.*)day',day)
	if (theDay):

		retDay =  theDay.group(0)
		retDay = retDay.replace(' ','').replace('\t','')
		return retDay

	else:
		return "";
	
def processText(element):
	return str(element.replace('\t','').replace(' ','').strip())

def checkIfNotEmpty(sParam):
	s = str(sParam)
	# print "checking if:"+s+"is empty"	
	s = ''.join([i if ord(i) < 128 else ' ' for i in s])
	s = s.replace(' ','')
	# print ord(s[0])	
	if s =="":
		# print "returning false"
		return False
	if s == ' ':
		# print "returning false"
		return False
	# print "returning true"
	return True

def parseWeekDayTable(data):

	soup = BeautifulSoup(data, "html5lib")	
	# table8 is the weekday table
	a = soup.find("table",{"id":"table8"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	# print str(e)

	time1 = processText(str(e[1].getText()))

	time2 = processText(str(e[2].getText()))

	iterTable = iter(c)

	next(iterTable)

	# daysofWeek = {"Monday","Tuesday","Wednesday","Thursday","Friday"}

	for day in iterTable:
		z = day.find_all('td')
		tD = findTheDay(day.getText())
		if(tD!=""):
			theDay = tD
		# print str(theDay)+"\n"
		if(len(z)==2):
			if ("background-color" not in str(z[0])):
				subject1 = processText(str(z[0].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+theDay+"\n"
					doWriteOperation(subject1,time1,theDay)
			if ("background-color" not in str(z[1])):
				subject2 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+theDay+"\n"				
					doWriteOperation(subject2,time2,theDay)
		elif(len(z)==3):
			if ("background-color" not in str(z[1])):
				subject1 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+theDay+"\n"
					doWriteOperation(subject1,time1,theDay)
			if ("background-color" not in str(z[2])):
				subject2 = processText(str(z[2].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+theDay+"\n"
					doWriteOperation(subject2,time2,theDay)

def parseSaturday2Hour(data):
	soup = BeautifulSoup(data, "html5lib")	
	# table9 is Saturday 1 hour table
	a = soup.find("table",{"id":"table9"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	dayText = processText(str(e[0].getText()))

	time1 = processText(str(e[1].getText()))

	time2= processText(str(e[2].getText()))

	time3 = processText(str(e[3].getText()))

	time4 = processText(str(e[4].getText()))

	time5 = processText(str(e[5].getText()))

	# print dayText+":"+time1+":"+time2+":"+time3+":"+time4+":"+time5

	iterTable = iter(c)

	next(iterTable)

	for day in iterTable:
		z = day.find_all('td')
		if(len(z)==5):
			if ("background-color" not in str(z[0])):
				subject1 = processText(str(z[0].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+dayText+"\n"
					doWriteOperation(subject1,time1,dayText)
			if ("background-color" not in str(z[1])):
				subject2 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+dayText+"\n"
					doWriteOperation(subject2,time2,dayText)
			if ("background-color" not in str(z[2])):
				subject3 = processText(str(z[2].getText()))
				if(checkIfNotEmpty(subject3)):
					# print subject3+":"+time3+":"+dayText+"\n"
					doWriteOperation(subject3,time3,dayText)
			if ("background-color" not in str(z[3])):
				subject4 = processText(str(z[3].getText()))
				if(checkIfNotEmpty(subject4)):
					# print subject4+":"+time4+":"+dayText+"\n"
					doWriteOperation(subject4,time4,dayText)
			if ("background-color" not in str(z[4])):
				subject5 = processText(str(z[4].getText()))
				if(checkIfNotEmpty(subject5)):
					# print subject5+":"+time5+":"+dayText+"\n"
					doWriteOperation(subject5,time5,dayText)

def parseSunday2Hour(data):
	soup = BeautifulSoup(data, "html5lib")	
	# table9 is Saturday 1 hour table
	a = soup.find("table",{"id":"table9"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	

	time1 = processText(str(e[1].getText()))

	time2= processText(str(e[2].getText()))

	time3 = processText(str(e[3].getText()))

	time4 = processText(str(e[4].getText()))

	time5 = processText(str(e[5].getText()))

	a = soup.find("table",{"id":"table10"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	dayText = processText(str(e[0].getText()))

	if ("background-color" not in str(e[1])):
		subject1 = processText(str(e[1].getText()))
		if(checkIfNotEmpty(subject1)):
			# print subject1+":"+time1+":"+dayText+"\n"
			doWriteOperation(subject1,time1,dayText)
	if ("background-color" not in str(e[2])):
		subject2 = processText(str(e[2].getText()))
		if(checkIfNotEmpty(subject2)):
			# print subject2+":"+time2+":"+dayText+"\n"
			doWriteOperation(subject2,time2,dayText)
	if ("background-color" not in str(e[3])):
		subject3 = processText(str(e[3].getText()))
		if(checkIfNotEmpty(subject3)):
			# print subject3+":"+time3+":"+dayText+"\n"
			doWriteOperation(subject3,time3,dayText)
	if ("background-color" not in str(e[4])):
		subject4 = processText(str(e[4].getText()))
		if(checkIfNotEmpty(subject4)):
			# print subject4+":"+time4+":"+dayText+"\n"
			doWriteOperation(subject4,time4,dayText)
	if ("background-color" not in str(e[5])):
		subject5 = processText(str(e[5].getText()))
		if(checkIfNotEmpty(subject5)):
			# print subject5+":"+time5+":"+dayText+"\n"
			doWriteOperation(subject5,time5,dayText)
	

	iterTable = iter(c)

	next(iterTable)

	for day in iterTable:
		z = day.find_all('td')
		if(len(z)==5):
			if ("background-color" not in str(z[0])):
				subject1 = processText(str(z[0].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+dayText+"\n"
					doWriteOperation(subject1,time1,dayText)
			if ("background-color" not in str(z[1])):
				subject2 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+dayText+"\n"
					doWriteOperation(subject2,time2,dayText)
			if ("background-color" not in str(z[2])):
				subject3 = processText(str(z[2].getText()))
				if(checkIfNotEmpty(subject3)):
					# print subject3+":"+time3+":"+dayText+"\n"
					doWriteOperation(subject3,time3,dayText)
			if ("background-color" not in str(z[3])):
				subject4 = processText(str(z[3].getText()))
				if(checkIfNotEmpty(subject4)):
					# print subject4+":"+time4+":"+dayText+"\n"
					doWriteOperation(subject4,time4,dayText)
			if ("background-color" not in str(z[4])):
				subject5 = processText(str(z[4].getText()))
				if(checkIfNotEmpty(subject5)):
					# print subject5+":"+time5+":"+dayText+"\n"
					doWriteOperation(subject5,time5,dayText)

def parseSaturday1Hour(data):
	soup = BeautifulSoup(data, "html5lib")	
	# table9 is Saturday 1 hour table
	a = soup.find("table",{"id":"table11"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	dayText = processText(str(e[0].getText()))

	time1 = processText(str(e[1].getText()))

	time2= processText(str(e[2].getText()))

	time3 = processText(str(e[3].getText()))

	time4 = processText(str(e[4].getText()))

	time5 = processText(str(e[5].getText()))


	# print dayText+":"+time1+":"+time2+":"+time3+":"+time4+":"+time5

	iterTable = iter(c)

	next(iterTable)

	for day in iterTable:
		z = day.find_all('td')
		if(len(z)==5):
			if ("background-color" not in str(z[0])):
				subject1 = processText(str(z[0].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+dayText+"\n"
					doWriteOperation(subject1,time1,dayText)
			if ("background-color" not in str(z[1])):
				subject2 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+dayText+"\n"
					doWriteOperation(subject2,time2,dayText)
			if ("background-color" not in str(z[2])):
				subject3 = processText(str(z[2].getText()))
				if(checkIfNotEmpty(subject3)):
					# print subject3+":"+time3+":"+dayText+"\n"
					doWriteOperation(subject3,time3,dayText)
			if ("background-color" not in str(z[3])):
				subject4 = processText(str(z[3].getText()))
				if(checkIfNotEmpty(subject4)):
					# print subject4+":"+time4+":"+dayText+"\n"
					doWriteOperation(subject4,time4,dayText)
			if ("background-color" not in str(z[4])):
				subject5 = processText(str(z[4].getText()))
				if(checkIfNotEmpty(subject5)):
					# print subject5+":"+time5+":"+dayText+"\n"
					doWriteOperation(subject5,time5,dayText)

def parseSunday1Hour(data):
	soup = BeautifulSoup(data, "html5lib")	
	# table9 is Saturday 1 hour table
	a = soup.find("table",{"id":"table11"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	dayText = processText(str(e[0].getText()))

	time1 = processText(str(e[1].getText()))

	time2= processText(str(e[2].getText()))

	time3 = processText(str(e[3].getText()))

	time4 = processText(str(e[4].getText()))

	time5 = processText(str(e[5].getText()))

	a = soup.find("table",{"id":"table12"})

	b = a.find('tbody')

	c = b.find_all('tr');

	d = c[0]

	e = d.find_all('td')

	dayText = processText(str(e[0].getText()))

	if ("background-color" not in str(e[1])):
		subject1 = processText(str(e[1].getText()))
		if(checkIfNotEmpty(subject1)):
			# print subject1+":"+time1+":"+dayText+"\n"
			doWriteOperation(subject1,time1,dayText)
	if ("background-color" not in str(e[2])):
		subject2 = processText(str(e[2].getText()))
		if(checkIfNotEmpty(subject2)):
			# print subject2+":"+time2+":"+dayText+"\n"
			doWriteOperation(subject2,time2,dayText)
	if ("background-color" not in str(e[3])):
		subject3 = processText(str(e[3].getText()))
		if(checkIfNotEmpty(subject3)):
			# print subject3+":"+time3+":"+dayText+"\n"
			doWriteOperation(subject3,time3,dayText)
	if ("background-color" not in str(e[4])):
		subject4 = processText(str(e[4].getText()))
		if(checkIfNotEmpty(subject4)):
			# print subject4+":"+time4+":"+dayText+"\n"
			doWriteOperation(subject4,time4,dayText)
	if ("background-color" not in str(e[5])):
		subject5 = processText(str(e[5].getText()))
		if(checkIfNotEmpty(subject5)):
			# print subject5+":"+time5+":"+dayText+"\n"
			doWriteOperation(subject5,time5,dayText)

	iterTable = iter(c)

	next(iterTable)

	for day in iterTable:
		z = day.find_all('td')
		if(len(z)==5):
			if ("background-color" not in str(z[0])):
				subject1 = processText(str(z[0].getText()))
				if(checkIfNotEmpty(subject1)):
					# print subject1+":"+time1+":"+dayText+"\n"
					doWriteOperation(subject1,time1,dayText)
			if ("background-color" not in str(z[1])):
				subject2 = processText(str(z[1].getText()))
				if(checkIfNotEmpty(subject2)):
					# print subject2+":"+time2+":"+dayText+"\n"
					doWriteOperation(subject2,time2,dayText)
			if ("background-color" not in str(z[2])):
				subject3 = processText(str(z[2].getText()))
				if(checkIfNotEmpty(subject3)):
					# print subject3+":"+time3+":"+dayText+"\n"
					doWriteOperation(subject3,time3,dayText)
			if ("background-color" not in str(z[3])):
				subject4 = processText(str(z[3].getText()))
				if(checkIfNotEmpty(subject4)):
					# print subject4+":"+time4+":"+dayText+"\n"
					doWriteOperation(subject4,time4,dayText)
			if ("background-color" not in str(z[4])):
				subject5 = processText(str(z[4].getText()))
				if(checkIfNotEmpty(subject5)):
					# print subject5+":"+time5+":"+dayText+"\n"
					doWriteOperation(subject5,time5,dayText)

class UpdateHandler(webapp2.RequestHandler):

	def get(self):
		# try:
			print "came to UpdateHandler"
			reload(sys)
			sys.setdefaultencoding('utf-8')

			query = TimeTable.query()
			for q in query:
				q.key.delete()
				# print "deleted"			
			# db.delete(query)
			# db.delete(db.Query())

			logging.info("delete Successful");

			# url = "http://vu.bits-pilani.ac.in/onlineLecture/LectSchedule.htm";
			
			url = "https://elearn.bits-pilani.ac.in/static/lschedule/"

			r = urlfetch.fetch(url)
			# r = requests.get(url);

			if r.status_code == 200:
				data = r.content
			# data = r.text;
			else:
				raise Exception('Someting wrong with bits server!') 

			# logging.info("data:"+data)
			data = data.replace("\r","");

			data = data.replace("\n","");

			parseWeekDayTable(data)

			self.response.write("Weekday entries done<br>")

			parseSaturday2Hour(data)

			self.response.write("Saturday 2 hour done<br>")

			parseSunday2Hour(data)

			self.response.write("Sunday 2 hour done<br>")

			parseSaturday1Hour(data)

			self.response.write("Saturday 1 hour done<br>")

			parseSunday1Hour(data)

			self.response.write("Sunday 1 hour done<br>")

		# except:

			# self.response.write("something went wrong!"+str(sys.exc_info()[0]))

class MainHandler(webapp2.RequestHandler):

	
	def get(self):

		show = self.request.get('show')

		if(show):
			timeTables = TimeTable.query(TimeTable.courseCode==show)

			jsonTimeTable = json.dumps([a.to_dict() for a in timeTables])
			
			self.response.write(jsonTimeTable)	
		
		else:

			self.response.write('Welcome to the landing page of WILP time table!')
		

	def post(self):
		courseCode = self.request.get('courseCode','CC1')
		subjectCode = self.request.get('subjectCode','SC1')
		day = self.request.get('day','TAD1')
		time = self.request.get('time','TT1')
		key = self.request.get('key','')

		if(key==""):

			timeTable = TimeTable()
			timeTable.courseCode = courseCode
			timeTable.subjectCode = subjectCode
			timeTable.day = day
			timeTable.time = time
			timeTable.put()
			self.response.write('Successful Write')

		else:

			self.response.write('better luck next time!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/updateTimeTable', UpdateHandler)
], debug=True)
