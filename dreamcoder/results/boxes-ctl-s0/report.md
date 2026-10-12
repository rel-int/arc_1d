# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 901 (50 per family, drawn with seed 0), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/boxes-ctl-s0/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 835/901 (93%) | 857/901 | 894/901 | 46.3 | 10 | 150 | 1617s |
| 1 | 839/901 (93%) | 866/901 | 885/901 | 45.8 | 10 | 150 | 2010s |
| 2 | 844/901 (94%) | 863/901 | 884/901 | 44.9 | 10 | 150 | 2013s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 48/50 | 48/50 | 47/50 |
| denoising_mc | 43/50 | 48/50 | 47/50 |
| fill | 45/50 | 49/50 | 47/50 |
| flip | 50/50 | 50/50 | 50/50 |
| hollow | 49/50 | 49/50 | 50/50 |
| mirror | 50/50 | 50/50 | 50/50 |
| move_1p | 50/50 | 49/50 | 49/50 |
| move_2p | 50/50 | 50/50 | 50/50 |
| move_2p_dp | 50/50 | 50/50 | 50/50 |
| move_3p | 50/50 | 50/50 | 50/50 |
| move_dp | 50/50 | 49/50 | 50/50 |
| padded_fill | 48/50 | 47/50 | 48/50 |
| pcopy_1c | 21/50 | 16/50 | 20/50 |
| pcopy_mc | 42/50 | 44/50 | 45/50 |
| recolor_cmp | 50/50 | 50/50 | 49/50 |
| recolor_cnt | 50/50 | 50/50 | 50/50 |
| recolor_oe | 43/50 | 41/50 | 43/50 |
| scale_dp | 46/51 | 49/51 | 49/51 |

## Library growth

- no fragment had support in two tasks

## Examples from the last iteration

### Solved: `1d_denoising_1c_49`

`paint(slide(shift(x)), local(x))`, DL 29.5 = 13.0 structure + 14.4 parameters + 2.1 data bits, fits its training pairs exactly.

![1d_denoising_1c_49](figures/1d_denoising_1c_49.png)

| pair | input | output |
|---|---|---|
| train 0 | `.4444444444444....4..............` | `.4444444444444...................` |
| train 1 | `...2....2222222222222...2...2..2.` | `........2222222222222............` |
| train 2 | `....5......55555555555555..5...5.` | `...........55555555555555........` |
| **test** | `..5..5...5.......555555555555....` | `.................555555555555....` |
| predicted | | `.................555555555555....` |

### Solved: `1d_move_2p_dp_12`

`slide(x)`, DL 5.8 = 5.8 structure + 0.0 parameters + 0.0 data bits, fits its training pairs exactly.

![1d_move_2p_dp_12](figures/1d_move_2p_dp_12.png)

| pair | input | output |
|---|---|---|
| train 0 | `..33333333333333..2......` | `....333333333333332......` |
| train 1 | `..555555555555555..2.....` | `....5555555555555552.....` |
| train 2 | `.11111111111111..2.......` | `...111111111111112.......` |
| **test** | `.....8888888888888888..2.` | `.......88888888888888882.` |
| predicted | | `.......88888888888888882.` |

### Solved: `1d_recolor_oe_35`

`paint(paint(x, segment(x)), local(shift(x)))`, DL 62.5 = 12.8 structure + 49.4 parameters + 0.3 data bits, fits its training pairs exactly.

![1d_recolor_oe_35](figures/1d_recolor_oe_35.png)

| pair | input | output |
|---|---|---|
| train 0 | `...4444..4.44444..4444...4.......` | `...8888..1.11111..8888...1.......` |
| train 1 | `..44444.44..44444.4.444..........` | `..11111.88..11111.1.111..........` |
| train 2 | `...444444...444..44444...444.....` | `...888888...111..11111...111.....` |
| **test** | `...44444.44...44444...44..4444...` | `...11111.88...11111...88..8888...` |
| predicted | | `...11111.88...11111...88..8888...` |

### Failed: `1d_fill_44`

`shift(x)`, DL 59.0 = 4.2 structure + 40.5 parameters + 14.4 data bits, does not fit its training pairs exactly.

![1d_fill_44](figures/1d_fill_44.png)

| pair | input | output |
|---|---|---|
| train 0 | `.2..2.....` | `.2222.....` |
| train 1 | `4.4.......` | `444.......` |
| train 2 | `......7.7.` | `......777.` |
| **test** | `....3..3..` | `....3333..` |
| predicted | | `....3..3..` |

### Failed: `1d_pcopy_1c_16`

`paint(reverse(x), local(x))`, DL 85.8 = 9.8 structure + 73.4 parameters + 2.6 data bits, fits its training pairs exactly.

![1d_pcopy_1c_16](figures/1d_pcopy_1c_16.png)

| pair | input | output |
|---|---|---|
| train 0 | `..999...9.......................` | `..999..999......................` |
| train 1 | `.222...2...2....................` | `.222..222.222...................` |
| train 2 | `..888....8.....8...8............` | `..888...888...888.888...........` |
| **test** | `..999..9...9....9...............` | `..999.999.999..999..............` |
| predicted | | `..999..99.999..999..............` |

### Failed: `1d_scale_dp_13`

`paint(x, local(paint(x, scan(x))))`, DL 62.9 = 9.6 structure + 52.2 parameters + 1.0 data bits, fits its training pairs exactly.

![1d_scale_dp_13](figures/1d_scale_dp_13.png)

