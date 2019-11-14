#复用性很高的通用代码
##完美读取二维结构的数据，分离出第一行和第一列的标题，单独读取出数据
def readfile(filename):
  file=open(filename)
  lines=[line for line in file]
  
  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is the rowname
    rownames.append(p[0])
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data
blognames,word,data=readfile('C:/Users/USER/testdata.txt')###这里一定要把本地txt文件的后缀txt三个字母去掉
print(blognames,word,data)
