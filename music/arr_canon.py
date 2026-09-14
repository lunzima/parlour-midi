"""Canon in D (Pachelbel).

The music is Pachelbel's; the arrangement is this project's own.

    python arr_canon.py [out.mid]
"""
import os
import struct
import sys

# Beside THIS FILE, not beside the shell. A bare 'output' is relative to
# the cwd, so running this from the repository root would quietly write
# the piece one directory up from where every other copy of it lives -
# and a file in the wrong place still opens, so nothing would say so.
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
# The tempo map: (beat, beats per minute). Written as the round number
# a player would be given rather than as the microsecond value read back
# out of the finished file - that file says 960004, which is 62.4997
# bpm, which is nobody's tempo marking.
#
# This piece is the only one of the five that never changes tempo: it
# runs the whole way at one speed and does not even slow to finish.
TEMPO = [
    (0.0, 63),
]
BPM = TEMPO[0][1]
TIME_SIG = (4, 4)
BAR = 4          # beats per bar
# Silence at each end, in beats: nothing begins on a note or ends on
# one. Every piece here gets about 2 s before the first note and 4 s
# after the last, rounded to whole beats at the tempo in force there -
# at 63 bpm that is 1.9 s and 3.8 s.
LEAD_IN = 2
TAIL = 4
# Every note gives up a little of its tail, so the next stroke of the
# same pitch starts against silence instead of picking up exactly where
# the last one stopped. Stepped by whole beats, five per cent as the
# floor: 5 under a beat and at one beat, 10 at two, 15 at three, 20 at
# four and no further. Thirty-two joins in this piece met dead on.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))


TITLE = 'Canon in D (Pachelbel)'

