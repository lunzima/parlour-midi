"""Report what is wrong with a MIDI file, for playback on old hardware.

These files are meant for machines with a PC speaker, an OPL2 card or an
early GM module: one to nine voices, no velocity curve to hide behind, and a
synth that plays exactly what is written. Anything a modern soft-synth
smooths over comes through.

Two kinds of finding, and the difference matters.

HARD - the device cannot do it, so the file is wrong until it changes:

    polyphony       More notes sounding at once than the device has
                    voices. An OPL2 has nine, a PC speaker has one.
                    Whatever is over the budget is simply not heard.
    short notes     Notes below the shortest the target can articulate.
                    A PC speaker reprograms a divider per note and an
                    OPL2 has an attack to get through; under that the
                    note is a click or nothing.
    self-overlap    One channel striking a pitch it is already holding.
                    A note-off does not say which note-on it ends, so
                    the first release silences both and a hole opens in
                    what was meant to be held.

SOFT - it will play, and whether it should is a judgement:

    clashes         Intervals held long enough to be heard as one sound.
                    A minor second is harsh anywhere; a major second is
                    fine up high and mud low down; a major seventh is
                    harsh unless the lower note is a bass an octave or
                    more below; a tritone is correct inside a dominant
                    seventh and wrong outside one, so the chord sounding
                    is named before the interval is judged. Measured by
                    overlap: a melody note crossing a chord for a
                    sixteenth is not a clash, the same second held for a
                    beat is.
    spacing         Below C3 a third is thick and a second growls,
                    whatever the harmony says.
    hands           What a player is asked for, if this is ever to be
                    played rather than only sequenced: a reach wider
                    than a tenth struck at once, a key restruck before
                    the action can return, or a leap with no time to
                    travel. Ornaments are exempt - fingers manage a fast
                    pair, what stops a hand is being asked to keep it up.
    grid            How far onsets sit from a 1/32. Near 0% is stepped
                    in or engraved; 35-50% is played in with swing,
                    which is the performance and not something to
                    quantise away.

    python midi_check.py <file.mid> [all] [voices=N] [minms=N] [split=N|ch]

By default the melody is left out of the clash test - a tune crossing its
own accompaniment makes intervals that belong to the tune. Pass `all` to
include it, and do that before believing a clean report.
"""
import sys
from collections import defaultdict

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
DRUM = 9

# --- hard limits, from the hardware ---------------------------------------
VOICES = 9              # OPL2's melodic budget
MIN_NOTE_MS = 40        # shorter than this a beeper clicks and an OPL2
                        # envelope has not finished attacking

# --- soft limits ----------------------------------------------------------
MIN_OVERLAP = 0.2       # beats two notes must share before the ear fuses them
LOW = 48                # C3
SPLIT = 60              # middle C, for the hand split
SPAN_LIMIT = 16         # a tenth: what one hand reaches without rolling
MAX_TOGETHER = 5        # five fingers
REPEAT_MS = 70          # a piano action needs this to return the key
SUSTAINED_RUN = 3       # this many fast gaps in a row is a run, not a flourish
MS_PER_SEMITONE = 5     # travel budget for a leap


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
    """[(start, dur, pitch, channel)] in ticks, the division, the tempo map."""
    b = open(path, 'rb').read()
    div = (b[12] << 8) | b[13]
    ntrk = (b[10] << 8) | b[11]
    i = 8 + ((b[4] << 24) | (b[5] << 16) | (b[6] << 8) | b[7])
    out, tempi = [], []
    for _ in range(ntrk):
        if b[i:i + 4] != b'MTrk':
            break
        ln = (b[i + 4] << 24) | (b[i + 5] << 16) | (b[i + 6] << 8) | b[i + 7]
        p, end = i + 8, i + 8 + ln
        i = end
        t, st, live = 0, 0, []
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
                    tempi.append((t, us))
                continue
            if st in (0xF0, 0xF7):
                n, p = vlq(b, p)
                p += n
                continue
            hi, ch = st & 0xF0, st & 0x0F
            if hi in (0xC0, 0xD0):
                p += 1
                continue
            note, vel = b[p], b[p + 1]
            p += 2
            if hi == 0x90 and vel > 0:
                live.append([t, note, ch])
            elif hi in (0x80, 0x90):
                for e in reversed(live):
                    if e[1] == note and e[2] == ch:
                        out.append((e[0], t - e[0], note, ch))
                        live.remove(e)
                        break
        for e in live:
            out.append((e[0], t - e[0], e[1], e[2]))
    out.sort()
    return out, div, sorted(tempi) or [(0, 500000)]


def ms_at(tick, div, tempi):
    """Milliseconds from the start of the file to a tick."""
    us, prev, rate = 0.0, 0, tempi[0][1]
    for t, r in tempi:
        if t >= tick:
            break
        us += (t - prev) * rate / div
        prev, rate = t, r
    us += (tick - prev) * rate / div
    return us / 1000.0


