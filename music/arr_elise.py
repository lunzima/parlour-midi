"""Fur Elise (arr.).

Arranged from Mutopia's Fur Elise engraving.

    python arr_elise.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
# The tempo map: (beat, beats per minute). Written as the round numbers
# a player would be given, not as the microsecond values read back out
# of the finished file - those are the same numbers after a division and
# a rounding, and 833333 says nothing to anyone.
#
# The tempo map is part of the arrangement, not of the playback.
TEMPO = [
    (0.0, 72),            # the tune
    (122.0, 78),          # the middle section presses forward
    (152.0, 70),          # and gives the ground back
    (156.0, 66),
    (157.0, 72),          # a tempo
    (186.0, 60),          # the close
]
BPM = TEMPO[0][1]
TIME_SIG = (3, 8)
BAR = 1.5          # beats per bar
# Silence at each end, in beats: nothing begins on a note or ends on
# one. Every piece here gets about 2 s before the first note and 4 s
# after the last, rounded to whole beats at the tempo in force there -
# at 72 bpm that is 1.7 s and 3.3 s.
LEAD_IN = 2
TAIL = 4
# Every note gives up a little of its tail, so the next stroke of the
# same pitch starts against silence instead of picking up exactly where
# the last one stopped. Stepped by whole beats, five per cent as the
# floor: 5 under a beat and at one beat, 10 at two, 15 at three, 20 at
# four and no further. In 3/8 almost everything here is under a beat,
# so almost everything takes the floor - which is the case the floor
# exists for.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))
TITLE = 'Fur Elise (arr.)'

# ---- voice 0 ----
# 47 distinct bars over 125 bars of music.
VOICE_0_CELLS = [
    [(0, 0.25, 76), (0.25, 0.25, 75), (0.5, 0.25, 76), (0.75, 0.25, 75), (1, 0.25, 76), (1.25, 0.25, 71)],
    [(0, 0.25, 74), (0.25, 0.25, 72), (0.5, 0.5, 69), (1.25, 0.25, 60)],
    [(0, 0.25, 64), (0.25, 0.25, 69), (0.5, 0.5, 71), (1.25, 0.25, 64)],
    [(0, 0.25, 68), (0.25, 0.25, 71), (0.5, 0.5, 72), (1.25, 0.25, 64)],
    [(0, 0.25, 72), (0.25, 0.25, 71), (0.5, 1, 69)],
    [(0, 0.25, 72), (0.25, 0.25, 71), (0.5, 0.5, 69), (1.25, 0.25, 71)],
    [(0, 0.25, 72), (0.25, 0.25, 74), (0.5, 0.75, 76), (1.25, 0.25, 67)],
    [(0, 0.25, 77), (0.25, 0.25, 76), (0.5, 0.75, 74), (1.25, 0.25, 65)],
    [(0, 0.25, 76), (0.25, 0.25, 74), (0.5, 0.75, 72), (1.25, 0.25, 64)],
    [(0, 0.25, 74), (0.25, 0.25, 72), (0.5, 0.5, 71), (1.25, 0.25, 64)],
    [(0, 0.25, 76), (0.75, 0.25, 76), (1, 0.25, 88)],
    [(0.25, 0.25, 75), (0.5, 0.5, 76), (1.25, 0.25, 75)],
    [(0, 0.25, 72), (0.25, 0.25, 71), (0.5, 0.5, 69), (1.25, 0.25, 72)],
    [(0, 0.25, 72), (0.25, 0.25, 72), (0.5, 0.125, 65), (0.625, 0.125, 69), (0.75, 0.75, 72)],
    [(0, 0.375, 77), (0.375, 0.125, 76), (0.5, 0.5, 76), (1, 0.5, 74)],
    [(0, 0.375, 82), (0.375, 0.125, 81), (0.5, 0.25, 81), (0.75, 0.25, 79), (1, 0.25, 77), (1.25, 0.25, 76)],
    [(0, 0.25, 74), (0.25, 0.25, 72), (0.5, 0.5, 70), (1, 0.5, 69)],
    # Bar 49. The score's \appoggiatura bes'32 is in voice 1, not here:
    # sharing the 32nd with it left both at 12 ticks, 47.7 ms, the two
    # shortest notes in the piece and the only ones the beeper struggles
    # with. The a' it leans on keeps its whole 32nd.
    [(0, 0.125, 69), (0.125, 0.125, 67), (0.25, 0.125, 69), (0.375, 0.125, 70), (0.5, 1, 72)],
    [(0, 0.25, 74), (0.25, 0.25, 75), (0.5, 0.75, 76), (1.25, 0.25, 76)],
    [(0, 0.25, 77), (0.25, 0.25, 69), (0.5, 1, 72)],
    [(0, 0.375, 74), (0.375, 0.125, 71), (0.5, 0.125, 72), (0.625, 0.125, 79), (0.75, 0.125, 67), (0.875, 0.125, 79), (1, 0.125, 69), (1.125, 0.125, 79), (1.25, 0.125, 71), (1.375, 0.125, 79)],
    [(0, 0.125, 72), (0.125, 0.125, 79), (0.25, 0.125, 74), (0.375, 0.125, 79), (0.5, 0.125, 76), (0.625, 0.125, 79), (0.75, 0.125, 84), (0.875, 0.125, 83), (1, 0.125, 81), (1.125, 0.125, 79), (1.25, 0.125, 77), (1.375, 0.125, 76)],
    [(0, 0.125, 74), (0.125, 0.125, 79), (0.25, 0.125, 77), (0.375, 0.125, 74), (0.5, 0.125, 72), (0.625, 0.125, 79), (0.75, 0.125, 67), (0.875, 0.125, 79), (1, 0.125, 69), (1.125, 0.125, 79), (1.25, 0.125, 71), (1.375, 0.125, 79)],
    [(0, 0.125, 74), (0.125, 0.125, 79), (0.25, 0.125, 77), (0.375, 0.125, 74), (0.5, 0.125, 76), (0.625, 0.125, 77), (0.75, 0.125, 76), (0.875, 0.125, 75), (1, 0.125, 76), (1.125, 0.125, 71), (1.25, 0.125, 76), (1.375, 0.125, 75)],
    [(0, 0.125, 76), (0.125, 0.125, 71), (0.25, 0.125, 76), (0.375, 0.125, 75), (0.5, 0.75, 76), (1.25, 0.25, 71)],
    [(0, 0.25, 76), (0.25, 0.25, 75), (0.5, 0.75, 76), (1.25, 0.25, 71)],
    [(0, 0.25, 76), (0.25, 0.25, 75), (0.5, 0.25, 76), (0.75, 0.25, 75), (1, 0.25, 76), (1.25, 0.25, 75)],
    [(0.25, 0.25, 75), (0.5, 0.25, 76), (1.25, 0.25, 75)],
    [(0, 0.25, 72), (0.25, 0.25, 71), (0.5, 0.5, 69)],
    [(0.5, 1.5, 73)],
    [(0.5, 1, 74)],
    [(0, 0.25, 76), (0.25, 0.25, 77), (0.5, 1, 77)],
    [(0, 0.5, 77), (0.5, 1.5, 76)],
    [(0, 0.5, 69), (0.5, 0.5, 69), (1, 0.5, 72)],
    [(0, 0.5, 71), (0.5, 1.5, 69)],
    [(0, 0.5, 77), (0.5, 1.5, 77)],
    [(0.5, 1, 75)],
    [(0, 0.25, 74), (0.25, 0.25, 72), (0.5, 1, 70)],
    [(0, 0.5, 69), (0.5, 1, 68)],
    [(0, 0.5, 68), (0.5, 1, 69)],
    [(0.5, 0.5, 71)],
    [(0.5, 0.166667, 57), (0.666667, 0.166667, 60), (0.833333, 0.166667, 64), (1, 0.166667, 69), (1.166667, 0.166667, 72), (1.333333, 0.166667, 76)],
    [(0, 0.166667, 74), (0.166667, 0.166667, 72), (0.333333, 0.166667, 71), (0.5, 0.166667, 69), (0.666667, 0.166667, 72), (0.833333, 0.166667, 76), (1, 0.166667, 81), (1.166667, 0.166667, 84), (1.333333, 0.166667, 88)],
    [(0, 0.166667, 86), (0.166667, 0.166667, 84), (0.333333, 0.166667, 83), (0.5, 0.166667, 81), (0.666667, 0.166667, 84), (0.833333, 0.166667, 88), (1, 0.166667, 93), (1.166667, 0.166667, 96), (1.333333, 0.166667, 100)],
    [(0, 0.166667, 98), (0.166667, 0.166667, 96), (0.333333, 0.166667, 95), (0.5, 0.166667, 94), (0.666667, 0.166667, 93), (0.833333, 0.166667, 92), (1, 0.166667, 91), (1.166667, 0.166667, 90), (1.333333, 0.166667, 89)],
    [(0, 0.166667, 88), (0.166667, 0.166667, 87), (0.333333, 0.166667, 86), (0.5, 0.166667, 85), (0.666667, 0.166667, 84), (0.833333, 0.166667, 83), (1, 0.166667, 82), (1.166667, 0.166667, 81), (1.333333, 0.166667, 80)],
    [(0, 0.166667, 79), (0.166667, 0.166667, 78), (0.333333, 0.166667, 77), (0.5, 0.25, 76), (0.75, 0.25, 75), (1, 0.25, 76), (1.25, 0.25, 71)],
]
VOICE_0_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 0), (6, 1), (7, 2), (8, 4), (9, 0), (10, 1), (11, 2), (12, 3), (13, 0), (14, 1), (15, 2), (16, 5), (17, 6), (18, 7), (19, 8), (20, 9), (21, 10), (22, 11), (23, 0), (24, 1), (25, 2), (26, 3), (27, 0), (28, 1), (29, 2), (30, 5), (31, 6), (32, 7), (33, 8), (34, 9), (35, 10), (36, 11), (37, 0), (38, 1), (39, 2), (40, 3), (41, 0), (42, 1), (43, 2), (44, 12), (45, 13), (46, 14), (47, 15), (48, 16), (49, 17), (50, 18), (51, 19), (52, 20), (53, 21), (54, 22), (55, 21), (56, 23), (57, 24), (58, 25), (59, 26), (60, 0), (61, 1), (62, 2), (63, 3), (64, 0), (65, 1), (66, 2), (67, 5), (68, 6), (69, 7), (70, 8), (71, 9), (72, 10), (73, 27), (74, 0), (75, 1), (76, 2), (77, 3), (78, 0), (79, 1), (80, 2), (81, 28), (82, 29), (83, 30), (84, 31), (85, 32), (86, 30), (87, 4), (88, 33), (89, 34), (90, 29), (91, 30), (92, 31), (93, 35), (94, 36), (95, 37), (96, 38), (97, 39), (98, 40), (99, 41), (100, 42), (101, 43), (102, 44), (103, 45), (104, 46), (105, 1), (106, 2), (107, 3), (108, 0), (109, 1), (110, 2), (111, 5), (112, 6), (113, 7), (114, 8), (115, 9), (116, 10), (117, 27), (118, 0), (119, 1), (120, 2), (121, 3), (122, 0), (123, 1), (124, 2), (125, 28)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# 33 distinct bars over 105 bars of music.
VOICE_1_CELLS = [
    [(0.5, 0.25, 45), (0.75, 0.25, 52), (1, 0.25, 57)],
    [(0.5, 0.25, 40), (0.75, 0.25, 52), (1, 0.25, 56)],
    [(0.5, 0.25, 48), (0.75, 0.25, 55), (1, 0.25, 60)],
    [(0.5, 0.25, 43), (0.75, 0.25, 55), (1, 0.25, 59)],
    [(0.5, 0.25, 40), (0.75, 0.25, 52), (1, 0.25, 64)],
    [(0.25, 0.25, 64), (0.5, 0.25, 76), (1.25, 0.25, 75)],
    [(0, 0.25, 76), (0.75, 0.25, 75), (1, 0.25, 76)],
    [(0.5, 0.25, 45), (0.75, 0.25, 52), (1, 0.25, 57), (1.25, 0.25, (58, 60))],
    [(0, 0.25, (57, 60)), (0.25, 0.25, (55, 58, 60)), (0.5, 0.25, 53), (0.75, 0.25, 57), (1, 0.25, 60), (1.25, 0.25, 57)],
    [(0, 0.25, 60), (0.25, 0.25, 57), (0.5, 0.25, 53), (0.75, 0.25, 58), (1, 0.25, 62), (1.25, 0.25, 58)],
    [(0, 0.25, 62), (0.25, 0.25, 58), (0.5, 0.25, 53), (0.75, 0.25, 64), (1, 0.25, (53, 55, 58)), (1.25, 0.25, 64)],
    [(0, 0.25, (53, 55, 58)), (0.25, 0.25, 64), (0.5, 0.25, 53), (0.75, 0.25, 57), (1, 0.25, 60), (1.25, 0.25, 57)],
    # Bar 49, with the appoggiatura moved off the lead - see voice 0.
    [(0, 0.0625, 70), (0, 0.25, 60), (0.25, 0.25, 57), (0.5, 0.25, 53), (0.75, 0.25, 57), (1, 0.25, 60), (1.25, 0.25, 57)],
    [(0, 0.25, 60), (0.25, 0.25, 57), (0.5, 0.25, 52), (0.75, 0.25, 57), (1, 0.25, 60), (1.25, 0.25, 57)],
    [(0, 0.25, (50, 62)), (0.25, 0.25, 53), (0.5, 0.25, 55), (0.75, 0.25, 64), (1, 0.25, 55), (1.25, 0.25, 64)],
    [(0, 0.25, 55), (0.25, 0.25, 65), (0.5, 0.5, (60, 64)), (1.25, 0.25, (65, 67))],
    [(0, 0.25, (64, 67)), (0.25, 0.25, (62, 65, 67)), (0.5, 0.5, (60, 64, 67)), (1, 0.5, (53, 57))],
    [(0, 0.5, (55, 59)), (0.5, 0.5, 60), (1.25, 0.25, (65, 67))],
    [(0, 0.5, (55, 59)), (0.5, 0.5, (56, 59))],
    [(0.5, 0.25, 45), (0.75, 0.25, 45), (1, 0.25, 45), (1.25, 0.25, 45)],
    [(0, 0.25, 45), (0.25, 0.25, 45), (0.5, 0.25, 45), (0.75, 0.25, 45), (1, 0.25, 45), (1.25, 0.25, 45)],
    [(0, 0.25, 45), (0.25, 0.25, 45), (0.5, 0.25, (38, 45)), (0.75, 0.25, (38, 45)), (1, 0.25, (38, 45)), (1.25, 0.25, (38, 45))],
    [(0, 0.25, (38, 45)), (0.25, 0.25, (38, 45)), (0.5, 0.25, (39, 45)), (0.75, 0.25, (39, 45)), (1, 0.25, (39, 45)), (1.25, 0.25, (39, 45))],
    [(0, 0.25, (39, 45)), (0.25, 0.25, (39, 45)), (0.5, 0.25, (40, 45)), (0.75, 0.25, (40, 45)), (1, 0.25, (40, 45)), (1.25, 0.25, (40, 45))],
    [(0, 0.25, (40, 44)), (0.25, 0.25, (40, 44)), (0.5, 0.25, (33, 45)), (0.75, 0.25, 45), (1, 0.25, 45), (1.25, 0.25, 45)],
    [(0, 0.25, 45), (0.25, 0.25, 45), (0.5, 0.25, 46), (0.75, 0.25, 46), (1, 0.25, 46), (1.25, 0.25, 46)],
    [(0, 0.25, 46), (0.25, 0.25, 46), (0.5, 0.25, 46), (0.75, 0.25, 46), (1, 0.25, 46), (1.25, 0.25, 46)],
    [(0, 0.25, 46), (0.25, 0.25, 46), (0.5, 0.25, 47), (0.75, 0.25, 47), (1, 0.25, 47), (1.25, 0.25, 47)],
    [(0, 0.25, 47), (0.25, 0.25, 47), (0.5, 1, 48)],
    [(0.5, 0.5, (52, 56))],
    [(0.5, 0.5, 45)],
    [(0, 0.5, (57, 60, 64)), (0.5, 0.5, (57, 60, 64))],
    [(0.5, 0.5, (33, 45))],
]
VOICE_1_PLAN = [(2, 0), (3, 1), (4, 0), (6, 0), (7, 1), (8, 0), (10, 0), (11, 1), (12, 0), (14, 0), (15, 1), (16, 0), (17, 2), (18, 3), (19, 0), (20, 4), (21, 5), (22, 6), (24, 0), (25, 1), (26, 0), (28, 0), (29, 1), (30, 0), (31, 2), (32, 3), (33, 0), (34, 4), (35, 5), (36, 6), (38, 0), (39, 1), (40, 0), (42, 0), (43, 1), (44, 7), (45, 8), (46, 9), (47, 10), (48, 11), (49, 12), (50, 13), (51, 14), (52, 15), (53, 16), (54, 17), (55, 16), (56, 18), (61, 0), (62, 1), (63, 0), (65, 0), (66, 1), (67, 0), (68, 2), (69, 3), (70, 0), (71, 4), (72, 5), (73, 6), (75, 0), (76, 1), (77, 0), (79, 0), (80, 1), (81, 19), (82, 20), (83, 20), (84, 20), (85, 20), (86, 21), (87, 22), (88, 23), (89, 24), (90, 20), (91, 20), (92, 20), (93, 25), (94, 26), (95, 26), (96, 27), (97, 28), (98, 29), (99, 30), (100, 31), (101, 31), (102, 31), (105, 0), (106, 1), (107, 0), (109, 0), (110, 1), (111, 0), (112, 2), (113, 3), (114, 0), (115, 4), (116, 5), (117, 6), (119, 0), (120, 1), (121, 0), (123, 0), (124, 1), (125, 32)]
VOICE_1_VOICE = (0, 72)   # program, velocity

VOICES = [
    ('Voice 0', VOICE_0_CELLS, VOICE_0_PLAN, VOICE_0_VOICE),
    ('Voice 1', VOICE_1_CELLS, VOICE_1_PLAN, VOICE_1_VOICE),
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
    the piece stopped asking at bar 82."""
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
    out = argv[1] if len(argv) > 1 else os.path.join(OUT_DIR,
                                                     'elise_arr.mid')
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
