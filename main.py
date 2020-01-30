# coding: UTF-8
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
		self.date_unix = np.empty(0)
		self.lv = []
		self.rem_exp = []
		self.total_exp = np.empty(0, dtype=np.int)

	def load_data(self, filename):
		"""
			レベリングの記録を保存したテキストデータから情報をロードしクラスへ格納
			テキストデータのエンコード形式はUTF-8。気をつけよう。
			Parameters
			----------
			filename : str
				レベリングの記録を保存したテキストファイルのファイルネーム
			
		"""
		with open(filename,encoding='utf-8') as f:
			self.name = f.readline().strip("\n")
			self.dst_lv = int(f.readline().strip("\n") )
			self.dst_exp = TE.TE_calc(self.dst_lv-1, 0)
			datas = f.readlines()
			for i in datas:
				date, lv, rem_exp = i.split()
				date = dt.datetime.strptime(date, '%y.%m.%d')
				lv = int(lv)
				rem_exp = int(rem_exp)
				self.date.append( date)
				self.lv.append(lv)
				self.rem_exp.append(rem_exp)
				self.total_exp = np.append(self.total_exp, TE.TE_calc(lv, rem_exp) )
		
	def cov_date_unix(self):
		"""
			最小二乗法の計算用にdateをUNIX時間へ変換しdate_unixへ代入
		"""
		self.date_unix = np.array( [ [ i.timestamp() for i in self.date ], np.ones(len(self.date) ) ] ).T

TE = Total_EXP()
TE.TE_List_read()

one = FG_data()
one.load_data("sampledata 赤城.txt")


print('[{}]'.format(one.name) )
print('[{}]'.format(one.dst_lv) )
print('[{}]'.format(one.dst_exp) )

print("日付    \t Lv\t     RE\t     TE")	
for i in range( len(one.date) ):
	print("{}\t{:>3}\t{:>7}\t{:>7}".format( 
			one.date[i].strftime('%y.%m.%d'),
			one.lv[i],
			one.rem_exp[i],
			one.total_exp[i]
		)
	)

one.cov_date_unix()
print(  )

a,b = np.linalg.lstsq(one.date_unix, one.total_exp, rcond=0)[0]
dst_day_unix = (one.dst_exp - b)/a
dst_day = dt.datetime.fromtimestamp( dst_day_unix )
print("レベリング終了予定日：{}".format(dst_day.strftime('%y.%m.%d') ) )



print("あと{}日ほど".format( (dst_day-dt.datetime.now() ).days) )
print("EXP/day={}".format(a*24*60*60) )

fig = plt.figure() # Figureオブジェクトを作成
ax1 = fig.add_subplot(3,2,1) # figに属するAxesオブジェクトを作成

ax1.plot(one.date, one.total_exp, "ro")
#ax1.plot(A[:,0], np.full(A[:,0].shape, Dst_LV), "b--")



ax1.plot(one.date, (a*one.date_unix[:,0]+b), "g--")


# DayLocatorで間隔を日数に
ax1.xaxis.set_major_locator( mdates.DayLocator() )

# Formatterでx軸の日付ラベルを月・日に設定
ax1.xaxis.set_major_formatter( mdates.DateFormatter("%m/%d") )
# ラベルを270度回す
ax1.tick_params(axis='x', rotation=270)
ax1.grid(True)
plt.show()