def chord_at(notes, tick):
    return {p % 12 for s, d, p, c in notes if s <= tick < s + d}


def in_seventh(pcs):
    for root in pcs:
        if {(root + i) % 12 for i in (0, 4, 7, 10)} >= pcs:
            return True
    return False


def clashes(notes, div, lead_ch):
    found = defaultdict(list)
    play = [n for n in notes if n[3] != DRUM]
    for i, (s1, d1, p1, c1) in enumerate(play):
        for s2, d2, p2, c2 in play[i + 1:]:
            if s2 >= s1 + d1:
                break
            if p1 == p2:
                continue
            if lead_ch is not None and lead_ch in (c1, c2) and c1 != c2:
                continue
            ov = (min(s1 + d1, s2 + d2) - max(s1, s2)) / float(div)
            if ov < MIN_OVERLAP:
                continue
            lo, hi = (p1, p2) if p1 < p2 else (p2, p1)
            iv = (hi - lo) % 12
            if (hi - lo) >= 12 and iv in (2, 11):
                continue
            at = max(s1, s2)
            if iv == 6 and not in_seventh(chord_at(play, at)):
                found['tritone'].append((at, lo, hi, ov))
            elif iv == 1:
                found['minor second'].append((at, lo, hi, ov))
            elif iv == 2:
                found['major second'].append((at, lo, hi, ov))
            elif iv == 11:
                found['major seventh'].append((at, lo, hi, ov))
            if hi < LOW and (hi - lo) < 5:
                found['close below C3'].append((at, lo, hi, ov))
    return found


def self_overlap(notes):
    out, by = [], defaultdict(list)
    for s, d, p, c in notes:
        by[(c, p)].append((s, d))
    for (c, p), v in by.items():
        v.sort()
        for i in range(len(v) - 1):
            if v[i + 1][0] < v[i][0] + v[i][1]:
                out.append((v[i + 1][0], p, c,
                            v[i][0] + v[i][1] - v[i + 1][0]))
    return sorted(out)


def polyphony(notes, budget):
    edges = sorted({s for s, d, p, c in notes} |
                   {s + d for s, d, p, c in notes})
    worst, over = 0, []
    for t in edges:
        n = sum(1 for s, d, p, c in notes if s <= t < s + d and c != DRUM)
        worst = max(worst, n)
        if n > budget:
            over.append((t, n))
    return worst, over


def short_notes(notes, div, tempi, limit_ms):
    out = []
    for s, d, p, c in notes:
        if c == DRUM:
            continue
        ms = ms_at(s + d, div, tempi) - ms_at(s, div, tempi)
        if ms < limit_ms:
            out.append((s, p, c, ms))
    return sorted(out)


def hands(notes, div, tempi, split):
    """Reach, repeats and leaps, per hand. Returns {hand: {...}}."""
    out = {}
    for label in ('right', 'left'):
        if split == 'ch':
            want = {0} if label == 'right' else {1, 2}
            hand = [n for n in notes if n[3] in want]
        else:
            hand = [n for n in notes if n[3] != DRUM and
                    ((n[2] >= split) == (label == 'right'))]
        if not hand:
            out[label] = None
            continue
        by_onset = defaultdict(list)
        for s, d, p, c in hand:
            by_onset[s].append(p)
        onsets = sorted(by_onset)
        times = {t: ms_at(t, div, tempi) for t in onsets}

        wide = [(t, max(g) - min(g)) for t, g in by_onset.items()
                if max(g) - min(g) > SPAN_LIMIT]
        many = [(t, len(g)) for t, g in by_onset.items()
                if len(g) > MAX_TOGETHER]

        # Same key struck again before the action returns.
        by_note = defaultdict(list)
        for s, d, p, c in hand:
            by_note[p].append(s)
        repeats = []
        for p, ts in by_note.items():
            ts.sort()
            for a, b in zip(ts, ts[1:]):
                g = times.get(b, ms_at(b, div, tempi)) - \
                    times.get(a, ms_at(a, div, tempi))
                if g < REPEAT_MS:
                    repeats.append((a, p, g))

        # Runs of onsets too close to sustain. An isolated pair is an
        # ornament; SUSTAINED_RUN in a row is a texture no hand keeps up.
        close = [times[b] - times[a] < REPEAT_MS
                 for a, b in zip(onsets, onsets[1:])]
        runs, k = 0, 0
        for c in close:
            k = k + 1 if c else 0
            if k == SUSTAINED_RUN:
                runs += 1

        leaps = []
        for a, b in zip(onsets, onsets[1:]):
            dist = abs(max(by_onset[b]) - max(by_onset[a]))
            if dist > SPAN_LIMIT and (times[b] - times[a]) < \
                    dist * MS_PER_SEMITONE:
                leaps.append((a, dist, times[b] - times[a]))
        out[label] = dict(wide=wide, many=many, repeats=sorted(repeats),
                          runs=runs, leaps=sorted(leaps, key=lambda x: -x[1]))
    return out


