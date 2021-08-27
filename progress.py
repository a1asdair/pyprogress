# Progress tracker
# Alasdair Rutherford
# Created: 26 Aug 21
# Last edited: 26 Aug 21

from time import time
import csv

class Progress:

	# Companies House documentation
	# Director details
	# 

	def __init__(self, totalops, datestamp = '', log=False):

		self.totalops = totalops
		self.starttime = time()
		self.ticktime = self.starttime
		self.lasttime = time()
		self.ticks= 1
		self.varsum = 0

		self.reportstring = 'an unknown time'
		self.reportlower = 'unknown'
		self.reportupper = 'unknown'

		self.ticksum = 0
		self.ticksum2 = 0

		if log == True:
			self.log = True
			self.filename = 'progresslog-' + datestamp + '.csv'
			self.logfile = open(self.filename, 'w', encoding="utf-8", newline='')
			self.logfields = ("tick", "time", "timepertick", "estimate", "lower", "upper")
			logwr = csv.DictWriter(self.logfile, self.logfields)
			logwr.writeheader()
			#self.logcsv = logwr
			logwr.writerow({'tick': self.ticks, 'time': self.starttime, 'timepertick': '', 'estimate': '', 'lower': '', 'upper': ''})
			self.logfile.close()
		else:
			self.log=False

	def tick(self):
		self.ticks +=1
		self.lasttime = self.ticktime
		self.ticktime = time()

		self.elapsed = (self.ticktime - self.starttime)
		self.ticklength = self.ticktime - self.lasttime
		self.timepertick = self.elapsed / self.ticks
		self.expected_secs = (self.totalops - self.ticks) * self.timepertick
		self.expected_mins = self.expected_secs / 60
		self.expected_hours = self.expected_mins / 60

		if self.expected_hours > 1:
			self.reporttime = round(self.expected_hours, 1)
			self.reportstring = str(self.reporttime) + ' hours'
		else:
			if self.expected_mins > 3:
				self.reporttime = round(self.expected_mins, 1)
				self.reportstring = str(self.reporttime) + ' mins'
			else:
				self.reporttime = round(self.expected_secs, 0)
				self.reportstring = str(self.reporttime) + ' secs'

		self.percent = int((self.ticks / self.totalops)*100)

		#devfrommean = ((self.ticklength) - self.timepertick) ** 2

		#self.varsum = self.varsum + devfrommean
		
		self.ticksum = self.ticksum + self.ticklength
		self.ticksum2 = self.ticksum2 + (self.ticklength ** 2)

		self.variance = (self.ticksum2 - ( self.ticks * (self.timepertick ** 2))) / (self.ticks - 1)

		self.stddev = self.variance ** 0.5       #(self.varsum / self.ticks) ** 0.5
		self.se = self.stddev / ((self.ticks) ** 0.5)

		self.lower = max(self.timepertick - (1.96 * self.se), 0)
		self.upper = self.timepertick + (1.96 * self.se)

		print(self.varsum, self.stddev, self.se, self.lower, self.upper)

		self.lowersecs = (self.totalops - self.ticks) * self.lower
		self.uppersecs = (self.totalops - self.ticks) * self.upper

		self.reportlower = self.converttime(self.lowersecs)
		self.reportupper = self.converttime(self.uppersecs)


		if self.log == True:
			try:
				self.logfile = open(self.filename, 'a', encoding="utf-8", newline='')
				logwr = csv.DictWriter(self.logfile, self.logfields)
				logwr.writerow({'tick': self.ticks, 'time': round(self.ticktime,3), 'timepertick': round(self.timepertick,3), 'estimate': round(self.expected_secs, 0), 'lower': round(self.lowersecs, 0), 'upper': round(self.uppersecs, 0)})		
				self.logfile.close()
			except:
				print('** Logfile did not work!')

				
	def converttime(self, time):

		if time > 60 * 60:
			reporttime = round(time / 3600, 1)
			reportstring = str(reporttime) + ' hours'
		else:
			if time > 3 * 60:
				reporttime = round(time / 60, 1)
				reportstring = str(reporttime) + ' mins'
			else:
				reporttime = round(time, 0)
				reportstring = str(reporttime) + ' secs'

		return reportstring

	def remaining(self):
		return self.reporttime

	def progress(self):
		progress = str(self.percent) + '%'
		return progress

	def report(self):
		report = '| Progress: row ' + str(self.ticks) + ' of ' + str(self.totalops) + ' or ' + self.progress() + '. Averaging ' + str(round(self.timepertick,2)) + ' seconds per row. Expected completion in ' + self.reportstring +  ' between ' + self.reportlower + ' and ' + self.reportupper + '.'
		return report