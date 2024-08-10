import CSVsamp

def test1():
    CSVsamp.MAXSTR == 20000
    
def test2():
    # test implementation of coordinates
    coor1 = CSVsamp.CSVcoors()
    assert coor1.currow == 1
    assert coor1.curcol == 1
    

def test2_1():
    # test equality of coordinates
    coor1 = CSVsamp.CSVcoors()
    coor2 = CSVsamp.CSVcoors()
    assert coor1 == coor2

def test2_2():
    # test incrementation of coordinates
    coor1 = CSVsamp.CSVcoors()
    coor2 = CSVsamp.CSVcoors()
    assert coor1 == coor2
    coor1.incRow(1)
    assert coor1 != coor2
    assert coor1.currow == 2
    coor2.incRow(1)
    assert coor1 == coor2
    coor1.incCol(4)
    coor2.incCol(4)
    assert coor1 == coor2

def test2_3():

    # test implementation of print function
    coor3 = CSVsamp.CSVcoors()
    assert str(coor3) == '(1,1)'

def test3():
    
    cell1 = CSVsamp.CSVsampCell()
    assert cell1.coord.currow == 1
    assert cell1.coord.curcol == 1
    assert cell1.eof == False
    assert cell1.eol == False

def test3_1():
    # test incrementation of cell address
    cell1 = CSVsamp.CSVsampCell()
    assert cell1.coord.currow == 1
    assert cell1.coord.curcol == 1

    cell1.coord.incRow()
    assert cell1.coord.currow == 2
    assert cell1.coord.curcol == 1
    
    cell1.coord.incCol()
    assert cell1.coord.currow == 2
    assert cell1.coord.curcol == 2   

    cell1.coord.incRow()
    assert cell1.coord.currow == 3
    assert cell1.coord.curcol == 1  
    
def test4_1():
    # test management of data at the cell level    
    cell41 = CSVsamp.CSVsampCell()
    cell41.dataStr = str('123456789012')
    assert len(cell41) == 12

def test4_2():
    # test truncation with CSVsamp.MAXCELLPTR
    import io
    output = io.StringIO()
    cell12dat = '123456789012'
    cell41 = CSVsamp.CSVsampCell()
    cell41.dataStr = str('123456789012')
    assert len(cell41.dataStr) == 12
    # print to output will add a newline character without the end default set to null
    print(cell41,file=output,end="")
    cell10dat = output.getvalue()
    assert len(cell10dat) == CSVsamp.MAXCELLPTR
    



test1()
test2()
test2_1()
test2_2()
test2_3()
test3()
test3_1()
test4_1()
test4_2()

print('tst1samp.py completed')