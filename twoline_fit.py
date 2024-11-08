import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def linefn(x,cs,unf):
    y=np.max(((cs-x),np.repeat(0,len(x))),axis=0)+unf
    return y

def line_err(x,cs,unf):
    return linefn(x,cs,unf)

class Solver():
    def __init__(self,x,y,fn,dolog=False):
        self.x=x
        self.y=y
        self.fn=fn
        self.dolog=dolog
        if self.dolog:
            self.xr = 10**np.linspace( np.log10(x.min()), np.log10(x.max()) )
        else:
            self.xr = np.linspace( x.min(), x.max())
    
    def fun_val(self,p,x=None):
        if x is None:
            x=self.x
        if self.dolog:
            val = 10 ** ( self.fn(np.log10(x),*p) )
        else:
            val = self.fn(x,*p)
        return val
        
    def err_fun(self,p):
        #print( self.fn(x,*p))
        if self.dolog:
            ssq = np.sum( (self.fun_val(p) - (self.y))**2 )
        else:
            ssq = np.sum( (self.fun_val(p) -self.y)**2 )
        return ssq
    
    def solve(self,p0):
        opt1=minimize( self.err_fun, p0, method='Nelder-Mead')
        #self.opt1=opt1['x']
        self.opt = opt1
        return opt1
    
    def plot(self):
        plt.plot( self.x, self.y, 'o')
        
        unf=self.opt['x'] [1]
        cs=self.opt['x'][0]

        if self.dolog:
            unf=10**unf
            cs = 10 ** cs

        cs_abs = cs * unf
        lbl="Unflanked=%0.3f$^o$\ncrit. spac. (nom)=%0.3fx\ncrit. spac. (abs)=%0.3f$^o$" %(unf,cs,cs_abs, )
            
        plt.plot( self.xr,( self.fun_val(self.opt['x'],(self.xr) ) ), '-', label=lbl)
        plt.legend(loc='best')
        plt.xlabel("Nominal spacing (multiples of size)", size=18)
        plt.ylabel("Letter size (deg)", size=18)
        
        if self.dolog:
            plt.loglog()
