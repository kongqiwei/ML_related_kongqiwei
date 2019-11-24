class matchrow:
	def __init__(self,row,allnum=False):
		if allnum:
			self.data=[float(row[i]) for i in range(len(row)-1)]
		else:
			self.data=row[0:len(row)-1]
		self.match=int(row[len(row)-1])

	def loadmatch(f,allnum=False):
		rows=[]
		for line in file(f):
			rows.append(matchrow(line.split(','),allnum))
		return rows

'''
from pylab import*
def  plotagematches(rows):
	xdm,ydm=[r.data[0] for i in rows if r.match==1],[r.data[1] for i in rows if r.match==1]
	xdm,ydm=[r.data[0] for i in rows if r.match==0],[r.data[1] for i in rows if r.match==0]
	plot(xdm,ydm,'go')
	plot(xdn,ydn,'ro')
	show()
'''

def lineartrain(rows):
	averages={}
	counts={}
	for row in rows:
		#得到该坐标点所属的分类
		c1=row.match
		averages.setdefault(c1,[0]*(len(row.data)))
		counts.setdefault(c1,0)
		#将该坐标点加入averages中
		for i in range(len(row.data)):
			averages[c1][i]+=float(row.data[i])
		#记录每个分类中有多少个坐标点
		counts[c1]+=1
	#将总和除以计数值以求的平均值
	for c1,avg in averages.items():
		for i in range(len(avg)):
			avg[i]/=counts[c1]
	return averages

def dotprobduct(v1,v2):
	return sum([v1[i]*v2[i] for i in range(len(v1))])

def dpclassify(point,avgs):
	b=(dotprobduct(avgs[1],avgs[1])-dotprobduct(avgs[0],avgs[0]))/2
	y=dotprobduct(point,avgs[0])-dotprobduct(point,avgs[1])+b
	if y>0:
		return 0
	else:
		return 1

def yesno(v):
	if v=='yes':
		return 1
	elif v=='no':
		return -1
	else:
		return 0

def matchcount(interst1,interst2):
	l1=interst1.split(':')
	l2=interst2.split(':')
	x=0
	for v in l1:
		if v in l2:
			x+=1
	return x

def loadnumerical():
	oldrows=('matchmaker.csv')
	newrows=[]
	for row in oldrows:
		d=row.data
		data=[float(d[0]),yesno(d[1]),yesno(d[2]),float(d[5]),yesno(d[6]),yesno(d[7]),matchcount(d[3],d[8]),milesdistance(d[4],d[9]),row.match]
		newrows.append(matchrow(data))
	return newrows

def scaledata(rows):
	low=[99999999]*len(rows[0].data)
	high=[-99999999]*len(rows[0].data)
	#寻找最大值和最小值
	for row in rows:
		d=row.data
		for i in range(len(d)):
			if d[i]<low[i]:
				low[i]=d[i]
			if d[i]>high[i]:
				high[i]=d[i]
	#对数据进行缩放处理的函数
	def scaleinput(d):
		return [(d.data[i]-low[i])/(high[i]-low[i]) for i in range(len(low))]

	#对所有数据进行缩放处理
	newrows=[matchrow(scaleinput(row.data)+[row.match]) for row in rows]
	#返回新的数据和缩放处理函数
	return  newrows,scaleinput


def rbf(v1,v2,gamma=20):
	dv=[v[i]-v2[i] for i in range(len(v1))]
	l=veclength(dv)
	return math.e**(-gamma)

def nlclassify(point,rows,offset,gamma=10):
	sum0=0
	sum1=0
	count0=0
	count1=0
	for  row in rows:
		if row.match==0:
			sum0+=rbf(point,row.data,gamma)
			count0+=1
		else:
			sum1+=rbf(point,row.data,gamma)
			cou+=1
	y=(1/count0)*sum0-(1/count1)*sum1+offset
	if y<0:
		return 0
	else:
		return 1

def getoffset(rows,gamma=10):
	l0=[]
	l1=[]
	for row in rows:
		if row.match==0:
			l0.append(row.data)
		else:
			l1.append(row.data)
	sum0=sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
	sum1=sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)
	return (1/(len(l1)**2))*sum1-(1/(len(l0)**2))*sum0

