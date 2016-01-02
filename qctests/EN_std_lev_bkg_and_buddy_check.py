""" 
Implements the background check on standard levels and the buddy check
from the EN quality control system, 
http://www.metoffice.gov.uk/hadobs/en3/OQCpaper.pdf
"""

from cotede.qctests.possible_speed import haversine
import datetime
import EN_background_check
import EN_constant_value_check
import EN_increasing_depth_check
import EN_range_check
import EN_spike_and_step_check
import EN_stability_check
import util.main as main
import __main__
import numpy as np

def test(p):
    """ 
    Runs the quality control check on profile p and returns a numpy array 
    of quality control decisions with False where the data value has 
    passed the check and True where it failed. 
    """

    # Define an array to hold results.
    qc = np.zeros(p.n_levels(), dtype=bool)

    # Obtain the obs minus background differences on standard levels.
    result = stdLevelData(p)
    if result is None: return qc

    # Unpack the results.
    levels, origLevels, assocLevels = result

    # Retrieve the background and observation error variances.
    bgev = EN_background_check.bgevStdLevels
    obev = EN_background_check.auxParam['obev']

    # Loop through the levels and calculate the PGE.
    pgeData      = np.ma.array(np.ndarray(len(levels)))
    pgeData.mask = True
    for iLevel, level in enumerate(levels):
        if levels.mask[iLevel] or bgev.mask[iLevel]: continue
        bgevLevel = bgev[iLevel]
        if np.abs(p.latitude() < 10.0): bgevLevel *= 1.5**2
        obevLevel = obev[iLevel]
        pge = EN_background_check.estimatePGE(p.probe_type(), False)

        evLevel = obevLevel + bgevLevel
        sdiff   = level**2 / evLevel
        pdGood  = np.exp(-0.5 * np.min([sdiff, 160.0])) / np.sqrt(2.0 * np.pi * evLevel)
        pdTotal = 0.1 * pge + pdGood * (1.0 - pge)
        pgeData[iLevel] = 0.1 * pge / pdTotal

    # Find buddy.
    profiles = __main__.profiles
    lat = p.latitude()
    lon = p.longitude()
    minDist  = 1000000000.0
    iMinDist = None
    for iProfile, profile in enumerate(profiles):
        # Check that it is not the same profile and that they
        # are near in time. The time criteria matches the EN 
        # processing but would probably be better if it checked
        # that the profiles were within a time threshold. The
        # cruise is compared as two profiles from the same instrument
        # should not be compared.
        if (profile.uid() == p.uid() or
            profile.year() != p.year() or
            profile.month() != p.month() or
            profile.cruise() == p.cruise()): continue
        # Do a rough check of distance.
        latDiff = np.abs(profile.latitude() - lat)
        if latDiff > 5: continue
        # Do a more detailed check of distance.
        lonComp = profile.longitude()
        # Check in case they are either side of the edge of the map.
        if np.abs(lonComp - lon) > 180:
            if lonComp < lon:
                lonComp += 360.0
            else:
                lonComp -= 360.0
        # Calculate distance and compare to previous.
        pDist = haversine(lat, lon, profile.latitude(), lonComp)
        if pDist < minDist:
            minDist  = pDist
            iMinDist = iProfile
    # Check if we have found a buddy and process if so.
    if minDist <= 400000:
        fid = None
        pBuddy, currentFile, fid = main.profileData(profiles[iMinDist], '', fid)
        fid.close()
        Fail = False
        if pBuddy.var_index() is None:
            Fail = True
        if Fail == False:
            main.catchFlags(pBuddy)
            if np.sum(pBuddy.t().mask == False) == 0:
                Fail = True
        if Fail == False:
          result = stdLevelData(pBuddy)
          if result is not None: 
            # This code should ideally be separated into a function.
            levelsBuddy, origLevelsBuddy, assocLevelsBuddy = result
            bgevBuddy     = EN_background_check.bgevStdLevels
            pgeBuddy      = np.ma.array(np.ndarray(len(levelsBuddy)))
            pgeBuddy.mask = True

            for iLevel, level in enumerate(levels):
                if levelsBuddy.mask[iLevel] or bgevBuddy.mask[iLevel]: continue
                bgevLevel = bgevBuddy[iLevel]
                if np.abs(pBuddy.latitude() < 10.0): bgevLevel *= 1.5**2
                obevLevel = obev[iLevel]
                pge = EN_background_check.estimatePGE(pBuddy.probe_type(), False)
                evLevel = obevLevel + bgevLevel
                sdiff   = level**2 / evLevel
                pdGood  = np.exp(-0.5 * np.min([sdiff, 160.0])) / np.sqrt(2.0 * np.pi * evLevel)
                pdTotal = 0.1 * pge + pdGood * (1.0 - pge)
                pgeBuddy[iLevel] = 0.1 * pge / pdTotal

            for iLevel in range(len(levelsBuddy)):
                if levels.mask[iLevel] or levelsBuddy.mask[iLevel]: continue
                
                # For simplicity, going to assume that length scales
                # are isotropic and the same everywhere; in the EN 
                # processing length scales are stretched in E/W direction
                # near the equator and this functionality could be added
                # later.
                corScaleA = 300.0 # In km.             
                corScaleB = 400.0 # In km.
                corScaleT = 21600.0 # In secs.
                mesSDist  = minDist / (1000.0 * corScaleA)
                synSDist  = minDist / (1000.0 * corScaleB)
                timeDiff2 = (timeDiff(p, pBuddy) / corScaleT)**2 
                
                covar = (np.sqrt(bgev[iLevel] * bgevBuddy[iLevel]) * 
                         (1.0 + mesSDist) * np.exp(-mesSDist - timeDiff2) + 
                         np.sqrt(bgev[iLevel] * bgevBuddy[iLevel]) *
                         (1.0 + synSDist) * np.exp(-synSDist - timeDiff2))

                errVarA = obev[iLevel] + 2.0 * bgev[iLevel]
                errVarB = obev[iLevel] + 2.0 * bgevBuddy[iLevel]
                rho2    = covar**2 / (errVarA + errVarB)
                expArg  = (-(0.5 * rho2 / (1.0 - rho2)) *  
                           (levels[iLevel]**2 / errVarA + 
                            levelsBuddy[iLevel]**2 / errVarB - 
                            2.0 * levels[iLevel] * levelsBuddy[iLevel] / covar))
                expArg  = -0.5 * np.log(1.0 - rho2) + expArg
                expArg  = min(80.0, max(-80.0, expArg))
                Z       = 1.0 / (2.0 - (1.0 - pgeData[iLevel]) * 
                                 (1.0 - pgeBuddy[iLevel]) * (1.0 - expArg))
                if Z < 0.0: Z = 1.0 # In case of rounding errors.
                Z = Z**0.5
                pgeData[iLevel] = pgeData[iLevel] * Z

    # Assign the QC flags.
    for i, pge in enumerate(pgeData):
        if pgeData.mask[i]: continue
        if pge < 0.5: continue
        for j, assocLevel in enumerate(assocLevels):
            if assocLevel == i:
                origLevel = origLevels[j]        
                qc[origLevel] = True

    return qc

    
