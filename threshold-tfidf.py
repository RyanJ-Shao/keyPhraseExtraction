# coding=utf-8
# tfidf.py
#作者：ryan，时间：2014年10月26号
from __future__ import division
import nltk
import os
import math
import MySQLdb
import string
import sys
from nltk.stem.porter import PorterStemmer

#计算TF
def calculTF(str,filename):
    f = open(filename,'r')
    s=f.read().decode('utf-8')
    tf=[]
    ls=str
    for term in ls:
        res=s.count(term)
        #res=s.count(term)/len(s)
        tf.append(res)
    return tf



#计算IDF,文件夹下所有文本提前写入一个文本，每个文本占一行
def calculIDF(str,idfpath):
    #读入预先处理的文本
    docli=open(idfpath,'r').read().decode('utf-8').split('\n')
    idf=[]
    ls=str
    for term in ls:
        i=0
        for text in docli:
            if text.count(term)!=0:
                i+=1
        idf.append(math.log((len(docli)+1)/(i+1),2))
    return idf

#计算tfif
def tfidf(ls,TFfilename,tfwritepath,idfwritepath,IDFidfpath):
    tf=calculTF(ls,TFfilename)
    idf=calculIDF(ls,IDFidfpath)
    tfidf=[]
    #写入TF
    f=open(tfwritepath,'w')
    for i in range(0,len(ls)):
        if i==len(ls)-1:f.write((ls[i]+','+str(tf[i])).encode('utf-8'))
        else:f.write((ls[i]+','+str(tf[i])+'\n').encode('utf-8'))
    f.close()
    #写入IDF
    f=open(idfwritepath,'w')
    for i in range(0,len(ls)):
        if i==len(ls)-1:f.write((ls[i]+','+str(idf[i])).encode('utf-8'))
        else:f.write((ls[i]+','+str(idf[i])+'\n').encode('utf-8'))
    f.close()
    '''
    for i in range(0,len(tf)):
        tfidf.append(tf[i]*idf[i])
    
    #对tfidf进行排序,从大到小
    q=0
    for i in range(0,len(tfidf)):
        flag=0
        max=tfidf[i]
        linshis=ls[i]
        for j in range((i+1),len(tfidf)):
            if max<tfidf[j]:
                max=tfidf[j]
                q=j
                flag=1
        if flag==1:
            linshit=tfidf[i]
            tfidf[i]=max
            tfidf[q]=linshit
            ls[i]=ls[q]
            ls[q]=linshis
    '''
    return ls


def is_alphabet(uchar):

        """判断一个unicode是否是英文字母"""

        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):

            return False

        else:

            return True
#词性过滤，保留名词、形容词
def pos(s,stopword):
    stoplist=open(stopword,'r').read().decode('utf8').split('\n')
    print 'POS'
    text = nltk.word_tokenize(s)
    for i in range(0,len(text)):#停词
        #print '11:'+text[i]
        if stoplist.count(text[i].lower())!=0:
            #print '22:'+text[i]
            text[i]=0
        if text[i]!=0:
            a=list(text[i])
            for term in a :
                if is_alphabet(term):
                    text[i]=0
    splitls=[] #切分后的词汇list
    s=''
    for i in range(0,len(text)):#将相邻的词汇放在一个单元中
        if text[i]!=0:
            #s=s+PorterStemmer().stem_word(str(pos[i][0]).lower())
            s=s+text[i]
            if (i+1)!=len(text):
                if text[i+1]!=0:
                    s=s+','
                else:
                    splitls.append(s)
        else:
            s=''
            continue
    return splitls




#def chunk(g,posinputfile,Partextlenpath,MIidftxtpath,Paralllenpath,MIwritepath,Cvwritepath,stopword):
    	    


