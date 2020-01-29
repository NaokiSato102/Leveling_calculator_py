# coding: UTF-8
import datetime as dt


"""
変数　略語集
T.E = Total EXP
R.E = remainingEXP
P.E = PredictedEXP
P.Lv = PredictedLv
"""



'''str1 = '1919/1/23'
print(str1)
dt1 = dt.datetime.strptime(str1, '%y/%m/%d')
print(dt1)'''

class Total_EXP:
	def __init__(self):
		self.Lv_list = []
	
	def TE_List_read(self): # T.E = Total EXP
		self.Lv_list = [int(line) for line in open('Total_EXP_List.txt')]

	def TE_calc(self,Lv,RE):# R.E = remainingEXP
		'''
		Lv xを入力すると Lv x+1の累計EXP値が参照される。
		それから「次のLvまであとどれくらいか」のEXP値を引くと
		現在のEXPが求まる。
		'''

		return self.Lv_list[Lv] - RE

class F_data:
	def __init__(self, date, Lv, RE, diff_date, TE, PE, PLv):
		self.date = date
		self.Lv = Lv
		self.RE = RE
		self.diff_date =diff_date
		self.TE = TE
		self.PE = PE
		self.PLv = PLv

#print(TE_calc(55,1056))

TE = Total_EXP()
TE.TE_List_read()

with open("sampledata.txt",encoding='utf-8') as f:
	shipname = f.readline().strip("\n")
	print('[{}]'.format(shipname) )

	startdate_str = f.readline().strip("\n")
	startdate = dt.datetime.strptime(startdate_str, '%y.%m.%d')
	print('[{}]'.format(startdate) )

	startLv = int(f.readline().strip("\n") )
	print('[{}]'.format(startLv) )
	datas =f.readlines()
	F_datas = []
	for i in datas:
		data_s = i.split()
		print(len(data_s))
		F_datas.append(
			F_data(
				dt.datetime.strptime(data_s[0], '%y.%m.%d'),
				int( data_s[1] ),
				int( data_s[2] ),
				dt.datetime.strptime(data_s[0], '%y.%m.%d') - startdate ,
				TE.TE_calc( int(data_s[1]), int(data_s[2]) ),
				0,
				0
			)
		) 




print("日付    \t Lv\t     RE\thoge  \t     TE")	
for i in F_datas:
	print("{}\t{:>3}\t{:>7}\t{:>2}\t{:>7}".format( 
			i.date.strftime('%y.%m.%d'),
			i.Lv,
			i.RE,
			int(i.diff_date.days),
			i.TE
		)
	)
print(type(F_datas[0].date))