#!/usr/bin/env python3

"""Adjust timing in SRT files"""

import os
import argparse as ap


# -----------------------------
# Setting up parser
# -----------------------------

Parser = ap.ArgumentParser(description = 'Adjust timing in SRT file.')
Parser.add_argument('-m', '--magnitude', type = float, metavar = 'M',
                    required = True,
                    help = 'Number of seconds to adjust timing.')
Parser.add_argument('-d', '--direction', type = str, metavar = 'D',
                    required = True, choices = ("back", "forward"),
                    help = 'Direction to change subtitle timing. ' + \
                           'Choices are limited to "forward" and "back".')
Parser.add_argument('files', type = str, metavar = 'F', nargs = '+',
                    help = 'SRT file(s)')



# Dictionary of arguments supplied to script.
args = vars(Parser.parse_args())

# Extracting info from args dictionary.
srt_files = [os.path.expanduser(x) for x in args['files']]
direction = args['direction']
assert direction in ['back', 'forward'], 'direction variable is not one of "back" or ' + \
                                         '"forward"'
if direction == 'back':
    mult = -1
else:
    mult = 1
srt_mag = abs(args['magnitude']) * mult



"""

# ------------
# Testing area
# ------------
import os

file = os.path.expanduser('~/Desktop/Game of Thrones S06E10 - The Winds of ' + \
                          'Winter.srt')
mult = 1
magnitude = 60 * mult
# ------------

"""




def secs_to_str_i(secs):
    """Convert a single seconds-float to string for SRT output."""
    hrs = int(secs // 60**2)
    mins = int((secs - ((secs // 60**2) * 60**2)) // (60**1))
    secs = round(secs % 60, 3)
    secs_str = '{:06.3f}'.format(secs).replace('.', ',')
    out_str = '%02d:%02d:%s' % (hrs, mins, secs_str)
    return out_str

def secs_to_str(secs_list):
    """Convert list of seconds-floats to a string for SRT output."""
    str_list = [secs_to_str_i(x) for x in secs_list]
    return ' --> '.join(str_list) + '\n'

def str_to_secs(line_str):
    """Converts line from SRT to list of floats in seconds."""
    se = [[float(z) for z in x.replace(',', '.').split(':')] for x in 
        line_str.split(' --> ')]
    se_secs = [[round(x * (60**y), 3) for x,y in zip(a, [2, 1, 0])] for a in se]
    secs = [sum(x) for x in se_secs]
    return secs


def update_srt(file, magnitude):
    with open(file, 'rt') as f, open(file.replace('.srt', '_new.srt'), 'wt') as new:
        i = 1
        for line in f:
            if line.rstrip('\n').isdigit():
                new_line = str(str(i) + '\n')
                i += 1
            elif line.count('-->') > 0:
                se_secs = str_to_secs(line)
                new_se = [x + magnitude for x in se_secs]
                new_line = secs_to_str(new_se)
            else:
                new_line = line
            new.write(new_line)
    return



def main():
    for file in srt_files:
        update_srt(file, srt_mag)
    return




if __name__ == '__main__':
    main()





