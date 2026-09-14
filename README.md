# parlour-midi

Standard MIDI Files arranged for machines with a PC speaker, an OPL2 card or an
early GM module. Those have between one and nine voices, no velocity curve, and
a synth that plays exactly what is written. Everything a modern soft-synth would
paper over is audible on them, so the arrangements deal with it beforehand.

The repertoire is mixed: a baroque canon, a Beethoven bagatelle, a Brazilian
choro, a Soviet standard, a couple of game themes. That is the older sense of a
parlour arrangement, which took a tune people already knew and cut it down to
whatever instrument was in the room.

Each piece is a Python script that writes the file. There is no MIDI library and
no editor project; the score sits in the source as literal data, and running the
script reproduces the file in `output/` byte for byte.

## Layout

```
music/   the pieces        music/output/*.mid
sfx/     the cues          sfx/output/*.mid
```

The pieces loop and are meant to play under something else. A cue lasts about
half a second, plays once, and is meant to be heard on its own, so it gets its
own directory.

```
python music/arr_canon.py           # -> music/output/canon_arr.mid
python sfx/arr_success.py           # -> sfx/output/success_arr.mid
python music/arr_canon.py out.mid   # -> out.mid
```

Output lands beside the script, so it does not matter which directory the
command runs from.

## The pieces

Voices is the measured peak, so it is the voice budget a device needs to play
the file whole.

**Canon in D** — `music/arr_canon.py` · 4 voices · 2:09 · 4/4 at 63 bpm
Pachelbel's ground bass and the lines that accumulate over it. The tune is a
single unbroken line on channel 0, so a one-voice buzzer can play this one
complete by taking that channel on its own and ignoring the rest.

**Le Souvenir avec le crépuscule** — `music/arr_crepuscule.py` · 7 voices ·
1:22 · 3/4 at 162 bpm
The densest of the set, and out of reach of anything with six voices or fewer.

**Für Elise** — `music/arr_elise.py` · 4 voices · 2:36 · 3/8 at 70 bpm
The whole rondo, both episodes included.

**Gadameiren** — `music/arr_gadameiren.py` · 6 voices · 2:32 · 4/4 at 81 bpm
A rock tune, with the bass line taken down into the bottom octave.

**Greensleeves** — `music/arr_greensleeves.py` · 5 voices · 2:57 · 4/4 at 79 bpm
The Clayderman setting, arpeggios and all. The longest here.

**Septette for the Dead Princess** — `music/arr_septette.py` · 6 voices · 2:19 ·
4/4 at 135 bpm
1815 notes over 83 bars, and 27 tempo steps. The busiest file in the set.

**Snezhnograd Nights** — `music/arr_snezhnograd.py` · 5 voices · 1:57 · 2/4 at
66 bpm
Slow, and the only piece in 2/4.

**Tico-Tico no Fubá** — `music/arr_ticotico.py` · 4 voices · 1:28 · 2/2 at
190 bpm
The fastest of them, at a choro tempo.

**Success chime** — `sfx/arr_success.py` · 3 voices · 0.5 s
Five notes, three tones, over in under half a second.

## Checking

`midi_check.py` reports what is wrong with a file. Two kinds of finding:

- **Hard** — the device cannot do it, so the file is wrong until it changes.
  Polyphony over the voice budget, notes shorter than the target can
  articulate, and one channel striking a pitch it is already holding.
- **Soft** — it will play, and whether it should is a judgement. Clashing
  intervals held long enough to be heard as one sound, spacing that growls
  low down, reaches and restrikes no hand could manage, and how far the
  onsets sit off the grid.

`midi_stats.py` only counts and measures.

```
python midi_check.py music/output/canon_arr.mid
python midi_check.py music/output/canon_arr.mid voices=6 minms=60
python midi_stats.py music/output/canon_arr.mid
```

`voices=` sets the budget and `minms=` the shortest note the target can
articulate. They default to 9 and 40 ms, which is an OPL2.

## Provenance

These are arrangements rather than faithful transcriptions, and what may be done
with one depends on what it was made from, so each source is named.

Three are out of copyright. One is arranged under guidelines its rightsholder
publishes. Four are arranged from work that is still held, and the chime comes
from another project.

| Piece | After | Underlying work |
|---|---|---|
| Canon in D | Pachelbel | public domain (d. 1706) |
| Für Elise | Mutopia's engraving | public domain (Beethoven, d. 1827) |
| Tico-Tico no Fubá | a four-part engraving | public domain in life+70 (Zequinha de Abreu, d. 1935) |
| Septette for the Dead Princess | ZUN's own General MIDI rendition | see below |
| Greensleeves | Richard Clayderman's arrangement | tune traditional; that arrangement is not |
| Snezhnograd Nights | a transcription of Liao Changyong's *Moscow Nights* | held (Solovyov-Sedoi / Matusovsky, 1955) |
| Le Souvenir avec le crépuscule | a transcription of the HOYO-MiX cue | held |
| Gadameiren | a transcription of the rock band's recording | held |
| Success chime | DeepSeek Reasonix's completion chime | three tones, from that project |

### Septette for the Dead Princess

原曲「亡き王女の為のセプテット」— composed by **ZUN**, from 東方紅魔郷 ~ the
Embodiment of Scarlet Devil (2002), where it is the stage six boss theme.
東方Project © 上海アリス幻樂団 (Team Shanghai Alice).

This arrangement is a derivative work — 東方Projectの二次創作 — made under the
derivative-work guidelines Team Shanghai Alice publishes, and it is neither
official nor endorsed. Rights in the original stay with 上海アリス幻樂団, and the
licence below covers only the arrangement. Official site:
<https://www16.big.or.jp/~zun/>

## Licence

- `midi_check.py` and `midi_stats.py` are **MIT**. See `LICENSE-TOOLS`.
- Everything under `music/` and `sfx/` is **CC BY 4.0**. See `LICENSE-MUSIC`.
  Attribute to Lunzima. This covers the `arr_*.py` as well as the `.mid`, since
  the score is held in those files as literal data.

There is no file called `LICENSE`. GitHub derives one repository badge from that
name, and this repository has two licences. With the files named as they are the
badge reads CC BY 4.0, which is right for every arrangement and every `.mid`;
the two check tools are the exception.

Neither licence reaches past the arrangement itself. Rights in the underlying
works stay with their composers and publishers, and only three of the nine are
made from work that has fallen out of copyright.
