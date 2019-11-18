import time
import random
import math
people= [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
     #机场数据
destination='LGA'
flights={}

def readfile(filename):
  file=open(filename)
  return file

file=readfile("C:/Users/USER/schedule.txt")
for line in file:
	origin,dest,depart,arrive,price=line.strip().split(',')
	flights.setdefault((origin,dest),[])
	#将航班详情添加到航班列表中
	flights[(origin,dest)].append((depart,arrive,int(price)))

def  getminutes(t):
	x=time.strptime(t,'%H:%M')
	return x[3]*60+x[4]

def printschedule(r):
	for d in range(int(len(r)/2)):  #python 默认为float,要加上int强制转化
		name=people[d][0]
		origin=people[d][1]
		out=flights[(origin,destination)][r[2*d]]  #第d个人的返程
		ret=flights[(destination,origin)][r[2*d+1]]
		print("%10s%10s %5s-%5s $%3s %5s-%5s $%3s"%(name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[2]))

s=[1,4,3,2,7,3,6,3,2,4,5,3]
printschedule(s)

