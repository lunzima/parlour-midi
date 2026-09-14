"""Gadameiren.

Arranged from a transcription of the rock-band Gadameiren.

    python arr_gadameiren.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
TIME_SIG = (4, 4)
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
    (0, 78),
    (16, 82),
    (56, 83),
    (136, 84),
    (176, 80),
    (200, 78),
]
BPM = TEMPO[0][1]

# Silence at each end, in beats: nothing begins on a note
# or ends on one. About 2 s before the first note and 4 s
# after the last, whole beats at the tempo in force there -
# at 78 bpm the tail is 3.8 s. The head is longer than the
# 2 s target because the music's own first attack is at
# beat 4 and LEAD_IN cannot pull it earlier.
LEAD_IN = 2
TAIL = 5

# The note lengths below are AS WRITTEN. build() takes
# the articulation off them on the way out - five per
# cent of a beat, a fifth at most - the same way every
# other arrangement here does.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.2
TITLE = 'Gadameiren'

# ---- voice 0 ----
# 21 distinct bars over 49 bars of music.
VOICE_0_CELLS = [
    [(0, 1, 64), (1, 0.5, 64), (1.5, 0.5, 62), (2, 1.25, 64), (3.25, 0.25, 67), (3.5, 0.25, 69), (3.75, 0.25, 67)],
    [(0, 1, 64), (1, 1, 71), (2, 1, 71), (3, 0.5, 69), (3.5, 0.5, 71)],
    [(0, 1, 74), (1, 1, 76), (2, 1, 67), (3, 1, 64)],
    [(0, 1, 69), (1, 0.5, 71), (1.5, 0.5, 69), (2, 1, 67), (3, 1, 64)],
    [(0, 1.5, 69), (1.5, 0.5, 71), (2, 1, 74), (3, 0.5, 79), (3.5, 0.25, 81), (3.75, 0.25, 79)],
    [(0, 2.5, 76)],
    [(0, 1, 74), (1, 1, 76), (2, 1, 74), (3, 0.5, 71), (3.5, 0.5, 74)],
    [(0, 1, 67), (1, 0.5, 64), (1.5, 0.5, 67), (2, 1, 62), (3, 1, 64)],
    [(0, 1.5, 69), (1.5, 0.25, 71), (1.75, 0.25, 71), (2, 1, 74), (3, 1, 67)],
    [(0, 2.5, 64)],
    [(0, 1.5, 69), (1.5, 0.5, 71), (2, 1, 74), (3, 1, 79)],
    [(0, 1, 67), (1, 0.5, 64), (1.5, 0.5, 67), (2, 1, 62), (3, 1, 67)],
    [(0, 1, 74), (1, 1, 76), (2, 1, 67), (3, 0.75, 64), (3.75, 0.25, 64)],
    [(0, 1.5, 69), (1.5, 0.5, 71), (2, 1, 74), (3, 0.5, 67), (3.5, 0.25, 67), (3.75, 0.25, 69)],
    [(0, 0.5, 64), (0.5, 7, 71)],
    [(3.5, 0.25, 69), (3.75, 0.25, 71)],
    [(0, 8, 69)],
    [(0, 0.25, 69), (0.25, 0.25, 71), (0.5, 0.25, 74), (0.75, 0.25, 69), (1, 0.25, 71), (1.25, 0.25, 74), (1.5, 0.25, 69), (1.75, 0.25, 71), (2, 0.25, 74), (2.25, 0.25, 69), (2.5, 0.25, 71), (2.75, 0.25, 74), (3, 0.25, 69), (3.25, 0.25, 71), (3.5, 0.25, 74), (3.75, 0.25, 69)],
    [(0, 0.25, 71), (0.25, 0.25, 74), (0.5, 0.25, 76), (0.75, 0.25, 79), (1, 0.25, 81), (1.25, 0.25, 83), (1.5, 0.25, 81), (1.75, 0.25, 79), (2, 0.25, 76), (2.25, 0.25, 74), (2.5, 0.25, 76), (2.75, 0.25, 74), (3, 0.25, 71), (3.25, 0.25, 69), (3.5, 0.25, 67), (3.75, 0.25, 64)],
    [(0, 4, 67)],
    [(0, 2, 67)],
]
VOICE_0_PLAN = [(2, 0), (3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (9, 6), (10, 2), (11, 7), (12, 8), (13, 9), (14, 1), (15, 2), (16, 3), (17, 10), (18, 5), (19, 6), (20, 2), (21, 7), (22, 8), (23, 9), (24, 1), (25, 2), (26, 3), (27, 10), (28, 5), (29, 6), (30, 2), (31, 11), (32, 8), (33, 9), (34, 1), (35, 12), (36, 3), (37, 10), (38, 5), (39, 6), (40, 2), (41, 7), (42, 13), (43, 9), (44, 14), (45, 15), (46, 16), (48, 17), (49, 18), (50, 19), (51, 20)]
VOICE_0_VOICE = (0, 100)   # program, velocity

# ---- voice 1 ----
# 24 distinct bars over 51 bars of music.
VOICE_1_CELLS = [
    [(0.5, 3.5, 78)],
    [(0, 0.5, 52), (0.5, 0.5, 52), (1, 0.5, 52), (1.5, 0.5, 52), (2, 0.5, 55), (2.5, 0.5, 55), (3, 0.5, 55), (3.5, 0.5, 55)],
    [(0, 0.5, 55), (0.5, 0.5, 55), (1, 0.5, 55), (1.5, 0.5, 55), (2, 0.5, 55), (2.5, 0.5, 55), (3, 0.5, 55), (3.5, 0.5, 55)],
    [(0, 2, 67), (2, 2, 64)],
    [(0, 2, 66), (2, 2, 60)],
    [(0, 2, 64), (2, 2, 60)],
    [(0, 2, 67), (2, 0.5, 71), (2, 2, 67), (2.5, 0.25, 71), (2.75, 0.25, 74), (3, 0.5, 76), (3.5, 0.5, 74)],
    [(0, 2, 67), (2, 2, 67)],
    [(0, 2, 66), (2, 2, 59)],
    [(0, 2, 60), (2, 2, 55)],
    [(0, 2, 59), (2, 0.5, 67), (2, 2, 59), (2.5, 0.25, 67), (2.75, 0.25, 69), (3, 0.5, 71), (3.5, 0.5, 69)],
    [(0, 0.5, 67), (0.5, 0.5, 67), (1, 0.5, 67), (1.5, 0.5, 67), (2, 0.5, 64), (2.5, 0.5, 64), (3, 0.5, 64), (3.5, 0.5, 64)],
    [(0, 0.5, 62), (0.5, 0.5, 62), (1, 0.5, 62), (1.5, 0.5, 62), (2, 0.5, 60), (2.5, 0.5, 60), (3, 0.5, 60), (3.5, 0.5, 60)],
    [(0, 0.5, 64), (0.5, 0.5, 64), (1, 0.5, 64), (1.5, 0.5, 64), (2, 0.5, 60), (2.5, 0.5, 60), (3, 0.5, 60), (3.5, 0.5, 60)],
    [(0, 0.5, 64), (0.5, 0.5, 64), (1, 0.5, 64), (1.5, 0.5, 64), (2, 0.5, 64), (2.5, 0.5, 64), (3, 0.5, 64), (3.5, 0.5, 64)],
    [(0, 0.5, 64), (0.5, 0.5, 64), (1, 0.5, 64), (1.5, 0.5, 64), (2, 0.5, (64, 71)), (2.5, 0.25, 71), (2.5, 0.5, 64), (2.75, 0.25, 74), (3, 0.5, (64, 76)), (3.5, 0.5, (64, 74))],
    [(0, 0.5, 62), (0.5, 0.5, 62), (1, 0.5, 62), (1.5, 0.5, 62), (2, 0.5, 62), (2.5, 0.5, 62), (3, 0.5, 62), (3.5, 0.5, 62)],
    [(0, 0.5, 62), (0.5, 0.5, 62), (1, 0.5, 62), (1.5, 0.5, 62), (2, 0.5, 59), (2.5, 0.5, 59), (3, 0.5, 59), (3.5, 0.5, 59)],
    [(0, 0.5, 60), (0.5, 0.5, 60), (1, 0.5, 60), (1.5, 0.5, 60), (2, 0.5, 59), (2.5, 0.5, 59), (3, 0.5, 59), (3.5, 0.5, 59)],
    [(0, 0.5, 59), (0.5, 0.5, 59), (1, 0.5, 59), (1.5, 0.5, 59), (2, 0.5, (59, 67)), (2.5, 0.25, 67), (2.5, 0.5, 59), (2.75, 0.25, 69), (3, 0.5, (59, 71)), (3.5, 0.5, (59, 69))],
    [(0, 0.5, 67), (0.5, 0.5, 67), (1, 0.5, 67), (1.5, 0.5, 67), (2, 0.5, 67), (2.5, 0.5, 67), (3, 0.5, 67), (3.5, 0.5, 67)],
    [(0, 0.5, 67), (0.5, 0.5, 67), (1, 0.5, 67), (1.5, 0.5, 67), (2, 0.5, 62), (2.5, 0.5, 62), (3, 0.5, 62), (3.5, 0.5, 62)],
    [(0, 0.5, 60), (0.5, 0.5, 60), (1, 0.5, 60), (1.5, 0.5, 60), (2, 0.5, 60), (2.5, 0.5, 60), (3, 0.5, 60), (3.5, 0.5, 60)],
    [(0, 4, 71)],
]
VOICE_1_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 5), (8, 6), (9, 7), (10, 8), (11, 9), (12, 5), (13, 10), (14, 11), (15, 12), (16, 13), (17, 14), (18, 15), (19, 16), (20, 17), (21, 18), (22, 14), (23, 19), (24, 11), (25, 12), (26, 13), (27, 14), (28, 15), (29, 16), (30, 17), (31, 18), (32, 14), (33, 19), (34, 11), (35, 12), (36, 13), (37, 14), (38, 15), (39, 16), (40, 17), (41, 18), (42, 14), (43, 19), (44, 20), (45, 21), (46, 22), (47, 22), (48, 14), (49, 14), (50, 16), (51, 23)]
VOICE_1_VOICE = (0, 74)   # program, velocity

# ---- voice 2 ----
# 22 distinct bars over 51 bars of music.
VOICE_2_CELLS = [
    [(0, 4, 52), (0.125, 3.875, 53), (0.25, 3.75, 57), (0.375, 3.625, 59)],
    [(0, 1, 40), (1, 1, 47), (2, 1, 52), (3, 1, 47)],
    [(0, 2, (40, 52, 55)), (2, 2, (52, 55))],
    [(0, 2, (38, 50, 54)), (2, 2, (36, 48, 52))],
    [(0, 2, (45, 48, 57)), (2, 2, (48, 57))],
    [(0, 2, (43, 55, 59)), (2, 2, (55, 59))],
    [(0, 2, (47, 50, 59)), (2, 2, (40, 52, 55))],
    [(0, 2, (36, 48, 52)), (2, 2, (35, 47, 50))],
    [(0, 0.5, 40), (0.5, 0.5, 47), (1, 0.5, (52, 55)), (1.5, 1, 47), (2.5, 0.5, 47), (3, 0.5, (52, 55)), (3.5, 0.5, 47)],
    [(0, 0.5, 38), (0.5, 0.5, 45), (1, 0.5, (50, 54)), (1.5, 0.5, 45), (2, 0.5, 36), (2.5, 0.5, 43), (3, 0.5, (48, 52)), (3.5, 0.5, 43)],
    [(0, 0.5, 45), (0.5, 0.5, 52), (1, 0.5, (48, 57)), (1.5, 1, 52), (2.5, 0.5, 52), (3, 0.5, (48, 57)), (3.5, 0.5, 52)],
    [(0, 0.5, 43), (0.5, 0.5, 50), (1, 0.5, (55, 59)), (1.5, 1, 50), (2.5, 0.5, 50), (3, 0.5, (55, 59)), (3.5, 0.5, 50)],
    [(0, 0.5, 47), (0.5, 0.5, 54), (1, 0.5, (50, 59)), (1.5, 0.5, 54), (2, 0.5, 40), (2.5, 0.5, 47), (3, 0.5, (52, 55)), (3.5, 0.5, 47)],
    [(0, 0.5, 36), (0.5, 0.5, 43), (1, 0.5, (48, 52)), (1.5, 0.5, 43), (2, 0.5, 35), (2.5, 0.5, 43), (3, 0.5, (47, 50)), (3.5, 0.5, 43)],
    [(0, 0.5, (28, 40)), (0.5, 0.5, 47), (1, 0.5, (52, 55)), (1.5, 1, 47), (2.5, 0.5, 47), (3, 0.5, (52, 55)), (3.5, 0.5, 47)],
    [(0, 0.5, (26, 38)), (0.5, 0.5, 45), (1, 0.5, (50, 54)), (1.5, 0.5, 45), (2, 0.5, (24, 36)), (2.5, 0.5, 43), (3, 0.5, (48, 52)), (3.5, 0.5, 43)],
    [(0, 0.5, (33, 45)), (0.5, 0.5, 52), (1, 0.5, (48, 57)), (1.5, 1, 52), (2.5, 0.5, 52), (3, 0.5, (48, 57)), (3.5, 0.5, 52)],
    [(0, 0.5, (31, 43)), (0.5, 0.5, 50), (1, 0.5, (55, 59)), (1.5, 1, 50), (2.5, 0.5, 50), (3, 0.5, (55, 59)), (3.5, 0.5, 50)],
    [(0, 0.5, (35, 47)), (0.5, 0.5, 54), (1, 0.5, (50, 59)), (1.5, 0.5, 54), (2, 0.5, (28, 40)), (2.5, 0.5, 47), (3, 0.5, (52, 55)), (3.5, 0.5, 47)],
    [(0, 0.5, (24, 36)), (0.5, 0.5, 43), (1, 0.5, (48, 52)), (1.5, 0.5, 43), (2, 0.5, (23, 35)), (2.5, 0.5, 43), (3, 0.5, (47, 50)), (3.5, 0.5, 43)],
    [(0, 0.5, (29, 41)), (0.5, 0.5, 48), (1, 0.5, (53, 57)), (1.5, 1, 48), (2.5, 0.5, 48), (3, 0.5, (53, 57)), (3.5, 0.5, 48)],
    [(0, 4, (31, 43, 50, 55))],
]
VOICE_2_PLAN = [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (6, 4), (7, 4), (8, 2), (9, 5), (10, 6), (11, 7), (12, 4), (13, 2), (14, 8), (15, 9), (16, 10), (17, 10), (18, 8), (19, 11), (20, 12), (21, 13), (22, 10), (23, 8), (24, 8), (25, 9), (26, 10), (27, 10), (28, 8), (29, 11), (30, 12), (31, 13), (32, 10), (33, 8), (34, 14), (35, 15), (36, 16), (37, 16), (38, 14), (39, 17), (40, 18), (41, 19), (42, 16), (43, 14), (44, 17), (45, 17), (46, 20), (47, 20), (48, 14), (49, 14), (50, 17), (51, 21)]
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
        OUT_DIR, 'gadameiren_arr.mid')
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
