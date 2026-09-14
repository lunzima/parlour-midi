"""Snezhnograd Nights.

Arranged from a transcription of Liao Changyong's Moscow Nights.

    python arr_snezhnograd.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
TIME_SIG = (2, 4)
BAR = 2          # beats per bar

# (beat, microseconds per quarter). The whole map, not just
# the opening: the ritardandi and the pushes are the
# arrangement, not the playback. Microseconds because that
# is what the file stores - a ritardando steps in fractions
# of a beat per minute and rounding it to whole bpm flattens
# it.
# IN BPM AND NOT IN MICROSECONDS. The note above was the
# reason this held microseconds - a ritardando steps in
# fractions of a beat per minute, and whole bpm would flatten
# it. That is a reason to allow fractions, not a reason to
# store the reciprocal. The ritardando is 67 down to 64 in
# steps of three sevenths of a beat per minute, which is what
# it always was and now says so.
#
# FOUR PLACES, WHICH IS THE SERIES ITSELF. 67 down to 64 in
# seven steps is three sevenths of a beat per minute each, and
# these are that series rounded once. Two of them land one
# microsecond off what the file held when this list was in
# microseconds - a part in nine hundred thousand, and about two
# microseconds across the whole ritardando. Written to five
# places they match to the byte; that is not worth carrying, and
# the number a musician reads is the one to keep readable.
TEMPO = [
    (0, 67),
    (116, 66.5714),
    (118, 66.1429),
    (120, 65.7143),
    (122, 65.2857),
    (124, 64.8571),
    (126, 64.4286),
    (128, 64),
]
BPM = TEMPO[0][1]

# Silence at each end, in beats: nothing begins on a note
# or ends on one. About 2 s before the first note and 4 s
# after the last, whole beats at the tempo in force there -
# at 67 bpm that is 1.8 s and 3.6 s.
LEAD_IN = 2
TAIL = 4

# Every note gives up a little of its tail so the next stroke
# of the same pitch starts against silence. Stepped by whole
# beats, five per cent as the floor - the same rule the other
# arrangements here use, applied at build time to note lengths
# written out in full, so the data says what a score would say
# and the articulation is a decision the script makes.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))

TITLE = 'Snezhnograd Nights'

# ---- voice 0 ----
# 16 distinct bars over 61 bars of music.
VOICE_0_CELLS = [
    [(0, 1, 69), (1, 1, 71)],
    [(0, 0.5, 74), (0.5, 0.5, 72), (1, 1.5, 67)],
    [(0.5, 1, 62), (1.5, 0.5, 60)],
    [(0, 0.5, 67), (0.5, 0.5, 65), (1, 2, 68)],
    [(1, 0.5, 70), (1.5, 0.5, 68)],
    [(0, 1, 67), (1, 0.5, 65), (1.5, 0.5, 63)],
    [(0, 1, 67), (1, 1, 65)],
    [(0, 2, 60)],
    [(0, 0.5, 60), (0.5, 0.5, 63), (1, 0.5, 67), (1.5, 0.5, 63)],
    [(0, 1, 65), (1, 0.5, 63), (1.5, 0.5, 62)],
    [(0, 0.5, 63), (0.5, 0.5, 67), (1, 0.5, 70), (1.5, 0.5, 70)],
    [(0, 1, 72), (1, 0.5, 70), (1.5, 0.5, 68)],
    [(0, 2, 67)],
    [(0, 1.5, 60), (1.5, 0.25, 58), (1.75, 0.25, 62)],
    [(0, 0.5, 67), (0.5, 0.25, 60), (0.75, 0.25, 62), (1, 0.25, 63), (1.25, 0.25, 65), (1.5, 0.25, 67), (1.75, 0.25, 70)],
    [(0, 3, 72)],
]
VOICE_0_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (10, 8), (11, 9), (12, 6), (13, 7), (14, 10), (15, 11), (16, 12), (17, 0), (18, 1), (19, 2), (20, 3), (21, 4), (22, 5), (23, 6), (24, 7), (26, 8), (27, 9), (28, 6), (29, 13), (30, 10), (31, 11), (32, 14), (33, 0), (34, 1), (35, 2), (36, 3), (37, 4), (38, 5), (39, 6), (40, 7), (42, 8), (43, 9), (44, 6), (45, 13), (46, 10), (47, 11), (48, 14), (49, 0), (50, 1), (51, 2), (52, 3), (53, 4), (54, 5), (55, 6), (56, 7), (57, 0), (58, 1), (59, 2), (60, 3), (61, 4), (62, 5), (63, 6), (64, 15)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# 33 distinct bars over 64 bars of music.
VOICE_1_CELLS = [
    [(0, 1, (60, 66)), (1, 1, (59, 65))],
    [(0.5, 0.5, (60, 63, 67)), (1.5, 0.5, (55, 60, 63))],
    [(0.5, 0.5, (51, 55, 60)), (1.5, 0.5, (51, 55, 60))],
    [(0.5, 0.5, (56, 60)), (1.5, 0.5, (56, 60, 65))],
    [(0.5, 0.5, (55, 63)), (1, 0.5, 55), (1.5, 0.5, (51, 55, 60))],
    [(0.5, 0.5, (56, 60)), (1, 0.5, 55), (1.5, 0.5, (53, 59))],
    [(0.5, 0.5, (63, 67, 72)), (1.5, 0.5, (63, 67, 72))],
    [(0.5, 0.5, (51, 55)), (1.5, 0.5, (51, 55))],
    [(0.5, 0.5, (56, 60)), (1.5, 0.5, (56, 60))],
    [(0.5, 0.5, (59, 65)), (1, 0.5, 55), (1.5, 0.5, (59, 62))],
    [(0.5, 0.5, (55, 58)), (1, 0.5, 63), (1.5, 0.5, (61, 67))],
    [(0.5, 0.5, (60, 63)), (1, 0.5, 68), (1.5, 0.5, (60, 63))],
    [(0.5, 0.5, (55, 58)), (1, 0.5, 63), (1.5, 0.5, (55, 58))],
    [(0.5, 0.5, (63, 67)), (1.5, 0.5, (55, 63))],
    [(0.5, 0.5, (55, 63)), (1, 0.5, 55), (1.5, 0.5, (51, 55))],
    [(0.5, 0.5, (68, 72)), (1.5, 0.5, (67, 71))],
    [(0.5, 0.5, (55, 60)), (1, 0.5, 63), (1.5, 0.5, (55, 60))],
    [(0, 0.5, 62), (0.5, 0.5, (56, 60)), (1.5, 0.5, (56, 60))],
    [(0.5, 0.5, (59, 65)), (1.5, 0.5, (59, 62))],
    [(0, 0.5, 48), (0.5, 0.5, (51, 55)), (1.5, 0.5, (51, 55))],
    [(0.5, 0.5, (55, 58)), (1.5, 0.5, (61, 67))],
    [(0.5, 0.5, (60, 63)), (1.5, 0.5, (60, 63))],
    [(0.5, 0.5, (55, 58)), (1.5, 0.5, (55, 58))],
    [(0, 0.5, 60), (0.5, 0.5, (63, 67)), (1.5, 0.5, (55, 63))],
    [(0, 0.5, 60), (0.5, 0.5, (51, 55)), (1.5, 0.5, (51, 55))],
    [(0.5, 0.5, (56, 60)), (1, 0.5, 60), (1.5, 0.5, (56, 60))],
    [(0.5, 0.5, (55, 63)), (1.5, 0.5, (51, 55))],
    [(0.5, 0.5, (56, 60)), (1.5, 0.5, (55, 59))],
    [(0, 0.5, 62), (0.5, 0.5, (68, 72)), (1.5, 0.5, (67, 71))],
    [(0.5, 0.5, (60, 66)), (1.5, 0.5, (59, 65, 67))],
    [(0.5, 0.5, (55, 60, 63)), (1, 0.5, 55), (1.5, 0.5, (51, 55, 60))],
    [(0.5, 0.5, (56, 60, 65)), (1, 0.5, 55), (1.5, 0.5, (53, 55, 59))],
    [(0, 3, (63, 67))],
]
VOICE_1_PLAN = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 3), (6, 4), (7, 5), (8, 2), (9, 6), (10, 7), (11, 8), (12, 9), (13, 7), (14, 10), (15, 11), (16, 12), (17, 0), (18, 13), (19, 7), (20, 8), (21, 8), (22, 14), (23, 5), (24, 7), (25, 15), (26, 16), (27, 17), (28, 18), (29, 19), (30, 20), (31, 21), (32, 22), (33, 0), (34, 23), (35, 24), (36, 25), (37, 17), (38, 26), (39, 27), (40, 19), (41, 28), (42, 16), (43, 17), (44, 18), (45, 7), (46, 20), (47, 21), (48, 22), (49, 0), (50, 13), (51, 7), (52, 25), (53, 17), (54, 26), (55, 27), (56, 7), (57, 29), (58, 13), (59, 7), (60, 25), (61, 17), (62, 30), (63, 31), (64, 32)]
VOICE_1_VOICE = (0, 70)   # program, velocity

# ---- voice 2 ----
# 35 distinct bars over 64 bars of music.
VOICE_2_CELLS = [
    # (43, 43) was G2 written twice - two note-ons, one note-off, and the
    # first release silences both. Reduced to the single note it already
    # sounded. The neighbouring event is an octave (D2-D3), so this was
    # probably meant to be one too, but which way is not recoverable.
    [(0, 1, (38, 50)), (1, 1, 43)],
    [(0, 2, 48), (1, 0.5, 43)],
    [(0, 0.5, 41), (0.5, 1.5, 53), (1, 0.5, 48)],
    [(0, 0.5, 50), (0.5, 1.5, 53), (1, 0.5, 41)],
    [(0, 1.5, 43), (0.5, 1.5, 48)],
    [(0, 1.5, 43), (0.5, 0.5, 53), (1.5, 0.5, 43)],
    [(0, 2, 48), (1, 0.5, 39)],
    [(0, 2, 48), (1, 0.5, 51)],
    [(0, 0.5, 50), (0.5, 1.5, 53), (1, 0.5, 44)],
    # Same pitch struck again while still held. The first is cut to end
    # where the second begins; the sound is unchanged and the collision
    # is gone.
    [(0, 0.5, 43), (0.5, 1.5, 43)],
    [(0, 1.5, 39), (0.5, 1.5, 51)],
    [(0, 0.5, 44), (0.5, 1.5, 44)],
    [(0, 0.5, 50), (0.5, 0.5, 53), (1, 1, 43)],
    [(0, 0.5, 48), (0.5, 0.5, 51), (1, 0.5, 48), (1.5, 0.5, 51)],
    [(0, 0.5, 44), (0.5, 0.5, 53), (1, 0.5, 44), (1.5, 0.5, 53)],
    [(0, 0.5, 43), (0.5, 0.5, 43), (1, 0.5, 43), (1.5, 0.5, 43)],
    [(0, 0.5, 43), (0.5, 0.5, 48), (1, 0.5, 43), (1.5, 0.5, 48)],
    [(0, 0.5, 39), (0.5, 0.5, 51), (1, 0.5, 39), (1.5, 0.5, 51)],
    [(0, 0.5, 44), (0.5, 0.5, 44), (1, 0.5, 44), (1.5, 0.5, 44)],
    [(0, 0.5, 38), (0.5, 0.5, 50), (1, 0.5, 38), (1.5, 0.5, 50)],
    [(0, 0.5, 41), (0.5, 0.5, 53), (1, 0.5, 41), (1.5, 0.5, 53)],
    [(0, 0.5, 43), (0.5, 0.5, 53), (1, 0.5, 43), (1.5, 0.5, 53)],
    [(0, 0.5, 39), (0.5, 0.5, 48), (1, 0.5, 39), (1.5, 0.5, 48)],
    [(0, 0.5, (36, 48)), (0.5, 0.5, 51), (1, 0.5, (36, 48)), (1.5, 0.5, 51)],
    [(0, 0.5, (29, 44)), (0.5, 0.5, 53), (1, 0.5, (29, 44)), (1.5, 0.5, 53)],
    [(0, 0.5, (31, 43)), (0.5, 0.5, 43), (1, 0.5, (31, 43)), (1.5, 0.5, 43)],
    [(0, 0.5, (36, 43)), (0.5, 0.5, 48), (1, 0.5, (36, 43)), (1.5, 0.5, 48)],
    [(0, 0.5, (27, 39)), (0.5, 0.5, 51), (1, 0.5, (27, 39)), (1.5, 0.5, 51)],
    [(0, 0.5, (32, 44)), (0.5, 0.5, 44), (1, 0.5, (32, 44)), (1.5, 0.5, 44)],
    [(0, 0.5, (31, 38)), (0.5, 0.5, 50), (1, 0.5, (31, 38)), (1.5, 0.5, 50)],
    [(0, 0.5, (29, 41)), (0.5, 0.5, 53), (1, 0.5, (29, 41)), (1.5, 0.5, 53)],
    [(0, 0.5, (29, 43)), (0.5, 0.5, 53), (1, 0.5, (29, 43)), (1.5, 0.5, 53)],
    [(0, 0.5, (24, 39)), (0.5, 0.5, 48), (1, 0.5, (24, 39)), (1.5, 0.5, 48)],
    [(0, 2, 43)],
    [(0, 3, (36, 48))],
]
VOICE_2_PLAN = [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 6), (10, 7), (11, 8), (12, 9), (13, 1), (14, 10), (15, 11), (16, 10), (17, 0), (18, 1), (19, 1), (20, 2), (21, 3), (22, 4), (23, 5), (24, 6), (25, 12), (26, 13), (27, 14), (28, 15), (29, 16), (30, 17), (31, 18), (32, 17), (33, 19), (34, 16), (35, 16), (36, 20), (37, 20), (38, 16), (39, 21), (40, 22), (41, 21), (42, 23), (43, 24), (44, 25), (45, 26), (46, 27), (47, 28), (48, 27), (49, 29), (50, 26), (51, 26), (52, 30), (53, 30), (54, 26), (55, 31), (56, 32), (57, 29), (58, 26), (59, 26), (60, 30), (61, 30), (62, 33), (63, 33), (64, 34)]
VOICE_2_VOICE = (0, 80)   # program, velocity

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
    # Articulation last, so the piece keeps its length.
    laid = [(ch, [(o, d - trim_of(d), p) for o, d, p in n], v)
            for ch, n, v in laid]
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
        OUT_DIR, 'snezhnograd_arr.mid')
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
