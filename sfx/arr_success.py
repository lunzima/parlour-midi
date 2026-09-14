"""Success chime.

Transcribed from DeepSeek Reasonix's completion chime.

    python arr_success.py [out.mid]
"""
import os
import struct
import sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

DIV = 192          # ticks per beat
# One step. 125 of them a minute puts a beat at 480 ms, so every 10 ms
# of the source lands on a whole tick and no onset is rounded into the
# file.
TEMPO = [
    (0.0, 125),
]
BPM = TEMPO[0][1]
TIME_SIG = (4, 4)
BAR = 4            # beats per bar
# Silence at each end, in beats. The other pieces here take about 2 s
# and 4 s; this one takes 120 ms and 600 ms. It is a chime that
# announces something, and a chime arriving two seconds behind the event
# announces nothing. 120 ms is still enough to keep the first note clear
# of tick 0, where the program change sits.
LEAD_IN = 0.25
TAIL = 1.25
# Every note gives up a little of its tail - see arr_elise.py. One
# handover needs it: voice 0 lets E6 go exactly where voice 1 takes the
# same pitch up, and untrimmed the two run into each other.
TRIM_PER_BEAT = 0.05
TRIM_CAP = 0.20


def trim_of(d):
    """How much of its length a note of `d` beats gives up."""
    return d * min(TRIM_CAP, TRIM_PER_BEAT * max(1, int(d + 1e-9)))


def ms(x):
    """Milliseconds as beats. The source states its chime in seconds."""
    return x * BPM / 60000.0


TITLE = 'Success chime'

# ---- voice 0 ----
# Three tones stacked, not played in turn: E6 rings for 200 ms, G6 joins
# at 70 and rings for 220, C7 joins at 140 and rings for 300, and at 440
# it is over. One voice cannot stack anything, so the tune clips each
# tone where the next one starts.
#
# The frequencies are notes: 1318.5 Hz is E6, 1568.0 is G6, 2093.0 is C7.
VOICE_0_CELLS = [
    [(0, ms(70), 88), (ms(70), ms(70), 91), (ms(140), ms(300), 96)],
]
VOICE_0_PLAN = [(0, 0)]
VOICE_0_VOICE = (0, 96)   # program, velocity

# ---- voice 1 ----
# The tails: what is left of E6 and G6 once the tune has moved off them.
# Two voices sounding together are the chime as written; a device with
# one voice plays voice 0 and hears it as an arpeggio.
VOICE_1_CELLS = [
    [(ms(70), ms(130), 88), (ms(140), ms(150), 91)],
]
VOICE_1_PLAN = [(0, 0)]
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
    # ../music/arr_canon.py.
    out = argv[1] if len(argv) > 1 else os.path.join(OUT_DIR,
                                                     'success_arr.mid')
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
