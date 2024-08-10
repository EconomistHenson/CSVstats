# test out the categorical variables

import CSVsamp

WIN10 = True



def test4_1():
    # test with empty dataframe
    tst4 = CSVsamp.CatCum()
    assert tst4.recno == 0
    # unknown category is still a category
    retval = tst4.addCat('1')
    # will include Nocat and 1 at this point
    assert tst4.catnum == 2
    retval =  tst4.addcelldata("1") 
    print('*** 14 retval=',retval)
    assert tst4.minchar == 1
    assert tst4.maxchar == 1
    retval = tst4.addCell("")
    assert retval == False
    # not that the DateCum object will not update recno
    # this will rest with the CSVsampFile
    assert tst4.NAcnt == 1 

def test4_2A():
    if WIN10:
        tst4Afil = "".join(['.\\','testfiles\\','libre2by1c.csv'])
    else:
        tst2fil = '.\testfiles\libre2by2imple.csv'
    # csv file has two records with no header
    tst4A = CSVsamp.CSVsampFile(tst4Afil)
    assert tst4A.InHdl is None
    tst4A.openInPath()
    assert tst4A.InHdl is not None
    tst4A.setCumField(1,'asCat')
    tst4A.CumDict[1].addCat('TRUE')
    tst4A.CumDict[1].addCat('FALSE')
    tst4A.getSamp()  
    # input file had two row and one column
    assert tst4A.InMaxRow == 2
    assert tst4A.InMaxCol == 1
    retval = tst4A.showRes()
    
    print(retval)

def test4_2():
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre5by2c.csv'])
    else:
        tst2fil = '.\testfiles\libre2by2imple.csv'
    # csv file has five records with no header
    tst4 = CSVsamp.CSVsampFile(tst4fil)
    assert tst4.InHdl is None
    tst4.openInPath()
    assert tst4.InHdl is not None
    tst4.setCumField(1,'asCat')
    tst4.getSamp()  
    assert tst4.InMaxRow == 5
    retval = tst4.showRes()
    print(retval)

def test4_3():
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre5by2c.csv'])
    else:
        tst4fil = '.\testfiles\libre2by2imple.csv'
    # csv file has five records with no header
    tst4C = CSVsamp.CSVsampFile(tst4fil)
    assert tst4C.InHdl is None
    tst4C.openInPath()
    assert tst4C.InHdl is not None
    tst4C.setCumField(1,'asCat')
    tst4C.setCumField(2,'asCat')
    tst4C.getSamp()  
    assert tst4C.InMaxRow == 5
    print('*** 57 ',tst4C.InMaxCol)
    assert tst4C.InMaxCol == 2
    tst4C.showRes()

def test4_4():
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre5by2c.csv'])
    else:
        tst4fil = '.\testfiles\libre3by2.csv'
    # no header two columns of categories
    # one column letters another boolean
    
    tst4D = CSVsamp.CSVsampFile(tst4fil)
    assert tst4D.InHdl is None
    tst4D.openInPath()
    assert tst4D.InHdl is not None
    tst4D.setCumField(1,'asCat')
    tst4D.CumDict[1].addCat('A')
    tst4D.CumDict[1].addCat('B')
    tst4D.CumDict[1].addCat('C')
    tst4D.setCumField(4,'asCat')
    tst4D.CumDict[2].addCat('TRUE')
    tst4D.CumDict[2].addCat('FALSE')
    tst4D.getSamp()  
    assert tst4D.InMaxRow == 5
    assert tst4D.InMaxCol == 2
    print('*** 104 in tst4',tst4D.CumDict[1].minchar)
    print('*** 105 in tst4',tst4D.CumDict[2].minchar)
    print('*** 106 in tst4',tst4D.CumDict[1].maxchar)
    print('*** 107 in tst4',tst4D.CumDict[2].maxchar)    
    # A,B,C plus NoCat gives catnum = 4
    assert tst4D.CumDict[1].catnum == 4
    # TRUE, FALSE plus NoCat catnum = 3
    assert tst4D.CumDict[2].catnum == 3
    print('*** 86 ', tst4D.CumDict[1].catDict['C'])
    print('*** 87 ', tst4D.CumDict[1])
    # test cat c first as it is the simplest
    assert str(tst4D.CumDict[1].catDict['C']) == 1
    assert tst4D.CumDict[1].catDict['A']==2
    assert tst4D.CumDict[1].catDict['B']==2
    assert tst4D.CumDict[2].catDict['TRUE']==2
    assert tst4D.CumDict[2].catDict['FALSE']==3
    tst4D.showRes()

# test4_1()
# test4_2()
# test4_2A()
# test4_3()
test4_4()


 
print('completed tst4samp.py')    
   

 