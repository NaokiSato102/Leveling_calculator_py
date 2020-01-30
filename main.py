# coding: UTF-8
import datetime as dt
import numpy as np

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
		"""
			Expリストを読み込む。
			今後のLv上限拡張に対して柔軟に対応可能なように、
			コードにべた書きでなく 別途テキストデータを読み込む形に。
		"""

		self.Lv_list = [int(line) for line in open('Total_EXP_List.txt')]

	def TE_calc(self,lv,rem_exp):# R.E = remainingEXP
		'''
			Lvと、次のレベルまでの残りEXPによって累計EXPを計算する。

			Lv xを入力すると Lv x+1の累計EXP値が参照される。  
			それから「次のLvまであとどれくらいか」のEXP値を引くと
			現在のEXPが求まる。

			Parameters
			----------
			lv : int
				Lv
			rem_exp : int
				次のレベルまでの残りExp remaining exp

			Return
			-------
			total_exp : int
				累計Exp
		'''

		return self.Lv_list[lv] - rem_exp

class FG_data:
	def __init__(self):
		self.name = ""
		self.dst_lv = 0
		self.dst_exp = 0
		self.date = []
		self.lv = []
		self.rem_exp = []
		self.total_exp = np.empty(0, dtype=np.int)





TE = Total_EXP()
TE.TE_List_read()



one = FG_data()
with open("sampledata.txt",encoding='utf-8') as f:
	one.name = f.readline().strip("\n")
	 


	
	one.dst_lv = int(f.readline().strip("\n") )
	print('[{}]'.format(one.dst_lv) )

	one.dst_exp = TE.TE_calc(one.dst_lv-1, 0)
	print('[{}]'.format(one.dst_exp) )
	
	datas = f.readlines()
	
	for i in datas:
		date, lv, rem_exp = i.split()

		date = dt.datetime.strptime(date, '%y.%m.%d')
		lv = int(lv)
		rem_exp = int(rem_exp)

		one.date = np.append(one.date, date)
		one.lv.append(lv)
		one.rem_exp.append(rem_exp)
		one.total_exp = np.append(one.total_exp, TE.TE_calc(lv, rem_exp) )



print("日付    \t Lv\t     RE\t     TE")	
for i in range( len(one.date) ):
	print("{}\t{:>3}\t{:>7}\t{:>7}".format( 
			one.date[i].strftime('%y.%m.%d'),
			one.lv[i],
			one.rem_exp[i],
			one.total_exp[i]
		)
	)


