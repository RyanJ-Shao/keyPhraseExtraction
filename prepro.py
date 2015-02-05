# coding=utf-8
# prepro.py
#作者：ryan，时间：2014年9月4号
from __future__ import division
import string
import os
from nltk.stem.porter import PorterStemmer
import nltk

#预处理：将全部文本写入一个文本，每个文本占一行
def alltext(documentpath,writepath):
    f=open(writepath,'w')
    for file in os.listdir(documentpath):
        s=open(os.path.join(documentpath,file),'r').read().replace('\n',' ').encode('utf-8')
        f.write(s+'\n')

#对全文进行stemming
def stem(documentpath,writepath):   
    for file in os.listdir(documentpath):
        print file
        text=''
        s=open(os.path.join(documentpath,file),'r').read().decode('utf-8')
        tokens=nltk.word_tokenize(s)
        for i in range(0,len(tokens)):
            text=text+PorterStemmer().stem_word(str(tokens[i]).lower())+' '
        f=open(os.path.join(writepath,file),'w')
        f.write(text.encode('utf-8'))
        f.close



#将全部文本停词，生成bigram和trigram，写入文本:
def lscall(alltext,writepath,stopword):
    stoplist=open(stopword,'r').read().decode('utf8').split('\n')
    alls = open(alltext,'r').read().decode('utf-8')
    print '分词'
    alldocu=nltk.word_tokenize(alls)
    print 'stop words!'
    for i in range(0,len(alldocu)) :#停词
        if stoplist.count(alldocu[i])!=0:
            alldocu[i]=0
        if i%10000==0:
            print '已完成:'
            print i/len(alldocu)
    splitall=[]
    s=''
    for i in range(0,len(alldocu)):#将相邻的词汇放在一个单元中
        if alldocu[i]!=0:
            s=s+str(alldocu[i])
            if (i+1)!=len(alldocu):
                if alldocu[i+1]!=0:
                    s=s+','
                else:
                    splitall.append(s)
        else:
            s=''
            continue
    
    lscall=[]
    for term in splitall:#对每个单元进行循环
        #print term
        win=0
        if len(term.split(','))<=3:
            win=len(term.split(','))
        else:win=3
        for i in range(1,win+1):#按照每个单元的词汇数量从小到大生成序列
            for j in range(0,len(term.split(','))):#计算文本的i序列
                o=''
                jjj=j
                for jj in range(0,i):
                    o=o+term.split(',')[jjj]
                    if (jj+1)!=i:
                        o=o+','
                    jjj+=1
                #print o
                lscall.append(o)
                if (j+i)==len(term.split(',')):
                    break
    f=open(writepath,'w')
    i=0
    lscnew=list(set(lscall))
    lscall3=[]
    for term in lscall:
        if len(term.split(','))==3:
            lscall3.append(term)
    for term in lscnew:
        ta=[]
        fb=0
        i=i+1
        if i%100==0:
            print '已完成:'
            print i/len(lscnew)
        if len(term.split(','))==3:#term+词频
            f.write((term+'~~'+str(lscall3.count(term))+'\n').encode('utf-8'))
        if len(term.split(','))==2:
            for termall in lscall3:#计算ta和fb
                if termall.count(term)!=0:
                    ta.append(termall)
            fb=len(ta)#fb
            ta=list(set(ta))#ta
            f.write((term+'~~'+str(fb)+' '+str(len(ta))+'\n').encode('utf-8'))   
    f.close()
          

#计算括号对在句法树字符串中的位置,参数s为句法分析后的单句子
def getloca(s):
    s=list(s)
    localst=[]#存储括号对的位置
    for i in range(0,len(s)):
        linshis=''
        j=0
        #从前向后遍历，当遇到’）‘时，即向前找对应的’（‘,然后将位置记录，替换为replaced
        if cmp(')',s[i])==0:
            j=i
            while j>=0:
                j-=1
                if cmp(s[j],'(')==0:
                    break
            for jj in range(j+1,i):
                    linshis=linshis+s[jj]
            if linshis.count('replaced')!=0:#从’（‘向后遍历，将节点名称记录，遇到第一个’）‘时停止,含有replaced就代表不是叶子节点
                linshis=''
                for jj in range(j+1,i):
                    if cmp(s[jj],'replaced')==0:
                        break
                    linshis=linshis+s[jj]
                #判断节点内是否含有词
                if len(linshis.strip().split())>1:
                    localst.append(str(j)+','+str(i)+','+linshis.strip().split(' ')[1]+','+'leaf')
                else:
                    localst.append(str(j)+','+str(i)+','+linshis.strip())
            else:#叶子节点
                linshis=''
                for jj in range(j+1,i):
                    linshis=linshis+s[jj]
                localst.append(str(j)+','+str(i)+','+linshis.split(' ')[1]+','+'leaf')
            s[j]='replaced'
            s[i]='replaced'
    return localst
