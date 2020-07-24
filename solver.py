'''
$mmls Dumpfile
--> find filesystem offset
fls -o 206848(offset) -r "Dumpfile" > fls_dump3.txt
'''

'''
dump1 : pure state
dump2 : safety app installed state
dump3 : remove app state
dd if=/dev/mapper/vg-windows7--sp1 of=./dump1 bs=1024
'''

import sys
import shutil
import os
import argparse

list1 = []
list2 = []
list3 = []

list_tmp = []

not_include=['.tmp','.log']
not_count=len(not_include)
#not_count=0
    

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def init_dump(fileName):
    string = '003:  000:001   '

    index = os.popen(r'mmls ./'+fileName).read().strip()
    #print index
    tmp = index.find('003:  000:001   ')+len(string)
    index =  int(index[tmp:tmp+10],10)

    result = os.popen(r'fls -o '+str(index)+' -r ./'+fileName+' > fls_'+fileName+'.txt')
    
    print "\t[*]Success Disk Dump file Init "+fileName+"\n"

    return 'fls_'+fileName+'.txt' , index
    
def fileParser(line, ii):
    tmp_count=0
    if line.find('r/r') is not -1:
        line = line[line.index('\t')+1:-1]
        
        if ii is 1:
            if line not in list1:
                for i in range(0,not_count):
                    if line.find(not_include[i]) is not -1:
                        tmp_count=1
                if tmp_count is 0:    
                    list1.append(line)
                    tmp_count=0

        elif ii is 2:
            if line not in list2:
                for i in range(0,not_count):
                    if line.find(not_include[i]) is not -1:
                        tmp_count=1
                if tmp_count is 0:
                    list2.append(line)
                    tmp_count=0

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print bcolors.FAIL+"Useage: python script.py -h"+bcolors.ENDC
        exit(0)

    #argparse setting
    parser = argparse.ArgumentParser(description='['+bcolors.OKGREEN+'+'+bcolors.ENDC+'] python script.py DiskFile')
    parser.add_argument('--extract','-e',help=bcolors.WARNING+'Useage: python script.py DiskFile'+bcolors.ENDC)
    parser.add_argument('--diff','-d', nargs='+',help=bcolors.WARNING+'Useage: python script.py -d[--diff] Disk1 Disk2'+bcolors.ENDC+ '--> Difference of Disk2 for Disk1')
    parser.add_argument('--dump','-u', nargs='+',help=bcolors.WARNING+'Useage: python script.py -u[--dump] PATH Ouputfile'+bcolors.ENDC)
    parser.add_argument('--percentage','-p',nargs='+',help=bcolors.WARNING+'Useage: python script.py -p[--percentage] Disk1 Disk2 Disk3'+bcolors.ENDC)

    args=parser.parse_args()

    if args.extract is not None:

        print bcolors.FAIL+"\nExtract FileList From "+bcolors.ENDC+args.extract
        first_file = args.extract

        if os.path.isfile('fls_'+first_file+'.txt') is True:
            os.remove('fls_'+first_file+'.txt')

        if os.path.isfile('fileList'+first_file) is True:
            os.remove('fileList'+first_file)

        flsName1,index = init_dump(first_file)
        f = open("fls_"+first_file+".txt",'r')
        while True:
            line = f.readline()
            if not line: break
            fileParser(line,1)


        f.close()

        f1=open('fileList'+first_file,'w')

        for i in range(0, len(list1)):
            f1.write(list1[i]+'\n')

        f1.close()

        print bcolors.OKBLUE+"Success!!"+bcolors.ENDC

    elif args.dump is not None: #Not Yet
        print bcolors.FAIL+"\nDump DiskState"+bcolors.ENDC
        path = args.dump[0]
        outfile = args.dump[1]

        cmd = r'dd if='+path+' of='+outfile+' bs=1024'

        os.popen(cmd).read().strip()

    elif args.diff is not None:   
        print bcolors.FAIL+"\nDifference of SecondFileList for FirstFileList (FirstFileList - SecondFileList)"+bcolors.ENC

        first_file = args.diff[0]
        second_file = args.diff[1]

        if os.path.isfile('fls_'+first_file+'.txt') is True:
            os.remove('fls_'+first_file+'.txt')

        if os.path.isfile('fls_'+second_file+'.txt') is True:
            os.remove('fls_'+second_file+'.txt')

        if os.path.isfile('fileList'+first_file) is True:
            os.remove('fileList'+first_file)

        if os.path.isfile('fileList'+second_file) is True:
            os.remove('fileList'+second_file)
  
        #check
        print bcolors.FAIL+"\n[*]Diff File List: "+bcolors.ENDC+first_file+" - "+second_file+"\n"

        flsName1,index1 = init_dump(first_file) #dump1
        flsName2,index2 = init_dump(second_file) #dump2

        for i in range(0,2):
            f = open("fls_"+args.diff[i]+".txt",'r')
            while True:
                line = f.readline()
                if not line: break
                fileParser(line,i+1)
            

            f.close()

        f1=open('fileList'+first_file,'w')
        f2=open('fileList'+second_file,'w')

        for i in range(0, len(list1)):
            f1.write(list1[i]+'\n')

        for i in range(0, len(list2)):
            f2.write(list2[i]+'\n')

        f1.close()
        f2.close()
   
        s1=set(list1)
        s2=set(list2)

        list3=list(s1&s2)

        print "Number of "+args.diff[0]+": "+bcolors.WARNING+str(len(list1))+bcolors.ENDC
        print "Number of "+args.diff[1]+": "+bcolors.WARNING+str(len(list2))+bcolors.ENDC
        print "Intersection of "+args.diff[0]+" and "+args.diff[1]+": "+bcolors.WARNING+str(len(list3))+bcolors.ENDC
        print args.diff[0] +" - "+args.diff[1]+": "+bcolors.WARNING+str(len(list(set(list1)-set(list3))))+bcolors.ENDC


        f=open("file_diff.txt","w")
        file_ = ''
        list_diff=list(set(list1)-set(list3))

        for i in range(0, len(list_diff)):
            file_ += list_diff[i]+'\n'

        f.write(file_)
        f.close()

    elif args.percentage is not None:
        print bcolors.FAIL+"\nWindows Aging percent."+bcolors.ENDC
        print bcolors.FAIL+"\tPure State FileList vs. Installed State vs. Remove State FileList"+bcolors.ENDC

        first_file = args.percentage[0] #pure state
        second_file = args.percentage[1] #installed state

        third_file = args.percentage[2] #removed state

        #first Stage Install State - Pure State
        
        if os.path.isfile('fls_'+first_file+'.txt') is True:
            os.remove('fls_'+first_file+'.txt')

        if os.path.isfile('fls_'+second_file+'.txt') is True:
            os.remove('fls_'+second_file+'.txt')

        if os.path.isfile('fls_'+third_file+'.txt') is True:
            os.remove('fls_'+third_file+'.txt')

        if os.path.isfile('fileList'+first_file) is True:
            os.remove('fileList'+first_file)

        if os.path.isfile('fileList'+second_file) is True:
            os.remove('fileList'+second_file)

        if os.path.isfile('fileList'+third_file) is True:
            os.remove('fileList'+third_file)

        print "\n[*]First Stage.(Installed State - Pure State)"
        print "\t-Get a list of installed files"
        print "\t-Diff File List: "+second_file+" - "+first_file+"\n"

        flsName1,index1 = init_dump(first_file) #dump1
        flsName2,index2 = init_dump(second_file) #dump2


        for i in range(0,2):
            f = open("fls_"+args.percentage[i]+".txt",'r')
            while True:
                line = f.readline()
                if not line: break
                fileParser(line,i+1)

            f.close()

        f1=open('fileList'+first_file,'w')
        f2=open('fileList'+second_file,'w')

        for i in range(0, len(list1)):
            f1.write(list1[i]+'\n')

        for i in range(0, len(list2)):
            f2.write(list2[i]+'\n')

        f1.close()
        f2.close()

        s1=set(list1)
        s2=set(list2)

        list3=list(s1&s2)

        print "\nResult 1/2:"
        print "\tNumber of "+args.percentage[0]+": "+bcolors.WARNING+str(len(list1))+bcolors.ENDC
        print "\tNumber of "+args.percentage[1]+": "+bcolors.WARNING+str(len(list2))+bcolors.ENDC
        #print "\tInstalled file("+args.percentage[1] +" - "+args.percentage[0]+"): "+str(len(list(set(list2)-set(list3))))

        f=open("InstalledFileList.txt","w")
        file_ = ''
        list_diff=list(set(list2)-set(list3))
        print "\tNumber of Installed file: "+bcolors.WARNING+str(len(list_diff))+bcolors.ENDC

        for i in range(0, len(list_diff)):
            file_ += list_diff[i]+'\n'

        f.write(file_)
        f.close()


        print bcolors.OKBLUE+"\n[*]Success!! First Stage."+bcolors.ENDC
        
        print "[*]Second Stage.(Intersection of (Installed Stated - Pure Stated) and Removded Stated)\n"
        print "\t-Get list of files thar are not removed"
        print "\t-Intersection of (("+args.percentage[1]+" - "+args.percentage[0]+") and "+args.percentage[2]+")"

        print "\t-Extract FileList From "+args.percentage[2]

        flsName3,index3 = init_dump(third_file)
        f = open("fls_"+third_file+".txt",'r')

        while True:
            line = f.readline()
            if not line: break
            fileParser(line,1) #reuse list1

        f.close()

        f1=open('fileList'+third_file,'w')

        for i in range(0, len(list1)):
            f1.write(list1[i]+'\n')

        f1.close()

        s1=set(list1) #extract fileList of dump3 
        s2=set(list_diff) #installed fileList

        list3=list(s1&s2) #remind fileList

        print "\nResult 2/2:"
        print "\t-Number of "+args.percentage[2]+": "+bcolors.WARNING+str(len(list1))+bcolors.ENDC
        print "\t-Number of not removed file: "+bcolors.WARNING+str(len(list3))+bcolors.ENDC
        print "\t-Number of Installed file: "+bcolors.WARNING+str(len(list_diff))+bcolors.ENDC

        f = open("NotRemovedFile.txt","w")
        file_ = ''
       
        for i in range(0, len(list3)):
            file_ += list3[i] + '\n'

        f.write(file_)
        f.close()

        #f=open('fls_'+second_file+'.txt','r')
        
        Not_removed_fileSize=0
        Installed_fileSize=0

        #first = 'r/r '
        second = '128'
        i=0

        f=open('fls_'+second_file+'.txt','r')
        number = ''
        count2=0

        while True: #Obataining Removed file Size

            line = f.readline()
            if not line: break

            if line.find(list3[i]) is not -1:

                if line.find('r/r') is not -1:
                    number = line[line.find('r/r')+len('r/r'):line.find(second)+len(second)+2]

                elif line.find('-/r') is not -1:
                    number = line[line.find('-/r')+len('-/r'):line.find(second)+len(second)+2]

                elif line.find('r/-') is not -1:
                    number = line[line.find('r/-')+len('r/-'):line.find(second)+len(second)+2]

                if len(number) is not 12:
                    number = line[line.find('/')+3:line.find(':')]
                    if number[0] is ' ' or number[0] is '*':
                        number = line[line.find('/')+4:line.find(':')]
                        if line.find('(realloc)') is not -1:
                            number = line[line.find('/')+4:line.find('(')]
                        if number.find(':') is not -1:
                            number = line[line.find('/')+4:line.find(':')]

                if number == ' 0':
                    number = ' 9999'
                    count2 += 1

                #print r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+number
                a = os.popen(r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+number).read().strip()

                Not_removed_fileSize += len(a)

                if i < len(list3)-1:
                    i+=1
                else:
                    break

                f.close()
                f=open('fls_'+second_file+'.txt','r')
        
        a = os.popen(r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+'9999').read().strip()
        Not_removed_fileSize -= len(a) * count2
        f.close()
        f=open('fls_'+second_file+'.txt','r')

        print "\t-Calc Number of file : "+str(i+1)

        i=0
        count2=0

        while True: #Obataining Removed file Size
            line = f.readline()
            if not line: break

            if line.find(list_diff[i]) is not -1:
                if line.find('r/r') is not -1:
                    number = line[line.find('r/r')+len('r/r'):line.find(second)+len(second)+2]

                elif line.find('-/r') is not -1:
                    number = line[line.find('-/r')+len('-/r'):line.find(second)+len(second)+2]

                elif line.find('r/-') is not -1:
                    number = line[line.find('r/-')+len('r/-'):line.find(second)+len(second)+2]

                if len(number) is not 12:
                    number = line[line.find('/')+3:line.find(':')]
                    if number[0] is ' ' or number[0] is '*':
                        number = line[line.find('/')+4:line.find(':')]
                        if line.find('(realloc)') is not -1:
                            number = line[line.find('/')+4:line.find('(')]
                        if number.find(':') is not -1:
                            number = line[line.find('/')+4:line.find(':')]

                if number == ' 0':
                    number = ' 9999'
                    count2 += 1

                #print r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+number
                a = os.popen(r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+number).read().strip()

                Installed_fileSize += len(a)

                if i< len(list_diff)-1:
                    i+=1
                else:
                    break

                a = os.popen(r'icat -o '+str(index2)+ ' ./'+args.percentage[1]+' '+'9999').read().strip()
                Installed_fileSize -= len(a) * count2

                f.close()
                f=open('fls_'+second_file+'.txt','r')


        print "\t-Calc Number of file : "+str(i+1)

        f.close()

        print "[*]Not Removed FileSize is "+bcolors.FAIL+str(Not_removed_fileSize)+bcolors.ENDC+" byte"
        print "[*]Installed FileSize is "+bcolors.FAIL+str(Installed_fileSize)+bcolors.ENDC+" byte"
        print "\n--> Aging Number of file(%): "+bcolors.FAIL+str(float(len(list3)) / float(len(list_diff)) * 100) +bcolors.ENDC+' %'
        print "\n--> Aging Size of file(%): "+bcolors.FAIL+str(float(Not_removed_fileSize) / float(Installed_fileSize) * 100)+bcolors.ENDC +' %'
