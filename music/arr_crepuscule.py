"""Le Souvenir avec le crepuscule (arr.).

Arranged from a transcription of HOYO-MiX's Le Souvenir avec le
crepuscule.

    python arr_crepuscule.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
# The tempo map: (beat, beats per minute). Written as the round numbers
# a player would be given rather than as the microsecond values read
# back out of the finished file - 359928 is 166.7 bpm, and 167 is what
# anyone would actually have written.
#
# The tempo map is part of the arrangement, not of the playback.
TEMPO = [
    (0.0, 167),
    # One bar held back, at 0:54. The running quavers stop here and all
    # three voices move together in crotchets - Bb minor to A flat - and
    # the bar after restarts the figure in a new register. It is the one
    # place in the piece where the texture pauses to change, and taking
    # it at the same speed as the running bars steps over the turn.
    # Written against the music's own beats: the piece is preceded by a
    # bar of silence, so bar 51 of the file begins at beat 150.
    (150.0, 160),
    (153.0, 167),         # a tempo
    (219.0, 160),         # the last two bars draw back
    (222.0, 155),
]
BPM = TEMPO[0][1]
TIME_SIG = (3, 4)
BAR = 3          # beats per bar
# Silence at each end, in beats: nothing begins on a note or ends on
# one. Every piece here gets about 2 s before the first note and 4 s
# after the last, rounded to whole beats at the tempo in force there -
# at 167 bpm that is 2.2 s and 3.9 s.
LEAD_IN = 6
TAIL = 10
# Every note gives up a little of its tail, so the next stroke of the
# same pitch starts against silence instead of picking up exactly where
# the last one stopped. Stepped by whole beats, five per cent as the
# floor: 5 under a beat and at one beat, 10 at two, 15 at three, 20 at
# four and no further. This piece had 379 joins that met dead on, by far
# the most of the five - it is the one whose accompaniment repeats a
# pitch on every beat.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))


TITLE = 'Le Souvenir avec le crepuscule (arr.)'

# ---- voice 0 ----
# 47 distinct bars over 73 bars of music.
VOICE_0_CELLS = [
    [(0, 3, 87)],
    [(0, 2, 85), (2, 1, 83)],
    [(0, 3, 82)],
    [(1, 1, 75), (2, 1, 77)],
    [(0, 1, 78), (1, 1, 80), (2, 1, 82)],
    [(0, 1, 80), (1, 1, 78), (2, 1, 75)],
    [(0, 3, 78)],
    [(0, 3, 77)],
    [(1, 2, 87)],
    [(0, 1, 80), (1, 1, 78), (2, 1, 77)],
    [(0, 3, 75)],
    [(0, 1, 78), (1, 1, 77), (2, 1, 78)],
    [(0, 2, 80), (2, 1, 85)],
    [(1, 1, 82), (2, 1, 84)],
    [(0, 1, 85), (1, 1, 84), (2, 1, 82)],
    [(0, 2, 84), (2, 1, 77)],
    [(0, 1, 82), (1, 1, 80), (2, 1, 78)],
    [(0, 2, 80), (2, 1, 73)],
    [(0, 1, 78), (1, 1, 77), (2, 1, 75)],
    [(0, 2, 73), (2, 1, 72)],
    [(0, 1, 70), (2.5, 0.5, 82)],
    [(1, 1, 77), (2, 1, 82)],
    [(0, 2, 80), (2, 1, 78)],
    [(1, 1, 70), (2, 1, 72)],
    [(0, 1, 73), (1, 1, 75), (2, 1, 77)],
    [(0, 1, 75), (1, 1, 73), (2, 1, 70)],
    [(0, 3, 73)],
    [(0, 3, 72)],
    [(1, 2, 82)],
    [(0, 1, 75), (1, 1, 73), (2, 1, 72)],
    [(0, 3, 70)],
    [(0, 1, 73), (1, 1, 72), (2, 1, 73)],
    [(0, 2, 75), (2, 1, 80)],
    [(0, 2, 75), (2, 1, 84)],
    [(1, 1, 77), (2, 1, 79)],
    [(0, 1, 80), (1, 1, 79), (2, 1, 77)],
    [(0, 2, 79), (2, 1, 72)],
    [(0, 2, 77), (2, 1, 70)],
    [(0, 2, 70), (2, 1, 69)],
    [(0, 1, 70), (1, 2, 82)],
    [(1, 2, 81)],
    [(1, 2, 80)],
    [(1, 2, 79)],
    [(1, 2, 78)],
    [(1, 2, 77)],
    [(1, 2, 75)],
    [(1, 2, 73)],
]
VOICE_0_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 1), (11, 2), (12, 3), (13, 4), (14, 9), (15, 10), (16, 3), (17, 11), (18, 12), (19, 2), (20, 3), (21, 11), (22, 12), (23, 2), (24, 13), (25, 14), (26, 15), (27, 16), (28, 17), (29, 18), (30, 19), (31, 20), (32, 2), (33, 3), (34, 21), (35, 2), (36, 22), (37, 7), (38, 23), (39, 24), (40, 25), (41, 26), (42, 27), (43, 28), (44, 22), (45, 7), (46, 23), (47, 24), (48, 29), (49, 30), (50, 23), (51, 31), (52, 32), (53, 7), (54, 23), (55, 31), (56, 33), (57, 7), (58, 34), (59, 35), (60, 36), (61, 18), (62, 37), (63, 29), (64, 38), (65, 39), (66, 40), (67, 41), (68, 42), (69, 43), (70, 44), (71, 45), (72, 46), (74, 2)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# 56 distinct bars over 70 bars of music.
VOICE_1_CELLS = [
    [(0, 3, (75, 78, 82))],
    [(0, 2, (73, 78, 81)), (2.125, 0.875, 85)],
    [(0, 3, (70, 75, 78))],
    [(0, 1, (66, 71, 75))],
    [(0, 3, (68, 71, 77))],
    [(0, 3, (66, 70, 75))],
    [(0, 3, (65, 68, 74))],
    [(1, 2, (75, 78, 82))],
    [(0, 2, (73, 78, 81))],
    [(1, 1, (63, 66, 70)), (2, 1, (65, 70))],
    [(0, 1, (66, 71, 75)), (1, 1, 68), (2, 1, 70)],
    [(0, 1, (68, 74)), (1, 1, 66), (2, 1, 65)],
    [(0, 3, (63, 66, 70))],
    [(0, 1, (66, 71, 75)), (1, 1, 65), (2, 1, 66)],
    [(0, 2, (68, 73, 77)), (2, 1, 73)],
    [(0, 3, (70, 73, 77))],
    [(1, 1, 63), (2, 1, 65)],
    [(0, 2, (70, 73, 77)), (2, 1, 65)],
    [(0, 1, (65, 70, 73)), (1, 1, 70), (2, 1, 72)],
    [(0, 1, (73, 77, 82)), (1, 1, 72), (2, 1, 70)],
    [(0, 2, (72, 77, 80)), (2, 1, 65)],
    [(0, 1, (70, 73, 78)), (1, 1, 68), (2, 1, 66)],
    [(0, 2, (68, 73, 77)), (2, 1, 61)],
    [(0, 1, (66, 70, 75)), (1, 1, 65), (2, 1, 63)],
    [(0, 2, (61, 65, 69)), (2, 1, 60)],
    [(0, 1, (58, 61, 65)), (2.5, 0.5, (73, 77))],
    [(0, 3, (73, 77))],
    [(0.5, 1.5, 65), (2, 1, 70)],
    [(0, 2, (68, 71, 75)), (2, 1, 66)],
    [(0, 3, (65, 70, 73))],
    [(0, 1, (66, 70))],
    [(0, 3, (67, 70))],
    [(0, 3, (65, 69))],
    [(1, 2, 70)],
    [(0, 1, (65, 69, 72))],
    [(0, 3, (61, 65))],
    [(1, 1, (58, 61, 65)), (2, 1, (60, 63, 68))],
    [(0, 1, (61, 66, 70)), (1, 1, 60), (2, 1, 61)],
    [(0, 2, (63, 68, 72)), (2, 1, 68)],
    [(0, 3, (65, 68, 73))],
    [(1, 1, (61, 65)), (2, 1, (60, 65))],
    [(0, 2, (63, 68, 72)), (2, 1, 72)],
    [(1, 1, 65), (2, 1, 67)],
    [(0, 1, (68, 72, 77)), (1, 1, 67), (2, 1, 65)],
    [(0, 2, (67, 72, 75)), (2, 1, 60)],
    [(0, 2, (65, 70, 73)), (2, 1, 58)],
    [(0, 1, (63, 66, 70)), (1, 1, 61), (2, 1, 60)],
    [(0, 2, (58, 60, 65)), (2, 1, 57)],
    [(0, 1, (58, 61, 65)), (1, 2, (70, 73, 77))],
    [(1, 2, (69, 74, 78))],
    [(1, 2, (68, 73, 77))],
    [(1, 2, (67, 72, 76))],
    [(1, 2, (66, 71, 75))],
    [(1, 2, (65, 68, 73))],
    [(1, 2, (66, 71, 78))],
    [(1, 2, (65, 70, 77))],
]
VOICE_1_PLAN = [(1, 0), (2, 1), (3, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8), (11, 2), (12, 9), (13, 10), (14, 11), (15, 12), (16, 9), (17, 13), (18, 14), (19, 15), (20, 16), (21, 13), (22, 14), (23, 17), (24, 18), (25, 19), (26, 20), (27, 21), (28, 22), (29, 23), (30, 24), (31, 25), (32, 26), (33, 16), (34, 27), (35, 15), (36, 28), (37, 29), (39, 30), (40, 30), (41, 31), (42, 32), (43, 33), (44, 28), (45, 29), (47, 30), (48, 34), (49, 35), (50, 36), (51, 37), (52, 38), (53, 39), (54, 40), (55, 37), (56, 41), (57, 39), (58, 42), (59, 43), (60, 44), (61, 23), (62, 45), (63, 46), (64, 47), (65, 48), (66, 49), (67, 50), (68, 51), (69, 52), (70, 53), (71, 54), (72, 55), (74, 15)]
VOICE_1_VOICE = (0, 76)   # program, velocity

# ---- voice 2 ----
# 46 distinct bars over 73 bars of music.
VOICE_2_CELLS = [
    [(0, 1, 39), (1, 1, (63, 66, 70)), (2, 1, (63, 66, 70))],
    [(0, 1, 39), (1, 1, (63, 66, 69)), (2, 1, (63, 66, 69))],
    [(0, 1, 32), (1, 1, (59, 63, 68)), (2, 1, (59, 63, 68))],
    [(0, 1, 32), (1, 1, (59, 63, 65)), (2, 1, (59, 63, 65))],
    [(0, 1, 34), (1, 1, (58, 63, 66)), (2, 1, (58, 63, 66))],
    [(0, 1, 34), (1, 1, (56, 58, 62)), (2, 1, (56, 58, 62))],
    [(0, 1, 40), (1, 1, (62, 66, 69)), (2, 1, (62, 66, 69))],
    [(0, 1, 36), (1, 1, 60), (2, 1, (60, 63, 66))],
    [(0, 1, 32), (1, 1, (56, 59, 63)), (2, 1, (56, 59, 63))],
    [(0, 1, 39), (1, 1, (54, 58)), (2, 1, (54, 58))],
    [(0, 1, 37), (1, 1, (56, 59, 65)), (2, 1, (56, 59, 65))],
    [(0, 1, 30), (1, 1, (49, 54, 58)), (2, 1, (49, 54, 58))],
    [(0, 1, 30), (1, 1, (53, 58, 61)), (2, 1, (53, 58, 61))],
    [(0, 1, 34), (1, 1, (53, 58, 61)), (2, 1, (53, 58, 61))],
    [(0, 1, 29), (1, 1, (53, 56, 60)), (2, 1, (53, 56, 60))],
    [(0, 1, 30), (1, 1, (54, 58, 61)), (2, 1, (54, 58, 61))],
    [(0, 1, 37), (1, 1, (53, 56, 61)), (2, 1, (53, 56))],
    [(0, 1, 39), (1, 1, (54, 58, 63)), (2, 1, (54, 58))],
    [(0, 1, 29), (1, 1, (53, 57, 60)), (2, 1, (53, 57))],
    [(0, 0.5, 34), (0.5, 0.5, 53), (1, 0.5, (58, 61)), (1.5, 0.5, 60), (2, 1, (58, 61))],
    [(0, 0.5, (34, 46)), (0.5, 0.5, (53, 58, 61)), (1, 0.5, (53, 58, 61)), (1.5, 0.5, (53, 58, 61)), (2, 0.5, (53, 58, 63)), (2.5, 0.5, (53, 58, 61))],
    [(0, 0.5, (34, 46)), (0.5, 0.5, (53, 58, 61)), (1, 0.5, (53, 58, 61)), (1.5, 0.5, (53, 58, 61)), (2, 0.5, (53, 58)), (2.5, 0.5, (53, 58, 61))],
    [(0, 0.5, (34, 46)), (0.5, 0.5, (53, 58, 61)), (1, 0.5, (53, 58, 61)), (1.5, 0.5, (53, 58, 61)), (2, 0.5, (53, 58, 60)), (2.5, 0.5, (53, 58, 61))],
    [(0, 0.5, (34, 46)), (0.5, 0.5, (53, 58, 61)), (1, 0.5, (53, 58, 61)), (1.5, 0.5, (53, 58, 61)), (2, 0.5, (53, 58, 61)), (2.5, 0.5, (53, 58, 61))],
    [(0, 0.5, (35, 47)), (0.5, 0.5, (54, 59, 63)), (1, 0.5, (54, 59, 63)), (1.5, 0.5, (54, 59, 63)), (2, 0.5, (54, 59, 63)), (2.5, 0.5, (54, 59, 63))],
    [(0, 0.5, (39, 51)), (0.5, 0.5, (54, 58, 63)), (1, 0.5, (54, 58, 63)), (1.5, 0.5, (54, 58, 63)), (2, 0.5, (54, 58, 63)), (2.5, 0.5, (54, 58, 63))],
    [(0, 0.5, (41, 53)), (0.5, 0.5, (55, 58, 61)), (1, 0.5, (55, 58, 61)), (1.5, 0.5, (55, 58, 61)), (2, 0.5, (55, 58, 61)), (2.5, 0.5, (55, 58, 61))],
    [(0, 0.5, (41, 53)), (0.5, 0.5, (51, 57, 60)), (1, 0.5, (51, 57, 60)), (1.5, 0.5, (51, 57, 60)), (2, 0.5, (51, 57, 60)), (2.5, 0.5, (51, 57, 60))],
    [(0, 0.5, (31, 43)), (0.5, 0.5, (53, 58, 61)), (1, 0.5, (53, 58, 61)), (1.5, 0.5, (53, 58, 61)), (2, 0.5, (53, 58, 61)), (2.5, 0.5, (53, 58, 61))],
    [(0, 0.5, (34, 46)), (0.5, 0.5, (53, 58)), (1, 0.5, (53, 58)), (1.5, 0.5, (53, 58)), (2, 0.5, (53, 58)), (2.5, 0.5, (53, 58))],
    [(0, 1, 34), (1, 1, (34, 46)), (2, 1, (32, 44))],
    [(0, 0.5, (27, 39)), (0.5, 0.5, (51, 54)), (1, 0.5, 58), (1.5, 0.5, (51, 54)), (2, 0.5, 58), (2.5, 0.5, (51, 54))],
    [(0, 0.5, (32, 44)), (0.5, 0.5, (51, 56)), (1, 0.5, (56, 60)), (1.5, 0.5, (51, 56)), (2, 0.5, (56, 60)), (2.5, 0.5, (51, 56))],
    [(0, 0.5, (37, 49)), (0.5, 0.5, (53, 56)), (1, 0.5, (56, 60)), (1.5, 0.5, (53, 56)), (2, 0.5, (56, 60)), (2.5, 0.5, (53, 56))],
    [(0, 0.5, (37, 49)), (0.5, 0.5, (53, 58)), (1, 0.5, 58), (1.5, 0.5, (53, 58)), (2, 0.5, 58), (2.5, 0.5, (53, 58))],
    [(0, 0.5, (29, 41)), (0.5, 0.5, (53, 56)), (1, 0.5, (56, 60)), (1.5, 0.5, (53, 56)), (2, 0.5, (56, 60)), (2.5, 0.5, (53, 56))],
    [(0, 0.5, (36, 48)), (0.5, 0.5, (51, 55)), (1, 0.5, 60), (1.5, 0.5, (51, 55)), (2, 0.5, 60), (2.5, 0.5, (51, 55))],
    [(0, 0.5, 34), (0.5, 0.5, (49, 53)), (1, 0.5, 58), (1.5, 1.5, (49, 53))],
    [(0, 0.5, (36, 48)), (0.5, 0.5, (51, 54)), (1, 0.5, 58), (1.5, 0.5, (51, 54)), (2, 0.5, 58), (2.5, 0.5, (51, 54))],
    [(0, 0.5, 29), (0.5, 0.5, (48, 53)), (1, 0.5, 57), (1.5, 1.5, (48, 53))],
    [(0, 1, 34), (1, 1, (58, 61, 65)), (2, 1, (58, 61, 65))],
    [(0, 1, 34), (1, 1, (58, 62, 66)), (2, 1, (58, 62, 66))],
    [(0, 1, 34), (1, 1, (58, 60, 64)), (2, 1, (58, 60, 64))],
    [(0, 1, 34), (1, 1, (59, 63)), (2, 1, (59, 63))],
    [(0, 1, 34), (1, 1, (58, 61)), (2, 1, (58, 61))],
    [(0, 3, (34, 46))],
]
VOICE_2_PLAN = [(1, 0), (2, 1), (3, 0), (4, 0), (5, 2), (6, 3), (7, 4), (8, 5), (9, 0), (10, 6), (11, 0), (12, 7), (13, 8), (14, 5), (15, 9), (16, 9), (17, 8), (18, 10), (19, 11), (20, 11), (21, 8), (22, 10), (23, 12), (24, 12), (25, 13), (26, 14), (27, 15), (28, 16), (29, 17), (30, 18), (31, 19), (32, 20), (33, 21), (34, 22), (35, 23), (36, 24), (37, 23), (38, 23), (39, 25), (40, 25), (41, 26), (42, 27), (43, 23), (44, 24), (45, 23), (46, 28), (47, 25), (48, 27), (49, 29), (50, 30), (51, 31), (52, 32), (53, 33), (54, 34), (55, 31), (56, 32), (57, 33), (58, 33), (59, 35), (60, 36), (61, 31), (62, 37), (63, 38), (64, 39), (65, 40), (66, 41), (67, 40), (68, 42), (69, 43), (70, 44), (71, 43), (72, 44), (74, 45)]
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
        OUT_DIR, 'crepuscule_arr.mid')
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
    # way build() shifts them. See arr_canon.py.
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