# ---- voice 0 ----
# 28 distinct bars over 33 bars of music.
VOICE_0_CELLS = [
    [(2, 2, 78)],
    [(0, 2, 76), (2, 2, 74)],
    [(0, 2, 73), (2, 2, 71)],
    [(0, 2, 69), (2, 2, 71)],
    [(0, 2, 73), (2, 2, 78)],
    [(0, 2, 73), (2, 1, 74), (3, 1, 78)],
    [(0, 1, 81), (1, 1, 83), (2, 1, 79), (3, 1, 74)],
    [(0, 1, 78), (1, 1, 66), (2, 1, 67), (3, 1, 74)],
    [(0, 1, 74), (1, 0.5, 74), (1.5, 0.5, 73), (2, 0.5, 74), (2.5, 0.5, 73), (3, 0.5, 74), (3.5, 0.5, 67)],
    [(0, 1, 69), (1, 1, 73), (2, 1, 74), (3, 1, 78)],
    [(0, 0.5, 81), (0.5, 0.5, 78), (1, 0.5, 81), (1.5, 0.5, 83), (2, 0.5, 79), (2.5, 0.5, 78), (3, 0.5, 76), (3.5, 0.5, 79)],
    [(0, 0.5, 78), (0.5, 0.5, 76), (1, 0.5, 74), (1.5, 0.5, 73), (2, 0.5, 71), (2.5, 0.5, 67), (3, 1, 74)],
    [(0, 1.5, 74), (1.5, 0.5, 73), (2, 0.75, 78), (3, 0.5, 78), (3.5, 0.25, 74), (3.75, 0.5, 76)],
    [(0.75, 0.25, 78), (1, 0.25, 79), (1.25, 0.25, 78), (1.5, 0.25, 76), (1.75, 0.25, 66), (2, 0.75, 74), (2.75, 0.5, 74), (3.5, 0.25, 73), (3.75, 0.25, 74)],
    [(0, 0.5, 73), (0.5, 0.25, 69), (0.75, 0.5, 66), (1.25, 0.5, 69), (1.75, 0.25, 62), (2, 0.75, 71), (2.75, 0.5, 73), (3.25, 0.25, 62), (3.5, 0.25, 74), (3.75, 0.25, 62)],
    [(0, 1.5, 69), (1.5, 0.5, 62), (2, 0.25, 71), (2.25, 0.5, 62), (2.75, 0.25, 62), (3, 0.25, 67), (3.25, 0.25, 71), (3.5, 0.25, 74), (3.75, 0.25, 76)],
    [(0, 0.25, 74), (0.25, 0.5, 64), (0.75, 0.5, 73), (1.25, 0.25, 74), (1.5, 0.25, 76), (1.75, 0.25, 69), (2, 0.25, 78), (2.25, 0.5, 69), (2.75, 0.25, 69), (3, 0.25, 78), (3.25, 0.25, 69), (3.5, 0.25, 74), (3.75, 0.5, 76)],
    [(0.75, 0.25, 78), (1, 0.25, 79), (1.25, 0.25, 78), (1.5, 0.25, 76), (1.75, 0.25, 66), (2, 0.75, 76), (2.75, 0.5, 74), (3.5, 0.25, 73), (3.75, 0.25, 74)],
    [(0, 0.5, 73), (0.5, 0.25, 69), (0.75, 0.5, 66), (1.25, 0.5, 69), (1.75, 0.25, 62), (2, 0.75, 71), (2.75, 0.5, 74), (3.25, 0.25, 71), (3.5, 0.25, 79), (3.75, 0.25, 67)],
    [(0, 0.25, 78), (0.25, 0.25, 69), (0.5, 0.25, 76), (0.75, 0.75, 74), (1.5, 0.5, 62), (2, 0.25, 71), (2.25, 0.5, 62), (2.75, 0.25, 62), (3, 0.25, 67), (3.25, 0.25, 71), (3.5, 0.25, 74), (3.75, 0.25, 76)],
    [(0, 0.75, 73), (0.75, 0.75, 74), (1.5, 0.25, 76), (1.75, 0.25, 78), (2, 0.5, 81), (2.5, 0.25, 78), (2.75, 0.25, 79), (3, 0.5, 81), (3.5, 0.25, 78), (3.75, 0.25, 79)],
    [(0, 0.25, 81), (0.25, 0.25, 73), (0.5, 0.25, 71), (0.75, 0.25, 73), (1, 0.25, 74), (1.25, 0.25, 76), (1.5, 0.25, 78), (1.75, 0.25, 79), (2, 0.5, 78), (2.5, 0.25, 74), (2.75, 0.25, 76), (3, 0.75, 78), (3.75, 0.25, 64)],
    [(0, 0.25, 66), (0.25, 0.25, 67), (0.5, 0.25, 66), (0.75, 0.25, 64), (1, 0.25, 66), (1.25, 0.25, 74), (1.5, 0.25, 73), (1.75, 0.25, 74), (2, 0.5, 71), (2.5, 0.25, 74), (2.75, 0.25, 73), (3, 0.5, 71), (3.5, 0.25, 69), (3.75, 0.25, 67)],
    [(0, 0.25, 69), (0.25, 0.25, 67), (0.5, 0.25, 66), (0.75, 0.25, 67), (1, 0.25, 69), (1.25, 0.25, 71), (1.5, 0.25, 73), (1.75, 0.25, 74), (2, 0.5, 71), (2.5, 0.25, 74), (2.75, 0.25, 73), (3, 0.5, 74), (3.5, 0.25, 73), (3.75, 0.25, 71)],
    [(0, 0.25, 73), (0.25, 0.25, 71), (0.5, 0.25, 73), (0.75, 0.25, 74), (1, 0.25, 76), (1.25, 0.25, 78), (1.5, 0.25, 79), (1.75, 0.25, 81), (2, 0.5, 81), (2.5, 0.25, 78), (2.75, 0.25, 79), (3, 0.5, 81), (3.5, 0.25, 78), (3.75, 0.25, 79)],
    [(0, 0.25, 73), (0.25, 0.25, 71), (0.5, 0.25, 73), (0.75, 0.25, 74), (1, 0.25, 76), (1.25, 0.25, 78), (1.5, 0.25, 79), (1.75, 0.25, 81), (2, 0.5, 78), (2.5, 0.25, 74), (2.75, 0.25, 76), (3, 0.5, 78), (3.5, 0.25, 76), (3.75, 0.25, 74)],
    [(0, 0.25, 76), (0.25, 0.25, 73), (0.5, 0.25, 74), (0.75, 0.25, 76), (1, 0.25, 78), (1.25, 0.25, 76), (1.5, 0.25, 74), (1.75, 0.25, 73), (2, 0.5, 74), (2.5, 0.25, 71), (2.75, 0.25, 73), (3, 0.75, 74), (3.75, 0.25, 64)],
    [(0, 0.25, 73), (0.25, 0.25, 74), (0.5, 0.25, 76), (0.75, 0.25, 74), (1, 0.25, 73), (1.25, 0.5, 69), (1.75, 0.25, 73), (2, 2, 74)],
]
VOICE_0_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 21), (26, 22), (27, 23), (28, 25), (29, 26), (30, 22), (31, 23), (32, 27)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# 22 distinct bars over 33 bars of music.
VOICE_1_CELLS = [
    [(2.5, 0.5, 57), (3, 0.5, 62), (3.5, 0.5, 57)],
    [(0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 54), (3, 0.5, 59), (3.5, 0.5, 54)],
    [(0.5, 0.5, 49), (1, 0.5, 54), (1.5, 0.5, 49), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0.5, 0.5, 57), (1, 0.5, 62), (1.5, 0.5, 57), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2, 2, 69), (2.5, 0.5, 57), (3, 0.5, 62), (3.5, 0.5, 57)],
    [(0, 2, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2, 1, 71), (2.5, 0.5, 54), (3, 0.5, 59), (3, 1, 71), (3.5, 0.5, 54)],
    [(0, 1, 78), (0.5, 0.5, 49), (1, 0.5, 54), (1, 1, 76), (1.5, 0.5, 49), (2, 1, 71), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0, 1, 69), (0.5, 0.5, 57), (1, 0.5, 62), (1.5, 0.5, 57), (2, 1, 64), (2.5, 0.5, 50), (3, 0.5, 55), (3, 1, 71), (3.5, 0.5, 50)],
    [(0, 1, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2, 0.5, 66), (2.5, 0.5, 57), (3, 0.5, 62), (3.5, 0.5, 57)],
    [(0, 1, 61), (0.5, 0.5, 52), (1, 0.5, 57), (1, 1, 69), (1.5, 0.5, 52), (2, 1, 66), (2.5, 0.5, 54), (3, 0.5, 59), (3, 1, 71), (3.5, 0.5, 54)],
    [(0, 0.5, 73), (0.5, 0.5, 49), (1, 0.5, (54, 76)), (1.5, 0.5, 49), (2, 0.5, 71), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0, 0.5, 69), (0.5, 0.5, 57), (1, 0.5, 62), (1.5, 0.5, 57), (2, 0.5, 67), (2.5, 0.5, (50, 64)), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0, 1.5, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2, 0.75, 69), (2.5, 0.5, 57), (2.75, 0.25, 69), (3, 0.5, 62), (3.5, 0.5, 57), (3.75, 0.5, 69)],
    [(0.25, 0.5, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 54), (2.75, 0.5, 66), (3, 0.5, 59), (3.25, 0.25, 66), (3.5, 0.5, 54)],
    [(0.5, 0.5, 49), (1, 0.5, 54), (1.5, 0.5, 49), (2, 0.75, 67), (2.5, 0.5, 50), (2.75, 0.5, 69), (3, 0.5, 55), (3.5, 0.25, 69), (3.5, 0.5, 50)],
    [(0, 1.5, 66), (0.5, 0.5, 57), (1, 0.5, 62), (1.5, 0.5, 57), (2, 0.25, 67), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0.5, 0.5, 52), (0.75, 0.5, 64), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 57), (3, 0.5, 62), (3.5, 0.5, 57), (3.75, 0.5, 69)],
    [(0.5, 0.5, 49), (1, 0.5, 54), (1.5, 0.5, 49), (2, 0.75, 67), (2.5, 0.5, 50), (3, 0.5, 55), (3.5, 0.5, 50)],
    [(0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 57), (3, 0.5, 62), (3.5, 0.5, 57)],
    [(0.25, 0.25, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 54), (3, 0.5, 59), (3.5, 0.5, 54)],
    [(0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2, 0.5, 78), (2.5, 0.25, 74), (2.5, 0.5, 57), (2.75, 0.25, 76), (3, 0.5, (62, 78)), (3.5, 0.25, 74), (3.5, 0.5, 57), (3.75, 0.25, 76)],
    [(0, 0.25, 78), (0.25, 0.25, 69), (0.5, 0.5, 52), (1, 0.5, 57), (1.5, 0.5, 52), (2.5, 0.5, 54), (3, 0.5, 59), (3.5, 0.5, 54)],
]
VOICE_1_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 13), (18, 17), (19, 3), (20, 18), (21, 19), (22, 2), (23, 3), (24, 20), (25, 21), (26, 2), (27, 3), (28, 18), (29, 1), (30, 2), (31, 3), (32, 18)]
VOICE_1_VOICE = (0, 72)   # program, velocity

