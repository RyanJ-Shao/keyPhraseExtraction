# coding=utf-8
# parsertree.py
from __future__ import division
import string


def textlen(alllenpath,lscnew):#读取全部文本句法分析的结果，调用nodelength函数计算节点距离并且选出2元组合和3元组合
    import string
    alllen=[]#所有节点两两间的距离
    lsc=[]
    alllen=open(alllenpath,'r').read().decode('utf-8').split('\n')#形如(5,ab)
    bilsc=[]#2-gram组合
    trilsc=[]#3-gram组合
    for term in lscnew:#可能遇到两个句子首尾词汇相同的情况，概率很小
        if len(term.split(','))==2:
            bilsc.append(term)
            continue
        if len(term.split(','))==3:
            trilsc.append(term)
            continue
        lsc.append(term)
    print 'first!'
    mo=[]
    alen={}
    if alllen.count('')!=0:
        alllen.remove('')
    map(lambda x:alen.setdefault(x.split(',')[0], x.split(',')[1]), alllen)
    for i in range(0,len(bilsc)):#ab<bc<cd,删除bc和cd
        #print bilsc[i]
        if i+1<len(bilsc) and cmp(bilsc[i].split(',')[1],bilsc[i+1].split(',')[0])==0:
            if alen.has_key(bilsc[i].split(',')[0]+' '+bilsc[i].split(',')[1]):
                a=alen[bilsc[i].split(',')[0]+' '+bilsc[i].split(',')[1]]
            else:
                a=1000
            if alen.has_key(bilsc[i+1].split(',')[0]+' '+bilsc[i+1].split(',')[1]):
                b=alen[bilsc[i+1].split(',')[0]+' '+bilsc[i+1].split(',')[1]]
            else:
                b=1000
            if a>b:
                mo.append(bilsc[i])
            if a<b:
                mo.append(bilsc[i+1])
            #此种情况是两个节点都穿过倒数第二个节点，在alllen中找不到
            if a==b and a==1000:
                mo.append(bilsc[i])
                mo.append(bilsc[i+1])
    mo=list(set(mo))
    for term in mo:
        bilsc.remove(term)
    lsc.extend(bilsc)
    print 'second'
    for i in range(0,len(trilsc)):#ab<bc<cd,删除bc和cd
        if i+1<len(trilsc) and (cmp(trilsc[i].split(',')[2],trilsc[i+1].split(',')[0])==0 or cmp(trilsc[i].split(',')[2],trilsc[i+1].split(',')[1])==0): 
            if alen.has_key(trilsc[i].split(',')[0]+' '+trilsc[i].split(',')[1]) and alen.has_key(trilsc[i].split(',')[1]+' '+trilsc[i].split(',')[2]):
                a=alen[trilsc[i].split(',')[0]+' '+trilsc[i].split(',')[1]]
                a=a+alen[trilsc[i].split(',')[1]+' '+trilsc[i].split(',')[2]]
            else:
                a=1000
            
            if alen.has_key(trilsc[i+1].split(',')[0]+' '+trilsc[i+1].split(',')[1]) and alen.has_key(trilsc[i+1].split(',')[1]+' '+trilsc[i+1].split(',')[2]):
                b=alen[trilsc[i+1].split(',')[0]+' '+trilsc[i+1].split(',')[1]]
                b=b+alen[trilsc[i+1].split(',')[1]+' '+trilsc[i+1].split(',')[2]]
            else:
                b=1000
            if a>b:
                mo.append(trilsc[i])
            if a<b:
                mo.append(trilsc[i+1])
            if a==b and a==1000:
                mo.append(trilsc[i])
                mo.append(trilsc[i+1])
    mo=list(set(mo))
    for term in mo:
        if trilsc.count(term)==0:
            continue
        else:trilsc.remove(term)
    lsc.extend(trilsc)
    return lsc







        

if __name__=="__main__":
    lsc=open(r'e:\python\2.txt').read().decode('gbk').split('\n')
    print len(lsc)
    alllen=textlen('e:\\python\\parsered.txt',lsc)
    for i in alllen:
        print i
