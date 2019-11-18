import urllib
from bs4 import BeautifulSoup
ingorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
	#初始化类并传入数据库名称
	def  __init__(self,dbname):
		pass

	def __del__(self):
		pass

	def  dbcommit(self):
		pass

	##辅助函数，用于获取条目的id,并且如果条目不存在，就将其加入数据库中
	def getentryid(self,table,field,value,createnew=True):
		cur=self.con.execute("select rowid  from %s where %s='%s'"%(table,field,value))
		res=cur.fetchone()
		if res==None:
			cur=self.con.execute("insert into %s(%s) values ('%s')"%(table,field,value))
			return cur.lastrowid
		else:
			return res[0]

	#为每一个网页建立索引
	def addtoindex(self,url,soup):
		if self.isindexed(url):
			return 
		print("indexing"+url)
		#获取每一个单词
		text=self.gettextonly(soup)
		words=self.separatewords(text)
		#得到URl的id
		urlid=self.getentryid('urllist','url',url)
		#将每一个单词与url关联
		for i in range(len(words)):
			word=words[i]
			if word in ingorewords:
				continue
			wordid=self.getentryid('wordlist','word',word)
			self.con.execute("insert into wordlocation (urlid,wordid,location) values (%d,%d,%d)"%(urlid,wordid,i))



	#从一个html网页中提取文字
	def gettextonly(self,soup):
		v=soup.string
		if v==None:
			c=soup.contents
			resulttext=' '
			for t in c:
				subtext=self.gettextonly(t)
				resulttext+=subtext+'\n'
			return resulttext
		else:
			return v.strip()

	#根据任何非空白字符进行分词处理
	def  separatewords(self,text):
		splitter=re.compile('\\W*')
		return [s.lower() for s in splitter.split(text)  if s!=' ']

	#如果url已经建立过索引，则返回true
	def isindexed(self,url):
		u=self.con.execute("select rowid from urllist where url='%s'"%url).fetchone()
		if u!=None:
			#检查是否已经被检索过了
			v=self.con.execute('select *from wordlocation where urlid=%d' %u[0]).fetchone()
			if v!=None:
				return True
		return False


	#添加一个关联两个网页的链接
	def addlinkref(self,urlFrom,urlTo,linkText):
		pass

	#从一组网页开始进行广度优先搜索，直至某一给定深度
	#期间为网页建立索引
	def crawl(self,pages,depth=2):
		pass

	#创建数据库表
	def createindextables(self):
		self.con.execute('create table urllist(url)')
    	self.con.execute('create table wordlist(word)')
    	self.con.execute('create table wordlocation(urlid,wordid,location)')
    	self.con.execute('create table link(fromid integer,toid integer)')
    	self.con.execute('create table linkwords(wordid,linkid)')
    	self.con.execute('create index wordidx on wordlist(word)')
    	self.con.execute('create index urlidx on urllist(url)')
    	self.con.execute('create index wordurlidx on wordlocation(wordid)')
    	self.con.execute('create index urltoidx on link(toid)')
    	self.con.execute('create index urlfromidx on link(fromid)')

def crawl(self,pages,depth=2):
	for i in range(depth):
		newpages=set()
		for page in pages:
			try:
				c=urllib.request.urlopen(page)
			except:
				print("Could not open %s"%page)
				continue
			soup=BeautifulSoup(c.read())
			self.addtoindex(page,soup)
			links=soup('a')
			for  link in links:
				if('href'in dict(link.attrs)):
					url=urljoin(page,link['href'])
					if url.find("'")!=-1:
						continue
					url=url.split('#')[0]  #去掉位置部分
					if url[0:4]=='http' and not self.isindexed(url):
						newpages.add(url)
					linkText=self.gettextonly(link)
					self.addlinkref(page,url,linkText)
			self.dbcommit()
		pages=newpages
class searcher:
	def __init__(self,dbname):
		self.con=sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def getscoredlist(self,rows,wordids):
		totalscores=dict([(row[0],0) for row in rows])
		#后面放置评价函数
		weights=[(1,self.frequencyscore(rows))]
		for (weight,scores) in weights:
			for url in totalscores:
				totalscores[url]+=weights*scores[url]
		return totalscores

	def geturlname(self,id):
		return self.con.execute("select url from urllist where rowid=%d"%id).fetchone()[0]

	def query(self,q):
		rows,wordids=self.getmatchrows(q)
		scores=self.getscoredlist(rows,wordids)
		rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
		for (score,urlid) in rankedscores[0:10]:
			print("%f\t%s"%(score,self.geturlname(urlid)))



	def getmatchrows(self,q):
		#构造查询的字符串
		fieldlist='w0.urlid'
		tablelist=' '
		clauselist=' '
		wordids=[]
		#根据空格拆分单词
		words=q.split(' ')
		tablenumber=0
		for word in words:
			#获取单词的id
			wordrow=self.con.execute("select rowid  from wordlist where word='%'"%word).fetchone()
			if wordrow!=None:
				wordid=wordi [0]
				wordids.append(wordid)
				if tablenumber>0:
					tablelist+=(',')
					clauselist+=('and')
					clauselist+=('w%d.urlid=w%d.urlid and '%(tablenumber-1,tablenumber))
				fieldlist+=(',w%d.location'%tablenumber)
				tablelist+=('wordlocation w%d' %tablenumber)
				clauselist+=('w%d.wordid=%d'%(tablenumber,wordid))
				tablenumber+=1
		#根据各个组分，建立查询
		fullquery=('select %s from %s where %s'%(fieldlist,tablenumber,clauselist))
		cur=self.con.execute(fullquery)
		rows=[row for row in cur]
		return rows,wordids

	def frequencyscore(self,rows):
		counts=dict([(row[0],0) for row in rows])
		for row in rows:
			counts[rows[0]]+=1
		return self.normalizescores(counts)

'''
select w0.urlid,w0.location,w1.location
from wordlocation w0,wordlocation w1
where w0.urlid=w1.urlid
  and w0.wordid=10
  and w1.wordid=17

'''
def normalizescores(self,scores,smallIsBetter=0):
	vsmall=0#避免被零整除
	if smallIsBetter:
		minscore=min(scores.values())
		return dict([(u,float(minscore)/max(vsmall,1)) for (u,l) in scores.items()])
	else:
		maxscore=max(scores.values())
		if maxscore==0:
			maxscore=vsmall
		return dict([(u,float(c)/maxscore) for (u,l) in scores.items()])


pagelist=['http://opac.nufe.edu.cn/opac/search.php']
crawler=crawler(' ')
print(crawler.crawl(pagelist))
