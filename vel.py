#!python3
#function that takes pressure and curve parameters, and outputs a final velocity value

def trunc(num, min=1, max=127):
    #truncate to appropate range
    if num > max:
        return(max)
    elif num < min:
        return(min)
    else:
        return(num)


def curve(press, steps=7, min=1, max=127, mode ="linear"):
    """
    steps is the number of values your pressure sensor can detect. guitar hero drums send their pressure as a value between 1 and 7.
    min is the velocity value for a pressure of 1
    max is the velocity value for the highest pressure
    mode is unused. in the future, exponential, random, or other modes could be added
    boost will be added to the final result before being reduced back down

    a hacky way to get a lighter or heavier touch curve with only linear math is to set the min or max much higher or lower than normal. velocity that is too high or low will be brought back in range.
    """
    if mode == "linear":

        """
          127|             .max
        V    |          .
        E    |       .
        L    |   .
             |.min
           1 |_______________
               1 2 3 4 5 6 7
                 PRESSURE
        """
        #get slope m=(y2-y1)/(x2-x1)
        m=(max-min)/(steps-1)
        #get y intercept b=y-mx
        b=min-m
        #slove for the pressure
        vel = m*press+b
        return(trunc(vel))
