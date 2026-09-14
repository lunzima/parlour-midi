"""Measure a MIDI file. Numbers only - nothing here is a complaint.

These files are written for machines with a PC speaker, an OPL2 card or an
early GM module, so the numbers that matter are the ones those devices care
about: how many voices are asked for, how wide the compass is, how much of
the time each channel is actually sounding.

WHAT IS MEASURED:

    per channel     notes, compass, the share of the piece it sounds for,
                    and its program number
    texture         attacks per bar, average voices sounding, distinct
                    bars played, and compass - given for each hand,
                    split at middle C. A hand that repeats one figure
                    for fifty bars is busy and empty at the same time,
                    which the attack count alone does not show.
    tempo           the map, and the mean weighted by how long each
                    step is in force
    length          bars, beats, and seconds

    python midi_stats.py <file.mid> [more.mid ...]
    python midi_stats.py --texture <file.mid> [more.mid ...]

Without --texture the per-channel table is printed; with it, the two-hand
one. Both are printed for a single file.
"""
import sys
from collections import defaultdict

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
DRUM = 9
SPLIT = 60          # middle C: at or above it the right hand


def nm(p):
    return NAMES[p % 12] + str(p // 12 - 1)


def vlq(b, p):
    v = 0
    while True:
        c = b[p]
        p += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, p


def read(path):
    """notes, division, tempo map, time signature."""
    b = open(path, 'rb').read()
    div = (b[12] << 8) | b[13]
    ntrk = (b[10] << 8) | b[11]
    i = 8 + ((b[4] << 24) | (b[5] << 16) | (b[6] << 8) | b[7])
    notes, tempi, sig, progs = [], [], None, {}
    for _ in range(ntrk):
        if b[i:i + 4] != b'MTrk':
            break
        ln = (b[i + 4] << 24) | (b[i + 5] << 16) | (b[i + 6] << 8) | b[i + 7]
        p, end = i + 8, i + 8 + ln
        i = end
        t, st, open_notes = 0, 0, []
        while p < end:
            d, p = vlq(b, p)
            t += d
            c = b[p]
            if c & 0x80:
                st = c
                p += 1
            if st == 0xFF:
                ty = b[p]
                p += 1
                n, p = vlq(b, p)
                data = b[p:p + n]
                p += n
                if ty == 0x51 and n == 3:
                    us = (data[0] << 16) | (data[1] << 8) | data[2]
                    tempi.append((t, 60000000.0 / us))
                elif ty == 0x58 and n >= 2 and sig is None:
                    sig = (data[0], 1 << data[1])
                continue
            if st in (0xF0, 0xF7):
                n, p = vlq(b, p)
                p += n
                continue
            hi, ch = st & 0xF0, st & 0x0F
            if hi == 0xC0:
                progs[ch] = b[p]
                p += 1
                continue
            if hi == 0xD0:
                p += 1
                continue
            note, vel = b[p], b[p + 1]
            p += 2
            if hi == 0x90 and vel > 0:
                open_notes.append([t, note, ch])
            elif hi in (0x80, 0x90):
                for e in reversed(open_notes):
                    if e[1] == note and e[2] == ch:
                        notes.append((e[0], t - e[0], note, ch))
                        open_notes.remove(e)
                        break
        for e in open_notes:
            notes.append((e[0], t - e[0], e[1], e[2]))
    notes.sort()
    return notes, div, sorted(tempi), (sig or (4, 4)), progs


def seconds(notes, div, tempi):
    if not notes:
        return 0.0
    end = max(s + d for s, d, p, c in notes)
    steps = tempi or [(0, 120.0)]
    total = 0.0
    for i, (t, bpm) in enumerate(steps):
        nxt = steps[i + 1][0] if i + 1 < len(steps) else end
        span = max(0, min(nxt, end) - t)
        total += (span / float(div)) * 60.0 / bpm
    return total


def per_channel(notes, div, progs, tempi):
    end = max(s + d for s, d, p, c in notes)
    rows = []
    for ch in sorted({c for s, d, p, c in notes}):
        v = [n for n in notes if n[3] == ch]
        ps = [p for s, d, p, c in v]
        sounding = sum(d for s, d, p, c in v)
        rows.append((ch, len(v), min(ps), max(ps),
                     100.0 * sounding / (end * max(1, len(v))) * len(v) / 1.0
                     if end else 0.0, progs.get(ch)))
    return rows, end


def texture(notes, div, sig):
    bar = div * sig[0] * 4 // sig[1]
    hands = {'left': [], 'right': []}
    for s, d, p, c in notes:
        if c == DRUM:
            continue
        hands['right' if p >= SPLIT else 'left'].append((s, d, p))
    out = {}
    for name, v in hands.items():
        if not v:
            out[name] = None
            continue
        bars = defaultdict(list)
        for s, d, p in v:
            bars[s // bar].append(p)
        nbars = (max(s + d for s, d, p in v) // bar) + 1
        held = sum(d for s, d, p in v)
        ps = [p for s, d, p in v]
        shapes = {tuple(sorted(x)) for x in bars.values()}
        out[name] = dict(att=len(v) / float(nbars),
                         vox=held / float(nbars * bar),
                         dist=len(shapes),
                         span=max(ps) - min(ps),
                         lo=min(ps), hi=max(ps))
    return out, bar


def report(path, want_texture, only):
    notes, div, tempi, sig, progs = read(path)
    if not notes:
        print('%s: no notes' % path)
        return
    rows, end = per_channel(notes, div, progs, tempi)
    secs = seconds(notes, div, tempi)
    bar = div * sig[0] * 4 // sig[1]
    mean = (sum(b for t, b in tempi) / len(tempi)) if tempi else 120.0
    print('%s' % path)
    print('   %d notes  %d/%d  %.0f bars  %.1f beats  %.1f s  '
          '%.4g bpm over %d step(s)'
          % (len(notes), sig[0], sig[1], end / float(bar), end / float(div),
             secs, mean, max(1, len(tempi))))
    if not only or not want_texture:
        print('   %-4s %6s  %-9s %6s  %s'
              % ('ch', 'notes', 'compass', 'sound%', 'program'))
        for ch, n, lo, hi, pct, prog in rows:
            held = sum(d for s, d, p, c in notes if c == ch)
            print('   %-4d %6d  %-9s %5.0f%%  %s'
                  % (ch, n, '%s..%s' % (nm(lo), nm(hi)),
                     100.0 * held / end if end else 0,
                     '-' if prog is None else prog))
    if not only or want_texture:
        tx, bar = texture(notes, div, sig)
        print('   %-6s %6s %6s %6s %6s  %s'
              % ('hand', 'att/bar', 'voices', 'bars', 'span', 'compass'))
        for name in ('right', 'left'):
            h = tx[name]
            if h is None:
                print('   %-6s (silent)' % name)
                continue
            print('   %-6s %7.1f %6.2f %6d %6d  %s..%s'
                  % (name, h['att'], h['vox'], h['dist'], h['span'],
                     nm(h['lo']), nm(h['hi'])))
    print()


def main(argv):
    args = [a for a in argv[1:] if not a.startswith('--')]
    want_texture = '--texture' in argv
    if not args:
        print('usage: midi_stats.py [--texture] <file.mid> [more.mid ...]')
        return 1
    only = len(args) > 1
    for path in args:
        report(path, want_texture, only)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
