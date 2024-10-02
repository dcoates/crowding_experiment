import numpy
from psychopy import visual

def listOr1( item, idx ):
    try:
        return item[idx]
    except (TypeError, IndexError) as e:
        return item

	#if isinstance( list, collections.Iterable):
	# the above is True for string. We want false for the single character text

	#print( item )
	#if getattr( item, '__iter__', False):
		#return item[idx]
	#else:
		#return item

class stim_letter():
	"""Generic letter with list of pre-computed (passed in) parameters:
			xpos, ypos, and text """

	def __init__(self, win, height, targcol, selfont,  list ):
		self.param_list = list.copy() # Hopefully will not be that deep
		self.widget = visual.TextStim(win,alignHoriz='center',height=height, rgb=targcol, ori=0,font="Sloan", fontFiles=["Sloan.otf"] )
		self.pos = (0,0)
		self.text = ""
		self.height = height
		self.ori = 0 # need to init all thes to something reasonable

	def getval(self, which, num):
		return listOr1( self.param_list[which], num )

	def getTrial(self, trialNum=0):
		self.pos = (self.getval('xpos',trialNum), self.getval('ypos',trialNum))
		self.text = self.getval('text',trialNum)
		self.height =  self.getval('height',trialNum)
		self.ori =  self.getval('ori',trialNum)

	def strvals(self ):
		result = "%s %s %s %s" % (self.pos[0], self.pos[1], self.text, self.height )
		return result

	def draw(self, c=-999):
		self.widget.setOri(self.ori) 
		self.widget.setPos(self.pos) 
		self.widget.setText(self.text) 
		self.widget.setHeight(self.height)
		if not (c==-999):
			self.widget.setRGB( c )
		self.widget.draw()
