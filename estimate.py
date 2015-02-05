# coding=utf-8
# estimate.py
#作者：ryan，时间：2014年10月24号

from __future__ import division
import MySQLdb
import os

#计算查全率，R
def calculR(key,calculkey):   
    o=0
    for i in range(0,len(calculkey)):
        for terms in calculkey[i]:  
            if key[i].count(terms)!=0:
                o+=1
    div=0
    for i in range(0,len(key)):
        for j in range(0,len(key[i])):
            div+=1
    print 'R:'+str(o/div)
    return o/div


#计算准确率，P
def calculP(key,calculkey):
    o=0
    div=0
    for i in range(0,len(calculkey)):
        for terms in calculkey[i]:
            div+=1
            if key[i].count(terms)!=0:
                o+=1
    print 'P:'+str(o/div)
    return o/div

def calculF(trainkey,testkey):
    R=calculR(trainkey,testkey)
    P=calculP(trainkey,testkey)
    print 'F:'+str((2*P*R)/(P+R))

if __name__=="__main__":
    db = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="train",charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT keydata,testkeydata1 FROM train.testdata")
    result = cursor.fetchall()
    key=[]
    testkey=[]
    filename=[]
    for term in result:
        key.append(term[0].split(','))
        testkey.append(term[1].split(',')[:15])
    calculF(key,testkey)

            






    
    
