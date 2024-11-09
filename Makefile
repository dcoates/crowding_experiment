all:
	#grep mean results/*vert*1028* > res
	grep mean results/berkeley/* > res

#from twoline_fit import Solver,linefn

#fil=open("./res")
#res=[]
#for line1 in fil.readlines():
    #fields=line1.split(':')
    #meant=float( fields[2].split('\t')[0] )#.find('mean value:')+len('mean value+')
    #spac=float( fields[3].split('\t')[0] )#
    ##spac=float(line1[22:(line1[22:].find('_')+22)])
    ##meant=float(line1[mean1:mean1+7])
    #res += [[spac,meant]]
    #
#res=np.array(res)
#sortidx=np.argsort(res[:,0])
#res = res[sortidx]
#res[:,0] = res[sortidx,0]
