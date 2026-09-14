"""Tico-Tico no Fuba.

Arranged from a four-part Tico-Tico no Fuba engraving.

    python arr_ticotico.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
TIME_SIG = (2, 2)
BAR = 4          # beats per bar

# (beat, bpm). The whole map, not just the opening: the
# ritardandi and the pushes are the arrangement, not the
# playback.
#
# IN BPM, WHICH IS THE NUMBER A MUSICIAN SETS AND READS.
# The file stores its reciprocal, microseconds to the
# quarter, and build() converts on the way out. Fractions
# are allowed because a ritardando steps in fractions of a
# beat per minute and whole bpm would flatten it.
TEMPO = [
    (0, 190),
]
BPM = TEMPO[0][1]

# Silence at each end, in beats: nothing begins on a note
# or ends on one. About 2 s before the first note and 4 s
# after the last, whole beats at the tempo in force there.
# This is the fastest piece here, so the same seconds take
# more beats than elsewhere - which is why the rest is
# measured in seconds and not in bars.
LEAD_IN = 6
TAIL = 13

# The note lengths below are AS WRITTEN. build() takes
# the articulation off them on the way out - five per
# cent of a beat, a fifth at most - the same way every
# other arrangement here does.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.2
TITLE = 'Tico-Tico no Fuba'

# ---- voice 0 ----
# 25 distinct bars over 68 bars of music.
VOICE_0_CELLS = [
    [(0, 0.5, 67), (0.5, 0.5, 66), (1, 0.5, 67), (1.5, 0.5, 69), (2, 0.5, 72), (2.5, 0.5, 70), (3, 0.5, 69), (3.5, 0.5, 70)],
    [(0, 0.5, 74), (0.5, 0.5, 65), (1, 0.5, 70), (1.5, 0.5, 74), (2, 0.5, 77), (2.5, 0.5, 76), (3, 0.5, 75), (3.5, 0.5, 74)],
    [(0, 0.5, 72), (0.5, 0.5, 70), (1, 0.5, 69), (1.5, 0.5, 67), (2, 0.5, 65), (2.5, 0.5, 63), (3, 0.5, 62), (3.5, 0.5, 60)],
    [(0, 1, 58), (2, 0.5, 70), (2.5, 0.5, 62), (3, 0.5, 61), (3.5, 0.5, 62)],
    [(0, 0.5, 63), (0.5, 1, 62), (1.5, 1, 67), (2.5, 0.5, 62), (3, 0.5, 61), (3.5, 0.5, 62)],
    [(0, 0.5, 63), (0.5, 1, 62), (1.5, 1, 66), (2.5, 0.5, 62), (3, 0.5, 61), (3.5, 0.5, 62)],
    [(0, 0.5, 63), (0.5, 0.5, 62), (1, 0.5, 72), (1.5, 0.5, 69), (2, 0.5, 66), (2.5, 0.5, 62), (3, 0.5, 60), (3.5, 0.5, 59)],
    [(0, 2, 58), (2.5, 0.5, 67), (3, 0.5, 66), (3.5, 0.5, 65)],
    [(0, 0.5, 63), (0.5, 1, 67), (1.5, 1, 72), (2.5, 0.5, 70), (3, 0.5, 67), (3.5, 0.5, 63)],
    [(0, 0.5, 62), (0.5, 1, 67), (1.5, 1, 70), (2.5, 0.5, 70), (3, 0.5, 69), (3.5, 0.5, 68)],
    [(0, 0.5, 69), (0.5, 0.5, 57), (1, 0.5, 61), (1.5, 0.5, 64), (2, 0.5, 67), (2.5, 0.5, 70), (3, 0.5, 69), (3.5, 0.5, 67)],
    [(0, 2, 66), (2.5, 0.5, 62), (3, 0.5, 61), (3.5, 0.5, 62)],
    [(0, 0.5, 69), (0.5, 0.5, 62), (1, 0.5, 66), (1.5, 0.5, 69), (2, 0.5, 74), (2.5, 0.5, 72), (3, 0.5, 70), (3.5, 0.5, 69)],
    [(0, 2, 67), (2.5, 0.5, 69), (3, 0.5, 67), (3.5, 0.5, 66)],
    [(0, 0.5, 65), (0.5, 0.5, 58), (1, 0.5, 62), (1.5, 0.5, 65), (2, 0.5, 58), (2.5, 0.5, 62), (3, 0.5, 65), (3.5, 0.5, 66)],
    [(0, 1, 67), (1, 1, 63), (2.5, 0.5, 69), (3, 0.5, 67), (3.5, 0.5, 66)],
    [(0, 0.5, 65), (0.5, 0.5, 57), (1, 0.5, 60), (1.5, 0.5, 63), (2, 0.5, 57), (2.5, 0.5, 60), (3, 0.5, 63), (3.5, 0.5, 65)],
    [(0, 1, 67), (1, 1, 62), (2.5, 0.5, 70), (3, 0.5, 70), (3.5, 0.5, 70)],
    [(0, 0.5, 70), (0.5, 0.5, 69), (1, 0.5, 69), (1.5, 1, 69), (2.5, 0.5, 67), (3, 0.5, 67), (3.5, 0.5, 67)],
    [(0, 0.5, 67), (0.5, 0.5, 63), (1, 0.5, 63), (1.5, 1, 63), (2.5, 0.5, 69), (3, 0.5, 69), (3.5, 0.5, 69)],
    [(0, 0.5, 69), (0.5, 0.5, 65), (1, 0.5, 65), (1.5, 0.5, 69), (2, 0.5, 67), (2.5, 0.5, 63), (3, 0.5, 63), (3.5, 0.5, 67)],
    [(0, 2, 65), (2.5, 0.5, 69), (3, 0.5, 67), (3.5, 0.5, 66)],
    [(0, 1, 67), (1, 1, 62), (2.5, 0.5, 70), (3, 0.5, 69), (3.5, 0.5, 68)],
    [(0, 1, 58), (2.5, 0.5, 62), (3, 0.5, 61), (3.5, 0.5, 62)],
    [(0, 1, 58), (2, 1, 70)],
]
VOICE_0_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 4), (14, 5), (15, 6), (16, 7), (17, 8), (18, 9), (19, 12), (20, 13), (21, 14), (22, 15), (23, 16), (24, 17), (25, 18), (26, 19), (27, 20), (28, 21), (29, 14), (30, 15), (31, 16), (32, 22), (33, 0), (34, 1), (35, 2), (36, 23), (37, 4), (38, 5), (39, 6), (40, 7), (41, 8), (42, 9), (43, 10), (44, 11), (45, 4), (46, 5), (47, 6), (48, 7), (49, 8), (50, 9), (51, 12), (52, 13), (53, 14), (54, 15), (55, 16), (56, 17), (57, 18), (58, 19), (59, 20), (60, 21), (61, 14), (62, 15), (63, 16), (64, 22), (65, 0), (66, 1), (67, 2), (68, 24)]
VOICE_0_VOICE = (0, 100)   # program, velocity

# ---- voice 1 ----
# 26 distinct bars over 68 bars of music.
VOICE_1_CELLS = [
    [(0, 1.5, 51), (1.5, 0.5, 48), (2, 1, 51), (3, 1, 52)],
    [(0, 1.5, 53), (1.5, 0.5, 46), (2, 1, 50), (3, 1, 53)],
    [(0, 1.5, 51), (1.5, 0.5, 48), (2, 1, 45), (3, 1, 51)],
    [(0, 1, 50), (1, 1, 53), (2, 1, 46)],
    [(0, 1, 55), (2, 1, 55), (3, 1, 55)],
    [(0, 1, 54), (2, 1, 54), (2.5, 0.5, 62), (3, 0.5, 61), (3, 1, 54), (3.5, 0.5, 62)],
    [(0, 0.5, 63), (0, 1, 50), (0.5, 0.5, 62), (1, 0.5, 72), (1.5, 0.5, 69), (2, 0.5, 66), (2, 1, 50), (2.5, 0.5, 62), (3, 0.5, 60), (3, 1, 50), (3.5, 0.5, 59)],
    [(0, 0.5, 50), (0, 2, 58), (0.5, 1, 50), (1.5, 0.5, 50), (2, 1, 55)],
    [(0, 1, 55), (2, 1, 51), (3, 1, 51)],
    [(0, 1, 55), (2, 1, 50), (2.5, 0.5, 70), (3, 0.5, 69), (3, 1, 50), (3.5, 0.5, 68)],
    [(0, 0.5, 69), (0, 1, 55), (0.5, 0.5, 57), (1, 0.5, 61), (1.5, 0.5, 64), (2, 0.5, 67), (2, 1, 52), (2.5, 0.5, 70), (3, 0.5, 69), (3, 1, 52), (3.5, 0.5, 67)],
    [(0, 0.5, 50), (0, 2, 66), (0.5, 1, 50), (1.5, 0.5, 50), (2, 1, 50)],
    [(0, 1, 50), (2, 1, 50), (2.5, 0.5, 70), (3, 0.5, 69), (3, 1, 50), (3.5, 0.5, 68)],
    [(0, 0.5, 69), (0, 1, 50), (0.5, 0.5, 62), (1, 0.5, 66), (1.5, 0.5, 69), (2, 0.5, 74), (2, 1, 62), (2.5, 0.5, 72), (3, 0.5, 70), (3, 1, 60), (3.5, 0.5, 69)],
    [(0, 0.5, 58), (0, 2, 67), (0.5, 1, 55), (1.5, 0.5, 55), (2, 1, 55), (2.5, 0.5, 69), (3, 0.5, 67), (3.5, 0.5, 66)],
    [(0, 0.5, 65), (0, 1, 46), (0.5, 0.5, 58), (1, 0.5, 62), (1.5, 0.5, 65), (2, 0.5, 58), (2.5, 0.5, 62), (3, 0.5, 65), (3.5, 0.5, 66)],
    [(0, 1, (60, 63)), (1, 1, 60), (2, 1, 53), (2.5, 0.5, 69), (3, 0.5, 67), (3, 1, 57), (3.5, 0.5, 66)],
    [(0, 0.5, 65), (0, 1, 53), (0.5, 0.5, 57), (1, 0.5, 60), (1.5, 0.5, 63), (2, 0.5, 57), (2.5, 0.5, 60), (3, 0.5, 63), (3.5, 0.5, 65)],
    [(0, 1, (58, 62)), (1, 1, 58), (2, 1, 53), (2.5, 0.5, 67), (3, 0.5, 67), (3, 1, 50), (3.5, 0.5, 67)],
    [(0, 0.5, 67), (0, 1, 58), (0.5, 0.5, 65), (1, 0.5, 65), (1.5, 1, 65), (2, 1, 55), (2.5, 0.5, 63), (3, 0.5, 63), (3, 1, 59), (3.5, 0.5, 63)],
    [(0, 0.5, 63), (0, 0.5, 60), (0.5, 0.5, 60), (1, 0.5, 58), (1.5, 1, 57), (2, 1, 53), (2.5, 0.5, 65), (3, 0.5, 65), (3, 1, 53), (3.5, 0.5, 64)],
    [(0, 0.5, 63), (0, 1, 53), (0.5, 0.5, 57), (1, 0.5, 57), (1.5, 0.5, 65), (2, 0.5, 63), (2, 1, 53), (2.5, 0.5, 57), (3, 0.5, 57), (3.5, 0.5, 58)],
    [(0, 0.5, 50), (0, 2, 58), (0.5, 1, 50), (1.5, 0.5, 50), (2, 1, 50), (2.5, 0.5, 69), (3, 0.5, 67), (3.5, 0.5, 66)],
    [(0, 1, (58, 62)), (1, 1, 58)],
    [(0, 1.5, 51), (1.5, 0.5, 48), (2, 1, 45), (3, 1, 53)],
    # (58, 58) was A#3 written twice. Reduced to the single note it
    # already sounded; the bar is the closing unison and the other
    # voices cover A#1, A#2 and A#4.
    [(0, 1, 58), (2, 1, (46, 70))],
]
VOICE_1_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 4), (14, 5), (15, 6), (16, 7), (17, 8), (18, 12), (19, 13), (20, 14), (21, 15), (22, 16), (23, 17), (24, 18), (25, 19), (26, 20), (27, 21), (28, 22), (29, 15), (30, 16), (31, 17), (32, 23), (33, 0), (34, 1), (35, 24), (36, 3), (37, 4), (38, 5), (39, 6), (40, 7), (41, 8), (42, 9), (43, 10), (44, 11), (45, 4), (46, 5), (47, 6), (48, 7), (49, 8), (50, 12), (51, 13), (52, 14), (53, 15), (54, 16), (55, 17), (56, 18), (57, 19), (58, 20), (59, 21), (60, 22), (61, 15), (62, 16), (63, 17), (64, 23), (65, 0), (66, 1), (67, 24), (68, 25)]
VOICE_1_VOICE = (0, 78)   # program, velocity

# ---- voice 2 ----
# 23 distinct bars over 68 bars of music.
VOICE_2_CELLS = [
    [(0, 1.5, 39)],
    [(0, 1.5, 41)],
    [(0, 1, 46), (1, 1, 41), (2, 1, 34)],
    [(0, 1, 43), (2, 1, 46), (3, 1, 46)],
    [(0, 1, 45), (2, 1, 45), (3, 1, 45)],
    [(0, 1, 42), (2, 1, 38), (3, 1, 42)],
    [(0, 0.5, 43), (0.5, 1, 43), (1.5, 0.5, 43), (2, 1, 43)],
    [(0, 1, 36), (2, 1, 43), (3, 1, 37)],
    [(0, 1, 38), (2, 1, 43), (3, 1, 41)],
    [(0, 1, 40), (2, 1, 37), (3, 1, 45)],
    [(0, 0.5, 38), (0.5, 1, 45), (1.5, 0.5, 45), (2, 1, 38)],
    [(0, 1, 38), (2, 1, 43), (3, 1, 38)],
    [(0, 1, 42), (2, 1, 45), (3, 1, 42)],
    [(0, 0.5, 43), (0.5, 1, 50), (1.5, 0.5, 50), (2, 1, 43)],
    [(0, 1, 46)],
    [(0, 1, 48), (2, 1, 41), (3, 1, 45)],
    [(0, 1, 41)],
    [(0, 1, 46), (2, 1, 41), (3, 1, 38)],
    [(0, 1, 46), (2, 1, 50), (3, 1, 47)],
    [(0, 1, 48), (2, 1, 41), (3, 1, 48)],
    [(0, 1, 41), (2, 1, 45)],
    [(0, 0.5, 46), (0.5, 1, 46), (1.5, 0.5, 46), (2, 1, 46)],
    [(0, 1, 46), (2, 1, 34)],
]
VOICE_2_PLAN = [(1, 0), (2, 1), (3, 0), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8), (11, 9), (12, 10), (13, 3), (14, 4), (15, 5), (16, 6), (17, 7), (18, 11), (19, 12), (20, 13), (21, 14), (22, 15), (23, 16), (24, 17), (25, 18), (26, 19), (27, 20), (28, 21), (29, 14), (30, 15), (31, 16), (32, 14), (33, 0), (34, 1), (35, 0), (36, 2), (37, 3), (38, 4), (39, 5), (40, 6), (41, 7), (42, 8), (43, 9), (44, 10), (45, 3), (46, 4), (47, 5), (48, 6), (49, 7), (50, 11), (51, 12), (52, 13), (53, 14), (54, 15), (55, 16), (56, 17), (57, 18), (58, 19), (59, 20), (60, 21), (61, 14), (62, 15), (63, 16), (64, 14), (65, 0), (66, 1), (67, 0), (68, 22)]
VOICE_2_VOICE = (0, 88)   # program, velocity

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


def track(events, end_tick):
    body = bytearray()
    prev = 0
    for tick, data in sorted(events, key=lambda e: e[0]):
        body += vlq(tick - prev) + data
        prev = tick
    body += vlq(max(0, end_tick - prev))
    body += bytes([0xFF, 0x2F, 0x00])
    return b"MTrk" + struct.pack(">I", len(body)) + bytes(body)


def seconds(end_beat):
    """The real length, tempo map and all."""
    total = 0.0
    for i, (beat, bpm) in enumerate(TEMPO):
        nxt = TEMPO[i + 1][0] if i + 1 < len(TEMPO) else end_beat
        total += max(0.0, min(nxt, end_beat) - beat) * 60.0 / bpm
    return total


def trim_of(d):
    return d * min(TRIM_CAP,
                   TRIM_PER_BEAT * max(1, int(d + 1e-9)))


def build():
    pw = 0
    while (1 << pw) < TIME_SIG[1]:
        pw += 1
    laid = []
    for ch, (name, cells, plan, voice) in enumerate(VOICES):
        laid.append((ch, unroll(cells, plan), voice))
    first = min(o for _, n, _ in laid for o, _, _ in n)
    shift = max(0.0, LEAD_IN - first)
    laid = [(ch, [(o + shift, d, p) for o, d, p in n], v)
            for ch, n, v in laid]
    end = max(o + d for _, n, _ in laid for o, d, _ in n)
    end_tick = int(round((end + TAIL) * DIV))
    laid = [(ch, [(o, d - trim_of(d), p) for o, d, p in n], v)
            for ch, n, v in laid]
    meta = []
    for beat, bpm in TEMPO:
        us = int(round(60000000.0 / bpm))
        meta.append(
            (0 if beat <= 0 else int(round((beat + shift) * DIV)),
             bytes([0xFF, 0x51, 0x03, (us >> 16) & 0xFF,
                    (us >> 8) & 0xFF, us & 0xFF])))
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
    # Into output/, and the directory is made if it is not
    # there.
    out = argv[1] if len(argv) > 1 else os.path.join(
        OUT_DIR, 'ticotico_arr.mid')
    here = os.path.dirname(out)
    if here and not os.path.isdir(here):
        os.makedirs(here)
    open(out, "wb").write(build())
    print("%s -> %s" % (TITLE, out))
    for name, cells, plan, _ in VOICES:
        print("  %-14s %3d bars, %3d distinct, %4d attacks"
              % (name, len(plan), len(cells),
                 len(unroll(cells, plan))))
    # MEASURED THE WAY build() LAYS IT OUT, so the number
    # printed is the number the player takes: the length
    # runs to the end-of-track mark and so includes TAIL,
    # the tempo events sit at `beat + shift` as build()
    # writes them, and the speed is the mean over the map
    # weighted by how long each step is in force.
    laid = [unroll(c, p) for _, c, p, _ in VOICES]
    first = min(o for n in laid for o, _, _ in n)
    shift = max(0.0, LEAD_IN - first)
    total = max(o + d for n in laid
                for o, d, _ in n) + shift + TAIL
    steps = [(0.0 if b <= 0 else b + shift, v)
             for b, v in TEMPO]
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
