# test with Covid data plus progress reporter

import CSVsamp

WIN10 = True



def test5_1(): 
    if WIN10:
        fName = 'vaccination-administration-bydosenumber_grouped.csv'
        tst5fil = "".join(['..\\C19\\vacines\\',fName])
    else:
        tst2fil = '.\test\libre2by2imple.csv'
    # csv file has two records with no header
    tst5 = CSVsamp.CSVsampFile(tst5fil)
    assert tst5.InHdl is None
    tst5.openInPath()
    assert tst5.InHdl is not None
    tst5.setCumField(7,'asQuant')
    tst5.getSamp()  
    assert tst5.InMaxRow > 5000
    retval = tst5.showRes()
    print(retval)


def test4_3():
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre5by2c.csv'])
    else:
        tst4fil = '.\testfiles\libre2by2imple.csv'
    # csv file has two records with no header
    tst4 = CSVsamp.CSVsampFile(tst4fil)
    assert tst4.InHdl is None
    tst4.openInPath()
    assert tst4.InHdl is not None
    tst4.setCumField(1,'asCat')
    tst4.setCumField(2,'asCat')
    tst4.getSamp()  
    assert tst4.InMaxRow == 5
    print(tst4.InMaxCol)
    assert tst4.InMaxCol == 2
    tst4.showRes()

def test4_4():
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre5by2c.csv'])
    else:
        tst4fil = '.\testfiles\libre3by2.csv'
    # no header two columns of categories
    # one column letters another boolean
    
    tst4 = CSVsamp.CSVsampFile(tst4fil)
    assert tst4.InHdl is None
    tst4.openInPath()
    assert tst4.InHdl is not None
    tst4.setCumField(1,'asCat')
    tst4.CumDict[1].addCat('A')
    tst4.CumDict[1].addCat('B')
    tst4.CumDict[1].addCat('C')
    tst4.setCumField(2,'asCat')
    tst4.CumDict[2].addCat('TRUE')
    tst4.CumDict[2].addCat('FALSE')
    tst4.getSamp()  
    assert tst4.InMaxRow == 5
    assert tst4.InMaxCol == 2
    # A,B,C plus NoCat gives catnum = 4
    assert tst4.CumDict[1].catnum == 4
    assert tst4.CumDict[2].catnum == 3
    assert tst4.CumDict[1].catDict['A']==2
    assert tst4.CumDict[1].catDict['B']==2
    assert tst4.CumDict[1].catDict['C']==1
    assert tst4.CumDict[2].catDict['TRUE']==2
    assert tst4.CumDict[2].catDict['FALSE']==3
    tst4.showRes()

# test4_1()
# test4_2()
# test4_3()
test5_1()


 
print('completed tst5samp.py')    
   

 