#将经过句法分析的句子进行解析，计算节点之间的距离，并且不计算路径经过倒数第二个节点的叶子节点的距离。
def nodelength(s):
    localst=[]#括号对位置
    localst=getloca(s)
    nodelen=[]
    for i in range(0,len(localst)-1):
        if len(localst[i].split(','))<4:
            continue
        for j in range(i+1,len(localst)):
            if len(localst[j].split(','))<4:
                continue
            fanode=[]
            linshiloca=[]#父节点与子节点之间的节点
            linshilocai=[]#i节点的父节点
            linshilocaj=[]#j节点的父节点
            linshilen=[]
            #当j节点是i的父节点
            if string.atof(localst[j].split(',')[0])<string.atof(localst[i].split(',')[0]) and string.atof(localst[j].split(',')[1])>string.atof(localst[i].split(',')[1]):
                for jj in range(0,len(localst)):
                    if string.atof(localst[j].split(',')[0])<string.atof(localst[jj].split(',')[0])<string.atof(localst[i].split(',')[0]) and string.atof(localst[j].split(',')[1])>string.atof(localst[jj].split(',')[1])>string.atof(localst[i].split(',')[1]):
                        linshiloca.append(localst[jj])
                nodelen.append(str(len(linshiloca)+1)+','+localst[i].split(',')[2]+' '+localst[j].split(',')[2]) 
            #j是其他节点
            else:
                if len(localst[i].split(','))==4:
                    flag=0
                    for jj in range(i+1,j):
                        if len(localst[jj].split(','))==4:
                            flag=1
                    if flag==1:
                        break
                #找出i节点和j节点的所有父节点
                for jj in range(0,len(localst)):
                    if string.atof(localst[jj].split(',')[0])<string.atof(localst[i].split(',')[0]) and string.atof(localst[jj].split(',')[1])>string.atof(localst[i].split(',')[1]):
                        linshilocai.append(localst[jj])
                    if string.atof(localst[jj].split(',')[0])<string.atof(localst[j].split(',')[0]) and string.atof(localst[jj].split(',')[1])>string.atof(localst[j].split(',')[1]):
                        linshilocaj.append(localst[jj])
                #找出i和j节点的共同父节点
                for termi in linshilocai:
                    for termj in linshilocaj:
                        if cmp(termi,termj)==0:
                            fanode.append(termi)
                #在共同父节点中找出距离最近的共同父节点
                for term in fanode:
                    linshilen.append(string.atof(term.split(',')[1])-string.atof(term.split(',')[0]))
                q=0
                linshis=0
                linshit=0
                max=0
                for ii in range(0,len(linshilen)):
                    flag=0
                    max=linshilen[ii]
                    linshis=fanode[ii]
                    for jj in range((ii+1),len(linshilen)):
                        if max<linshilen[jj]:
                            max=linshilen[jj]
                            q=jj
                            flag=1
                    if flag==1:
                        linshit=linshilen[ii]
                        linshilen[ii]=max
                        linshilen[q]=linshit
                        fanode[ii]=fanode[q]
                        fanode[q]=linshis
                #计算最近父节点与root节点的距离，若是1就break
                two=[]
                for jj in range(0,len(localst)):
                    if string.atof(localst[len(localst)-1].split(',')[0])<string.atof(localst[jj].split(',')[0])<string.atof(fanode[len(fanode)-1].split(',')[0]) and string.atof(localst[len(localst)-1].split(',')[1])>string.atof(localst[jj].split(',')[1])>string.atof(fanode[len(fanode)-1].split(',')[1]):
                        two.append(localst[jj])
                if len(two)==0:
                    break
                #计算i和父节点之间的距离
                linshilocaii=[]
                linshilocajj=[]
                for jj in range(0,len(localst)):
                    if string.atof(fanode[len(fanode)-1].split(',')[0])<string.atof(localst[jj].split(',')[0])<string.atof(localst[i].split(',')[0]) and string.atof(fanode[len(fanode)-1].split(',')[1])>string.atof(localst[jj].split(',')[1])>string.atof(localst[i].split(',')[1]):
                        linshilocaii.append(localst[jj])
                for jj in range(0,len(localst)):
                    if string.atof(fanode[len(fanode)-1].split(',')[0])<string.atof(localst[jj].split(',')[0])<string.atof(localst[j].split(',')[0]) and string.atof(fanode[len(fanode)-1].split(',')[1])>string.atof(localst[jj].split(',')[1])>string.atof(localst[j].split(',')[1]):
                        linshilocajj.append(localst[jj])
                nodelen.append(str(len(linshilocaii)+len(linshilocajj)+2)+','+localst[i].split(',')[2]+' '+localst[j].split(',')[2])
    return nodelen