#ngram生成当前带计算文本的2元，3元组合，调用：词性过滤函数：pos()、根据句法树的距离对句子进行组合：parsertree.textlen()、计算互信息MI()、计算cvalue()
def ngram(g,posinputfile,MIidftxtpath,Paralllenpath,MIwritepath,Cvwritepath,stopword):
    #lscall为训练集的biggram和trigram
    #读入预先处理的文本
    ones=open(posinputfile,'r').read().decode('utf-8')
    splitls=pos(ones,stopword)#调用词性标注
    lsc=[]
    for term in splitls:#对每个单元进行循环
        if len(term.split(','))<2:#过滤出单个词汇
            continue
        win=0
        if len(term.split(','))<=5:
            win=len(term.split(','))
        else:win=5
        for i in range(2,win+1):#按照每个单元的词汇数量从小到大生成序列
            for j in range(0,len(term.split(','))):#生成待计算文本的i序列
                o=''
                jjj=j
                for jj in range(0,i):
                    o=o+term.split(',')[jjj]
                    if (jj+1)!=i:
                        o=o+','
                    jjj+=1
                lsc.append(o)
                if (j+i)==len(term.split(',')):
                    break
    #调用句法分析模块，组合短语
    #sys.path.append(Partextlenpath)
    #import parsertree
    #lsc=parsertree.textlen(Paralllenpath,lsc)
    #删除不符合pos模式的组合
    ls=[]
    for term in lsc:
        s=''
        flag=0
        for terms in term.split(','):
            text = nltk.word_tokenize(terms)
            postag=nltk.pos_tag(text)
            try:
                if postag[0][1].count('NN')==0 and postag[0][1].count('VB')==0 and postag[0][1].count('JJ')==0:
                    flag=1
                
            except:
                continue
        if flag==0:
            for terms in term.split(','):
                if term.split(',').index(terms)==len(term.split(','))-1:
                    s=s+PorterStemmer().stem_word(terms.lower())
                else:
                    s=s+PorterStemmer().stem_word(terms.lower())+','
            ls.append(s)
    ls=list(set(ls))
    ls=MI(MIidftxtpath,ls,MIwritepath)
    ls=cvalue(lscpath,ls,g,Cvwritepath,MIidftxtpath)
    return ls

#计算cvalue
def cvalue(lsc,g,Cvwritepath,alltext):
    print 'Cvalue'
    cls=[]#待排除的短语
    mu=[]#需要移除的短语
    cor=open(alltext,'r').read().decode('utf-8')
    cvalue=[]
    print 'cvalue:0'
    '''
    for i in range(0,len(lsc)):
        link=[]#有关联的短语
        cv=[]#cvalue值
        link.append(lsc[i])
        for j in range(0,len(lsc)):#将相关联的词汇放到一起，link
            if cmp(lsc[i],lsc[j])!=0 and lsc[i].count(lsc[j])!=0:
                link.append(lsc[j])
        if len(link)==1:
            link=[]
            continue
        #print 'link:'+link
        flag=0
        for term in link:
            if len(link[0].split(','))!=len(term.split(',')):
                flag=1
        if flag!=1:
            continue
        else:
                #缺点：3:forthcoming,launch,event
                #2:forthcoming,launch
                #2:launch,event
            for term in link:#计算关联词汇的cvalue
                if len(str(term).split(','))==3:
                    if g.has_key(term):
                        cv.append(math.log(3,2)*string.atoi(g[term]))
                    else:
                        mu.append(term)
                if len(str(term).split(','))==2:
                    if g.has_key(term):
                        fb=string.atoi(g[term].split(' ')[0])#fb
                        ta=string.atoi(g[term].split(' ')[1])#ta
                        sss=''
                        for terms in term.split(','):
                            sss=sss+terms+' '
                        if ta==0:
                            ta=1
                        cv.append(math.log(2,2)*(cor.count(sss.strip())-fb/ta))
                    else:
                        mu.append(term)
            if len(cv)!=0:
                for term in link:
                    if link.index(term)==cv.index(max(cv)):
                        continue
                    else:mu.append(term)
    mu=list(set(mu))
    for term in mu:
        lsc.remove(term)
    '''
    print "cvalue:2"
    for term in lsc:
        sss=''
        for terms in term.split(','):
            sss=sss+terms+' '
        cvalue.append(math.log(len(term.split(',')),2)*cor.count(sss.strip()))
    for i in range(0,len(lsc)):#去除间隔逗号
        if len(lsc[i].split(','))!=1:
            s=''
            for term in lsc[i].split(','):
                   s=s+term+' '
            lsc[i]=s.strip()
    f=open(Cvwritepath,'w')
    for i in range(0,len(lsc)):
        if i==len(lsc)-1:
            f.write((lsc[i]+','+str(cvalue[i])).encode('utf-8'))
        else:
            f.write((lsc[i]+','+str(cvalue[i])+'\n').encode('utf-8'))
    f.close()
    return lsc

    
