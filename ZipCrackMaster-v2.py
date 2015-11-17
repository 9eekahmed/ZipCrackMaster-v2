#! /usr/bin/python3

import os,sys
import time
from zipfile import *
from argparse import ArgumentParser
import threading

start_time = time.time()


HEADER = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WHITE = '\033[37m'
WARNING = '\033[93m'
FAIL = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'

class Crack:
	
	pwdTried=0
	FilesList=[]
	notFilesList=[]
	passFound=[]
	all_pwd_lists=[]
	plist=[]
	thread_completed=[]
	splitNum=0

	def __init__(self,a_filename,a_pwdList):
		self.FileName=a_filename
		self.pwdFile= a_pwdList

		self.__arrangeData()


	def __arrangeData(self):
		for items in self.FileName:
			if is_zipfile(items):
				self.FilesList.append(items)
			else:
				self.notFilesList.append(items)
		
		if len(self.FilesList) > 0:
			print(BOLD,WHITE,"Valid zip files to crack: ",ENDC,BLUE,self.FilesList,ENDC)
			print(BOLD,WHITE,"Invalid files: ",ENDC,FAIL,self.notFilesList,ENDC)

			self.__readPwdList()
		else:
			print(FAIL,"[*] ZipFiles not found !",ENDC)

	def __readPwdList(self):
		
		self.splitNum = input('\nlist > 100k defuelt = 10000\nlist > 500k defuelt = 50000\nlist > 1m defuelt = 100000\n[#] Enter number to split password list to: ')
		try:
			if self.splitNum=='':
				self.splitNum=100000
				pass
			else:
				self.splitNum=int(self.splitNum)
		except:
			print(FAIL,'Invalid value ..!',ENDC)
			sys.exit(3)
			


		print('\n[#] Collecting list [',end='')
		try:
			with open(self.pwdFile,'r') as pwdfile:
				
				while True:
					word = pwdfile.readline()
					if word != '':
						word = word.strip()
						self.plist.append(word)
						if len(self.plist) == self.splitNum:
							self.all_pwd_lists.append(list(self.plist))
							self.clearlist()

					else:
						print(GREEN,'Done',ENDC,']')
						if not len(self.plist) == 0:
							self.all_pwd_lists.append(list(self.plist))
							self.clearlist()

						self.threader()
						break
				

		except Exception as e:
			print(FAIL,"[X] ",str(e),ENDC)

	def clearlist(self):
		while len(self.plist)>0:
			self.plist.pop()

	def threader(self):
		print(FAIL,"\nStart Cracking ...\n",ENDC)

		for x in self.all_pwd_lists:
			t=threading.Thread(target = self.use_Collected_pwd,args=(x,))
			t.start()

	def use_Collected_pwd(self,l=[]):
		for word in l:
			self.pwdTried+=1
			self.__crack(bytes(word,'utf-8'))

			if len(self.FilesList) == 0:
				break
		self.thread_completed.append(True)



	def __crack(self,word):
		for each in self.FilesList:
			try:

				with ZipFile(each) as zfile:
					zfile.extractall(pwd=word)

				self.FilesList.remove(each)
				self.passFound.append(each)

				print(WHITE,"[*]",GREEN,each,":",word.decode(),ENDC)
				
				if len(self.all_pwd_lists) == len(self.thread_completed) or len(self.FilesList)==0:
					self.results()
								
			except:
				pass

	def results(self):
		global start_time

		print(WHITE,"\n  Tested:",BOLD,self.pwdTried,WHITE,"word",ENDC)
		print('  Time: ',BOLD,round(time.time()-start_time,2),'s',ENDC)

def Main():

	parser = ArgumentParser()
	parser.add_argument('zipfile',help="Zip file name {file.zip} or list of zipfiles {file1.zip,file2.zip}", type=str)
	parser.add_argument('pwdlist', help="List of password to try it {pass.txt}",type=str)
	args=parser.parse_args()

	zipfiles=args.zipfile.split(',')
	pwdList=args.pwdlist


	print("==========================================================")
	print("  ZipCrackMaster | [Version]: 2.0  Pro                    ")
	print("==========================================================")
	print("  [E-mail]: 9eek.mohamed@gmail.com | [Twitter]: @Geekm    ")
	print("==========================================================\n")

	run=Crack(zipfiles,pwdList)

if __name__ == '__main__':
	os.system('cls' if os.name == 'nt' else 'clear')
	Main()