# ---- voice 2 ----
# 6 distinct bars over 34 bars of music.
VOICE_2_CELLS = [
    [(2, 0.5, 50)],
    [(0, 0.5, 45), (2, 0.5, 47)],
    [(0, 0.5, 42), (2, 0.5, 43)],
    [(0, 0.5, 50), (2, 0.5, 43)],
    [(0, 0.5, 45), (2, 0.5, 50)],
    [(0, 4, (50, 57, 62, 66))],
]
VOICE_2_PLAN = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 1), (6, 2), (7, 3), (8, 4), (9, 1), (10, 2), (11, 3), (12, 4), (13, 1), (14, 2), (15, 3), (16, 4), (17, 1), (18, 2), (19, 3), (20, 4), (21, 1), (22, 2), (23, 3), (24, 4), (25, 1), (26, 2), (27, 3), (28, 4), (29, 1), (30, 2), (31, 3), (32, 4), (33, 5)]
VOICE_2_VOICE = (0, 64)   # program, velocity

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
    # The finished pieces live in output/. The directory is made if it
    # is not there, so the script still runs from a bare copy of itself
    # - which is the property the whole set is checked for.
    out = argv[1] if len(argv) > 1 else os.path.join(OUT_DIR,
                                                     'canon_arr.mid')
    here = os.path.dirname(out)
    if here and not os.path.isdir(here):
        os.makedirs(here)
    open(out, "wb").write(build())
    print("%s -> %s" % (TITLE, out))
    for name, cells, plan, _ in VOICES:
        print("  %-14s %3d bars, %3d distinct, %4d attacks"
              % (name, len(plan), len(cells),
                 len(unroll(cells, plan))))
    # MEASURED THE WAY build() LAYS IT OUT, so the number printed is the
    # number the player takes: the length runs to the end-of-track mark
    # and so includes TAIL, the tempo events sit at `beat + shift` as
    # build() writes them, and the speed reported is the mean over the
    # map weighted by how long each step is in force.
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