def main(argv):
    if len(argv) < 2:
        print('usage: midi_check.py <file.mid> [all] [voices=N] [minms=N] '
              '[split=N|ch]')
        return 1
    path, opts = argv[1], argv[2:]
    budget, limit_ms, split = VOICES, MIN_NOTE_MS, SPLIT
    for o in opts:
        if o.startswith('voices='):
            budget = int(o.split('=')[1])
        elif o.startswith('minms='):
            limit_ms = float(o.split('=')[1])
        elif o.startswith('split='):
            v = o.split('=')[1]
            split = 'ch' if v == 'ch' else int(v)
    notes, div, tempi = read(path)
    if not notes:
        print('%s: no notes' % path)
        return 1
    chans = sorted({c for s, d, p, c in notes})
    lead = None if 'all' in opts else (chans[0] if len(chans) > 1 else None)

    print('%s  %d notes, %d channels, division %d'
          % (path, len(notes), len(chans), div))
    if lead is not None:
        print('   channel %d taken as the tune and left out of the clash '
              'test (`all` includes it)' % lead)

    hard = soft = 0
    print()
    print('HARD')
    worst, over = polyphony(notes, budget)
    if over:
        hard += len(over)
        print('   polyphony    peak %d against a budget of %d, over at %d '
              'moment(s)' % (worst, budget, len(over)))
        for t, n in over[:4]:
            print('                  %7.2f beats  %d sounding'
                  % (t / float(div), n))
    else:
        print('   polyphony    peak %d, budget %d - ok' % (worst, budget))

    sh = short_notes(notes, div, tempi, limit_ms)
    if sh:
        hard += len(sh)
        print('   short notes  %d under %g ms, shortest %.0f ms'
              % (len(sh), limit_ms, min(x[3] for x in sh)))
        for t, p, c, ms in sh[:4]:
            print('                  %7.2f beats  ch%d %-4s  %.0f ms'
                  % (t / float(div), c, nm(p), ms))
    else:
        print('   short notes  none under %g ms - ok' % limit_ms)

    so = self_overlap(notes)
    if so:
        hard += len(so)
        print('   self-overlap %d' % len(so))
        for t, p, c, ov in so[:4]:
            print('                  %7.2f beats  ch%d %-4s  %.2f beats lost'
                  % (t / float(div), c, nm(p), ov / float(div)))
    else:
        print('   self-overlap none - ok')

    print()
    print('SOFT')
    cl = clashes(notes, div, lead)
    total_cl = sum(len(v) for v in cl.values())
    soft += total_cl
    if total_cl:
        for kind in ('minor second', 'major seventh', 'close below C3',
                     'tritone', 'major second'):
            hits = cl.get(kind, [])
            if hits:
                print('   %-14s %d' % (kind, len(hits)))
                for t, lo, hi, ov in sorted(hits, key=lambda x: -x[3])[:3]:
                    print('                  %7.2f beats  %-4s %-4s  %.2f beats'
                          % (t / float(div), nm(lo), nm(hi), ov))
    else:
        print('   clashes      none')

    hd = hands(notes, div, tempi, split)
    for label in ('right', 'left'):
        h = hd[label]
        if h is None:
            continue
        bits = []
        if h['wide']:
            bits.append('%d reach past %d semitones (widest %d)'
                        % (len(h['wide']), SPAN_LIMIT,
                           max(d for t, d in h['wide'])))
        if h['many']:
            bits.append('%d chords of more than %d notes'
                        % (len(h['many']), MAX_TOGETHER))
        if h['repeats']:
            bits.append('%d same-key repeats under %d ms (fastest %.0f)'
                        % (len(h['repeats']), REPEAT_MS,
                           min(g for t, p, g in h['repeats'])))
        if h['runs']:
            bits.append('%d runs of %d+ onsets under %d ms'
                        % (h['runs'], SUSTAINED_RUN, REPEAT_MS))
        if h['leaps']:
            bits.append('%d rushed leaps (widest %d semitones)'
                        % (len(h['leaps']), h['leaps'][0][1]))
        soft += sum(len(h[k]) for k in ('wide', 'many', 'repeats', 'leaps'))
        print('   %-5s hand   %s' % (label, '; '.join(bits) or 'ok'))

    step = max(1, div // 8)
    by = defaultdict(lambda: [0, 0])
    for s, d, p, c in notes:
        by[c][1] += 1
        if s % step:
            by[c][0] += 1
    print('   grid         %s'
          % '  '.join('ch%d %d%%' % (c, round(100.0 * b / t))
                      for c, (b, t) in sorted(by.items())))

    print()
    print('   %d hard, %d soft' % (hard, soft))
    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