def stdLevelData(p):
    """
    Combines data that have passed other QC checks to create a 
    set of observation minus background data on standard levels.
    """

    # Combine other QC results.
    preQC = (EN_background_check.test(p) | 
             EN_constant_value_check.test(p) | 
             EN_increasing_depth_check.test(p) | 
             EN_range_check.test(p) |
             EN_spike_and_step_check.test(p) | 
             EN_stability_check.test(p))

    # Get the data stored by the EN background check.
    # As it was run above we know that the data held by the
    # module corresponds to the correct profile.
    origLevels = np.array(EN_background_check.origLevels)
    diffLevels = (np.array(EN_background_check.ptLevels) -
                      np.array(EN_background_check.bgLevels))
    nLevels    = len(origLevels)
    if nLevels == 0: return None # Nothing more to do.

    # Remove any levels that failed previous QC.
    use = np.ones(nLevels, dtype=bool)
    for i, origLevel in enumerate(origLevels):
        if preQC[origLevel]: use[i] = False
    nLevels = np.count_nonzero(use)
    if nLevels == 0: return None
    origLevels = origLevels[use]
    diffLevels = diffLevels[use]
    
    # Get the set of standard levels.
    stdLevels = EN_background_check.auxParam['depth']

    # Create arrays to hold the standard level data and aggregate.
    nStdLevels = len(stdLevels)
    levels     = np.zeros(nStdLevels)
    nPerLev    = np.zeros(nStdLevels) 
    z          = p.z()
    assocLevs  = []
    for i, origLevel in enumerate(origLevels):
        # Find the closest standard level.
        j          = np.argmin(np.abs(z[origLevel] - stdLevels))
        assocLevs.append(j)
        levels[j]  += diffLevels[i]
        nPerLev[j] += 1

    # Average the standard levels where there are data.
    iGT1 = nPerLev > 1
    levels[iGT1] /= nPerLev[iGT1]
    levels = np.ma.array(levels)
    levels.mask = False
    levels.mask[nPerLev == 0] = True

    return levels, origLevels, assocLevs

def timeDiff(p1, p2):

    dts = []
    for prof in [p1, p2]:
        year  = prof.year()
        month = prof.month()
        day   = prof.day()
        if day == 0: day = 15
        time  = prof.time()
        if time is None or time < 0 or time >= 24:
            hours   = 0
            minutes = 0
            seconds = 0
        else:
            hours = int(time)
            minutesf = (time - hours) * 60
            minutes  = int(minutesf)
            seconds  = int((minutesf - minutes) * 60)

        dts.append(datetime.datetime(year, month, day, hours, minutes, seconds))

    diff = dts[0] - dts[1]

    return np.abs(diff.total_seconds())

