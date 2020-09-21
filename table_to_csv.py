import sys, re
from html.parser import HTMLParser


class html_csv_parser(HTMLParser):

    def __init__(self):  
        HTMLParser.__init__(self)
        self.CSV = ''      # The CSV data
        self.CSVrow = ''   # The current CSV row constructed from HTML
        self.table_cnt = 0
        self.in_table = False
        self.in_th = False
        self.in_td = False      # Used to track if we are inside or outside a <TD>...</TD> tag.
        self.in_tr = False      # Used to track if we are inside or outside a <TR>...</TR> tag.
        self.re_multiplespaces = re.compile('\s+')  # regular expression used to remove spaces in excess
        self.rowCount = 0  # CSV output line counter.

    def handle_starttag(self, tag, attrs):
        if (tag.lower() == 'table'):        #Consider using tag.lower()
            self.start_table()        # I also have to consider for incorrect tags like putting space after tag or before

        if (tag.lower() == 'th'):
            self.start_th()

        if (tag.lower() == 'tr'): 
            self.start_tr()

        elif (tag.lower() == 'td'):
            self.start_td()

    def handle_endtag(self, tag):
        if (tag.lower() == 'tr'):
            self.end_tr()

        elif (tag.lower() == 'td'):
            self.end_td()

        elif (tag.lower() == 'th'):
            self.end_th()

    def start_table(self):
        if (self.in_table == True):
            self.end_table()
        self.in_table = True
        self.table_cnt += 1
        self.CSVrow = ('TABLE {}:\n' .format(self.table_cnt))

    def end_table(self):
        if (self.in_tr == False):
            self.end_tr()  

    def start_th(self):
        if (self.in_th == True):
            self.end_th() 
        self.in_th = True

    def end_th(self):
        if (self.in_th == True):
            self.CSVrow += ','  
            self.in_th = False

    def start_tr(self):
        if (self.in_tr == True):
            self.end_tr()  # <TR> implies </TR>
        self.in_tr = True

    def end_tr(self):
        if (self.in_td == False):
            self.end_td()  # </TR> implies </TD>
        self.in_tr = False            
        if len(self.CSVrow) > 0:
            self.CSV += self.CSVrow[:-1]
            self.CSVrow = ''
        self.CSV += '\n'
        self.rowCount += 1

    def start_td(self):
        if (self.in_tr != True):
            self.start_tr() # <TD> implies <TR>
        self.CSVrow += ''
        self.in_td = True

    def end_td(self):
        if (self.in_td == True):
            self.CSVrow += ','  
            self.in_td = False

    def handle_data(self, data):  
        if (self.in_td == True or self.in_th == True):
            self.CSVrow += self.re_multiplespaces.sub(' ',data.strip())
      
    def getCSV(self,chek=False):
        
        if ( chek and self.in_tr ): 
            self.end_tr()  
        
        data_out = self.CSV[:]
        self.CSV = ''
        return data_out


def main():

    
    if ( len(sys.argv) < 3 ):
        print("ERROR: You are missing an output statement.")
        sys.exit(2)

    elif ( len(sys.argv) > 3 ) :
        print("ERROR: Add better error sequence.")
        sys.exit(2)
    
    prog_name = sys.argv[0]
    html_inFile = sys.argv[1]
    csv_outFile = sys.argv[2] 

    parser = html_csv_parser()
    
    try:

        html_file = open(html_inFile, 'r')
        out_file = open(csv_outFile, 'w')
        data = html_file.read()
        while (data):
            parser.feed( data )
            out_file.write( parser.getCSV() )
            sys.stdout.write('%d CSV rows written.\n' % parser.rowCount)
            data = html_file.read()
        out_file.write( parser.getCSV(True) )
        out_file.close()
        html_file.close()

    except:

        print ('Error converting %s to CSV.' % html_inFile)
        try:    html_file.close()
        except: pass
        try:    out_file.close()
        except: pass



if __name__ == "__main__":
    main()
