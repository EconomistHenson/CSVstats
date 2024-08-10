import CSVsamp

WIN10 = True


def test2():
    assert CSVsamp.MAXSTR == 20000
    tst2cell = CSVsamp.CSVsampCell()
    tst2cell.addchar('C')
    assert tst2cell.charno == 1
    tststr = 'at1,dog1'
    for ichar in tststr:
        tst2cell.addchar(ichar)
    assert len(tst2cell.cellbuf) == 8
    assert tst2cell.charno == 8

def test2_1():
    if WIN10:
        tst2fil = "".join(['.\\','testfiles\\','libre3by2.csv'])
    else:
        tst2fil = '.\testfiles\libre3by2.csv'
    tst2 = CSVsamp.CSVsampFile(tst2fil)
    tst2.openInPath()
    tst2.openOutPath()
    
def test2_2():
    tstcell1 = CSVsamp.CSVsampCell()
    tstcell1.addchar('1')
    tstcell1.addchar('2')
    assert len(tstcell1.cellbuf) == 2 
    assert tstcell1.charno == 2

def test2_3():
    if WIN10:
        tst2fil = "".join(['.\\','testfiles\\','libre2by2simple.csv'])
    else:
        tst2fil = '.\testfiles\libre3by2.csv'
    tst2 = CSVsamp.CSVsampFile(tst2fil)
    tst2.openInPath()
    tst2.getSamp()
  



 
def test2_4():
    # pick one cell out
    if WIN10:
        tst2fil = "".join(['.\\','testfiles\\','Samp3by3.csv'])
    else:
        tst2fil = '.\testfiles\libre3by2.csv'
    tst2one = CSVsamp.CSVsampFile(tst2fil,outfile='Samp2one.csv')
    # should be middle cell
    tst2one.setTarget(2,2,2,2,1.0)
    retval = tst2one.getSamp()
    print(tst2one.thecell.dataStr)
    tst2one.__del__()
    print('tst2one complete')
 
def test2_4_1():
    if WIN10:
        tst2fil = "".join(['.\\','testfiles\\','Samp5by5.csv'])
    else:
        tst2fil = '.\testfiles\libre3by2.csv'
    tst2a = CSVsamp.CSVsampFile(tst2fil,outfile='Samp2a.csv')
    tst2a.setTarget(2,3,2,3,1.0)
    tst2a.getSamp()
    tst2a.__del__()
    tst2b = CSVsamp.CSVsampFile(tst2fil,outfile='Samp2b.csv')
    tst2b.setTarget(1,1,1,1,1.0)
    tst2b.getSamp()
    tst2b.__del__()

def test2_5():
    import csv
    if WIN10:
        # will contain the actual input data for test
        tst2fil = "".join(['.\\','testfiles\\','Samp5by5.csv'])
    else:
        tst2fil = '.\testfiles\libre3by2.csv'
    # the input test file has predictable contents 
    # 5x5 matrix withh 1,1 and 5,5 in the two corners
    # The contents are written out one cell at a time to Samp2e.csv
    # the individual cell is read in from Samp2e
    # compToo predicts the contents to the byte
    for therow in range(1,5):
        for thecol in range(1,5):
            # Samp2e should include one cell of data
            tstCell = CSVsamp.CSVsampFile(tst2fil,outfile='Samp2e.csv')
            tstCell.setTarget(therow,therow+1,thecol,thecol+1,1.0)
            assert thecol+1 == tstCell.maxcol
            assert thecol == tstCell.mincol
            assert therow+1 == tstCell.maxrow
            assert therow == tstCell.minrow
            print('*** 71',thecol)
            tstCell.getSamp()
            print('*** 73 ',tstCell.thecell.data)
            print('*** 74 ',tstCell.minrow)
            tstCell.__del__()
            SampHdl = open('Samp2e.csv','r') 
            TheStr = SampHdl.read() 
            # TheStr should in include on cell of data
            compToo = str(therow+1)+str(thecol+1)
            # these are two byte character arrays at this point
            print('*** 87 actual data in file',TheStr)
            print('*** 88 artifical construct comptoo',compToo)
            assert TheStr[0:2] == compToo[0:2]
            SampHdl.close()
   # Note that the rapid open close sequences can cause problems with the OS

# test2()
# test2_1()
# test2_2()
# test2_3()
test2_4()
# test2_5()
print('Tst2samp.py is complete')
