"""Greensleeves (Clayderman, arr.).

Arranged from a transcription of Richard Clayderman's Greensleeves.

    python arr_greensleeves.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
# The tempo map: (beat, beats per minute). Written as the round numbers
# a player would be given rather than as the microsecond values read
# back out of the finished file.
#
# The tempo map is part of the arrangement, not of the playback: this
# one leans on the tune and gives the ground back three times before it
# closes.
TEMPO = [
    (0.0, 79),
    (56.0, 83),           # press
    (64.0, 79),           # and back
    (124.0, 83),
    (136.0, 79),
    (164.0, 83),
    (192.0, 79),
    (224.0, 74),          # the close
    (228.0, 68),
]
BPM = TEMPO[0][1]
TIME_SIG = (4, 4)
BAR = 4          # beats per bar
# Silence at each end, in beats: nothing begins on a note or ends on
# one. Every piece here gets about 2 s before the first note and 4 s
# after the last, rounded to whole beats at the tempo in force there -
# at 79 bpm that is 2.3 s and 3.8 s.
LEAD_IN = 3
TAIL = 5
# Every note gives up a little of its tail, so the next stroke of the
# same pitch starts against silence instead of picking up exactly where
# the last one stopped. Stepped by whole beats, five per cent as the
# floor: 5 under a beat and at one beat, 10 at two, 15 at three, 20 at
# four and no further. Forty-nine joins in this piece met dead on.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))


TITLE = 'Greensleeves (Clayderman, arr.)'

# ---- voice 0 ----
# 39 distinct bars over 58 bars of music.
VOICE_0_CELLS = [
    [(0, 3, 86), (3, 0.5, 85), (3.5, 0.5, 83)],
    [(0, 3, 81), (3, 1, 78)],
    [(0, 3, 74), (3, 0.5, 76), (3.5, 0.5, 78)],
    [(0, 2, 79), (2, 1, 78), (3, 1, 76)],
    [(0, 2, 75), (2, 1, 73), (3, 1, 75)],
    [(0, 7, 76)],
    [(3, 1, 76)],
    [(0, 3, 79), (3, 1, 81)],
    [(0, 2, 83), (2, 0.5, 79), (2.5, 0.5, 84), (3, 0.25, 81), (3.25, 0.75, 83)],
    [(0, 2.5, 74), (2.5, 0.75, 76), (3.25, 0.75, 78)],
    [(0, 3, 79), (3, 1, 76)],
    [(0, 2.5, 76), (2.5, 0.75, 75), (3.25, 0.75, 76)],
    [(0, 3, 78), (3, 1, 75)],
    [(0, 1, 71), (2, 0.5, 69), (3, 0.5, 75), (3.5, 0.5, 78)],
    [(0, 0.5, 81), (0.5, 0.5, 83), (1, 0.5, 81), (1.5, 0.5, 83), (2, 0.5, 81), (2.5, 0.5, 83), (3, 0.5, 87), (3.5, 0.5, 90)],
    [(0, 3, 78), (3, 1, 76)],
    [(0, 2.5, 83), (2.5, 0.75, 84), (3.25, 0.75, 83)],
    [(0, 3, 81), (3, 1, 81)],
    [(0, 2.5, 78), (2.5, 0.75, 76), (3.25, 0.75, 78)],
    [(0, 2.5, 79), (2.5, 0.75, 78), (3.25, 0.75, 76)],
    [(0, 2.5, 75), (2.5, 0.75, 73), (3.25, 0.75, 75)],
    [(0, 6, 76)],
    [(2.5, 0.5, 76), (3, 0.5, 79), (3.5, 0.5, 83)],
    [(0, 4, 86)],
    [(0, 2, 86), (2, 1, 85), (3, 1, 83)],
    [(0, 3, 76), (3, 0.5, 75), (3.5, 0.5, 76)],
    [(0, 0.5, 78), (0.5, 0.25, 69), (0.75, 0.25, 71), (1, 0.25, 69), (1.25, 0.25, 71), (1.5, 0.25, 69), (1.75, 0.25, 66), (2, 0.5, 66), (2.5, 0.25, 69), (2.75, 0.25, 71), (3, 0.25, 75), (3.25, 0.25, 71), (3.5, 0.25, 69), (3.75, 0.25, 66)],
    [(0, 0.25, 71), (0.25, 0.25, 76), (0.5, 0.25, 66), (0.75, 0.25, 71), (1, 0.25, 76), (1.25, 0.25, 66), (1.5, 0.25, 71), (1.75, 0.25, 76), (2, 0.25, 66), (2.25, 0.25, 71), (2.5, 0.25, 76), (2.75, 0.25, 78), (3, 0.25, 71), (3.25, 0.25, 76), (3.5, 0.25, 78), (3.75, 0.25, 83)],
    [(0, 0.25, 71), (0.25, 0.25, 75), (0.5, 0.25, 78), (0.75, 0.25, 83), (1, 0.25, 75), (1.25, 0.25, 78), (1.5, 0.25, 83), (1.75, 0.25, 87), (2, 0.25, 78), (2.25, 0.25, 83), (2.5, 0.25, 87), (2.75, 0.25, 90), (3, 0.25, 83), (3.25, 0.25, 87), (3.5, 0.25, 90), (3.75, 0.25, 95)],
    [(0, 4, 76)],
    # Bar 42, and the only bar that uses this cell. The B5 that opens
    # this arpeggio is the one note in the whole arrangement that is
    # genuinely not in the transcription: the score writes a rising
    # B3 E4 G4 B4, and here three of the four stand an octave above it
    # while the first stands TWO octaves above, so the figure drops a
    # fifth before it climbs.
    #
    # KEPT ANYWAY, after listening to all three readings side by side:
    # B4 makes the figure rise as written and dropping the note leaves
    # a clean E5 G5 B5; the captured B5 was chosen over both. Left here
    # so the next person to measure this against the score finds the
    # decision rather than the defect. The three were built by a
    # throwaway that has been deleted; the three readings are B5 as it
    # stands, 83 -> 71, and the note removed.
    [(1, 0.25, 83), (1.25, 0.25, 76), (1.5, 0.25, 79), (1.75, 0.25, 83), (2, 1, 76), (3, 1, 76)],
    [(0, 0.5, 76), (0.5, 0.5, 83), (1, 0.5, 76), (1.5, 0.5, 83), (2, 0.5, 76), (2.5, 0.5, 83), (3, 0.5, 76), (3.5, 0.5, 83)],
    [(0, 0.5, 74), (0.5, 0.5, 81), (1, 0.5, 74), (1.5, 0.5, 81), (2, 0.5, 74), (2.5, 0.5, 81), (3, 0.5, 74), (3.5, 0.5, 81)],
    [(0, 0.5, 72), (0.5, 0.5, 79), (1, 0.5, 72), (1.5, 0.5, 79), (2, 0.5, 72), (2.5, 0.5, 79), (3, 0.5, 72), (3.5, 0.5, 79)],
    [(0, 0.5, 71), (0.5, 0.5, 78), (1, 0.5, 71), (1.5, 0.5, 78), (2, 0.5, 71), (2.5, 0.5, 78), (3, 0.5, 71), (3.5, 0.5, 78)],
    [(2, 0.5, 83), (2.5, 0.5, 76), (3, 0.5, 79), (3.5, 0.5, 83)],
    [(0, 2.5, 86), (2.5, 0.75, 85), (3.25, 0.75, 83)],
    [(0, 4, 75)],
    [(0, 2, 73), (2, 2, 75)],
]
VOICE_0_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 1), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (16, 15), (17, 7), (18, 16), (19, 17), (20, 18), (21, 19), (22, 20), (23, 21), (24, 22), (25, 23), (26, 24), (27, 1), (28, 9), (29, 10), (30, 25), (31, 26), (32, 27), (33, 28), (34, 23), (35, 24), (36, 1), (37, 9), (38, 3), (39, 4), (40, 29), (41, 30), (42, 31), (43, 31), (44, 32), (45, 32), (46, 33), (47, 34), (48, 29), (49, 35), (50, 23), (51, 36), (52, 1), (53, 9), (54, 3), (55, 37), (56, 38), (57, 29)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# 44 distinct bars over 55 bars of music.
VOICE_1_CELLS = [
    [(0, 3, (67, 71)), (3, 0.5, 69), (3.5, 0.5, 67)],
    [(0, 3, 66), (3, 1, 62)],
    [(0, 3, 59), (3, 0.5, 64), (3.5, 0.5, 66)],
    [(0, 2, (71, 76)), (2, 1, 66), (3, 1, 64)],
    [(0, 2, (66, 69)), (2, 1, 61), (3, 1, 63)],
    [(0, 7, (67, 71))],
    [(3, 1, 64)],
    [(0, 3, (71, 76)), (3, 1, 78)],
    [(0, 2, 79), (2.5, 0.5, 81), (3.25, 0.75, 79)],
    [(0, 3, 78), (3, 1, 66)],
    [(0, 2.5, 62), (2.5, 0.75, 64), (3.25, 0.75, 66)],
    [(0, 3, (67, 76)), (3, 1, 64)],
    [(0, 2.5, (64, 72)), (2.5, 0.75, 63), (3.25, 0.75, 64)],
    [(0, 3, (66, 75)), (3, 1, 63)],
    [(0, 1, (63, 66)), (1, 0.5, 57), (1.5, 0.5, 59), (2, 0.5, 57), (2.5, 0.5, 71), (3, 0.5, 63), (3.5, 0.5, 66)],
    [(0, 0.5, 69), (0.5, 0.5, 71), (1, 0.5, 69), (1.5, 0.5, 71), (2, 0.5, 69), (2.5, 0.5, 71), (3, 0.5, 75), (3.5, 0.5, 78)],
    [(0, 3, (81, 87)), (3, 1, 64)],
    [(0, 2.5, (71, 79)), (2.5, 0.75, (72, 81)), (3.25, 0.75, (71, 79))],
    [(0, 3, (69, 78)), (3, 1, (69, 78))],
    [(0, 2.5, (66, 74)), (2.5, 0.75, 64), (3.25, 0.75, 66)],
    [(0, 2.5, (67, 76)), (2.5, 0.75, (66, 74)), (3.25, 0.75, (64, 72))],
    [(0, 2.5, (63, 71)), (2.5, 0.75, 69), (3.25, 0.75, 71)],
    [(0, 6, (67, 71))],
    [(2.5, 0.5, 64), (3, 0.5, 67), (3.5, 0.5, 71)],
    [(0, 4, 74)],
    [(0, 2, 74), (2, 1, 73), (3, 1, 71)],
    [(0, 3, 69), (3, 1, 66)],
    [(0, 3, 64), (3, 0.5, 63), (3.5, 0.5, 64)],
    [(0, 0.5, 66)],
    [(0.75, 0.25, 59), (1, 0.25, 64), (1.5, 0.25, 59), (1.75, 0.25, 64)],
    [(0, 2, (63, 69)), (2, 1, 61), (3, 1, 63)],
    [(0, 4, 64)],
    [(0, 0.5, 91), (1, 0.5, 79), (3, 0.5, 93)],
    [(0, 0.5, 95), (1, 0.5, 79), (3, 0.5, 96)],
    [(0, 0.5, 93), (1, 0.5, 78), (3, 0.5, 90)],
    [(0, 0.5, 86), (1, 0.5, 78), (2.5, 0.5, 88), (3, 0.25, 78), (3.25, 0.25, 90), (3.75, 0.25, 83)],
    [(0, 0.5, 91), (1, 0.5, 76), (2, 0.5, 90), (3, 0.5, 88)],
    [(0, 0.5, 87), (1, 0.5, 75), (2, 0.5, 85), (3, 0.5, 87)],
    [(0, 4, (79, 83))],
    [(0, 2.5, 74), (2.5, 0.75, 73), (3.25, 0.75, 71)],
    [(0, 2, (71, 76)), (2, 1, (66, 72)), (3, 1, (64, 73))],
    [(0, 4, 71)],
    [(0, 2, 61), (2, 2, 63)],
    [(0, 4, (67, 71))],
]
VOICE_1_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 7), (18, 17), (19, 18), (20, 19), (21, 20), (22, 21), (23, 22), (24, 23), (25, 24), (26, 25), (27, 26), (28, 10), (29, 11), (30, 27), (31, 28), (32, 29), (34, 24), (35, 25), (36, 26), (37, 10), (38, 3), (39, 30), (40, 31), (42, 32), (43, 33), (44, 34), (45, 35), (46, 36), (47, 37), (48, 38), (50, 24), (51, 39), (52, 26), (53, 10), (54, 40), (55, 41), (56, 42), (57, 43)]
VOICE_1_VOICE = (0, 76)   # program, velocity

# ---- voice 2 ----
# 39 distinct bars over 57 bars of music.
VOICE_2_CELLS = [
    [(0, 0.5, 43), (0.5, 0.5, 50), (1, 0.5, 55), (1.5, 0.5, 59), (2, 0.5, 55), (2.5, 0.5, 59), (3, 1, 55)],
    [(0, 0.5, 38), (0.5, 0.5, 45), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 50), (2.5, 0.5, 54), (3, 0.5, 50), (3.5, 0.5, 45)],
    [(0, 0.5, 35), (0.5, 0.5, 47), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 50), (2.5, 1, 54), (3.5, 0.5, 54)],
    [(0, 4, (36, 48))],
    [(0, 4, (35, 47))],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 52), (2.5, 0.5, 55), (3, 0.5, 52), (3.5, 0.5, 47)],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 55), (1.5, 0.5, 40), (2, 0.5, 55), (2.5, 1, 59), (3.5, 0.5, 47)],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 40), (2.5, 1, 55), (3.5, 0.5, 47)],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 40), (2.5, 0.5, 55), (3, 0.5, 52), (3.5, 0.5, 47)],
    [(0, 0.5, 38), (0.5, 0.5, 45), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 38), (2.5, 0.5, 54), (3, 0.5, 57), (3.5, 0.5, 45)],
    [(0, 0.5, 35), (0.5, 0.5, 47), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 35), (2.5, 0.5, 50), (3, 0.5, 54), (3.5, 0.5, 47)],
    [(0, 0.5, 36), (0.5, 0.5, 48), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 36), (2.5, 0.5, 55), (3, 0.5, 59), (3.5, 0.5, 48)],
    [(0, 0.5, 33), (0.5, 0.5, 48), (1, 0.5, 52), (1.5, 0.5, 57), (2, 0.5, 33), (2.5, 0.5, 52), (3, 0.5, 57), (3.5, 0.5, 48)],
    [(0, 0.5, 35), (0.5, 0.5, 51), (1, 0.5, 54), (1.5, 0.5, 57), (2, 0.5, 54), (2.5, 1, 57), (3.5, 0.5, 47)],
    [(0, 4, 35)],
    [(0, 4, (47, 54, 63))],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 52), (2.5, 1, 55), (3.5, 0.5, 47)],
    [(0, 0.5, 38), (0.5, 0.5, 45), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 38), (2.5, 0.5, 54), (3, 0.5, 50), (3.5, 0.5, 45)],
    [(0, 0.5, 35), (0.5, 0.5, 47), (1, 0.5, 50), (1.5, 0.5, 54), (2, 0.5, 35), (2.5, 0.5, 50), (3, 0.5, 45), (3.5, 0.5, 47)],
    [(0, 0.5, 36), (0.5, 0.5, 48), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 36), (2.5, 0.5, 52), (3, 0.5, 48), (3.5, 0.5, 43)],
    [(0, 0.5, 35), (0.5, 0.5, 47), (1, 0.5, 51), (1.5, 0.5, 54), (2, 0.5, 39), (2.5, 0.5, 51), (3, 0.5, 47), (3.5, 0.5, 42)],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, 52), (1.5, 0.5, 55), (2, 0.5, 52), (2.5, 0.5, 55), (3, 0.25, 52), (3.25, 0.25, 54), (3.5, 0.5, 55)],
    [(0, 0.25, 43), (0.25, 0.25, 50), (0.5, 0.25, 55), (0.75, 0.25, 59), (1, 0.25, 55), (1.25, 0.25, 59), (1.5, 0.25, 55), (1.75, 0.25, 50), (2, 0.25, 43), (2.25, 0.25, 50), (2.5, 0.25, 55), (2.75, 0.25, 59), (3, 0.25, 55), (3.25, 0.25, 59), (3.5, 0.25, 55), (3.75, 0.25, 50)],
    [(0, 0.25, 38), (0.25, 0.25, 45), (0.5, 0.25, 50), (0.75, 0.25, 54), (1, 0.25, 50), (1.25, 0.25, 54), (1.5, 0.25, 50), (1.75, 0.25, 45), (2, 0.25, 38), (2.25, 0.25, 45), (2.5, 0.25, 50), (2.75, 0.25, 54), (3, 0.25, 50), (3.25, 0.25, 54), (3.5, 0.25, 50), (3.75, 0.25, 45)],
    [(0, 0.25, 36), (0.25, 0.25, 43), (0.5, 0.25, 48), (0.75, 0.25, 52), (1, 0.25, 48), (1.25, 0.25, 52), (1.5, 0.25, 48), (1.75, 0.25, 43), (2, 0.25, 36), (2.25, 0.25, 43), (2.5, 0.25, 48), (2.75, 0.25, 52), (3, 0.25, 48), (3.25, 0.25, 52), (3.5, 0.25, 48), (3.75, 0.25, 43)],
    [(0, 0.25, 35), (0.25, 0.25, 42), (0.5, 0.5, 47), (1, 0.5, 47), (1.5, 0.25, 47), (1.75, 0.25, 42), (2, 0.25, 35), (2.25, 0.25, 42), (2.5, 0.5, 47), (3, 0.5, 47), (3.5, 0.25, 47), (3.75, 0.25, 42)],
    [(0, 1, (35, 47)), (1, 1, 47), (2, 1, (35, 47))],
    [(0, 1, (35, 47)), (1, 1, (35, 47)), (2, 1, (35, 47)), (3, 1, (35, 47))],
    [(0, 0.25, 40), (0.25, 0.25, 47), (0.5, 0.25, 52), (0.75, 0.25, 55), (1, 0.25, 52), (1.25, 0.25, 55), (1.5, 0.25, 52), (1.75, 0.25, 47), (2, 0.25, 40), (2.25, 0.25, 47), (2.5, 0.25, 52), (2.75, 0.25, 55), (3, 0.25, 52), (3.25, 0.25, 55), (3.5, 0.25, 52), (3.75, 0.25, 47)],
    [(0, 0.25, 40), (0.25, 0.25, 47), (0.5, 0.25, 52), (0.75, 0.25, 55)],
    [(0, 2, 64), (2, 1, 64), (3, 1, 71)],
    [(0, 2, 62), (2, 1, 62), (3, 1, 78)],
    [(0, 2, 62), (2, 2, 62)],
    [(0, 2, 60), (2, 1, 60), (3, 1, 76)],
    [(0, 2, 59), (2, 1, 59), (3, 1, 75)],
    [(0, 0.5, 52), (0.5, 0.5, 59), (1, 0.5, 64), (1.5, 0.5, 67), (2, 0.5, 64), (2.5, 0.5, 67), (3, 0.5, 64), (3.5, 0.5, 59)],
    [(0, 0.5, 52), (0.5, 0.5, 59), (1, 0.5, 64), (1.5, 0.5, 67), (3, 1, 40)],
    [(0, 2, (36, 48)), (2, 1, (33, 45)), (3, 1, (34, 46))],
    [(0, 0.25, 40), (0.25, 0.25, 47), (0.5, 0.25, 52), (0.75, 0.25, 55), (1, 3, 59)],
]
VOICE_2_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 4), (17, 16), (18, 8), (19, 17), (20, 18), (21, 19), (22, 20), (23, 5), (24, 21), (25, 22), (26, 22), (27, 23), (28, 23), (29, 24), (30, 24), (31, 25), (32, 26), (33, 27), (34, 22), (35, 22), (36, 23), (37, 23), (38, 3), (39, 4), (40, 28), (41, 29), (42, 30), (43, 30), (44, 31), (45, 32), (46, 33), (47, 34), (48, 35), (49, 36), (50, 22), (51, 22), (52, 23), (53, 23), (54, 37), (55, 4), (57, 38)]
VOICE_2_VOICE = (0, 60)   # program, velocity

VOICES = [
    ('Voice 0', VOICE_0_CELLS, VOICE_0_PLAN, VOICE_0_VOICE),
    ('Voice 1', VOICE_1_CELLS, VOICE_1_PLAN, VOICE_1_VOICE),
    ('Voice 2', VOICE_2_CELLS, VOICE_2_PLAN, VOICE_2_VOICE),
]


def vlq(n):
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)


def unroll(cells, plan):
    """Bars back into a flat list of (onset, length, pitch)."""
    out = []
    for bar_index, cell_id in plan:
        base = bar_index * BAR
        for onset, length, pitch in cells[cell_id]:
            out.append((base + onset, length, pitch))
    return sorted(out)


def seconds(end_beat):
    """How long the piece really lasts, tempo map and all.

    Dividing the length in beats by the opening tempo answers a question
    the piece stopped asking at the first change."""
    total = 0.0
    for i, (beat, bpm) in enumerate(TEMPO):
        nxt = TEMPO[i + 1][0] if i + 1 < len(TEMPO) else end_beat
        total += max(0.0, min(nxt, end_beat) - beat) * 60.0 / bpm
    return total


def track(events, end_tick):
    body = bytearray()
    prev = 0
    for tick, data in sorted(events, key=lambda e: e[0]):
        body += vlq(tick - prev) + data
        prev = tick
    body += vlq(max(0, end_tick - prev))
    body += bytes([0xFF, 0x2F, 0x00])
    return b"MTrk" + struct.pack(">I", len(body)) + bytes(body)


def build():
    pw = 0
    while (1 << pw) < TIME_SIG[1]:
        pw += 1
    laid = []
    for ch, (name, cells, plan, voice) in enumerate(VOICES):
        laid.append((ch, unroll(cells, plan), voice))
    # Move the whole piece far enough in that LEAD_IN beats of silence
    # stand before its first note - however much of that the plan
    # already provides.
    first = min(o for _, n, _ in laid for o, _, _ in n)
    shift = max(0.0, LEAD_IN - first)
    laid = [(ch, [(o + shift, d, p) for o, d, p in n], v)
            for ch, n, v in laid]
    end = max(o + d for _, n, _ in laid for o, d, _ in n)
    end_tick = int(round((end + TAIL) * DIV))
    # Articulation, applied LAST so that the piece is the same length as
    # it was written: what changes is when each note is released, not
    # when the next one begins or where the file ends.
    laid = [(ch, [(o, d - trim_of(d), p) for o, d, p in n], v)
            for ch, n, v in laid]
    # The opening tempo stays at tick 0: the lead-in is silence, but a
    # file whose first tempo arrives late plays that silence at whatever
    # the default is, and the length of the rest would come out wrong.
    meta = [(0 if beat <= 0 else int(round((beat + shift) * DIV)),
             bytes([0xFF, 0x51, 0x03, (us >> 16) & 0xFF,
                    (us >> 8) & 0xFF, us & 0xFF]))
            for beat, us in ((b, int(round(60000000.0 / v)))
                             for b, v in TEMPO)]
    meta += [(0, bytes([0xFF, 0x03, len(TITLE)])
              + TITLE.encode("latin-1")),
             (0, bytes([0xFF, 0x58, 0x04, TIME_SIG[0], pw,
                        24, 8]))]
    parts = [track(meta, end_tick)]
    for ch, notes, (prog, vel) in laid:
        ev = [(0, bytes([0xC0 | ch, prog]))]
        for onset, length, pitch in notes:
            t = int(round(onset * DIV))
            n = max(1, int(round(length * DIV)))
            for p in (pitch if isinstance(pitch, tuple)
                      else (pitch,)):
                ev.append((t, bytes([0x90 | ch, p, vel])))
                ev.append((t + n, bytes([0x80 | ch, p, 0])))
        # The closing rest has to be something a player can SEE. Written
        # as a bare gap before end-of-track it is only a delta, and a
        # player that stops at the last event it finds drops it -
        # Windows Media Player does exactly that, cutting TAIL off every
        # piece here. So every track runs to end_tick and every channel
        # puts an All Notes Off there: the gap becomes an event.
        ev.append((end_tick, bytes([0xB0 | ch, 123, 0])))
        parts.append(track(ev, end_tick))
    return (b"MThd" + struct.pack(">IHHH", 6, 1, len(parts),
                                  DIV) + b"".join(parts))


def main(argv):
    # Into output/, and the directory is made if it is not there - see
    # arr_canon.py.
    out = argv[1] if len(argv) > 1 else os.path.join(
        OUT_DIR, 'greensleeves_arr.mid')
    here = os.path.dirname(out)
    if here and not os.path.isdir(here):
        os.makedirs(here)
    open(out, "wb").write(build())
    print("%s -> %s" % (TITLE, out))
    for name, cells, plan, _ in VOICES:
        print("  %-14s %3d bars, %3d distinct, %4d attacks"
              % (name, len(plan), len(cells),
                 len(unroll(cells, plan))))
    # To the end of track and not the last note-off; the mean of the
    # tempo map and not its first step; and the tempo beats shifted the
    # way build() shifts them - this is the one piece here whose shift
    # is not zero, and it is worth half a second. See arr_canon.py.
    laid = [unroll(c, p) for _, c, p, _ in VOICES]
    first = min(o for n in laid for o, _, _ in n)
    shift = max(0.0, LEAD_IN - first)
    total = max(o + d for n in laid for o, d, _ in n) + shift + TAIL
    steps = [(0.0 if b <= 0 else b + shift, v) for b, v in TEMPO]
    secs = weighted = 0.0
    for i, (b, v) in enumerate(steps):
        nxt = steps[i + 1][0] if i + 1 < len(steps) else total
        span = max(0.0, min(nxt, total) - b)
        secs += span * 60.0 / v
        weighted += span * v
    print("  %.1f s, %g bpm mean over %d steps, %d/%d"
          % (secs, round(weighted / total, 1), len(TEMPO),
             TIME_SIG[0], TIME_SIG[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
