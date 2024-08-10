import CSVsamp

WIN10 = True



def test3_1():
    # create 2 by 1 CSV plus one NA
    tst3 = CSVsamp.DateCum()
    assert tst3.recno == 0
    # should go up one with the addition of single record
    retval =  tst3.addcelldata("2023-04-01") 
    assert tst3.minchar == 10
    assert tst3.maxchar == 10
    retval = tst3.addCell("")
    assert retval == False
    # not that the DateCum object will not update recno
    # this will rest with the CSVsampFile
    assert tst3.NAcnt == 1 

def test3_2():
    if WIN10:
        tst2fil = "".join(['.\\','testfiles\\','libre2by1simple.csv'])
    else:
        tst2fil = '.\testfiles\libre2by2imple.csv'
    # csv file has two records with no header
    tst2 = CSVsamp.CSVsampFile(tst2fil)
    assert tst2.InHdl is None
    tst2.openInPath()
    assert tst2.InHdl is not None
    # tst2.setCumField(1,'asQuant')
    tst2.InCntRow = 0
    print('*** 33',tst2.InMaxRow)
    tst2.getSamp()  
    print('*** 35',tst2.InMaxRow)
    assert tst2.InMaxRow == 2
    tst2.showRes()

def test3_3():
    if WIN10:
        tst3fil = "".join(['.\\','testfiles\\','libre2by2simple.csv'])
    else:
        tst3fil = '.\testfiles\libre2by2imple.csv'
    # csv file has two records with no header
    tst3 = CSVsamp.CSVsampFile(tst3fil)
    assert tst3.InHdl is None
    tst3.openInPath()
    assert tst3.InHdl is not None
    tst3.setCumField(1,'asQuant')
    tst3.setCumField(2,'asQuant')
    print('*** 52',tst3)
    tst3.getSamp() 
    print('*** junk 54')
    print(tst3)
    print('*** junk') 
    print('*** 57 NaCnt = ',tst3.CumDict[1].NAcnt)
    print('*** 58 recno = ',tst3.CumDict[1].recno)
    print('*** 59 NaCnt = ',tst3.CumDict[2].NAcnt)
    print('*** 60 recno = ',tst3.CumDict[2].recno)
    if tst3.InMaxRow != 2:
        assert Fail
    else:
        print('*** 63 InMaxRow = 2')
    tst3.showRes()

def test3_4():
    print('======================== test 3_4')
    if WIN10:
        tst4fil = "".join(['.\\','testfiles\\','libre3by2date.csv'])
    else:
        tst4fil = '.\testfiles\libre3by2.csv'
    # no headers two columns of dates
    # each row one year apart
    # mm/dy/yr,mm/dy/yr 
    tst4 = CSVsamp.CSVsampFile(tst4fil)
    assert tst4.InHdl is None
    tst4.openInPath()
    assert tst4.InHdl is not None
    tst4.setCumField(1,'asDate',CumArgs='1')
    #tst4.setCumField(2,'asDate')
    tst4.getSamp()  
    assert tst4.InMaxRow == 3
    tst4.showRes()

# test3_1()
# test3_2()
test3_3()
test3_4()


 
print('completed tst3samp.py')    
   

 