#计算互信息，从大到小排序
def MI(idftxtpath,lsc,writpath):
    print 'MI'
    import os
    import math
    alls=open(idftxtpath,'r').read().decode('utf8')
    mi=[]
    ls=[]
    num=1
    for term in lsc:
        if num%100==0:
            print '已完成:'
            print num/len(lsc)
        lo=0
        co=0
        #for terms in term.split(','):
        for allterm in alls.split('\n'):
            sumlist=[]
            for terms in term.split(','):
                sumlist.append(allterm.count(terms.strip()))
            co=co+min(sumlist)
        for terms in term.split(','):
            lo=lo+alls.count(terms)
        try:
            mi.append(co/(lo-co))
            ls.append(term)
        except:
            continue
        num=num+1
    f=open(writpath,'w')
    for i in range(0,len(ls)):
        s=''
        for term in ls[i].split(','):
            s=s+term+' '
        if i==len(ls)-1:f.write((s.strip()+','+str(mi[i])).encode('utf-8'))
        else:f.write((s.strip()+','+str(mi[i])+'\n').encode('utf-8'))
    f.close()
    return ls


def dep(filepath,ls,writepath):
    print 'DEP'
    text=''
    s=''
    s=open(filepath,'r').read().decode('utf-8')
    text = nltk.word_tokenize(s)
    f=open(writepath,'w')
    for term in ls:
        try:
            if text.index(term.split(' ')[0])==0:
                if ls.index(term)==len(ls)-1:f.write((term+','+str(0.8/len(text))).encode('utf-8'))
                else:f.write((term+','+str(0.8/len(text))+'\n').encode('utf-8'))
            else:
                if ls.index(term)==len(ls)-1:f.write((term+','+str(text.index(term.split(' ')[0])/len(text))).encode('utf-8'))
                else:f.write((term+','+str(text.index(term.split(' ')[0])/len(text))+'\n').encode('utf-8'))
        except:
            continue
    f.close()




    

#将所有特征写入文本
def writefeature(file,ls,alllenpath,idfpath,tfpath,MIpath,cvaluepath,deppath):
    alllen=open(alllenpath,'r').read().decode('utf-8').split('\n')
    IDF=open(idfpath,'r').read().decode('utf-8').split('\n')
    TF=open(tfpath,'r').read().decode('utf-8').split('\n')
    MI=open(MIpath,'r').read().decode('utf-8').split('\n')
    cvalue=open(cvaluepath,'r').read().decode('utf-8').split('\n')
    dep=open(deppath,'r').read().decode('utf-8').split('\n')
    if dep.count('')!=0:
        dep.remove('')
    if alllen.count('')!=0:
        alllen.remove('')
    #将特征值转换成字典的形式存储
    a={}#句法树上的距离
    b={}#IDF
    c={}#TF
    d={}#MI
    e={}#cvalue
    g={}#DEP
    map(lambda x:a.setdefault(x.split(',')[0], string.atof(x.split(',')[1])), alllen)
    map(lambda y:b.setdefault(y.split(',')[0], string.atof(y.split(',')[1])), IDF)
    map(lambda z:c.setdefault(z.split(',')[0], string.atof(z.split(',')[1])), TF)
    map(lambda w:d.setdefault(w.split(',')[0], string.atof(w.split(',')[1])), MI)
    map(lambda u:e.setdefault(u.split(',')[0], string.atof(u.split(',')[1])), cvalue)
    map(lambda v:g.setdefault(v.split(',')[0], string.atof(v.split(',')[1])), dep)
    #连接数据库
    db = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="train",charset='utf8')
    cursor = db.cursor()
    threshold=[]
    mo=[]
    key=''
    cv=0
    parlen=0
    mi=0
    for term in ls:
        if len(term.split(' '))==2:
            parlen=2.0
            mi=0.5
        if len(term.split(' '))==3:
            parlen=2.0
            mi=0.153793261517
        if len(term.split(' '))==4:
            parlen=2.0
            mi=0.0
        if len(term.split(' '))==5:
            parlen=2.0
            mi=0.01
        aa=0
        flag=0
        for i in range(0,len(term.split(' '))-1):
            if a.has_key(term.split(' ')[i]+' '+term.split(' ')[i+1]):
                aa=aa+a[term.split(' ')[i]+' '+term.split(' ')[i+1]]
            else:
                flag=1
        if flag==1:
            continue
        else:
            if len(term.split(' '))<parlen:
                continue
            else:aa=aa/(len(term.split(' '))-1)
        if b.has_key(term):
            bb=b[term]
        else:
            continue
        if c.has_key(term):
            cc=c[term]
        else:
            continue
        if d.has_key(term) and len(term.split(' '))>=mi:
            dd=d[term]
        else:
            continue
        if e.has_key(term) :
            ee=e[term]
        else:
            continue
        if g.has_key(term):
            ff=g[term]
        else:
            continue
        try:
            #thre=(1/aa)*len(term)*bb*cc*ee*dd
            thre=len(term)*bb*cc
            threshold.append(thre)
            mo.append(term)
            #threshold.append((1/aa)*len(term)*bb*cc*dd*ee*(1/ff))
        except:
            continue
    #对threshold进行排序,从大到小
    q=0
    for i in range(0,len(threshold)):
        flag=0
        max=threshold[i]
        linshis=mo[i]
        for j in range((i+1),len(threshold)):
            if max<threshold[j]:
                max=threshold[j]
                q=j
                flag=1
        if flag==1:
            linshit=threshold[i]
            threshold[i]=max
            threshold[q]=linshit
            mo[i]=mo[q]
            mo[q]=linshis
    for term in mo[:15]:
        key=key+term+','
    filename=file.split('.')[0]
    print key
    sql="UPDATE train.testdata SET testkeydata='%s' WHERE filename='%s'"%(key,filename)
    # 执行SQL语句
    try:
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
        print 'successful!!'
    except:
    # 发生错误时回滚
        print 'ERROR！！！'
        db.rollback()
    db.close()

