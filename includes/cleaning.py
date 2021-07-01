from datetime import datetime, timedelta
from os import listdir, remove
from os.path import isfile, join
## Cleans the all_requests folder to reduce size

def isbetween(d, bound_1, bound_2):
    if d > bound_1 and d < bound_2:
        return True
    elif d < bound_1 and d > bound_2:
        return True
    else:
        return False

class File:
    def __init__(self, name):

        self.fullname = name

        cname = name.replace('data_','')
        cname = cname.replace('.txt','')

        self.year = int(cname[0:4])
        self.month = int(cname[4:6])
        self.day = int(cname[6:8])
        self.hrs = int(cname[8:10])
        self.mins = int(cname[10:12])

        self.dt = datetime(self.year, self.month, self.day, self.hrs, self.mins)
        self.span = (self.dt - timedelta(hours=72), self.dt)

    def clashes_with(self, file):
        if isbetween(self.span[0], file.span[0], file.span[1]) or isbetween(self.span[1], file.span[0], file.span[1]):
            return True
        else:
            return False
    
def span_covered(File1, File2):
    if File1.span[1] >= File2.span[0]:
        return True
    else:
        return False



def time_diff(File1, File2):

    delta = abs(File1.dt - File2.dt)
    hours = (delta.days * 86400 + delta.seconds)/3600
    return hours

def clean():
    d = 'raw_data/'
    files = [f for f in listdir(d) if isfile(join(d,f))]
    '''files.append('data_20210702130000.txt')
    files.append('data_20210703140000.txt')
    files.append('data_20210704090000.txt')
    files.append('data_20210705140000.txt')'''
    fileobj = []
    for name in files:

        new_file = File(name)

        fileobj.append(new_file)

    
    finished = False
    i = 0
    while finished != True and len(fileobj) >= 3:

        if fileobj[i+1].clashes_with(fileobj[i]) and fileobj[i+1].clashes_with(fileobj[i+2]) and span_covered(fileobj[i], fileobj[i+2]):
            fileobj.remove(fileobj[i+1])
        else:
            i += 1

        if i >= (len(fileobj)-2):
            finished = True
    
    keep_names = []
    for o in fileobj:
        keep_names.append(o.fullname)

    for file in files:
        if file not in keep_names:
            fp = 'raw_data/' + file
            remove(fp)

    return (len(files)-len(keep_names))