#对待计算文本分词，过滤标点符号，然后写入文本
def getsen(filename,writefilename):
    ls=nltk.word_tokenize(open(filename,'r').read().decode('utf-8'))#分词
    for i in range(0,len(ls)) :#用零替换所有的标点符号
        li=list(ls[i])
        flag=0
        for lii in li:
            if str(lii).isalpha() is True:
                flag=1
        if flag==1:
            continue
            #ls[i]=PorterStemmer().stem_word(str(ls[i]))
        else:ls[i]=0 
    splitall=[]
    s=''
    for i in range(0,len(ls)):#将相邻的词汇放在一个单元中
        if ls[i]!=0:
            s=s+ls[i]
            if (i+1)!=len(ls):
                if ls[i+1]!=0:
                    s=s+' '
                else:
                    splitall.append(s)
        else:
            s=''
            continue
    #将处理后的句子写入文本，进行句法分析
    f=open(writefilename,'w')
    for term in splitall:
        f.write((term+'\n').encode('utf-8'))
    f.close()

#对每个文本进行分句,然后进行句法分析
def sepsen(documentpath,writepath):
    for file in os.listdir(documentpath):
        print file
        getsen(os.path.join(documentpath,file),os.path.join(writepath,file))

#计算文本中重复出现的节点的平均距离
def avglen(lenlist):
    lenlists=list(set(lenlist))
    for i in range(0,len(lenlists)):
        link=[]
        for terms in lenlist:
            if cmp(lenlists[i].split(',')[1],terms.split(',')[1])==0:
                link.append(terms)
        if len(link)>1:
            summ=0
            for li in link:
                summ=summ+string.atof(li.split(',')[0])
            lenlists[i].split(',')[0]=(str(summ/len(link)))
    return lenlists

#计算每个句法分析后的文本中，节点两两间的距离，写入文本
def leng(parseredpath,writepath):
    for file in os.listdir(parseredpath):
        alllen=[]
        print file
        line=open(os.path.join(parseredpath,file),'r').read().decode('utf-8').split('\n')
        for term in line:
            alllen.extend(nodelength(term))
        alllen=avglen(alllen)
        for i in range(0,len(alllen)):
            alllen[i]=alllen[i].split(',')[1]+','+alllen[i].split(',')[0]
        f=open(os.path.join(writepath,file),'w')
        for term in alllen:
            if alllen.index(term)==len(alllen)-1:
                f.write(term.encode('utf-8'))
            else:
                f.write((term+'\n').encode('utf-8'))
        f.close()



#对alllen中的词汇进行stemming
def lenstem(readpath,writepath):
    for file in os.listdir(readpath): 
        text=open(os.path.join(readpath,file),'r').read().decode('utf-8').split('\n')
        s=''
        f=open(os.path.join(writepath,file),'w')
        for term in text:
            waitstem=nltk.word_tokenize(term.split(',')[0])
            for words in waitstem:
                s=s+PorterStemmer().stem_word(str(words).lower())+' '
            f.write((s.strip()+','+term.split(',')[1]+'\n').encode('utf-8'))
            s=''
    f.close()


if __name__=="__main__":
    #-2.对所有文本stemming，写入新的文本
    #stem('E:\\KeyExtraction\\engParser\\calculcandidate\\waitparser','E:\\KeyExtraction\\engParser\\calculcandidate\\stemmed')   
    #-1.合并所有文本，每个文本占一行,需要stemming
    #alltext('E:\\KeyExtraction\\engParser\\calculcandidate\\stemmed','E:\\KeyExtraction\\engParser\\calculcandidate\\alltext-test.txt')
    #0.读入所有文本，分词，停词，将相邻的词汇放一起，生成2元，3元组合，需要stemming
    #lscall('E:\\KeyExtraction\\engParser\\calculcandidate\\alltext-test.txt','E:\\KeyExtraction\\engParser\\calculcandidate\\lscall-test.txt','E:\\KeyExtraction\\engParser\\calculcandidate\\sl.txt')
    #1.对所有文本分句，写入文件夹，不需要stemming
    #sepsen('E:\\KeyExtraction\\engParser\\calculcandidate\\document-test','E:\\KeyExtraction\\engParser\\calculcandidate\\waitparser')
    #2.调用句法分析器对所有文本进行句法分析，然后写入文件夹
    #3.对所有句法分析后的文本计算两两节点的距离，对重复出现的短语计算在一片文章范围内的平均值
    leng('F:\\Desktop\\report\\parsered','F:\\Desktop\\report')
    #4.对alllen中的词汇进行stemming
    #lenstem('E:\\KeyExtraction\\engParser\\calculcandidate\\alllen','E:\\KeyExtraction\\engParser\\calculcandidate\\stemmedalllen')
    