if __name__=="__main__":
    #停词
    stopwordfile='E:\\KeyExtraction\\engParser\\calculcandidate\\sl.txt'
    #将此路径加入系统路径，此文件夹内涵调用的.py文件
    nowpath='E:\\python\\engParser\\calculcandidate'
    #alltext.txt路径
    alltextpath='E:\\KeyExtraction\\engParser\\calculcandidate\\alltext-test.txt'
    #lscall.txt路径
    lscallpath='E:\\KeyExtraction\\engParser\\calculcandidate\\lscall-test.txt'
    #存储互信息的文本路径
    MIpath='E:\\KeyExtraction\\engParser\\calculcandidate\\MI'
    #存储cvalue的文本
    cvaluepath='E:\\KeyExtraction\\engParser\\calculcandidate\\cvalue'
    #当前处理的文本路径
    textpath='E:\\KeyExtraction\\engParser\\calculcandidate\\document-test'
    #当前待处理文本的句法树节点的距离文本
    alllenpath='E:\\KeyExtraction\engParser\\calculcandidate\\stemmedalllen'
    #TF路径
    TFpath='E:\\KeyExtraction\\engParser\\calculcandidate\\TF'
    #IDF路径
    IDFpath='E:\\KeyExtraction\\engParser\\calculcandidate\\IDF'
    #DEP路径
    deppath='E:\\KeyExtraction\\engParser\\calculcandidate\\DEP'
    #将所有特征数据写入文本的路径
    featurepath='E:\\KeyExtraction\\engParser\\calculcandidate\\feature'
    #计算首次出现位置的当前文本，需要stemmed
    stetext='E:\\KeyExtraction\\engParser\\calculcandidate\\stemmed'
    for file in os.listdir(textpath):
        print file
        #lsc=ngram(g,os.path.join(textpath,file),alltextpath,os.path.join(alllenpath,file),os.path.join(MIpath,file),os.path.join(cvaluepath,file),stopwordfile)
        #ls=tfidf(lsc,os.path.join(stetext,file),os.path.join(TFpath,file),os.path.join(IDFpath,file),alltextpath)
        ls=open(os.path.join('E:\\KeyExtraction\\engParser\\calculcandidate\\lsc-5',file),'r').read().decode('utf8').split('\n')
        writefeature(file,ls,os.path.join(alllenpath,file),os.path.join(IDFpath,file),os.path.join(TFpath,file),os.path.join(MIpath,file),os.path.join(cvaluepath,file),os.path.join(deppath,file))
    
