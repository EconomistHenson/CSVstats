class CSVdata():

    def __init__(self,numcols):
    
        self.numcols = numcols
        self.numrows = 1
        self.rownum = 1
        self.row0header = True
        
        self.lstofrows =[(self.rownum,[])]
        
    def addrow(self,newrow: list):  
        therownum = self.numrows
        thenewrow = (therownum,newrow)
        self.listofrows.append((therownum,thenewrow))
        
        return True
