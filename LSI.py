__author__ = 'penghao'
import numpy  as np
from scipy import sparse
from scipy import linalg
from numpy.linalg import inv
from operator import itemgetter, attrgetter, methodcaller

def setK(U,S,V,k):
    newU = U[:,:k]
    newS = S[:k]
    newV = V[:k,:]
    return newU, newS, newV

def getQuery(query):
    f2 = open('vocabulary.txt', 'r')
    l = [ map(str,line.split()) for line in f2 if line.strip() != "" ]

    #query = ['compnetwork']
    list = []
    for element in l[0]:
        if element in query:
            list.append(1)
        else:
            list.append(0)
    return list

def getRandomQuery(querynum,queryLen):
    l= [0]*23480

    #randomQuery = np.array.zeros(23480)
    np.random.seed(0)
    randomQuery = np.zeros((querynum,23480))

    s = np.random.random_integers(0,23479, size=(querynum,queryLen))
    for i in range(querynum):
        for num in s[i]:
            randomQuery[i][num] = 1

    return randomQuery

def tfcosineList(L,randomQuery): # L is original list of tfidf
    tfidf = L
    #print L.shape
    test = randomQuery
    tfcosineList=[]
    #print tfidf.shape
    for i in range (tfidf.shape[1]):
        c = np.dot(tfidf.T[i],test)/linalg.norm(tfidf.T[i])/linalg.norm(test)
        tfcosineList.append((c,i))
        #print (c,i)
    tfcosineList = sorted(tfcosineList,key=itemgetter(0),reverse=True)
    totalList = []
    for idx in range(len(tfcosineList)):
        if tfcosineList[idx][0]>0: #set the cosine
            #print cosineList[idx]
            totalList.append(tfcosineList[idx][1]+1)
    return len(totalList)

def getCosine(ainS, U, V,count,q):

    #print list
    #q = np.array(list)
    #q = inv(q)
    #print q.shape
    q2 = np.dot(q,U)
    q3 = np.dot(q2,ainS)
    cosineList =[]
    # Use every column in the V, V[;,i] should work same
    for i in range(V.shape[1]):# how many document
        c = np.dot(q3,V.T[i])/linalg.norm(q3)/linalg.norm(V.T[i])
        cosineList.append((c,i))
        #print c, i
    cosineList = sorted(cosineList,key=itemgetter(0),reverse=True)
    topList = []
    totalList  = [] #total list contain all the reulsts that cosine similirity > 0
    for idx in range(len(cosineList)):
        if cosineList[idx][0]>0: #set the cosine
            #print cosineList[idx]
            totalList.append(cosineList[idx][1]+1)
        if idx <count:
            #print cosineList[idx]
            topList.append(cosineList[idx][1]+1)
    return topList, totalList

def evaluation(idx):
    f = open ( 'output2.txt' , 'r')
    l = [ map(str,line.split()) for line in f if line.strip() != "" ]
    resultList = []
    for element in l:
        #print element[2]
        if int (element[0]) == idx:
            resultList.append(int(element[2]))
    return resultList

def bestK(S): #The first idx(th) element of S have a higher weight, this function aims to calulate the idx that effect the S more
    totoal = 0
    length = S.shape[0]
    k_total =0
    for idx in range(length):
        totoal += S[idx] * S[idx]
    for idx in range(length):
        k_total += S[idx] * S[idx]
        weight = k_total/totoal
        #print weight
        if weight > 0.95:
            print idx
            return idx
            break

def evaluateAveRecall(randomQuery):
    totalTFRecall = 0
    totalLSIRecall = 0
    i =0
    for query in randomQuery:
        tf = tfcosineList(L,query) #number of recall
        top, lsi = getCosine(ainS, newU, newV,0,query)
        lsiLength = len(lsi)
        i = i + 1
        totalTFRecall += tf
        totalLSIRecall += lsiLength
        #print (tf,lsiLength)
    aveTFRecall = float(totalTFRecall)/float(i)
    aveLSIRecall = float(totalLSIRecall)/float(i)
    return aveTFRecall, aveLSIRecall

if __name__ == '__main__':
    f = open ( 'output.txt' , 'r')
    l = [ map(float,line.split()) for line in f if line.strip() != "" ]
    L = np.array(l)
    '''
    U, S, V = np.linalg.svd(L,full_matrices=False)
    newU,newS,newV = setK(U,S,V,850)
    diaS = np.diag(newS)
    ainS = inv(diaS)
    qList = getQuery(['compnetwork'])
    q = np.array(qList)
    tf = tfcosineList(L,q)
    top, lsi = getCosine(ainS, newU, newV,0,q)
    lsiLength = len(lsi)
    print (tf,lsiLength)
    print bestK(S)
    listofQ = []
    for querylen in (1,10,50,100,300,500,1000,3000,5000,15000):

        randomQuery = getRandomQuery(100,querylen) # query num and query length
        aveTFRecall, aveLSIRecall =evaluateAveRecall(randomQuery)
        listofQ.append([aveTFRecall, aveLSIRecall])
        print aveTFRecall, aveLSIRecall
    np.savetxt('test.txt', listofQ, fmt='%s')

'''
# V is document
    U, S, V = np.linalg.svd(L,full_matrices=False)
    i = bestK(S)
    print i
    queryList = [['tcp'],['cloud'],['entiti'],['erfanfar'],['entiti'],['formal'],['jami'],['peopl'],['pedest'],['compnetwork'],['program'],['proven'],['schroll'],['signum'],['spring2004'],['swarthmor'],['testingtool'],['vassamedia'],['wheelchair'],['shelv'],['sharon'],['googlesearch'],['delaunai'],['brief'],['endem'],['fayyad']]
    aAveList = []
    pAveList = []
    rAVeList = []
    fAveList = []
    for k in (10,50,100,200,350,500,650,800,850,1000,1200,1400,1600,1800,2000,2300,2500):
        accList = []
        preList =[]
        recallList = []
        fList =[]
        kList = []
        for i in range(1,9):
            print "     " + str(k)
            kList.append(k)
            newU,newS,newV = setK(U,S,V,k)
            diaS = np.diag(newS)
            ainS = inv(diaS)
            resultList = evaluation(i)
            qList = getQuery(queryList[i-1])
            q= np.array(qList)
            topList , totalList = getCosine(ainS,newU,newV,len(resultList),q) #length of the right list

            print "accuracy: "
            count = 0
            for element in topList:
                if element in resultList:
                    count = count + 1
            ac = float(count)/float(len(resultList))
            accList.append(ac)
            print ac
            pcount = 0
            print "Precision: "
            for element in totalList:
                if element in resultList:
                    pcount = pcount + 1
            precision = float(pcount)/float(len(totalList))
            preList.append(precision)
            print precision
            rCount = 0
            print "Recall: "
            for element in totalList:
                if element in resultList:
                    rCount = rCount + 1
            recall = float(rCount)/float(len(resultList))
            recallList.append(recall)

            print recall
            if precision+recall != 0:
                Fscore = 2*(precision*recall)/(precision+recall)
            else :
                Fscore = 0
            fList.append(Fscore)
            print "Fscore: "
            print Fscore

        aAveList.append(np.average(accList))
        pAveList.append(np.average(preList))
        rAVeList.append(np.average(recallList))
        fAveList.append(np.average(fList))

        print "accuracy", k
        for a in aAveList:
            print a
        print 'precision'
        for a in pAveList:
            print a
        print 'recall'
        for a in rAVeList:
            print a
        print 'fscore'
        for a in fAveList:
            print a
