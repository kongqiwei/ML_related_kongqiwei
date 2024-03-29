class decisionnode:
	def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb #对应于结果是true或者false时候，树上相对于当前节点的子树的节点
		self.fb=fb

#在某一列上对数据集进行拆分，能够处理数值型数据或名词性数据
def divideset(rows,column,value):
	#定义一个函数，令其告诉我们数据行属于第一组（true)还是第二组(false)
	split_function=None
	if isinstance(value,int) or isinstance(value,float):
		split_function=lambda row:row[column]>=value
	else:
		split_function=lambda row:row[column]==value
	#将数据集拆分成两个集合，并返回
	set1=[row for row in rows if split_function(row)]
	set2=[row for row in rows if not split_function(row)]
	return (set1,set2)

#对各种可能的结果进行计数（每一行的最后一列记录了这一计数结果
def uniquecounts(rows):
	results={}
	for row in rows:
		#计数结果在最后一列
		r=row[len(row)-1]
		if r not in results:
			results[r]=0
		results[r]+=1
	return results

#随机放置的数据项出现于错误类中的概率
def giniimpurity(rows):
	total=len(rows)
	counts=uniquecounts(rows)
	imp=0
	for k1 in counts:
		p1=float(counts[k1])/total
		for k2 in counts:
			if k1==k2:
				continue
			p2=float(counts[k2])/total
			imp+=p1*p2
	return imp

#熵是遍历所有可能的结果后u所得到的的概率之和
def entropy(rows):
	from math import log
	log2=lambda x:log(x)/log(2)
	results=uniquecounts(rows)
	#计算熵值
	ent=0
	for r in results.keys():
		p=float(results[r])/len(rows)
		ent=ent-p*log2(p)
	return ent

def buildtree(rows,scoref=entropy):
	if len(rows)==0:
		return decisionnode()
	current_score=scoref(rows)
	#定义一些变量记录最佳拆分条件
	best_gain=0
	best_criteria=None
	best_sets=None
	column_count=len(rows[0])-1
	for col in range(0,column_count):
		#在当前列中生成一个由不同值构造的序列
		column_values={}
		for row in rows:
			column_values[row[col]]=1
			#接下来根据这一列中的每一个值，尝试对数据集进行拆分
		for value in column_values.keys():
			(set1,set2)=divideset(rows,col,value)
			#信息增益
			p=float(len(set1))/len(rows)
			gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
			if gain>best_gain and len(set1)>0 and len(set2)>0:
				best_gain=gain
				best_criteria=(col,value)
				best_sets=(set1,set2)
	#创建子分支
	if best_gain>0:
		trueBranch=buildtree(best_sets[0])
		falseBranch=buildtree(best_sets[1])
		return decisionnode(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
	else:
		return decisionnode(results=uniquecounts(rows))

def classify(observation,tree):
	if tree.results!=None:
		return tree.results
	else:
		v=observation[tree.col]
		branch=None
		if isinstance(v,int) or isinstance(v,float):
			if v>=tree.value:
				branch=tree.tb
			else:
				branch=tree.fb
		else:
			if v==tree.value:
				branch=tree.tb
			else:
				branch=tree.fb
		return classify(observation,branch)

def prune(tree,mingain):
	#如果分支不是叶节点，则对其进行剪枝操作
	if tree.tb.results==None:
		prune(tree.tb,mingain)
	if tree.fb.results==None:
		prune(tree.fb,mingain)
	#如果两个子节点都是叶节点，则判断他们是否要合并
	if tree.tb.results!=None and tree.fb.results!=None:
		#构造合并后的数据集
		tb,fb=[],[]
		for v,c in tree.tb.results.items():
			tb+=[[v]]*c
		for v,c in tree.fb.results.items():
			fb+=[[v]]*c
		#检查熵的减少情况
		delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)
		if delta<mingain:
			#合并分支
			tree.tb,tree.fb=None,None
			tree.results=uniquecounts(tb+fb)
			
