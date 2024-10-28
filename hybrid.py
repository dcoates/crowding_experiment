from tumblee import experiment_runner
import numpy as np
from twoline_fit import Solver,linefn

USE_PUPIL_LABS=False

CROWDED_SPACING=1.6 
UNFLANKED_SPACING=99

NUM_HYBRID_WITHIN=5
MIN_HYBRID=1.4 # Minimumal nominal spacing
HYBRID_OUTSIDE_CS=[1.5,2]

DEBUG=False

if USE_PUPIL_LABS:
    from pupil_labs.realtime_api.simple import discover_one_device
    device = discover_one_device()
    print(f"Phone IP address: {device.phone_ip}")
    print(f"Phone name: {device.phone_name}")
    print(f"Battery level: {device.battery_level_percent}%")
    print(f"Free storage: {device.memory_num_free_bytes / 1024**3:.1f} GB")
    print(f"Serial number of connected glasses: {device.module_serial}")

    recording_id = device.recording_start()
    print(f"Started recording with id {recording_id}")
    device.send_event("START")

the_experiment = experiment_runner()
if DEBUG:
    thresh_crowded=1.89
    thresh_unflanked=0.433
elif np.random.rand() < 0.5: # Randomize the order of these
    thresh_crowded=the_experiment.run(CROWDED_SPACING)
    thresh_unflanked=the_experiment.run(UNFLANKED_SPACING)
else:
    thresh_unflanked=the_experiment.run(UNFLANKED_SPACING)
    thresh_crowded=the_experiment.run(CROWDED_SPACING)
trials_x = [CROWDED_SPACING,UNFLANKED_SPACING]
trials_y = [thresh_crowded,thresh_unflanked]

num_spacings = NUM_HYBRID_WITHIN + len(HYBRID_OUTSIDE_CS)
hybrid_order = np.arange( num_spacings )
hybrid_order = np.random.permutation( hybrid_order )

solver1=Solver( np.array(trials_x), np.array(trials_y), linefn, True )
p0=(1.2,-0.4)

nidx_cond=0
while(nidx_cond < num_spacings ):
    ncond = hybrid_order[nidx_cond]
    opt=solver1.solve( p0 ) # Refit each time
    cs=10**opt['x'][0]
    spacings = np.concatenate([
        np.linspace(MIN_HYBRID,cs,NUM_HYBRID_WITHIN),
        np.array(HYBRID_OUTSIDE_CS)*cs ] )
    spacing1=spacings[ncond]
    if DEBUG:
        print (nidx_cond, ncond, spacing1)
    else:
        threshold1=the_experiment.run(spacing1)

    trials_x += spacing1 # Add to the list for refitting
    trials_y += threshold1
    nidx_cond += 1

if USE_PUPIL_LABS:
    device.recording_stop_and_save()
