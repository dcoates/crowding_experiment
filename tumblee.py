from psychopy import *
import psychopy.data as pd 
import numpy
import time
import matplotlib.pyplot as pyplot
import os 
import sys

import stims as stimuli_functions
import conditions

backcol= (  0, 0, 0 ) # Mid-gray
targcol= ( -1,-1,-1) # Black
fullscr=False # Set to True when not debugging (Ready to run)
monitor_dims = (1024,768)
target_deg_ecc = 9
distance_mm = 1080.0
fixation_offset = 370
xpos=0; ypos=0
ntrials = 20
stimulus_duration =  0.150  # in sec use -1 for infinite
mask_duration = 0
targets = [0,90,180,270]
condition = "both" # or "radial" or "tangential"

SubjectName = 'drc_test'
repeats = 1
#spacings = [1.5, 3.0, 99.0 ]
spacings = [99]

# Randomize order of spacings:
allspacings = numpy.tile( spacings, (1, repeats ))[0]
allspacings = numpy.random.permutation( allspacings )

def buildtrialseq( vals, ntrials ):
	return numpy.random.permutation( numpy.tile ( vals, int(numpy.ceil( float(ntrials)/len(vals)) )) )[0:ntrials]

class experiment_runner():
    def __init__(self):
        return

    def run(self):
        # TODO: Monitor Info: (dimensions, ?, center of target X, distance (mm?) )
        exper = conditions.experimental_setup( monitor_dims, distance_mm, target_deg_ecc, fixation_offset )

        font = conditions.fontArial( targcol )
        stimHeightDeg = 2.25 # dummy (overwritten below)
        font.setCharDegs( stimHeightDeg, exper )

        OutputHeader = True
        # This experiment - trials, timing, etc. 
        maxtrials = ntrials

        # Set up the screen, etc.
        myWin = visual.Window(exper.screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr)
        myWin.setMouseVisible(False)
        myWin.setRecordFrameIntervals(True)

        fixation = visual.TextStim(myWin,pos=(0,exper.yloc_fixation_pix),alignHoriz='center',height=9, color=font.contrast, ori=0, font=font.selfont ) 

        test_heights = font.let_height_ptfont

        spacseq = buildtrialseq( [exper.deg2pix(angl) for angl in [1.5]], ntrials )
        spacing = exper.deg2pix( stimHeightDeg ) # +font.let_height_ptfont/2.0

        # Sequence of random orientation for target and flankers:
        targseq = [targets[i] for i in buildtrialseq( numpy.arange(len(targets)), maxtrials) ]
        seqL = [targets[i] for i in buildtrialseq( numpy.arange(len(targets)), maxtrials) ]
        seqR = [targets[i] for i in buildtrialseq( numpy.arange(len(targets)), maxtrials) ]
        seqU = [targets[i] for i in buildtrialseq( numpy.arange(len(targets)), maxtrials) ]
        seqD = [targets[i] for i in buildtrialseq( numpy.arange(len(targets)), maxtrials) ]

        targ = stimuli_functions.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
            {'height': test_heights, 'xpos':0.0, 'ypos':exper.yloc_pix, 'text':'E', 'ori':targseq}  )
        left = stimuli_functions.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
            {'xpos':-spacing, 'ypos':exper.yloc_pix, 'text':'E', 'height':test_heights, 'ori':seqL}  )
        right = stimuli_functions.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
            {'xpos':+spacing, 'ypos':exper.yloc_pix, 'text':'E', 'height':test_heights, 'ori':seqR}  )

        up = stimuli_functions.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
            {'xpos':+spacing, 'ypos':exper.yloc_pix+spacing, 'text':'E', 'height':test_heights, 'ori':seqU}  )
        down = stimuli_functions.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
                                {'xpos':+spacing, 'ypos':exper.yloc_pix-spacing, 'text':'E', 'height':test_heights, 'ori':seqD}  )
        if spacingMult < 99: # Flanked
            if condition=="radial":
                stims = [ targ, left, right] 
            elif condition=="tangential":
                stims = [ targ, up, down] 
            elif condition=="both":
                stims =[ targ, left, right, up, down ]
        else: #unflanked
            stims = [ targ ]

        outfilename = "results/%s_%s_%s_%s.csv" % (SubjectName, condition, str(spacingMult), time.strftime("%m%d%Y", time.localtime() ) )
        outfile = open(outfilename, "wt")
        trialNum=0

        # Calibrate by seeing how long 100 redraws takes
        fixation.setHeight(30)
        fixation.setPos( (0,0) )

        fixation.setText( 'Calibrating monitor. Please wait.' )
        for i in numpy.arange(100):
            fixation.draw()
            myWin.flip()
        savetimes = myWin.frameIntervals
        fliprate = numpy.mean( savetimes[20:80] )
        print ('fliprate=%f ms (%f Hz)' % (fliprate,1.0/fliprate) )

        print( targseq) 

        fixation.setText('Ready. Press a key.')
        fixation.draw()
        myWin.flip()
        event.waitKeys()

        fixation.setPos( (0,exper.yloc_fixation_pix) )
        fixation.setHeight(70)
        fixation.setText( '+' )
        fixation.draw()
        myWin.flip()
        event.waitKeys()

        thisStair = pd.StairHandler(startVal=4, nTrials=50, nUp=1, nDown=3, minVal = 0.5, maxVal=7, stepSizes=[3,2,1,0.75,0.5,0.5,0.2,0.2,0.2,0.2,0.2,0.2] ) #, stepSizes=[4,2,1,1,1,1,1,1])

        done = False
        while not done and trialNum<maxtrials:
            # Draw fixation
            fixation.draw()
            myWin.flip()

            # Get the parameters (orientation, size, etc.) for the next trial:
            [stim.getTrial(trialNum) for stim in stims]
            print(targ.ori)

            try:
                sval = thisStair.next()
            except StopIteration:#we got a StopIteration error
                print ('Done. Final intensity: %f' % (numpy.mean( thisStair.reversalIntensities[2:] ) ) )
                break

            font.setCharDegs( sval, exper )
            for stim in stims:
                stim.height=font.let_height_ptfont

            left.pos =	(spacingMult * exper.deg2pix(sval), exper.yloc_pix )
            right.pos =	 (-spacingMult * exper.deg2pix(sval), exper.yloc_pix )
            up.pos =	(spacingMult * exper.deg2pix(sval), exper.yloc_pix )
            down.pos =	 (-spacingMult * exper.deg2pix(sval), exper.yloc_pix )

            for nflips in range(int(stimulus_duration/fliprate)):
                # Show stimulus for correct number of "flips"
                [stim.draw( targcol ) for stim in stims]
                fixation.draw()
                myWin.flip()

            if mask_duration > 0:
                # Draw mask if desired for appropriate duration. TODO
                pass

            # IF duration is positive, clear the screen. Else leave on (infinite display).
            if (stimulus_duration >= 0):
                fixation.draw()
                myWin.flip()

            resp_ori = numpy.floor(numpy.random.rand()*4)*90
            for key in event.waitKeys():
                if key in [ 'escape' ]:
                    done = True
                if key in [ 'left' ]:
                    resp_ori = 180
                if key in [ 'right' ]:
                    resp_ori = 0
                if key in [ 'up' ]: # WTF.. For some reason up/down seem reversed now (2022.2.3)
                    resp_ori = 270 
                if key in [ 'down' ]:
                    resp_ori = 90

            outfile.write( "%s, %s\n" % (key, targ.strvals() ) )
            iscorrect = (resp_ori == targ.ori)
            thisStair.addData( iscorrect )

            trialNum += 1

        outfile.write( 'height=' + str(stimHeightDeg) + "\n")
        outfile.write ('mean value: %f\t' % (numpy.mean( thisStair.reversalIntensities[2:] ) ) )
        outfile.write ('spacingMult: %s\t' % str( spacingMult ) )
        outfile.write ('SubjectName: %s\n' %  SubjectName )

        if OutputHeader:
            outfile.write( '#END\n' )
            outfile.write( '%s\n' % [str(stim) for stim in stims])
            outfile.write( "#V 0.2\n" )
            outfile.write( '#font=' + str(font.let_height_ptfont) + "\n")
            outfile.write( '#font.let_height_pixels=' + str(font.let_height_pixels) + "\n")
            outfile.write('#font.let_height_mm=' + str(font.let_height_mm) + "\n")
            outfile.write('#font.let_height_deg=' + str(font.let_height_deg) + "\n")
            #outfile.write('#ratio of (ascender+descender) to o=' + str(ascender_and_descender_to_o) + "\n")
            #outfile.write('#ratio of ptfont to pixels=0' + str(ptfont_to_pixels) + "\n")
            #utfile.write( '#distance=' + str(distance) + "\n")
            #utfile.write( '#pixels per mm=' + str(screensize) + "\n")
            #utfile.write( '#degrees_eccentricity=' + str(degrees_eccentricity) + "\n" )
            outfile.write( '#exper.yloc_pix=' + str(exper.yloc_pix) + "\n" )
            outfile.write( '#duration=' + str(stimulus_duration) + "\n")
            outfile.write( "key, targ.strvals(), olL.strvals(), olR.strvals() ")

        outfile.close()
        myWin.close()


the_experiment = experiment_runner()
for spacingMult in allspacings:
    print (spacingMult)
    the_experiment.run()