| pair | input | output |
|---|---|---|
| train 0 | `..777777777...9.....` | `..7777777777779.....` |
| train 1 | `.........4444444..9.` | `.........4444444449.` |
| train 2 | `4444444444444444..9.` | `4444444444444444449.` |
| **test** | `..44444444444.....9.` | `..44444444444444449.` |
| predicted | | `..4444444444444...9.` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_0 | `paint(x, local(paint(x, scan(x))))` | 50.0 | ✓ |
| 1d_denoising_1c_1 | `slide(paint(x, local(x)))` | 44.3 | ✓ |
| 1d_denoising_1c_10 | `paint(shift(paint(x, segment(x))), local(x))` | 54.0 | ✓ |
| 1d_denoising_1c_11 | `paint(x, segment(paint(x, segment(x))))` | 47.2 | ✓ |
| 1d_denoising_1c_12 | `slide(paint(x, local(x)))` | 41.0 | ✓ |
| 1d_denoising_1c_13 | `paint(paint(x, scan(x)), local(x))` | 55.6 | ✓ |
| 1d_denoising_1c_14 | `paint(x, local(paint(x, scan(x))))` | 46.5 | ✗ |
| 1d_denoising_1c_15 | `paint(paint(x, scan(x)), local(x))` | 51.3 | ✓ |
| 1d_denoising_1c_16 | `paint(paint(x, scan(x)), segment(x))` | 37.4 | ✓ |
| 1d_denoising_1c_17 | `paint(paint(x, scan(x)), segment(x))` | 37.9 | ✓ |
| 1d_denoising_1c_18 | `paint(shift(x), local(reverse(x)))` | 52.7 | ✗ |
| 1d_denoising_1c_19 | `paint(slide(shift(x)), local(x))` | 35.7 | ✓ |
| 1d_denoising_1c_2 | `paint(paint(x, scan(x)), segment(x))` | 38.0 | ✓ |
| 1d_denoising_1c_20 | `paint(paint(x, scan(x)), segment(x))` | 39.6 | ✓ |
| 1d_denoising_1c_21 | `slide(paint(x, local(x)))` | 47.8 | ✓ |
| 1d_denoising_1c_22 | `paint(paint(shift(x), scan(x)), local(x))` | 24.5 | ✓ |
| 1d_denoising_1c_23 | `paint(x, segment(paint(x, segment(x))))` | 41.9 | ✓ |
| 1d_denoising_1c_24 | `paint(paint(x, local(x)), scan(x))` | 52.0 | ✓ |
| 1d_denoising_1c_25 | `paint(paint(shift(x), scan(x)), local(x))` | 30.7 | ✓ |
| 1d_denoising_1c_26 | `paint(paint(x, scan(x)), local(x))` | 57.6 | ✗ |
| 1d_denoising_1c_27 | `paint(slide(shift(x)), local(x))` | 39.8 | ✓ |
| 1d_denoising_1c_28 | `paint(slide(shift(x)), local(x))` | 42.6 | ✓ |
| 1d_denoising_1c_29 | `pivot(paint(x, segment(x)))` | 31.9 | ✓ |
| 1d_denoising_1c_3 | `paint(paint(shift(x), local(x)), scan(x))` | 45.4 | ✓ |
| 1d_denoising_1c_30 | `paint(paint(shift(x), scan(x)), local(x))` | 49.7 | ✓ |
| 1d_denoising_1c_31 | `paint(paint(x, local(x)), local(shift(x)))` | 42.4 | ✓ |
| 1d_denoising_1c_32 | `slide(paint(x, local(x)))` | 42.4 | ✓ |
| 1d_denoising_1c_33 | `paint(paint(x, scan(x)), segment(x))` | 33.9 | ✓ |
| 1d_denoising_1c_34 | `slide(paint(x, local(x)))` | 41.3 | ✓ |
| 1d_denoising_1c_35 | `paint(paint(x, local(x)), segment(shift(x)))` | 44.5 | ✓ |
| 1d_denoising_1c_36 | `paint(reverse(shift(x)), local(x))` | 46.2 | ✓ |
| 1d_denoising_1c_37 | `paint(x, local(paint(x, segment(x))))` | 55.9 | ✓ |
| 1d_denoising_1c_38 | `paint(paint(x, scan(x)), segment(x))` | 38.0 | ✓ |
| 1d_denoising_1c_39 | `paint(x, segment(paint(x, segment(x))))` | 44.9 | ✓ |
| 1d_denoising_1c_4 | `slide(paint(x, local(x)))` | 46.8 | ✓ |
| 1d_denoising_1c_40 | `paint(x, segment(paint(x, segment(x))))` | 42.1 | ✓ |
| 1d_denoising_1c_41 | `paint(paint(shift(x), scan(x)), local(x))` | 42.2 | ✓ |
| 1d_denoising_1c_42 | `paint(shift(x), local(x))` | 49.5 | ✓ |
| 1d_denoising_1c_43 | `paint(paint(x, scan(x)), segment(x))` | 45.1 | ✓ |
| 1d_denoising_1c_44 | `paint(shift(x), local(x))` | 44.5 | ✓ |
| 1d_denoising_1c_45 | `slide(paint(x, local(x)))` | 47.5 | ✓ |
| 1d_denoising_1c_46 | `paint(paint(x, scan(x)), segment(x))` | 37.8 | ✓ |
| 1d_denoising_1c_47 | `paint(paint(x, scan(x)), segment(x))` | 37.9 | ✓ |
| 1d_denoising_1c_48 | `paint(paint(x, local(x)), local(x))` | 49.8 | ✓ |
| 1d_denoising_1c_49 | `paint(slide(shift(x)), local(x))` | 29.5 | ✓ |
| 1d_denoising_1c_5 | `paint(slide(shift(x)), local(x))` | 37.8 | ✓ |
| 1d_denoising_1c_6 | `paint(paint(shift(x), local(x)), local(x))` | 49.5 | ✓ |
| 1d_denoising_1c_7 | `paint(paint(x, scan(x)), segment(x))` | 54.3 | ✓ |
| 1d_denoising_1c_8 | `paint(paint(x, scan(x)), local(x))` | 50.9 | ✓ |
| 1d_denoising_1c_9 | `paint(paint(x, local(x)), local(shift(x)))` | 49.2 | ✓ |
| 1d_denoising_mc_0 | `paint(slide(shift(x)), local(x))` | 23.2 | ✓ |
| 1d_denoising_mc_1 | `paint(paint(shift(x), segment(x)), local(x))` | 41.2 | ✓ |
| 1d_denoising_mc_10 | `paint(paint(shift(x), segment(x)), local(x))` | 27.0 | ✗ |
| 1d_denoising_mc_11 | `paint(shift(slide(x)), local(x))` | 35.0 | ✓ |
| 1d_denoising_mc_12 | `paint(shift(x), local(reverse(x)))` | 42.7 | ✓ |
| 1d_denoising_mc_13 | `paint(paint(shift(x), segment(x)), local(x))` | 58.2 | ✓ |
| 1d_denoising_mc_14 | `paint(paint(shift(x), local(x)), segment(x))` | 25.9 | ✗ |
| 1d_denoising_mc_15 | `paint(reverse(shift(x)), local(x))` | 33.5 | ✓ |
| 1d_denoising_mc_16 | `paint(paint(shift(x), local(x)), local(x))` | 32.8 | ✓ |
| 1d_denoising_mc_17 | `paint(paint(shift(x), local(x)), scan(x))` | 17.8 | ✓ |
| 1d_denoising_mc_18 | `paint(paint(shift(x), local(x)), segment(x))` | 33.5 | ✓ |
| 1d_denoising_mc_19 | `paint(paint(shift(x), local(x)), scan(x))` | 30.2 | ✓ |
| 1d_denoising_mc_2 | `paint(paint(shift(x), local(x)), segment(x))` | 30.5 | ✓ |
| 1d_denoising_mc_20 | `paint(shift(paint(x, local(x))), local(x))` | 48.9 | ✓ |
| 1d_denoising_mc_21 | `paint(slide(shift(x)), local(x))` | 27.8 | ✓ |
| 1d_denoising_mc_22 | `paint(reverse(shift(x)), local(x))` | 52.6 | ✓ |
| 1d_denoising_mc_23 | `paint(paint(shift(x), local(x)), segment(x))` | 34.1 | ✓ |
| 1d_denoising_mc_24 | `paint(shift(x), local(x))` | 45.6 | ✓ |
| 1d_denoising_mc_25 | `paint(paint(shift(x), local(x)), scan(x))` | 21.9 | ✓ |
| 1d_denoising_mc_26 | `paint(shift(x), scan(x))` | 39.5 | ✓ |
| 1d_denoising_mc_27 | `paint(reverse(shift(x)), local(x))` | 42.3 | ✓ |
| 1d_denoising_mc_28 | `paint(reverse(shift(x)), local(x))` | 32.3 | ✓ |
| 1d_denoising_mc_29 | `paint(reverse(shift(x)), local(x))` | 26.2 | ✓ |
| 1d_denoising_mc_3 | `paint(paint(shift(x), local(x)), local(x))` | 24.8 | ✓ |
| 1d_denoising_mc_30 | `paint(paint(shift(x), local(x)), segment(x))` | 38.1 | ✓ |
| 1d_denoising_mc_31 | `paint(paint(shift(x), local(x)), scan(x))` | 38.7 | ✓ |
| 1d_denoising_mc_32 | `paint(paint(shift(x), local(x)), scan(x))` | 26.5 | ✓ |
| 1d_denoising_mc_33 | `paint(reverse(shift(x)), local(x))` | 35.0 | ✓ |
| 1d_denoising_mc_34 | `paint(shift(x), local(reverse(x)))` | 46.1 | ✓ |
| 1d_denoising_mc_35 | `paint(shift(x), local(reverse(x)))` | 49.3 | ✓ |
| 1d_denoising_mc_36 | `paint(slide(shift(x)), local(x))` | 42.4 | ✓ |
| 1d_denoising_mc_37 | `paint(shift(x), local(reverse(x)))` | 32.4 | ✓ |
| 1d_denoising_mc_38 | `paint(slide(shift(x)), local(x))` | 43.2 | ✓ |
| 1d_denoising_mc_39 | `paint(paint(shift(x), local(x)), local(x))` | 41.2 | ✓ |
| 1d_denoising_mc_4 | `paint(paint(shift(x), local(x)), scan(x))` | 26.7 | ✗ |
| 1d_denoising_mc_40 | `paint(paint(shift(x), local(x)), scan(x))` | 17.4 | ✓ |
| 1d_denoising_mc_41 | `paint(shift(slide(x)), local(x))` | 33.8 | ✓ |
| 1d_denoising_mc_42 | `paint(reverse(shift(x)), local(x))` | 24.2 | ✓ |
| 1d_denoising_mc_43 | `paint(paint(shift(x), local(x)), scan(x))` | 31.1 | ✓ |
| 1d_denoising_mc_44 | `paint(paint(x, local(x)), local(shift(x)))` | 35.0 | ✓ |
| 1d_denoising_mc_45 | `paint(paint(shift(x), segment(x)), local(x))` | 46.8 | ✓ |
| 1d_denoising_mc_46 | `paint(paint(shift(x), local(x)), local(x))` | 32.8 | ✓ |
| 1d_denoising_mc_47 | `paint(shift(x), local(reverse(x)))` | 36.8 | ✓ |
| 1d_denoising_mc_48 | `paint(shift(reverse(x)), local(x))` | 34.9 | ✓ |
| 1d_denoising_mc_49 | `paint(paint(shift(x), local(x)), segment(x))` | 28.1 | ✓ |
| 1d_denoising_mc_5 | `paint(paint(shift(x), local(x)), local(x))` | 16.9 | ✓ |
| 1d_denoising_mc_6 | `paint(reverse(shift(x)), local(x))` | 42.8 | ✓ |
| 1d_denoising_mc_7 | `paint(paint(shift(x), local(x)), segment(x))` | 30.4 | ✓ |
| 1d_denoising_mc_8 | `paint(shift(slide(x)), local(x))` | 51.3 | ✓ |
| 1d_denoising_mc_9 | `paint(paint(shift(x), local(x)), segment(x))` | 29.6 | ✓ |
| 1d_fill_0 | `paint(paint(x, scan(x)), local(shift(x)))` | 61.5 | ✓ |
| 1d_fill_1 | `paint(x, scan(paint(x, scan(x))))` | 79.1 | ✓ |
| 1d_fill_10 | `paint(x, local(paint(x, scan(x))))` | 81.7 | ✓ |
| 1d_fill_11 | `paint(paint(shift(x), scan(x)), local(x))` | 54.0 | ✓ |
| 1d_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 41.6 | ✓ |
| 1d_fill_13 | `paint(x, scan(paint(x, local(x))))` | 71.7 | ✓ |
| 1d_fill_14 | `paint(paint(x, scan(x)), local(x))` | 49.1 | ✓ |
| 1d_fill_15 | `paint(x, scan(paint(x, segment(x))))` | 81.3 | ✓ |
| 1d_fill_16 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.1 | ✓ |
| 1d_fill_17 | `paint(paint(x, scan(x)), local(shift(x)))` | 40.8 | ✓ |
| 1d_fill_18 | `paint(paint(x, scan(x)), local(x))` | 35.5 | ✓ |
| 1d_fill_19 | `paint(paint(x, scan(x)), local(x))` | 48.9 | ✓ |
| 1d_fill_2 | `paint(paint(shift(x), scan(x)), local(x))` | 77.5 | ✓ |
| 1d_fill_20 | `paint(paint(shift(x), scan(x)), local(x))` | 42.5 | ✓ |
| 1d_fill_21 | `paint(x, scan(shift(paint(x, local(x)))))` | 62.9 | ✗ |
| 1d_fill_22 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.5 | ✓ |
| 1d_fill_23 | `paint(paint(x, scan(x)), segment(x))` | 61.5 | ✓ |
| 1d_fill_24 | `slide(paint(x, scan(x)))` | 61.8 | ✓ |
| 1d_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 51.5 | ✓ |
| 1d_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 38.7 | ✓ |
| 1d_fill_27 | `paint(paint(shift(x), scan(x)), local(x))` | 50.2 | ✓ |
| 1d_fill_28 | `slide(paint(x, scan(x)))` | 29.7 | ✓ |
| 1d_fill_29 | `paint(x, local(paint(x, scan(x))))` | 69.1 | ✓ |
| 1d_fill_3 | `paint(paint(x, scan(x)), local(x))` | 41.3 | ✓ |
| 1d_fill_30 | `paint(paint(x, scan(x)), local(x))` | 34.7 | ✓ |
| 1d_fill_31 | `paint(paint(shift(x), scan(x)), local(x))` | 75.1 | ✓ |
| 1d_fill_32 | `paint(paint(x, scan(x)), local(x))` | 44.6 | ✓ |
| 1d_fill_33 | `paint(paint(x, scan(x)), segment(x))` | 47.4 | ✓ |
| 1d_fill_34 | `paint(paint(x, scan(x)), local(x))` | 30.2 | ✓ |
| 1d_fill_35 | `paint(x, scan(paint(x, segment(x))))` | 65.3 | ✓ |
| 1d_fill_36 | `paint(x, scan(paint(x, local(x))))` | 57.6 | ✓ |
| 1d_fill_37 | `shift(x)` | 63.3 | ✗ |
| 1d_fill_38 | `paint(paint(x, scan(x)), segment(x))` | 49.5 | ✓ |
| 1d_fill_39 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.5 | ✓ |
| 1d_fill_4 | `paint(paint(x, scan(x)), local(shift(x)))` | 45.8 | ✓ |
| 1d_fill_40 | `paint(paint(x, scan(x)), local(x))` | 43.2 | ✓ |
| 1d_fill_41 | `paint(paint(x, scan(x)), local(x))` | 53.6 | ✓ |
| 1d_fill_42 | `slide(paint(x, scan(x)))` | 66.5 | ✓ |
| 1d_fill_43 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.7 | ✓ |
| 1d_fill_44 | `shift(x)` | 59.0 | ✗ |
| 1d_fill_45 | `paint(x, local(paint(x, scan(x))))` | 75.1 | ✓ |
| 1d_fill_46 | `paint(paint(x, scan(x)), local(shift(x)))` | 37.4 | ✓ |
| 1d_fill_47 | `paint(x, scan(paint(x, scan(x))))` | 48.0 | ✓ |
| 1d_fill_48 | `slide(paint(x, scan(x)))` | 73.6 | ✓ |
| 1d_fill_49 | `paint(shift(shift(x)), scan(x))` | 47.8 | ✓ |
| 1d_fill_5 | `paint(paint(shift(x), scan(x)), local(x))` | 77.5 | ✓ |
| 1d_fill_6 | `paint(paint(x, scan(x)), segment(x))` | 56.1 | ✓ |
| 1d_fill_7 | `paint(paint(x, scan(x)), local(x))` | 28.7 | ✓ |
| 1d_fill_8 | `paint(paint(x, scan(x)), local(shift(x)))` | 49.1 | ✓ |
| 1d_fill_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.1 | ✓ |
| 1d_flip_0 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_1 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_10 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_11 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_12 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_13 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_14 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_15 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_16 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_17 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_18 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_19 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_2 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_20 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_21 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_22 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_23 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_24 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_25 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_26 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_27 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_28 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_29 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_3 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_30 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_31 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_32 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_33 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_34 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_35 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_36 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_37 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_38 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_39 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_4 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_40 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_41 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_42 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_43 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_44 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_45 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_46 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_47 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_48 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_49 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_5 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_6 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_7 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_8 | `reverse(x)` | 5.7 | ✓ |
| 1d_flip_9 | `reverse(x)` | 5.7 | ✓ |
| 1d_hollow_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 42.5 | ✓ |
| 1d_hollow_1 | `paint(paint(x, local(x)), segment(x))` | 43.9 | ✓ |
| 1d_hollow_10 | `paint(paint(shift(x), segment(x)), local(x))` | 63.1 | ✓ |
| 1d_hollow_11 | `paint(paint(x, local(x)), segment(shift(x)))` | 37.5 | ✓ |
| 1d_hollow_12 | `paint(paint(x, segment(x)), local(x))` | 63.1 | ✓ |
| 1d_hollow_13 | `paint(paint(x, scan(x)), segment(x))` | 41.6 | ✓ |
| 1d_hollow_14 | `paint(paint(x, segment(x)), local(x))` | 40.1 | ✓ |
| 1d_hollow_15 | `paint(pivot(x), local(x))` | 67.0 | ✓ |
| 1d_hollow_16 | `paint(paint(x, local(x)), segment(shift(x)))` | 54.4 | ✓ |
| 1d_hollow_17 | `paint(paint(shift(x), scan(x)), local(x))` | 36.7 | ✓ |
| 1d_hollow_18 | `paint(paint(x, local(x)), segment(shift(x)))` | 50.3 | ✓ |
| 1d_hollow_19 | `paint(paint(x, segment(x)), local(shift(x)))` | 60.5 | ✓ |
| 1d_hollow_2 | `paint(paint(x, segment(x)), scan(x))` | 56.9 | ✓ |
| 1d_hollow_20 | `paint(paint(x, local(x)), local(x))` | 53.5 | ✓ |
| 1d_hollow_21 | `paint(paint(x, scan(x)), scan(x))` | 44.5 | ✓ |
| 1d_hollow_22 | `paint(slide(x), scan(x))` | 77.2 | ✓ |
| 1d_hollow_23 | `paint(x, scan(pivot(x)))` | 76.5 | ✓ |
| 1d_hollow_24 | `paint(paint(x, local(x)), segment(x))` | 74.2 | ✓ |
| 1d_hollow_25 | `paint(paint(x, local(x)), segment(shift(x)))` | 48.9 | ✓ |
| 1d_hollow_26 | `paint(paint(x, local(x)), segment(shift(x)))` | 50.3 | ✓ |
| 1d_hollow_27 | `paint(x, scan(shift(x)))` | 59.1 | ✓ |
| 1d_hollow_28 | `paint(paint(x, local(x)), scan(shift(x)))` | 58.3 | ✓ |
| 1d_hollow_29 | `paint(paint(x, scan(x)), segment(x))` | 48.1 | ✓ |
| 1d_hollow_3 | `paint(paint(x, local(x)), scan(x))` | 46.0 | ✓ |
| 1d_hollow_30 | `paint(paint(x, scan(x)), local(shift(x)))` | 57.5 | ✓ |
| 1d_hollow_31 | `paint(paint(x, segment(x)), segment(x))` | 54.5 | ✓ |
| 1d_hollow_32 | `paint(x, local(pivot(x)))` | 73.0 | ✓ |
| 1d_hollow_33 | `paint(paint(x, local(x)), segment(shift(x)))` | 40.4 | ✓ |
| 1d_hollow_34 | `paint(paint(shift(x), scan(x)), local(x))` | 46.3 | ✓ |
| 1d_hollow_35 | `paint(paint(x, local(x)), segment(shift(x)))` | 47.7 | ✓ |
| 1d_hollow_36 | `paint(paint(x, local(x)), scan(x))` | 68.1 | ✓ |
| 1d_hollow_37 | `paint(paint(x, segment(x)), local(x))` | 50.7 | ✓ |
| 1d_hollow_38 | `paint(paint(x, local(x)), segment(shift(x)))` | 53.3 | ✓ |
| 1d_hollow_39 | `paint(paint(x, local(x)), segment(shift(x)))` | 57.5 | ✓ |
| 1d_hollow_4 | `paint(paint(x, segment(x)), local(x))` | 66.2 | ✓ |
| 1d_hollow_40 | `paint(paint(x, local(x)), segment(shift(x)))` | 41.2 | ✓ |
| 1d_hollow_41 | `paint(paint(x, segment(x)), local(x))` | 61.6 | ✓ |
| 1d_hollow_42 | `paint(paint(x, segment(shift(x))), local(x))` | 55.8 | ✓ |
| 1d_hollow_43 | `paint(paint(shift(x), local(x)), scan(x))` | 67.9 | ✓ |
| 1d_hollow_44 | `paint(paint(x, scan(x)), scan(x))` | 57.7 | ✓ |
| 1d_hollow_45 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.4 | ✓ |
| 1d_hollow_46 | `paint(paint(x, segment(x)), local(x))` | 65.5 | ✓ |
| 1d_hollow_47 | `paint(shift(x), segment(paint(x, local(x))))` | 65.0 | ✓ |
| 1d_hollow_48 | `paint(paint(shift(x), scan(x)), local(x))` | 45.3 | ✓ |
| 1d_hollow_49 | `paint(x, scan(x))` | 65.9 | ✓ |
| 1d_hollow_5 | `paint(paint(x, local(x)), segment(shift(x)))` | 46.0 | ✓ |
| 1d_hollow_6 | `paint(paint(x, local(x)), segment(shift(x)))` | 51.2 | ✓ |
| 1d_hollow_7 | `paint(paint(x, segment(x)), local(x))` | 71.0 | ✓ |
| 1d_hollow_8 | `paint(paint(x, segment(x)), local(x))` | 58.5 | ✓ |
| 1d_hollow_9 | `paint(paint(x, local(x)), segment(shift(x)))` | 29.7 | ✓ |
| 1d_mirror_0 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_1 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_10 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_11 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_12 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_13 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_14 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_15 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_16 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_17 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_18 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_19 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_2 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_20 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_21 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_22 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_23 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_24 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_25 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_26 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_27 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_28 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_29 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_3 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_30 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_31 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_32 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_33 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_34 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_35 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_36 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_37 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_38 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_39 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_4 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_40 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_41 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_42 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_43 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_44 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_45 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_46 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_47 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_48 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_49 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_5 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_6 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_7 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_8 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_9 | `pivot(x)` | 7.0 | ✓ |
| 1d_move_1p_0 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_1 | `paint(reverse(shift(x)), local(x))` | 41.2 | ✓ |
| 1d_move_1p_10 | `shift(x)` | 52.7 | ✓ |
| 1d_move_1p_11 | `shift(x)` | 52.7 | ✓ |
| 1d_move_1p_12 | `paint(reverse(shift(x)), local(x))` | 47.9 | ✓ |
| 1d_move_1p_13 | `paint(shift(x), local(reverse(x)))` | 52.5 | ✓ |
| 1d_move_1p_14 | `shift(x)` | 53.8 | ✓ |
| 1d_move_1p_15 | `paint(reverse(shift(x)), local(x))` | 50.9 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 53.3 | ✓ |
| 1d_move_1p_17 | `paint(reverse(shift(x)), local(x))` | 43.6 | ✓ |
| 1d_move_1p_18 | `paint(shift(x), local(x))` | 50.9 | ✗ |
| 1d_move_1p_19 | `shift(x)` | 54.9 | ✓ |
| 1d_move_1p_2 | `paint(shift(x), local(x))` | 47.9 | ✓ |
| 1d_move_1p_20 | `paint(shift(shift(x)), local(x))` | 50.9 | ✓ |
| 1d_move_1p_21 | `paint(paint(shift(x), segment(x)), local(x))` | 45.5 | ✓ |
| 1d_move_1p_22 | `paint(shift(x), local(x))` | 52.3 | ✓ |
| 1d_move_1p_23 | `paint(shift(x), local(x))` | 48.4 | ✓ |
| 1d_move_1p_24 | `shift(x)` | 52.1 | ✓ |
| 1d_move_1p_25 | `paint(shift(x), scan(x))` | 43.8 | ✓ |
| 1d_move_1p_26 | `paint(paint(shift(x), segment(x)), local(x))` | 38.0 | ✓ |
| 1d_move_1p_27 | `paint(reverse(shift(x)), local(x))` | 47.8 | ✓ |
| 1d_move_1p_28 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_29 | `paint(shift(x), local(x))` | 54.3 | ✓ |
| 1d_move_1p_3 | `paint(shift(x), local(reverse(x)))` | 47.1 | ✓ |
| 1d_move_1p_30 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_31 | `paint(shift(x), local(x))` | 49.6 | ✓ |
| 1d_move_1p_32 | `paint(shift(x), scan(x))` | 54.4 | ✓ |
| 1d_move_1p_33 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_34 | `shift(x)` | 54.0 | ✓ |
| 1d_move_1p_35 | `shift(x)` | 52.3 | ✓ |
| 1d_move_1p_36 | `paint(shift(paint(x, segment(x))), local(x))` | 50.9 | ✓ |
| 1d_move_1p_37 | `paint(shift(x), local(x))` | 39.0 | ✓ |
| 1d_move_1p_38 | `shift(x)` | 54.9 | ✓ |
| 1d_move_1p_39 | `shift(x)` | 56.0 | ✓ |
| 1d_move_1p_4 | `paint(shift(x), local(x))` | 46.1 | ✓ |
| 1d_move_1p_40 | `paint(reverse(shift(x)), local(x))` | 46.8 | ✓ |
| 1d_move_1p_41 | `paint(shift(paint(x, local(x))), local(x))` | 48.4 | ✓ |
| 1d_move_1p_42 | `paint(reverse(shift(x)), local(x))` | 42.8 | ✓ |
| 1d_move_1p_43 | `paint(shift(paint(x, local(x))), local(x))` | 54.8 | ✓ |
| 1d_move_1p_44 | `paint(reverse(shift(x)), local(x))` | 50.4 | ✓ |
| 1d_move_1p_45 | `paint(paint(shift(x), segment(x)), local(x))` | 48.8 | ✓ |
| 1d_move_1p_46 | `paint(shift(x), local(x))` | 50.8 | ✓ |
| 1d_move_1p_47 | `paint(reverse(shift(x)), local(x))` | 47.3 | ✓ |
| 1d_move_1p_48 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_49 | `paint(paint(shift(x), segment(x)), local(x))` | 51.2 | ✓ |
| 1d_move_1p_5 | `shift(x)` | 51.2 | ✓ |
| 1d_move_1p_6 | `paint(paint(shift(x), segment(x)), local(x))` | 46.2 | ✓ |
| 1d_move_1p_7 | `paint(shift(x), local(paint(x, segment(x))))` | 50.6 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 55.0 | ✓ |
| 1d_move_1p_9 | `paint(paint(shift(x), segment(x)), local(x))` | 46.4 | ✓ |
| 1d_move_2p_0 | `paint(shift(paint(x, local(x))), local(x))` | 41.3 | ✓ |
| 1d_move_2p_1 | `shift(x)` | 46.3 | ✓ |
| 1d_move_2p_10 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_11 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_12 | `paint(reverse(shift(x)), local(x))` | 43.4 | ✓ |
| 1d_move_2p_13 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_14 | `shift(x)` | 47.4 | ✓ |
| 1d_move_2p_15 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_16 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_17 | `paint(shift(paint(x, local(x))), local(x))` | 47.7 | ✓ |
| 1d_move_2p_18 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_19 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_2 | `shift(x)` | 46.4 | ✓ |
| 1d_move_2p_20 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_21 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_22 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_23 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_24 | `shift(x)` | 45.9 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_26 | `paint(shift(x), local(reverse(x)))` | 44.6 | ✓ |
| 1d_move_2p_27 | `shift(x)` | 49.0 | ✓ |
| 1d_move_2p_28 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_29 | `shift(x)` | 48.6 | ✓ |
| 1d_move_2p_3 | `paint(shift(paint(x, local(x))), local(x))` | 41.0 | ✓ |
| 1d_move_2p_30 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_31 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_32 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_33 | `shift(x)` | 46.4 | ✓ |
| 1d_move_2p_34 | `shift(x)` | 47.6 | ✓ |
| 1d_move_2p_35 | `shift(x)` | 46.3 | ✓ |
| 1d_move_2p_36 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_37 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_38 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_39 | `shift(x)` | 48.8 | ✓ |
| 1d_move_2p_4 | `shift(x)` | 46.3 | ✓ |
| 1d_move_2p_40 | `shift(x)` | 48.7 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.4 | ✓ |
| 1d_move_2p_42 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_43 | `paint(paint(shift(x), local(x)), segment(x))` | 43.4 | ✓ |
| 1d_move_2p_44 | `shift(x)` | 54.1 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_46 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.3 | ✓ |
| 1d_move_2p_48 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_49 | `paint(paint(shift(x), segment(x)), local(x))` | 41.2 | ✓ |
| 1d_move_2p_5 | `shift(x)` | 45.1 | ✓ |
| 1d_move_2p_6 | `paint(paint(shift(x), local(x)), segment(x))` | 44.5 | ✓ |
| 1d_move_2p_7 | `shift(x)` | 53.2 | ✓ |
| 1d_move_2p_8 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_9 | `paint(paint(shift(x), local(x)), segment(x))` | 44.0 | ✓ |
| 1d_move_2p_dp_0 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_1 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_10 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_11 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_12 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_13 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_14 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_15 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_16 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_17 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_18 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_19 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_2 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_20 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_21 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_22 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_23 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_24 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_25 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_26 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_27 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_28 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_29 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_3 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_30 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_31 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_32 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_33 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_34 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_35 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_36 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_37 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_38 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_39 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_4 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_40 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_41 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_42 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_43 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_44 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_45 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_46 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_47 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_48 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_49 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_5 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_6 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_7 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_8 | `slide(x)` | 5.8 | ✓ |
| 1d_move_2p_dp_9 | `slide(x)` | 5.8 | ✓ |
| 1d_move_3p_0 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_1 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_10 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_11 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_12 | `paint(reverse(shift(x)), local(x))` | 50.9 | ✓ |
| 1d_move_3p_13 | `shift(x)` | 54.1 | ✓ |
| 1d_move_3p_14 | `paint(shift(x), local(x))` | 52.0 | ✓ |
| 1d_move_3p_15 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_16 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_17 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_18 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_19 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_2 | `paint(reverse(shift(x)), local(x))` | 45.3 | ✓ |
| 1d_move_3p_20 | `shift(x)` | 54.1 | ✓ |
| 1d_move_3p_21 | `paint(paint(shift(x), local(x)), scan(x))` | 42.7 | ✓ |
| 1d_move_3p_22 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_23 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.9 | ✓ |
| 1d_move_3p_24 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_25 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_26 | `paint(reverse(shift(x)), local(x))` | 53.5 | ✓ |
| 1d_move_3p_27 | `shift(x)` | 54.4 | ✓ |
| 1d_move_3p_28 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_29 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_3 | `paint(shift(x), local(x))` | 52.7 | ✓ |
| 1d_move_3p_30 | `shift(x)` | 52.6 | ✓ |
| 1d_move_3p_31 | `paint(paint(x, local(x)), segment(shift(x)))` | 46.7 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_35 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_36 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_37 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_38 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_39 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_4 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_40 | `paint(reverse(shift(x)), local(x))` | 51.2 | ✓ |
| 1d_move_3p_41 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_43 | `paint(paint(x, local(x)), scan(shift(x)))` | 49.7 | ✓ |
| 1d_move_3p_44 | `shift(x)` | 57.1 | ✓ |
| 1d_move_3p_45 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_46 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_47 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_48 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_49 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_5 | `shift(x)` | 54.3 | ✓ |
| 1d_move_3p_6 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_7 | `shift(x)` | 56.9 | ✓ |
| 1d_move_3p_8 | `shift(x)` | 52.6 | ✓ |
| 1d_move_3p_9 | `shift(x)` | 54.3 | ✓ |
| 1d_move_dp_0 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_1 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_10 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_11 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_12 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_13 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_14 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_15 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_16 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_17 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_18 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_19 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_2 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_20 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_21 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_22 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_23 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_24 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_25 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_26 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_27 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_28 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_29 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_3 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_30 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_31 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_32 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_33 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_34 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_35 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_36 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_37 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_38 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_39 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_4 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_40 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_41 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_42 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_43 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_44 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_45 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_46 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_47 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_48 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_49 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_5 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_6 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_7 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_8 | `slide(x)` | 5.8 | ✓ |
| 1d_move_dp_9 | `slide(x)` | 5.8 | ✓ |
| 1d_padded_fill_0 | `paint(paint(x, scan(x)), segment(x))` | 58.4 | ✓ |
| 1d_padded_fill_1 | `paint(paint(x, scan(x)), segment(x))` | 47.8 | ✓ |
| 1d_padded_fill_10 | `paint(paint(x, scan(x)), local(x))` | 44.6 | ✓ |
| 1d_padded_fill_11 | `paint(paint(x, scan(x)), segment(x))` | 48.8 | ✓ |
| 1d_padded_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 56.6 | ✓ |
| 1d_padded_fill_13 | `paint(paint(x, scan(x)), segment(x))` | 62.1 | ✓ |
| 1d_padded_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 40.3 | ✓ |
| 1d_padded_fill_15 | `paint(paint(x, scan(x)), local(x))` | 42.5 | ✓ |
| 1d_padded_fill_16 | `paint(paint(x, scan(x)), segment(x))` | 52.4 | ✓ |
| 1d_padded_fill_17 | `paint(paint(x, scan(x)), segment(x))` | 59.3 | ✓ |
| 1d_padded_fill_18 | `paint(paint(x, scan(x)), local(x))` | 47.6 | ✓ |
| 1d_padded_fill_19 | `reverse(paint(x, scan(x)))` | 58.7 | ✓ |
| 1d_padded_fill_2 | `paint(paint(shift(x), scan(x)), local(x))` | 56.5 | ✓ |
| 1d_padded_fill_20 | `paint(paint(x, scan(x)), segment(x))` | 53.6 | ✓ |
| 1d_padded_fill_21 | `reverse(paint(x, scan(x)))` | 57.0 | ✓ |
| 1d_padded_fill_22 | `paint(paint(x, local(x)), scan(x))` | 55.4 | ✓ |
| 1d_padded_fill_23 | `paint(paint(x, scan(x)), segment(x))` | 44.9 | ✓ |
| 1d_padded_fill_24 | `paint(paint(x, scan(x)), segment(x))` | 40.2 | ✓ |
| 1d_padded_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 47.2 | ✓ |
| 1d_padded_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 52.1 | ✓ |
| 1d_padded_fill_27 | `paint(x, scan(paint(x, scan(x))))` | 59.3 | ✓ |
| 1d_padded_fill_28 | `paint(paint(x, scan(x)), segment(x))` | 45.5 | ✓ |
| 1d_padded_fill_29 | `paint(paint(x, scan(x)), segment(x))` | 49.0 | ✓ |
| 1d_padded_fill_3 | `paint(paint(x, scan(x)), local(x))` | 54.0 | ✓ |
| 1d_padded_fill_30 | `paint(paint(x, scan(x)), local(shift(x)))` | 47.5 | ✓ |
| 1d_padded_fill_31 | `paint(paint(x, scan(x)), local(x))` | 54.7 | ✓ |
| 1d_padded_fill_32 | `paint(paint(x, scan(x)), local(shift(x)))` | 55.4 | ✓ |
| 1d_padded_fill_33 | `paint(x, scan(x))` | 62.8 | ✗ |
| 1d_padded_fill_34 | `paint(paint(x, scan(x)), local(shift(x)))` | 34.1 | ✓ |
| 1d_padded_fill_35 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.9 | ✓ |
| 1d_padded_fill_36 | `paint(x, scan(paint(x, scan(x))))` | 65.9 | ✓ |
| 1d_padded_fill_37 | `paint(paint(shift(x), scan(x)), local(x))` | 48.9 | ✓ |
| 1d_padded_fill_38 | `paint(paint(x, scan(x)), segment(x))` | 40.9 | ✓ |
| 1d_padded_fill_39 | `paint(paint(x, scan(x)), local(shift(x)))` | 45.4 | ✓ |
| 1d_padded_fill_4 | `paint(paint(x, scan(x)), local(x))` | 44.6 | ✓ |
| 1d_padded_fill_40 | `paint(paint(x, scan(x)), segment(x))` | 54.3 | ✓ |
| 1d_padded_fill_41 | `paint(paint(x, scan(x)), local(x))` | 41.7 | ✓ |
| 1d_padded_fill_42 | `paint(paint(x, local(x)), scan(x))` | 59.1 | ✓ |
| 1d_padded_fill_43 | `paint(paint(x, scan(x)), segment(x))` | 53.0 | ✓ |
| 1d_padded_fill_44 | `paint(paint(x, scan(x)), local(shift(x)))` | 52.8 | ✓ |
| 1d_padded_fill_45 | `paint(paint(x, scan(x)), segment(x))` | 53.2 | ✓ |
| 1d_padded_fill_46 | `paint(paint(x, local(x)), scan(x))` | 69.9 | ✓ |
| 1d_padded_fill_47 | `paint(paint(x, local(shift(x))), scan(x))` | 54.1 | ✗ |
| 1d_padded_fill_48 | `paint(paint(x, scan(x)), local(x))` | 35.5 | ✓ |
| 1d_padded_fill_49 | `paint(paint(x, scan(x)), segment(x))` | 49.1 | ✓ |
| 1d_padded_fill_5 | `paint(paint(x, scan(x)), segment(x))` | 46.1 | ✓ |
| 1d_padded_fill_6 | `paint(paint(x, scan(x)), local(x))` | 66.8 | ✓ |
| 1d_padded_fill_7 | `paint(paint(x, scan(x)), local(shift(x)))` | 28.8 | ✓ |
| 1d_padded_fill_8 | `paint(paint(x, scan(x)), segment(x))` | 51.3 | ✓ |
| 1d_padded_fill_9 | `paint(x, scan(paint(x, scan(x))))` | 51.3 | ✓ |
| 1d_pcopy_1c_0 | `paint(x, local(paint(x, local(x))))` | 81.1 | ✓ |
| 1d_pcopy_1c_1 | `shift(x)` | 80.4 | ✗ |
| 1d_pcopy_1c_10 | `paint(reverse(x), local(x))` | 66.6 | ✓ |
| 1d_pcopy_1c_11 | `paint(paint(x, scan(x)), scan(x))` | 68.4 | ✗ |
| 1d_pcopy_1c_12 | `paint(x, local(slide(x)))` | 66.1 | ✗ |
| 1d_pcopy_1c_13 | `shift(x)` | 80.9 | ✗ |
| 1d_pcopy_1c_14 | `paint(paint(x, scan(x)), scan(x))` | 68.7 | ✗ |
| 1d_pcopy_1c_15 | `paint(paint(x, local(x)), scan(shift(x)))` | 55.4 | ✗ |
| 1d_pcopy_1c_16 | `paint(reverse(x), local(x))` | 85.8 | ✗ |
| 1d_pcopy_1c_17 | `paint(x, scan(paint(x, segment(x))))` | 73.0 | ✗ |
| 1d_pcopy_1c_18 | `paint(paint(x, scan(x)), local(x))` | 67.8 | ✗ |
| 1d_pcopy_1c_19 | `paint(x, local(paint(x, scan(x))))` | 66.5 | ✗ |
| 1d_pcopy_1c_2 | `paint(paint(x, scan(x)), local(x))` | 57.2 | ✓ |
| 1d_pcopy_1c_20 | `paint(shift(x), local(reverse(x)))` | 83.7 | ✗ |
| 1d_pcopy_1c_21 | `paint(paint(x, segment(x)), local(x))` | 72.6 | ✓ |
| 1d_pcopy_1c_22 | `paint(reverse(shift(x)), local(x))` | 82.3 | ✓ |
| 1d_pcopy_1c_23 | `paint(paint(x, segment(x)), local(x))` | 70.8 | ✓ |
| 1d_pcopy_1c_24 | `paint(paint(x, local(shift(x))), scan(x))` | 81.6 | ✗ |
| 1d_pcopy_1c_25 | `paint(paint(x, scan(x)), local(x))` | 61.1 | ✓ |
| 1d_pcopy_1c_26 | `paint(paint(x, scan(x)), local(x))` | 64.0 | ✗ |
| 1d_pcopy_1c_27 | `reverse(paint(x, local(x)))` | 82.5 | ✓ |
| 1d_pcopy_1c_28 | `paint(reverse(x), local(x))` | 74.7 | ✓ |
| 1d_pcopy_1c_29 | `paint(reverse(x), local(x))` | 60.8 | ✓ |
| 1d_pcopy_1c_3 | `paint(reverse(x), local(x))` | 73.9 | ✓ |
| 1d_pcopy_1c_30 | `paint(shift(x), local(reverse(x)))` | 73.8 | ✓ |
| 1d_pcopy_1c_31 | `paint(paint(x, local(x)), scan(shift(x)))` | 61.9 | ✓ |
| 1d_pcopy_1c_32 | `paint(paint(x, local(shift(x))), scan(x))` | 76.0 | ✗ |
| 1d_pcopy_1c_33 | `paint(paint(x, local(x)), local(x))` | 85.8 | ✓ |
| 1d_pcopy_1c_34 | `paint(paint(x, scan(x)), scan(x))` | 74.3 | ✗ |
| 1d_pcopy_1c_35 | `paint(paint(x, segment(shift(x))), local(x))` | 62.3 | ✗ |
| 1d_pcopy_1c_36 | `paint(paint(x, segment(x)), local(x))` | 77.9 | ✓ |
| 1d_pcopy_1c_37 | `paint(reverse(shift(x)), local(x))` | 88.0 | ✗ |
| 1d_pcopy_1c_38 | `paint(paint(x, segment(x)), local(x))` | 81.4 | ✗ |
| 1d_pcopy_1c_39 | `paint(reverse(x), local(x))` | 76.9 | ✗ |
| 1d_pcopy_1c_4 | `paint(paint(x, segment(x)), local(x))` | 68.4 | ✗ |
| 1d_pcopy_1c_40 | `paint(x, local(paint(x, scan(x))))` | 78.3 | ✗ |
| 1d_pcopy_1c_41 | `paint(paint(x, local(x)), scan(shift(x)))` | 63.4 | ✗ |
| 1d_pcopy_1c_42 | `paint(paint(x, local(shift(x))), scan(x))` | 74.9 | ✗ |
| 1d_pcopy_1c_43 | `paint(paint(x, scan(x)), scan(x))` | 73.4 | ✗ |
| 1d_pcopy_1c_44 | `paint(paint(x, segment(x)), local(x))` | 82.1 | ✗ |
| 1d_pcopy_1c_45 | `paint(x, local(paint(x, scan(x))))` | 74.8 | ✓ |
| 1d_pcopy_1c_46 | `paint(paint(x, local(x)), scan(shift(x)))` | 64.4 | ✗ |
| 1d_pcopy_1c_47 | `paint(paint(x, scan(x)), local(x))` | 70.9 | ✗ |
| 1d_pcopy_1c_48 | `paint(x, local(paint(x, scan(x))))` | 66.0 | ✓ |
| 1d_pcopy_1c_49 | `paint(shift(x), local(reverse(x)))` | 88.6 | ✓ |
| 1d_pcopy_1c_5 | `paint(reverse(x), local(x))` | 54.0 | ✗ |
| 1d_pcopy_1c_6 | `paint(x, local(x))` | 90.8 | ✗ |
| 1d_pcopy_1c_7 | `paint(reverse(x), local(x))` | 64.9 | ✓ |
| 1d_pcopy_1c_8 | `paint(paint(x, segment(x)), local(x))` | 61.3 | ✓ |
| 1d_pcopy_1c_9 | `shift(x)` | 86.4 | ✗ |
| 1d_pcopy_mc_0 | `paint(paint(x, segment(shift(x))), local(x))` | 45.7 | ✓ |
| 1d_pcopy_mc_1 | `paint(paint(x, segment(x)), local(x))` | 47.8 | ✗ |
| 1d_pcopy_mc_10 | `paint(shift(shift(x)), local(x))` | 76.7 | ✓ |
| 1d_pcopy_mc_11 | `paint(paint(x, segment(x)), local(x))` | 48.0 | ✓ |
| 1d_pcopy_mc_12 | `paint(paint(x, scan(x)), local(x))` | 60.2 | ✓ |
| 1d_pcopy_mc_13 | `paint(paint(x, segment(x)), local(x))` | 65.5 | ✓ |
| 1d_pcopy_mc_14 | `paint(x, local(paint(x, segment(x))))` | 85.0 | ✓ |
| 1d_pcopy_mc_15 | `paint(shift(x), local(reverse(x)))` | 71.3 | ✓ |
| 1d_pcopy_mc_16 | `paint(paint(x, segment(shift(x))), local(x))` | 46.9 | ✓ |
| 1d_pcopy_mc_17 | `reverse(paint(x, local(x)))` | 75.8 | ✗ |
| 1d_pcopy_mc_18 | `paint(paint(x, segment(x)), local(x))` | 39.0 | ✗ |
| 1d_pcopy_mc_19 | `paint(paint(x, segment(x)), local(x))` | 46.7 | ✓ |
| 1d_pcopy_mc_2 | `paint(reverse(x), local(x))` | 55.2 | ✓ |
| 1d_pcopy_mc_20 | `paint(reverse(shift(x)), local(x))` | 76.3 | ✓ |
| 1d_pcopy_mc_21 | `paint(reverse(x), local(x))` | 47.7 | ✓ |
| 1d_pcopy_mc_22 | `paint(reverse(x), local(x))` | 47.2 | ✓ |
| 1d_pcopy_mc_23 | `paint(paint(x, segment(x)), local(x))` | 51.3 | ✓ |
| 1d_pcopy_mc_24 | `paint(shift(x), local(x))` | 90.0 | ✓ |
| 1d_pcopy_mc_25 | `paint(x, local(paint(x, segment(x))))` | 65.4 | ✓ |
| 1d_pcopy_mc_26 | `paint(paint(x, segment(shift(x))), local(x))` | 49.5 | ✓ |
| 1d_pcopy_mc_27 | `paint(paint(x, segment(x)), local(x))` | 66.1 | ✓ |
| 1d_pcopy_mc_28 | `paint(paint(x, segment(x)), local(x))` | 55.2 | ✓ |
| 1d_pcopy_mc_29 | `paint(x, local(paint(x, segment(shift(x)))))` | 57.3 | ✓ |
| 1d_pcopy_mc_3 | `paint(paint(x, segment(x)), local(x))` | 42.4 | ✓ |
| 1d_pcopy_mc_30 | `paint(x, local(reverse(x)))` | 66.1 | ✗ |
| 1d_pcopy_mc_31 | `paint(paint(x, scan(x)), local(x))` | 55.2 | ✓ |
| 1d_pcopy_mc_32 | `paint(x, local(paint(shift(x), segment(x))))` | 86.2 | ✓ |
| 1d_pcopy_mc_33 | `paint(paint(x, scan(x)), local(x))` | 77.7 | ✓ |
| 1d_pcopy_mc_34 | `paint(paint(x, segment(x)), local(x))` | 74.7 | ✓ |
| 1d_pcopy_mc_35 | `paint(paint(x, segment(shift(x))), local(x))` | 44.9 | ✓ |
| 1d_pcopy_mc_36 | `paint(paint(x, segment(x)), local(x))` | 61.0 | ✗ |
| 1d_pcopy_mc_37 | `paint(paint(x, scan(x)), local(x))` | 49.5 | ✓ |
| 1d_pcopy_mc_38 | `paint(paint(x, local(shift(x))), local(x))` | 47.0 | ✓ |
| 1d_pcopy_mc_39 | `paint(paint(x, segment(x)), local(x))` | 47.8 | ✓ |
| 1d_pcopy_mc_4 | `paint(paint(x, scan(x)), local(x))` | 59.7 | ✓ |
| 1d_pcopy_mc_40 | `paint(paint(x, segment(x)), local(x))` | 58.9 | ✓ |
| 1d_pcopy_mc_41 | `paint(paint(x, segment(x)), local(x))` | 46.9 | ✓ |
| 1d_pcopy_mc_42 | `paint(paint(x, segment(shift(x))), local(x))` | 54.1 | ✓ |
| 1d_pcopy_mc_43 | `paint(paint(x, segment(x)), local(x))` | 46.0 | ✓ |
| 1d_pcopy_mc_44 | `paint(paint(x, segment(shift(x))), local(x))` | 43.6 | ✓ |
| 1d_pcopy_mc_45 | `paint(paint(x, segment(shift(x))), local(x))` | 45.1 | ✓ |
| 1d_pcopy_mc_46 | `paint(paint(x, local(shift(x))), local(x))` | 54.0 | ✓ |
| 1d_pcopy_mc_47 | `paint(paint(x, scan(x)), local(x))` | 46.1 | ✓ |
| 1d_pcopy_mc_48 | `paint(paint(x, segment(x)), local(x))` | 49.6 | ✓ |
| 1d_pcopy_mc_49 | `paint(x, local(x))` | 66.5 | ✓ |
| 1d_pcopy_mc_5 | `paint(paint(x, segment(x)), local(x))` | 46.0 | ✓ |
| 1d_pcopy_mc_6 | `paint(paint(x, local(shift(x))), local(x))` | 68.5 | ✓ |
| 1d_pcopy_mc_7 | `paint(x, local(paint(x, segment(shift(x)))))` | 64.1 | ✓ |
| 1d_pcopy_mc_8 | `paint(paint(x, segment(x)), local(x))` | 47.3 | ✓ |
| 1d_pcopy_mc_9 | `paint(paint(x, scan(x)), local(x))` | 42.7 | ✓ |
| 1d_recolor_cmp_0 | `paint(paint(x, local(x)), segment(x))` | 39.5 | ✓ |
| 1d_recolor_cmp_1 | `paint(paint(x, local(shift(x))), segment(x))` | 62.0 | ✓ |
| 1d_recolor_cmp_10 | `paint(paint(x, segment(x)), segment(x))` | 45.6 | ✓ |
| 1d_recolor_cmp_11 | `paint(paint(x, local(shift(x))), segment(x))` | 46.5 | ✓ |
| 1d_recolor_cmp_12 | `paint(x, segment(x))` | 75.2 | ✓ |
| 1d_recolor_cmp_13 | `paint(paint(x, segment(x)), local(x))` | 42.6 | ✓ |
| 1d_recolor_cmp_14 | `paint(paint(x, segment(x)), segment(x))` | 62.7 | ✓ |
| 1d_recolor_cmp_15 | `paint(paint(x, scan(x)), segment(x))` | 63.8 | ✓ |
| 1d_recolor_cmp_16 | `paint(paint(x, local(shift(x))), segment(x))` | 47.5 | ✓ |
| 1d_recolor_cmp_17 | `paint(paint(x, scan(x)), segment(x))` | 45.8 | ✓ |
| 1d_recolor_cmp_18 | `paint(paint(x, scan(x)), segment(x))` | 45.0 | ✓ |
| 1d_recolor_cmp_19 | `paint(paint(x, segment(x)), segment(x))` | 41.5 | ✓ |
| 1d_recolor_cmp_2 | `paint(paint(x, local(shift(x))), segment(x))` | 57.9 | ✓ |
| 1d_recolor_cmp_20 | `paint(paint(x, segment(x)), local(x))` | 32.7 | ✓ |
| 1d_recolor_cmp_21 | `paint(paint(x, segment(x)), scan(x))` | 40.4 | ✓ |
| 1d_recolor_cmp_22 | `paint(paint(x, scan(x)), segment(x))` | 51.1 | ✓ |
| 1d_recolor_cmp_23 | `paint(paint(x, segment(x)), segment(x))` | 43.7 | ✓ |
| 1d_recolor_cmp_24 | `paint(paint(x, scan(x)), segment(x))` | 55.6 | ✓ |
| 1d_recolor_cmp_25 | `paint(paint(x, scan(x)), segment(x))` | 43.2 | ✓ |
| 1d_recolor_cmp_26 | `paint(paint(x, scan(x)), segment(x))` | 55.2 | ✓ |
| 1d_recolor_cmp_27 | `paint(paint(x, scan(x)), segment(x))` | 45.8 | ✓ |
| 1d_recolor_cmp_28 | `paint(paint(x, segment(x)), segment(x))` | 45.2 | ✓ |
| 1d_recolor_cmp_29 | `paint(paint(x, scan(x)), segment(x))` | 29.7 | ✓ |
| 1d_recolor_cmp_3 | `paint(paint(x, local(shift(x))), segment(x))` | 68.8 | ✓ |
| 1d_recolor_cmp_30 | `paint(x, segment(paint(x, local(x))))` | 94.0 | ✓ |
| 1d_recolor_cmp_31 | `paint(paint(x, segment(x)), local(x))` | 52.1 | ✓ |
| 1d_recolor_cmp_32 | `paint(paint(x, scan(x)), segment(x))` | 53.2 | ✓ |
| 1d_recolor_cmp_33 | `paint(paint(x, scan(x)), segment(x))` | 72.5 | ✓ |
| 1d_recolor_cmp_34 | `paint(paint(x, segment(x)), segment(x))` | 43.9 | ✓ |
| 1d_recolor_cmp_35 | `paint(paint(x, scan(x)), segment(x))` | 82.2 | ✓ |
| 1d_recolor_cmp_36 | `paint(paint(x, scan(x)), segment(x))` | 38.8 | ✓ |
| 1d_recolor_cmp_37 | `paint(paint(x, segment(x)), scan(x))` | 30.2 | ✓ |
| 1d_recolor_cmp_38 | `paint(paint(x, scan(x)), segment(x))` | 45.6 | ✓ |
| 1d_recolor_cmp_39 | `paint(paint(x, scan(x)), segment(x))` | 42.5 | ✓ |
| 1d_recolor_cmp_4 | `paint(paint(x, segment(x)), segment(x))` | 59.6 | ✓ |
| 1d_recolor_cmp_40 | `paint(paint(x, scan(x)), segment(x))` | 59.7 | ✓ |
| 1d_recolor_cmp_41 | `paint(paint(x, scan(x)), segment(x))` | 46.7 | ✓ |
| 1d_recolor_cmp_42 | `paint(paint(x, segment(x)), scan(x))` | 63.2 | ✓ |
| 1d_recolor_cmp_43 | `paint(paint(x, scan(x)), segment(x))` | 55.3 | ✓ |
| 1d_recolor_cmp_44 | `paint(paint(x, scan(x)), segment(x))` | 37.3 | ✓ |
| 1d_recolor_cmp_45 | `paint(paint(x, segment(x)), local(shift(x)))` | 61.7 | ✓ |
| 1d_recolor_cmp_46 | `paint(paint(x, segment(x)), scan(x))` | 52.5 | ✓ |
| 1d_recolor_cmp_47 | `paint(paint(x, scan(x)), segment(x))` | 51.5 | ✓ |
| 1d_recolor_cmp_48 | `paint(paint(x, local(x)), scan(x))` | 65.5 | ✗ |
| 1d_recolor_cmp_49 | `paint(paint(x, segment(x)), scan(x))` | 64.2 | ✓ |
| 1d_recolor_cmp_5 | `paint(paint(x, segment(x)), segment(x))` | 44.2 | ✓ |
| 1d_recolor_cmp_6 | `paint(paint(x, scan(x)), segment(x))` | 68.1 | ✓ |
| 1d_recolor_cmp_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 55.6 | ✓ |
| 1d_recolor_cmp_8 | `paint(paint(x, scan(x)), segment(x))` | 35.3 | ✓ |
| 1d_recolor_cmp_9 | `paint(paint(x, segment(x)), scan(x))` | 44.0 | ✓ |
| 1d_recolor_cnt_0 | `paint(paint(x, scan(x)), segment(x))` | 83.6 | ✓ |
| 1d_recolor_cnt_1 | `paint(paint(x, segment(x)), local(x))` | 104.6 | ✓ |
| 1d_recolor_cnt_10 | `paint(paint(x, segment(x)), local(shift(x)))` | 100.7 | ✓ |
| 1d_recolor_cnt_11 | `paint(x, segment(reverse(x)))` | 97.8 | ✓ |
| 1d_recolor_cnt_12 | `paint(paint(x, segment(x)), local(x))` | 80.1 | ✓ |
| 1d_recolor_cnt_13 | `paint(x, segment(reverse(x)))` | 72.5 | ✓ |
| 1d_recolor_cnt_14 | `paint(paint(x, segment(x)), local(x))` | 100.6 | ✓ |
| 1d_recolor_cnt_15 | `paint(paint(x, segment(x)), local(x))` | 80.5 | ✓ |
| 1d_recolor_cnt_16 | `paint(paint(x, segment(x)), local(x))` | 72.8 | ✓ |
| 1d_recolor_cnt_17 | `paint(paint(x, segment(x)), local(x))` | 64.7 | ✓ |
| 1d_recolor_cnt_18 | `paint(paint(shift(x), segment(x)), local(x))` | 114.2 | ✓ |
| 1d_recolor_cnt_19 | `paint(x, segment(x))` | 83.2 | ✓ |
| 1d_recolor_cnt_2 | `paint(paint(x, segment(x)), local(x))` | 71.3 | ✓ |
| 1d_recolor_cnt_20 | `paint(paint(x, segment(x)), scan(x))` | 88.4 | ✓ |
| 1d_recolor_cnt_21 | `paint(paint(x, segment(x)), local(x))` | 68.9 | ✓ |
| 1d_recolor_cnt_22 | `paint(paint(x, segment(x)), local(x))` | 64.0 | ✓ |
| 1d_recolor_cnt_23 | `paint(paint(x, segment(x)), local(x))` | 76.2 | ✓ |
| 1d_recolor_cnt_24 | `paint(x, segment(reverse(x)))` | 67.4 | ✓ |
| 1d_recolor_cnt_25 | `paint(x, segment(paint(x, local(x))))` | 79.2 | ✓ |
| 1d_recolor_cnt_26 | `paint(paint(x, segment(x)), local(x))` | 76.9 | ✓ |
| 1d_recolor_cnt_27 | `paint(reverse(x), segment(x))` | 74.0 | ✓ |
| 1d_recolor_cnt_28 | `paint(x, segment(x))` | 78.9 | ✓ |
| 1d_recolor_cnt_29 | `paint(x, segment(reverse(x)))` | 100.4 | ✓ |
| 1d_recolor_cnt_3 | `paint(reverse(x), segment(x))` | 70.0 | ✓ |
| 1d_recolor_cnt_30 | `paint(paint(x, segment(x)), local(x))` | 77.0 | ✓ |
| 1d_recolor_cnt_31 | `paint(paint(x, segment(x)), scan(x))` | 76.3 | ✓ |
| 1d_recolor_cnt_32 | `paint(paint(x, segment(x)), local(x))` | 83.7 | ✓ |
| 1d_recolor_cnt_33 | `paint(paint(x, segment(x)), segment(x))` | 98.9 | ✓ |
| 1d_recolor_cnt_34 | `paint(x, segment(paint(x, segment(x))))` | 91.7 | ✓ |
| 1d_recolor_cnt_35 | `paint(x, segment(paint(x, segment(x))))` | 81.8 | ✓ |
| 1d_recolor_cnt_36 | `paint(x, segment(reverse(x)))` | 89.5 | ✓ |
| 1d_recolor_cnt_37 | `paint(paint(x, segment(x)), local(x))` | 67.6 | ✓ |
| 1d_recolor_cnt_38 | `paint(paint(x, scan(x)), segment(x))` | 73.9 | ✓ |
| 1d_recolor_cnt_39 | `paint(paint(x, segment(x)), segment(x))` | 70.0 | ✓ |
| 1d_recolor_cnt_4 | `paint(paint(x, segment(x)), local(x))` | 78.1 | ✓ |
| 1d_recolor_cnt_40 | `paint(paint(x, segment(x)), segment(x))` | 80.8 | ✓ |
| 1d_recolor_cnt_41 | `paint(x, segment(reverse(x)))` | 100.2 | ✓ |
| 1d_recolor_cnt_42 | `paint(paint(x, scan(x)), segment(x))` | 63.9 | ✓ |
| 1d_recolor_cnt_43 | `paint(paint(shift(x), segment(x)), local(x))` | 85.3 | ✓ |
| 1d_recolor_cnt_44 | `paint(paint(x, scan(x)), segment(x))` | 56.4 | ✓ |
| 1d_recolor_cnt_45 | `paint(paint(x, segment(x)), local(x))` | 104.2 | ✓ |
| 1d_recolor_cnt_46 | `paint(paint(x, segment(x)), local(x))` | 85.3 | ✓ |
| 1d_recolor_cnt_47 | `paint(x, segment(reverse(x)))` | 112.9 | ✓ |
| 1d_recolor_cnt_48 | `paint(paint(x, segment(x)), local(x))` | 90.5 | ✓ |
| 1d_recolor_cnt_49 | `paint(paint(x, scan(x)), segment(x))` | 84.0 | ✓ |
| 1d_recolor_cnt_5 | `paint(paint(x, segment(x)), local(x))` | 85.8 | ✓ |
| 1d_recolor_cnt_6 | `paint(x, segment(reverse(x)))` | 72.1 | ✓ |
| 1d_recolor_cnt_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 72.9 | ✓ |
| 1d_recolor_cnt_8 | `paint(x, segment(x))` | 78.0 | ✓ |
| 1d_recolor_cnt_9 | `paint(paint(x, scan(x)), segment(x))` | 89.7 | ✓ |
| 1d_recolor_oe_0 | `paint(reverse(x), segment(x))` | 78.8 | ✗ |
| 1d_recolor_oe_1 | `paint(paint(x, segment(x)), local(x))` | 62.5 | ✓ |
| 1d_recolor_oe_10 | `paint(paint(x, segment(x)), local(x))` | 104.0 | ✓ |
| 1d_recolor_oe_11 | `paint(paint(x, segment(x)), local(x))` | 83.7 | ✓ |
| 1d_recolor_oe_12 | `paint(paint(x, segment(x)), local(x))` | 106.2 | ✓ |
| 1d_recolor_oe_13 | `paint(paint(x, segment(x)), segment(x))` | 68.9 | ✓ |
| 1d_recolor_oe_14 | `paint(paint(x, segment(x)), local(x))` | 67.4 | ✓ |
| 1d_recolor_oe_15 | `paint(paint(x, segment(x)), scan(x))` | 75.8 | ✓ |
| 1d_recolor_oe_16 | `paint(paint(x, segment(x)), local(shift(x)))` | 95.5 | ✓ |
| 1d_recolor_oe_17 | `paint(paint(x, segment(x)), local(x))` | 99.6 | ✓ |
| 1d_recolor_oe_18 | `paint(paint(x, segment(x)), segment(x))` | 76.4 | ✓ |
| 1d_recolor_oe_19 | `paint(paint(x, segment(x)), local(x))` | 76.6 | ✓ |
| 1d_recolor_oe_2 | `paint(x, segment(x))` | 60.8 | ✓ |
| 1d_recolor_oe_20 | `paint(paint(x, segment(x)), segment(x))` | 90.8 | ✓ |
| 1d_recolor_oe_21 | `paint(paint(x, segment(x)), local(shift(x)))` | 118.2 | ✓ |
| 1d_recolor_oe_22 | `paint(paint(x, segment(x)), scan(x))` | 80.9 | ✓ |
| 1d_recolor_oe_23 | `paint(paint(x, segment(x)), segment(x))` | 62.8 | ✓ |
| 1d_recolor_oe_24 | `paint(paint(x, segment(x)), segment(x))` | 66.0 | ✓ |
| 1d_recolor_oe_25 | `paint(paint(x, segment(x)), scan(x))` | 92.9 | ✓ |
| 1d_recolor_oe_26 | `paint(x, segment(paint(x, scan(x))))` | 59.6 | ✓ |
| 1d_recolor_oe_27 | `paint(paint(x, segment(x)), local(x))` | 80.3 | ✓ |
| 1d_recolor_oe_28 | `paint(paint(x, segment(x)), local(x))` | 82.5 | ✗ |
| 1d_recolor_oe_29 | `paint(x, segment(reverse(x)))` | 68.5 | ✗ |
| 1d_recolor_oe_3 | `paint(paint(x, segment(x)), local(shift(x)))` | 70.4 | ✓ |
| 1d_recolor_oe_30 | `paint(x, segment(x))` | 69.2 | ✓ |
| 1d_recolor_oe_31 | `paint(x, segment(x))` | 60.6 | ✗ |
| 1d_recolor_oe_32 | `paint(paint(x, segment(x)), local(shift(x)))` | 111.5 | ✓ |
| 1d_recolor_oe_33 | `paint(paint(x, segment(x)), segment(x))` | 76.2 | ✓ |
| 1d_recolor_oe_34 | `paint(paint(x, local(shift(x))), segment(x))` | 87.5 | ✗ |
| 1d_recolor_oe_35 | `paint(paint(x, segment(x)), local(shift(x)))` | 62.5 | ✓ |
| 1d_recolor_oe_36 | `paint(x, segment(x))` | 54.8 | ✓ |
| 1d_recolor_oe_37 | `paint(paint(x, segment(x)), segment(x))` | 81.3 | ✓ |
| 1d_recolor_oe_38 | `paint(paint(x, segment(x)), segment(x))` | 101.4 | ✓ |
| 1d_recolor_oe_39 | `paint(x, segment(x))` | 58.9 | ✓ |
| 1d_recolor_oe_4 | `paint(paint(x, segment(x)), local(x))` | 74.5 | ✓ |
| 1d_recolor_oe_40 | `paint(reverse(x), segment(x))` | 62.7 | ✓ |
| 1d_recolor_oe_41 | `paint(paint(x, segment(x)), local(shift(x)))` | 84.0 | ✓ |
| 1d_recolor_oe_42 | `paint(paint(x, local(x)), segment(x))` | 76.2 | ✓ |
| 1d_recolor_oe_43 | `paint(x, segment(paint(x, scan(x))))` | 82.5 | ✓ |
| 1d_recolor_oe_44 | `paint(paint(x, segment(x)), segment(x))` | 91.9 | ✓ |
| 1d_recolor_oe_45 | `paint(paint(x, segment(x)), local(shift(x)))` | 76.7 | ✗ |
| 1d_recolor_oe_46 | `paint(paint(x, local(shift(x))), segment(x))` | 100.0 | ✓ |
| 1d_recolor_oe_47 | `paint(paint(x, segment(x)), segment(x))` | 69.7 | ✓ |
| 1d_recolor_oe_48 | `paint(paint(x, segment(x)), local(shift(x)))` | 87.3 | ✓ |
| 1d_recolor_oe_49 | `paint(paint(x, segment(x)), segment(x))` | 98.2 | ✓ |
| 1d_recolor_oe_5 | `paint(paint(x, segment(x)), segment(x))` | 65.0 | ✓ |
| 1d_recolor_oe_6 | `paint(paint(x, segment(x)), local(x))` | 107.5 | ✗ |
| 1d_recolor_oe_7 | `paint(paint(x, segment(x)), scan(x))` | 87.2 | ✓ |
| 1d_recolor_oe_8 | `paint(paint(x, segment(x)), segment(x))` | 56.6 | ✓ |
| 1d_recolor_oe_9 | `shift(paint(paint(x, segment(x)), local(x)))` | 105.2 | ✓ |
| 1d_scale_dp_0 | `paint(paint(x, scan(x)), segment(x))` | 35.3 | ✓ |
| 1d_scale_dp_1 | `paint(paint(x, scan(x)), scan(x))` | 53.7 | ✓ |
| 1d_scale_dp_10 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.0 | ✓ |
| 1d_scale_dp_11 | `paint(paint(x, scan(x)), scan(x))` | 38.7 | ✓ |
| 1d_scale_dp_12 | `paint(paint(x, local(shift(x))), segment(x))` | 52.8 | ✓ |
| 1d_scale_dp_13 | `paint(x, local(paint(x, scan(x))))` | 62.9 | ✗ |
| 1d_scale_dp_14 | `paint(x, scan(x))` | 55.3 | ✓ |
| 1d_scale_dp_15 | `paint(x, scan(x))` | 77.8 | ✓ |
| 1d_scale_dp_16 | `paint(reverse(x), scan(x))` | 57.7 | ✓ |
| 1d_scale_dp_17 | `paint(paint(x, scan(x)), local(x))` | 60.3 | ✓ |
| 1d_scale_dp_18 | `paint(paint(x, local(x)), scan(x))` | 28.5 | ✓ |
| 1d_scale_dp_19 | `paint(paint(x, scan(x)), scan(x))` | 44.4 | ✗ |
| 1d_scale_dp_2 | `paint(paint(x, scan(x)), segment(x))` | 59.9 | ✓ |
| 1d_scale_dp_20 | `paint(paint(x, scan(x)), segment(x))` | 49.0 | ✓ |
| 1d_scale_dp_21 | `paint(paint(x, local(x)), scan(x))` | 60.8 | ✓ |
| 1d_scale_dp_22 | `paint(x, local(x))` | 48.0 | ✓ |
| 1d_scale_dp_23 | `paint(reverse(x), scan(x))` | 61.3 | ✓ |
| 1d_scale_dp_24 | `paint(paint(x, scan(x)), scan(x))` | 30.5 | ✓ |
| 1d_scale_dp_25 | `paint(paint(x, scan(x)), scan(x))` | 43.0 | ✓ |
| 1d_scale_dp_26 | `paint(paint(x, scan(x)), scan(x))` | 36.7 | ✓ |
| 1d_scale_dp_27 | `paint(paint(x, local(x)), scan(x))` | 62.8 | ✓ |
| 1d_scale_dp_28 | `paint(reverse(x), scan(x))` | 65.5 | ✓ |
| 1d_scale_dp_29 | `paint(x, local(slide(x)))` | 47.7 | ✓ |
| 1d_scale_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 36.1 | ✓ |
| 1d_scale_dp_30 | `paint(paint(x, local(shift(x))), scan(x))` | 63.8 | ✓ |
| 1d_scale_dp_31 | `paint(reverse(x), scan(x))` | 53.6 | ✓ |
| 1d_scale_dp_32 | `paint(paint(x, scan(x)), scan(x))` | 38.9 | ✓ |
| 1d_scale_dp_33 | `paint(reverse(x), scan(x))` | 48.7 | ✓ |
| 1d_scale_dp_34 | `paint(paint(x, local(shift(x))), scan(x))` | 35.0 | ✓ |
| 1d_scale_dp_35 | `paint(paint(x, local(shift(x))), scan(x))` | 49.1 | ✓ |
| 1d_scale_dp_36 | `paint(reverse(x), scan(x))` | 59.7 | ✓ |
| 1d_scale_dp_37 | `paint(x, scan(paint(x, local(x))))` | 48.8 | ✓ |
| 1d_scale_dp_38 | `paint(paint(x, scan(x)), scan(x))` | 81.8 | ✓ |
| 1d_scale_dp_39 | `paint(paint(x, scan(x)), segment(x))` | 47.6 | ✓ |
| 1d_scale_dp_4 | `paint(reverse(x), scan(x))` | 53.2 | ✓ |
| 1d_scale_dp_40 | `paint(paint(x, scan(x)), scan(x))` | 48.0 | ✓ |
| 1d_scale_dp_41 | `paint(x, scan(reverse(x)))` | 60.1 | ✓ |
| 1d_scale_dp_42 | `paint(paint(x, scan(x)), local(shift(x)))` | 35.7 | ✓ |
| 1d_scale_dp_43 | `paint(paint(x, scan(x)), scan(x))` | 49.6 | ✓ |
| 1d_scale_dp_44 | `paint(shift(x), local(x))` | 36.1 | ✓ |
| 1d_scale_dp_45 | `paint(x, local(x))` | 57.8 | ✓ |
| 1d_scale_dp_46 | `paint(paint(x, scan(x)), scan(x))` | 61.4 | ✓ |
| 1d_scale_dp_47 | `paint(reverse(x), scan(x))` | 57.6 | ✓ |
| 1d_scale_dp_48 | `paint(paint(x, scan(x)), scan(x))` | 36.0 | ✓ |
| 1d_scale_dp_49 | `paint(paint(x, scan(x)), scan(x))` | 44.6 | ✓ |
| 1d_scale_dp_5 | `paint(reverse(x), scan(x))` | 57.9 | ✓ |
| 1d_scale_dp_50 | `paint(reverse(x), scan(x))` | 48.1 | ✓ |
| 1d_scale_dp_6 | `paint(paint(x, local(shift(x))), scan(x))` | 65.8 | ✓ |
| 1d_scale_dp_7 | `paint(shift(shift(x)), local(x))` | 43.8 | ✓ |
| 1d_scale_dp_8 | `paint(x, local(paint(x, segment(x))))` | 55.8 | ✓ |
| 1d_scale_dp_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 52.1 | ✓ |
