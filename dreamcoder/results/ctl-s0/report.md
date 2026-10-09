# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 901 (50 per family, drawn with seed 0), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/ctl-s0/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 662/901 (73%) | 723/901 | 799/901 | 65.0 | 7 | 150 | 1833s |
| 1 | 681/901 (76%) | 729/901 | 786/901 | 65.7 | 7 | 150 | 2004s |
| 2 | 689/901 (76%) | 730/901 | 786/901 | 64.4 | 7 | 150 | 2003s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 45/50 | 45/50 | 47/50 |
| denoising_mc | 39/50 | 42/50 | 45/50 |
| fill | 39/50 | 47/50 | 46/50 |
| flip | 7/50 | 5/50 | 6/50 |
| hollow | 49/50 | 47/50 | 49/50 |
| mirror | 2/50 | 5/50 | 3/50 |
| move_1p | 47/50 | 47/50 | 48/50 |
| move_2p | 49/50 | 50/50 | 49/50 |
| move_2p_dp | 42/50 | 43/50 | 40/50 |
| move_3p | 49/50 | 50/50 | 49/50 |
| move_dp | 3/50 | 2/50 | 4/50 |
| padded_fill | 45/50 | 46/50 | 47/50 |
| pcopy_1c | 25/50 | 23/50 | 26/50 |
| pcopy_mc | 39/50 | 40/50 | 47/50 |
| recolor_cmp | 48/50 | 49/50 | 49/50 |
| recolor_cnt | 49/50 | 50/50 | 50/50 |
| recolor_oe | 41/50 | 44/50 | 43/50 |
| scale_dp | 44/51 | 46/51 | 41/51 |

## Library growth

- no fragment had support in two tasks

## Examples from the last iteration

### Solved: `1d_denoising_1c_48`

`paint(paint(x, local(x)), local(x))`, DL 49.0 = 8.3 structure + 39.4 parameters + 1.3 data bits, fits its training pairs exactly.

![1d_denoising_1c_48](figures/1d_denoising_1c_48.png)

| pair | input | output |
|---|---|---|
| train 0 | `...1...1....1..1111111111111..1.` | `...............1111111111111....` |
| train 1 | `...66666666666....6...6....6....` | `...66666666666..................` |
| train 2 | `..8..8........88888888888..8....` | `..............88888888888.......` |
| **test** | `.44444444444....4...4....4......` | `.44444444444....................` |
| predicted | | `.44444444444....................` |

### Solved: `1d_move_2p_29`

`shift(x)`, DL 48.2 = 3.8 structure + 40.6 parameters + 3.8 data bits, fits its training pairs exactly.

![1d_move_2p_29](figures/1d_move_2p_29.png)

| pair | input | output |
|---|---|---|
| train 0 | `.22222....` | `...22222..` |
| train 1 | `444444....` | `..444444..` |
| train 2 | `8888......` | `..8888....` |
| **test** | `6666......` | `..6666....` |
| predicted | | `..6666....` |

### Solved: `1d_padded_fill_16`

`recolour(paint(x, scan(x)))`, DL 46.7 = 11.4 structure + 33.5 parameters + 1.7 data bits, fits its training pairs exactly.

![1d_padded_fill_16](figures/1d_padded_fill_16.png)

| pair | input | output |
|---|---|---|
| train 0 | `.................6..6....................6..6....................6..6...` | `.................6666....................6666....................6666...` |
| train 1 | `............7....7..................7....7..................7....7......` | `............777777..................777777..................777777......` |
| train 2 | `..8................8......8................8......8................8....` | `..888888888888888888......888888888888888888......888888888888888888....` |
| **test** | `..2..........2............2..........2............2..........2..........` | `..222222222222............222222222222............222222222222..........` |
| predicted | | `..222222222222............222222222222............222222222222..........` |

### Failed: `1d_flip_25`

`paint(shift(x), local(x))`, DL 86.4 = 7.5 structure + 73.1 parameters + 5.7 data bits, does not fit its training pairs exactly.

![1d_flip_25](figures/1d_flip_25.png)

| pair | input | output |
|---|---|---|
| train 0 | `5666666666..........` | `6666666665..........` |
| train 1 | `......6888888.......` | `......8888886.......` |
| train 2 | `.......488888888....` | `.......888888884....` |
| **test** | `..........2555555...` | `..........5555552...` |
| predicted | | `.........25555554...` |

### Failed: `1d_mirror_39`

`reflect(shift(shift(x)))`, DL 146.6 = 14.7 structure + 90.5 parameters + 41.4 data bits, does not fit its training pairs exactly.

![1d_mirror_39](figures/1d_mirror_39.png)

| pair | input | output |
|---|---|---|
| train 0 | `3333333.....9..................` | `............9.....3333333......` |
| train 1 | `..111111111....9...............` | `...............9....111111111..` |
| train 2 | `777777777...9..................` | `............9...777777777......` |
| **test** | `44444444....9..................` | `............9....44444444......` |
| predicted | | `..................44444444.....` |

### Failed: `1d_move_dp_12`

`paint(reflect(x), local(x))`, DL 100.4 = 12.7 structure + 74.5 parameters + 13.2 data bits, does not fit its training pairs exactly.

![1d_move_dp_12](figures/1d_move_dp_12.png)

| pair | input | output |
|---|---|---|
| train 0 | `..33333333333333.....4...` | `.......333333333333334...` |
| train 1 | `..555555555555555....4...` | `......5555555555555554...` |
| train 2 | `.11111111111111..4.......` | `...111111111111114.......` |
| **test** | `.....8888888888888888..4.` | `.......88888888888888884.` |
| predicted | | `.....888888888888888.....` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_0 | `paint(x, local(paint(x, scan(x))))` | 49.5 | ✓ |
| 1d_denoising_1c_1 | `paint(x, local(x))` | 53.6 | ✓ |
| 1d_denoising_1c_10 | `paint(shift(paint(x, segment(x))), local(x))` | 53.3 | ✓ |
| 1d_denoising_1c_11 | `paint(x, segment(paint(x, segment(x))))` | 47.0 | ✓ |
| 1d_denoising_1c_12 | `paint(x, local(x))` | 46.6 | ✓ |
| 1d_denoising_1c_13 | `paint(paint(x, scan(x)), local(x))` | 55.1 | ✓ |
| 1d_denoising_1c_14 | `paint(paint(x, scan(x)), segment(x))` | 37.8 | ✓ |
| 1d_denoising_1c_15 | `paint(paint(x, scan(x)), local(x))` | 50.8 | ✓ |
| 1d_denoising_1c_16 | `paint(paint(x, scan(x)), segment(x))` | 37.2 | ✓ |
| 1d_denoising_1c_17 | `paint(paint(x, scan(x)), segment(x))` | 37.7 | ✓ |
| 1d_denoising_1c_18 | `paint(shift(x), local(recolour(x)))` | 46.9 | ✓ |
| 1d_denoising_1c_19 | `paint(paint(shift(x), local(x)), local(x))` | 35.8 | ✗ |
| 1d_denoising_1c_2 | `paint(paint(x, scan(x)), segment(x))` | 37.8 | ✓ |
| 1d_denoising_1c_20 | `paint(paint(x, scan(x)), segment(x))` | 39.4 | ✓ |
| 1d_denoising_1c_21 | `paint(x, local(paint(x, segment(shift(x)))))` | 48.6 | ✓ |
| 1d_denoising_1c_22 | `paint(paint(shift(x), scan(x)), local(x))` | 23.6 | ✓ |
| 1d_denoising_1c_23 | `paint(x, segment(paint(x, segment(x))))` | 41.8 | ✓ |
| 1d_denoising_1c_24 | `paint(paint(x, local(x)), scan(x))` | 51.5 | ✓ |
| 1d_denoising_1c_25 | `paint(paint(shift(x), scan(x)), local(x))` | 29.8 | ✓ |
| 1d_denoising_1c_26 | `recolour(paint(shift(x), local(x)))` | 53.0 | ✓ |
| 1d_denoising_1c_27 | `paint(paint(x, scan(x)), local(x))` | 48.1 | ✓ |
| 1d_denoising_1c_28 | `paint(shift(x), local(x))` | 42.8 | ✓ |
| 1d_denoising_1c_29 | `paint(paint(x, scan(x)), segment(x))` | 46.1 | ✓ |
| 1d_denoising_1c_3 | `paint(paint(shift(x), local(x)), scan(x))` | 44.5 | ✓ |
| 1d_denoising_1c_30 | `paint(paint(shift(x), scan(x)), local(x))` | 48.8 | ✓ |
| 1d_denoising_1c_31 | `paint(paint(shift(x), segment(x)), local(x))` | 49.6 | ✗ |
| 1d_denoising_1c_32 | `paint(x, local(x))` | 51.4 | ✓ |
| 1d_denoising_1c_33 | `paint(paint(x, scan(x)), segment(x))` | 33.7 | ✓ |
| 1d_denoising_1c_34 | `paint(x, segment(paint(x, segment(x))))` | 48.8 | ✓ |
| 1d_denoising_1c_35 | `paint(paint(x, local(x)), segment(shift(x)))` | 43.7 | ✓ |
| 1d_denoising_1c_36 | `paint(recolour(x), local(x))` | 44.3 | ✓ |
| 1d_denoising_1c_37 | `paint(x, local(paint(x, segment(x))))` | 55.5 | ✓ |
| 1d_denoising_1c_38 | `paint(paint(x, scan(x)), segment(x))` | 37.8 | ✓ |
| 1d_denoising_1c_39 | `paint(x, segment(paint(x, segment(x))))` | 44.8 | ✓ |
| 1d_denoising_1c_4 | `paint(paint(x, scan(x)), local(x))` | 51.3 | ✓ |
| 1d_denoising_1c_40 | `paint(x, segment(paint(x, segment(x))))` | 42.0 | ✓ |
| 1d_denoising_1c_41 | `recolour(paint(shift(x), local(x)))` | 36.5 | ✓ |
| 1d_denoising_1c_42 | `paint(shift(x), local(x))` | 48.8 | ✓ |
| 1d_denoising_1c_43 | `paint(paint(x, scan(x)), segment(x))` | 44.9 | ✓ |
| 1d_denoising_1c_44 | `paint(shift(x), local(x))` | 43.8 | ✓ |
| 1d_denoising_1c_45 | `paint(x, local(x))` | 47.2 | ✓ |
| 1d_denoising_1c_46 | `paint(paint(x, scan(x)), segment(x))` | 37.6 | ✓ |
| 1d_denoising_1c_47 | `paint(paint(x, scan(x)), segment(x))` | 37.7 | ✓ |
| 1d_denoising_1c_48 | `paint(paint(x, local(x)), local(x))` | 49.0 | ✓ |
| 1d_denoising_1c_49 | `paint(x, local(paint(x, scan(x))))` | 43.0 | ✓ |
| 1d_denoising_1c_5 | `paint(recolour(x), local(x))` | 50.3 | ✓ |
| 1d_denoising_1c_6 | `paint(paint(shift(x), local(x)), local(x))` | 48.4 | ✓ |
| 1d_denoising_1c_7 | `paint(x, local(paint(x, scan(shift(x)))))` | 44.8 | ✓ |
| 1d_denoising_1c_8 | `paint(shift(x), local(x))` | 43.3 | ✗ |
| 1d_denoising_1c_9 | `paint(paint(x, local(x)), local(shift(x)))` | 48.1 | ✓ |
| 1d_denoising_mc_0 | `paint(paint(shift(x), local(x)), local(x))` | 29.9 | ✓ |
| 1d_denoising_mc_1 | `paint(paint(shift(x), segment(x)), local(x))` | 40.4 | ✓ |
| 1d_denoising_mc_10 | `paint(paint(shift(x), segment(x)), local(x))` | 26.2 | ✗ |
| 1d_denoising_mc_11 | `paint(shift(paint(x, scan(x))), local(x))` | 30.9 | ✓ |
| 1d_denoising_mc_12 | `recolour(paint(shift(x), local(x)))` | 34.6 | ✓ |
| 1d_denoising_mc_13 | `paint(shift(paint(x, scan(x))), local(x))` | 51.1 | ✓ |
| 1d_denoising_mc_14 | `paint(paint(shift(x), local(x)), segment(x))` | 25.1 | ✗ |
| 1d_denoising_mc_15 | `paint(paint(shift(x), local(x)), segment(x))` | 33.4 | ✓ |
| 1d_denoising_mc_16 | `paint(shift(paint(x, scan(x))), local(x))` | 28.4 | ✓ |
| 1d_denoising_mc_17 | `paint(paint(shift(x), local(x)), scan(x))` | 16.9 | ✓ |
| 1d_denoising_mc_18 | `paint(paint(shift(x), local(x)), segment(x))` | 32.7 | ✓ |
| 1d_denoising_mc_19 | `paint(paint(shift(x), local(x)), scan(x))` | 29.3 | ✓ |
| 1d_denoising_mc_2 | `paint(paint(shift(x), local(x)), segment(x))` | 29.7 | ✓ |
| 1d_denoising_mc_20 | `paint(shift(paint(x, local(x))), local(x))` | 47.8 | ✓ |
| 1d_denoising_mc_21 | `paint(paint(shift(x), local(x)), segment(x))` | 34.7 | ✓ |
| 1d_denoising_mc_22 | `paint(paint(x, local(x)), local(shift(x)))` | 53.7 | ✓ |
| 1d_denoising_mc_23 | `paint(shift(paint(x, scan(x))), local(x))` | 30.0 | ✓ |
| 1d_denoising_mc_24 | `paint(shift(x), local(x))` | 44.9 | ✓ |
| 1d_denoising_mc_25 | `paint(paint(shift(x), local(x)), scan(x))` | 21.0 | ✓ |
| 1d_denoising_mc_26 | `paint(shift(x), scan(x))` | 39.0 | ✓ |
| 1d_denoising_mc_27 | `paint(shift(paint(x, scan(x))), local(x))` | 48.1 | ✓ |
| 1d_denoising_mc_28 | `paint(shift(paint(x, scan(x))), local(x))` | 28.7 | ✓ |
| 1d_denoising_mc_29 | `recolour(paint(shift(x), local(x)))` | 17.0 | ✓ |
| 1d_denoising_mc_3 | `paint(paint(shift(x), local(x)), local(x))` | 23.7 | ✓ |
| 1d_denoising_mc_30 | `paint(paint(shift(x), local(x)), segment(x))` | 37.3 | ✓ |
| 1d_denoising_mc_31 | `paint(paint(shift(x), local(x)), scan(x))` | 37.8 | ✓ |
| 1d_denoising_mc_32 | `paint(paint(shift(x), local(x)), scan(x))` | 25.6 | ✓ |
| 1d_denoising_mc_33 | `paint(shift(paint(x, scan(x))), local(x))` | 24.5 | ✓ |
| 1d_denoising_mc_34 | `paint(paint(shift(x), local(x)), segment(x))` | 49.2 | ✓ |
| 1d_denoising_mc_35 | `paint(shift(paint(x, scan(x))), local(x))` | 47.0 | ✓ |
| 1d_denoising_mc_36 | `paint(shift(x), local(paint(x, local(x))))` | 44.5 | ✓ |
| 1d_denoising_mc_37 | `paint(shift(paint(x, scan(x))), local(x))` | 29.9 | ✓ |
| 1d_denoising_mc_38 | `paint(shift(x), local(x))` | 49.3 | ✓ |
| 1d_denoising_mc_39 | `paint(shift(paint(x, scan(x))), local(x))` | 53.7 | ✓ |
| 1d_denoising_mc_4 | `paint(recolour(shift(x)), local(x))` | 23.8 | ✗ |
| 1d_denoising_mc_40 | `paint(paint(shift(x), local(x)), scan(x))` | 16.5 | ✓ |
| 1d_denoising_mc_41 | `paint(shift(paint(x, scan(x))), local(x))` | 29.1 | ✓ |
| 1d_denoising_mc_42 | `paint(shift(paint(x, scan(x))), local(x))` | 33.5 | ✓ |
| 1d_denoising_mc_43 | `paint(recolour(shift(x)), local(x))` | 17.1 | ✗ |
| 1d_denoising_mc_44 | `paint(paint(x, local(x)), local(shift(x)))` | 33.9 | ✓ |
| 1d_denoising_mc_45 | `paint(shift(paint(x, scan(x))), local(x))` | 37.9 | ✓ |
| 1d_denoising_mc_46 | `recolour(paint(shift(x), local(x)))` | 25.3 | ✓ |
| 1d_denoising_mc_47 | `paint(shift(paint(x, scan(x))), local(x))` | 38.5 | ✓ |
| 1d_denoising_mc_48 | `paint(paint(shift(x), local(x)), scan(x))` | 38.1 | ✓ |
| 1d_denoising_mc_49 | `paint(paint(shift(x), local(x)), segment(x))` | 27.3 | ✓ |
| 1d_denoising_mc_5 | `paint(paint(shift(x), local(x)), local(x))` | 15.8 | ✓ |
| 1d_denoising_mc_6 | `paint(shift(paint(x, scan(x))), local(x))` | 38.8 | ✓ |
| 1d_denoising_mc_7 | `paint(paint(shift(x), local(x)), segment(x))` | 29.6 | ✓ |
| 1d_denoising_mc_8 | `paint(paint(shift(x), local(x)), segment(x))` | 46.2 | ✗ |
| 1d_denoising_mc_9 | `paint(paint(shift(x), local(x)), segment(x))` | 28.8 | ✓ |
| 1d_fill_0 | `paint(paint(x, scan(x)), local(shift(x)))` | 60.6 | ✓ |
| 1d_fill_1 | `paint(x, scan(paint(x, scan(x))))` | 78.8 | ✓ |
| 1d_fill_10 | `paint(x, local(paint(x, scan(x))))` | 81.2 | ✓ |
| 1d_fill_11 | `paint(paint(shift(x), scan(x)), local(x))` | 53.1 | ✓ |
| 1d_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 41.4 | ✓ |
| 1d_fill_13 | `paint(x, scan(paint(x, local(x))))` | 71.1 | ✓ |
| 1d_fill_14 | `paint(x, local(shift(paint(x, scan(x)))))` | 78.4 | ✓ |
| 1d_fill_15 | `paint(x, scan(paint(x, segment(x))))` | 81.1 | ✓ |
| 1d_fill_16 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.2 | ✓ |
| 1d_fill_17 | `paint(paint(x, scan(x)), local(shift(x)))` | 39.9 | ✓ |
| 1d_fill_18 | `paint(shift(paint(x, scan(x))), local(x))` | 79.8 | ✓ |
| 1d_fill_19 | `paint(paint(x, scan(x)), local(x))` | 48.3 | ✓ |
| 1d_fill_2 | `paint(x, local(paint(shift(x), scan(x))))` | 72.3 | ✓ |
| 1d_fill_20 | `paint(paint(shift(x), scan(x)), local(x))` | 41.6 | ✓ |
| 1d_fill_21 | `paint(paint(x, scan(x)), local(x))` | 66.3 | ✓ |
| 1d_fill_22 | `paint(paint(shift(x), scan(x)), local(x))` | 41.1 | ✗ |
| 1d_fill_23 | `paint(paint(shift(x), scan(x)), local(x))` | 57.3 | ✗ |
| 1d_fill_24 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.8 | ✓ |
| 1d_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 51.3 | ✓ |
| 1d_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 37.8 | ✓ |
| 1d_fill_27 | `paint(paint(shift(x), scan(x)), local(x))` | 49.3 | ✓ |
| 1d_fill_28 | `paint(reflect(x), scan(x))` | 73.0 | ✗ |
| 1d_fill_29 | `paint(x, local(paint(x, scan(x))))` | 68.6 | ✓ |
| 1d_fill_3 | `paint(paint(x, scan(x)), local(x))` | 40.7 | ✓ |
| 1d_fill_30 | `paint(x, local(shift(paint(x, scan(x)))))` | 79.0 | ✓ |
| 1d_fill_31 | `paint(paint(shift(x), scan(x)), local(x))` | 74.2 | ✓ |
| 1d_fill_32 | `paint(paint(x, scan(x)), local(x))` | 44.0 | ✓ |
| 1d_fill_33 | `paint(x, scan(recolour(x)))` | 79.7 | ✓ |
| 1d_fill_34 | `paint(x, scan(paint(x, scan(x))))` | 79.3 | ✓ |
| 1d_fill_35 | `paint(x, scan(paint(x, segment(x))))` | 65.1 | ✓ |
| 1d_fill_36 | `paint(x, scan(paint(x, local(x))))` | 57.0 | ✓ |
| 1d_fill_37 | `paint(paint(x, local(shift(x))), scan(x))` | 64.7 | ✓ |
| 1d_fill_38 | `paint(paint(x, scan(x)), segment(x))` | 49.3 | ✓ |
| 1d_fill_39 | `paint(paint(x, scan(x)), local(shift(x)))` | 41.6 | ✓ |
| 1d_fill_4 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.9 | ✓ |
| 1d_fill_40 | `paint(paint(x, scan(x)), local(x))` | 42.6 | ✓ |
| 1d_fill_41 | `paint(paint(x, scan(x)), local(x))` | 53.0 | ✓ |
| 1d_fill_42 | `paint(x, scan(paint(x, segment(x))))` | 70.0 | ✓ |
| 1d_fill_43 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.8 | ✓ |
| 1d_fill_44 | `paint(x, local(paint(x, scan(x))))` | 64.4 | ✓ |
| 1d_fill_45 | `paint(x, local(paint(x, scan(x))))` | 74.5 | ✓ |
| 1d_fill_46 | `paint(paint(x, scan(x)), local(shift(x)))` | 36.5 | ✓ |
| 1d_fill_47 | `paint(x, scan(paint(x, scan(x))))` | 47.7 | ✓ |
| 1d_fill_48 | `paint(shift(paint(x, scan(x))), local(x))` | 85.9 | ✓ |
| 1d_fill_49 | `paint(paint(shift(x), scan(x)), local(x))` | 46.9 | ✗ |
| 1d_fill_5 | `paint(paint(shift(x), scan(x)), local(x))` | 76.6 | ✓ |
| 1d_fill_6 | `paint(paint(x, scan(x)), segment(x))` | 55.9 | ✓ |
| 1d_fill_7 | `paint(paint(x, scan(x)), local(x))` | 28.2 | ✓ |
| 1d_fill_8 | `paint(paint(x, scan(x)), local(shift(x)))` | 48.2 | ✓ |
| 1d_fill_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.2 | ✓ |
| 1d_flip_0 | `paint(x, local(paint(x, scan(x))))` | 75.2 | ✗ |
| 1d_flip_1 | `paint(paint(shift(x), local(x)), scan(x))` | 83.7 | ✗ |
| 1d_flip_10 | `paint(paint(x, local(x)), local(x))` | 73.0 | ✓ |
| 1d_flip_11 | `paint(paint(shift(x), local(x)), local(x))` | 81.5 | ✗ |
| 1d_flip_12 | `paint(shift(paint(x, segment(x))), local(x))` | 81.8 | ✗ |
| 1d_flip_13 | `paint(shift(shift(x)), scan(x))` | 89.6 | ✗ |
| 1d_flip_14 | `paint(paint(shift(x), local(x)), local(x))` | 77.4 | ✗ |
| 1d_flip_15 | `paint(paint(shift(x), local(x)), local(x))` | 83.1 | ✗ |
| 1d_flip_16 | `paint(shift(x), local(paint(x, segment(x))))` | 82.2 | ✗ |
| 1d_flip_17 | `paint(paint(shift(x), local(x)), scan(x))` | 89.1 | ✗ |
| 1d_flip_18 | `paint(shift(x), local(paint(x, segment(x))))` | 87.6 | ✗ |
| 1d_flip_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 90.7 | ✓ |
| 1d_flip_2 | `paint(paint(shift(x), local(x)), local(x))` | 76.0 | ✗ |
| 1d_flip_20 | `paint(recolour(shift(x)), local(x))` | 84.7 | ✗ |
| 1d_flip_21 | `paint(paint(shift(x), scan(x)), local(x))` | 69.3 | ✗ |
| 1d_flip_22 | `paint(shift(paint(x, scan(x))), local(x))` | 97.2 | ✗ |
| 1d_flip_23 | `paint(paint(shift(x), local(x)), local(x))` | 76.2 | ✗ |
| 1d_flip_24 | `paint(paint(shift(x), local(x)), scan(x))` | 84.8 | ✗ |
| 1d_flip_25 | `paint(shift(x), local(x))` | 86.4 | ✗ |
| 1d_flip_26 | `paint(shift(paint(x, local(x))), local(x))` | 82.8 | ✗ |
| 1d_flip_27 | `paint(paint(shift(x), local(x)), scan(x))` | 80.9 | ✗ |
| 1d_flip_28 | `paint(shift(x), local(paint(x, segment(x))))` | 83.8 | ✗ |
| 1d_flip_29 | `paint(shift(x), local(paint(x, segment(x))))` | 73.7 | ✗ |
| 1d_flip_3 | `paint(paint(shift(x), scan(x)), local(x))` | 70.1 | ✓ |
| 1d_flip_30 | `paint(paint(shift(x), local(x)), scan(x))` | 78.3 | ✗ |
| 1d_flip_31 | `paint(reflect(x), local(x))` | 106.5 | ✗ |
| 1d_flip_32 | `paint(paint(shift(x), local(x)), scan(x))` | 78.9 | ✗ |
| 1d_flip_33 | `paint(shift(x), local(paint(x, scan(x))))` | 105.1 | ✓ |
| 1d_flip_34 | `paint(shift(x), local(x))` | 88.5 | ✗ |
| 1d_flip_35 | `paint(paint(shift(x), local(x)), scan(x))` | 90.3 | ✗ |
| 1d_flip_36 | `paint(shift(x), local(paint(x, scan(x))))` | 100.6 | ✗ |
| 1d_flip_37 | `paint(shift(shift(x)), local(x))` | 91.0 | ✗ |
| 1d_flip_38 | `paint(paint(shift(x), local(x)), scan(x))` | 80.7 | ✗ |
| 1d_flip_39 | `paint(paint(x, local(x)), segment(shift(x)))` | 56.0 | ✗ |
| 1d_flip_4 | `paint(x, local(recolour(x)))` | 94.5 | ✗ |
| 1d_flip_40 | `paint(paint(shift(x), local(x)), scan(x))` | 88.0 | ✗ |
| 1d_flip_41 | `paint(shift(x), local(paint(x, segment(x))))` | 75.6 | ✗ |
| 1d_flip_42 | `paint(paint(shift(x), local(x)), local(x))` | 95.3 | ✗ |
| 1d_flip_43 | `paint(shift(x), local(paint(x, segment(x))))` | 94.4 | ✗ |
| 1d_flip_44 | `paint(paint(shift(x), local(x)), scan(x))` | 81.8 | ✗ |
| 1d_flip_45 | `paint(x, scan(paint(x, local(shift(x)))))` | 89.0 | ✗ |
| 1d_flip_46 | `paint(paint(shift(x), local(x)), local(x))` | 70.9 | ✗ |
| 1d_flip_47 | `paint(x, local(paint(x, scan(x))))` | 68.1 | ✗ |
| 1d_flip_48 | `paint(shift(x), local(x))` | 90.7 | ✗ |
| 1d_flip_49 | `paint(paint(x, local(x)), scan(x))` | 61.8 | ✗ |
| 1d_flip_5 | `paint(paint(x, local(x)), local(x))` | 79.2 | ✗ |
| 1d_flip_6 | `paint(paint(shift(x), local(x)), local(x))` | 97.5 | ✗ |
| 1d_flip_7 | `paint(paint(shift(x), local(x)), local(x))` | 82.1 | ✓ |
| 1d_flip_8 | `paint(paint(shift(x), segment(x)), local(x))` | 68.4 | ✓ |
| 1d_flip_9 | `paint(shift(x), local(paint(x, segment(x))))` | 86.7 | ✗ |
| 1d_hollow_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 41.7 | ✓ |
| 1d_hollow_1 | `paint(paint(x, local(x)), segment(x))` | 43.4 | ✓ |
| 1d_hollow_10 | `paint(paint(shift(x), segment(x)), local(x))` | 62.4 | ✓ |
| 1d_hollow_11 | `paint(paint(x, local(x)), segment(shift(x)))` | 36.7 | ✓ |
| 1d_hollow_12 | `paint(recolour(shift(x)), scan(x))` | 62.4 | ✓ |
| 1d_hollow_13 | `paint(paint(x, scan(x)), segment(x))` | 41.4 | ✓ |
| 1d_hollow_14 | `paint(paint(x, segment(x)), local(x))` | 39.7 | ✓ |
| 1d_hollow_15 | `recolour(paint(x, segment(x)))` | 65.6 | ✓ |
| 1d_hollow_16 | `paint(paint(x, local(x)), segment(shift(x)))` | 53.6 | ✓ |
| 1d_hollow_17 | `paint(paint(shift(x), scan(x)), local(x))` | 35.8 | ✓ |
| 1d_hollow_18 | `paint(paint(x, local(x)), segment(shift(x)))` | 49.5 | ✓ |
| 1d_hollow_19 | `paint(x, scan(x))` | 75.2 | ✓ |
| 1d_hollow_2 | `paint(paint(x, segment(x)), scan(x))` | 56.7 | ✓ |
| 1d_hollow_20 | `paint(paint(x, local(x)), local(x))` | 52.7 | ✓ |
| 1d_hollow_21 | `paint(paint(x, scan(x)), scan(x))` | 44.2 | ✓ |
| 1d_hollow_22 | `paint(x, scan(shift(x)))` | 78.3 | ✓ |
| 1d_hollow_23 | `recolour(paint(x, scan(x)))` | 60.0 | ✓ |
| 1d_hollow_24 | `paint(paint(x, local(x)), segment(x))` | 73.8 | ✓ |
| 1d_hollow_25 | `paint(paint(x, local(x)), segment(shift(x)))` | 48.1 | ✓ |
| 1d_hollow_26 | `paint(paint(x, local(x)), segment(shift(x)))` | 49.5 | ✓ |
| 1d_hollow_27 | `paint(x, scan(shift(x)))` | 58.6 | ✓ |
| 1d_hollow_28 | `paint(paint(x, local(x)), scan(shift(x)))` | 57.4 | ✓ |
| 1d_hollow_29 | `paint(paint(x, scan(x)), segment(x))` | 47.9 | ✓ |
| 1d_hollow_3 | `paint(paint(x, local(x)), scan(x))` | 45.5 | ✓ |
| 1d_hollow_30 | `paint(paint(x, scan(x)), local(shift(x)))` | 56.6 | ✓ |
| 1d_hollow_31 | `paint(paint(x, segment(x)), segment(x))` | 54.4 | ✓ |
| 1d_hollow_32 | `recolour(paint(x, scan(x)))` | 71.8 | ✓ |
| 1d_hollow_33 | `paint(paint(x, local(x)), segment(shift(x)))` | 39.6 | ✓ |
| 1d_hollow_34 | `paint(paint(shift(x), scan(x)), local(x))` | 45.4 | ✓ |
| 1d_hollow_35 | `paint(paint(x, local(x)), segment(shift(x)))` | 46.9 | ✓ |
| 1d_hollow_36 | `paint(paint(x, local(x)), scan(x))` | 67.5 | ✓ |
| 1d_hollow_37 | `paint(paint(x, segment(x)), local(x))` | 50.3 | ✓ |
| 1d_hollow_38 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.5 | ✓ |
| 1d_hollow_39 | `paint(paint(x, local(x)), segment(shift(x)))` | 56.7 | ✓ |
| 1d_hollow_4 | `paint(x, local(paint(shift(x), local(x))))` | 64.4 | ✗ |
| 1d_hollow_40 | `paint(paint(x, local(x)), segment(shift(x)))` | 40.4 | ✓ |
| 1d_hollow_41 | `paint(paint(x, segment(x)), local(x))` | 61.1 | ✓ |
| 1d_hollow_42 | `paint(paint(x, segment(shift(x))), local(x))` | 55.1 | ✓ |
| 1d_hollow_43 | `recolour(paint(x, scan(x)))` | 66.0 | ✓ |
| 1d_hollow_44 | `paint(paint(x, scan(x)), scan(x))` | 57.4 | ✓ |
| 1d_hollow_45 | `paint(paint(x, local(x)), segment(shift(x)))` | 51.6 | ✓ |
| 1d_hollow_46 | `paint(paint(x, segment(x)), local(x))` | 65.0 | ✓ |
| 1d_hollow_47 | `paint(shift(x), segment(paint(x, local(x))))` | 64.2 | ✓ |
| 1d_hollow_48 | `paint(paint(shift(x), scan(x)), local(x))` | 44.4 | ✓ |
| 1d_hollow_49 | `recolour(paint(x, scan(x)))` | 62.9 | ✓ |
| 1d_hollow_5 | `paint(paint(x, local(x)), segment(shift(x)))` | 45.2 | ✓ |
| 1d_hollow_6 | `paint(paint(x, local(x)), segment(shift(x)))` | 50.4 | ✓ |
| 1d_hollow_7 | `paint(paint(x, segment(x)), local(x))` | 70.5 | ✓ |
| 1d_hollow_8 | `paint(paint(x, segment(x)), local(x))` | 58.0 | ✓ |
| 1d_hollow_9 | `paint(paint(x, local(x)), segment(shift(x)))` | 28.9 | ✓ |
| 1d_mirror_0 | `paint(paint(x, local(x)), scan(shift(x)))` | 187.4 | ✗ |
| 1d_mirror_1 | `reflect(shift(x))` | 86.9 | ✗ |
| 1d_mirror_10 | `reflect(shift(shift(x)))` | 111.6 | ✗ |
| 1d_mirror_11 | `paint(paint(x, scan(x)), segment(x))` | 178.5 | ✗ |
| 1d_mirror_12 | `shift(shift(reflect(x)))` | 127.5 | ✗ |
| 1d_mirror_13 | `paint(paint(x, scan(x)), segment(x))` | 149.2 | ✗ |
| 1d_mirror_14 | `reflect(shift(shift(x)))` | 111.5 | ✗ |
| 1d_mirror_15 | `reflect(shift(x))` | 96.8 | ✗ |
| 1d_mirror_16 | `paint(paint(x, local(x)), segment(shift(x)))` | 167.1 | ✗ |
| 1d_mirror_17 | `shift(reflect(x))` | 69.6 | ✗ |
| 1d_mirror_18 | `shift(reflect(x))` | 86.8 | ✗ |
| 1d_mirror_19 | `reflect(shift(x))` | 88.3 | ✗ |
| 1d_mirror_2 | `shift(shift(reflect(x)))` | 141.3 | ✗ |
| 1d_mirror_20 | `recolour(paint(x, local(shift(x))))` | 136.4 | ✗ |
| 1d_mirror_21 | `shift(reflect(x))` | 83.7 | ✗ |
| 1d_mirror_22 | `paint(x, local(shift(shift(x))))` | 146.2 | ✓ |
| 1d_mirror_23 | `reflect(shift(shift(x)))` | 116.9 | ✗ |
| 1d_mirror_24 | `paint(paint(x, scan(x)), segment(x))` | 145.7 | ✗ |
| 1d_mirror_25 | `paint(paint(x, segment(x)), scan(x))` | 171.0 | ✗ |
| 1d_mirror_26 | `paint(paint(x, scan(x)), segment(x))` | 131.6 | ✗ |
| 1d_mirror_27 | `paint(x, segment(paint(x, segment(x))))` | 143.5 | ✗ |
| 1d_mirror_28 | `reflect(shift(x))` | 87.1 | ✓ |
| 1d_mirror_29 | `paint(x, segment(x))` | 130.4 | ✗ |
| 1d_mirror_3 | `paint(paint(x, scan(x)), segment(x))` | 137.7 | ✗ |
| 1d_mirror_30 | `paint(x, scan(shift(x)))` | 173.0 | ✗ |
| 1d_mirror_31 | `reflect(paint(x, local(x)))` | 60.1 | ✗ |
| 1d_mirror_32 | `reflect(shift(x))` | 76.7 | ✗ |
| 1d_mirror_33 | `reflect(shift(shift(x)))` | 119.8 | ✗ |
| 1d_mirror_34 | `shift(reflect(x))` | 76.9 | ✗ |
| 1d_mirror_35 | `paint(shift(paint(x, local(x))), scan(x))` | 165.5 | ✗ |
| 1d_mirror_36 | `shift(shift(reflect(x)))` | 144.9 | ✗ |
| 1d_mirror_37 | `paint(paint(x, local(x)), local(shift(x)))` | 109.0 | ✗ |
| 1d_mirror_38 | `paint(x, scan(shift(x)))` | 186.7 | ✗ |
| 1d_mirror_39 | `reflect(shift(shift(x)))` | 146.6 | ✗ |
| 1d_mirror_4 | `paint(paint(x, scan(x)), segment(x))` | 171.8 | ✗ |
| 1d_mirror_40 | `shift(reflect(x))` | 89.4 | ✗ |
| 1d_mirror_41 | `shift(reflect(x))` | 77.1 | ✗ |
| 1d_mirror_42 | `paint(paint(x, local(x)), scan(shift(x)))` | 137.2 | ✗ |
| 1d_mirror_43 | `shift(reflect(x))` | 89.4 | ✗ |
| 1d_mirror_44 | `reflect(shift(x))` | 89.9 | ✗ |
| 1d_mirror_45 | `paint(paint(x, local(x)), local(shift(x)))` | 108.8 | ✗ |
| 1d_mirror_46 | `paint(paint(x, local(shift(x))), local(x))` | 86.4 | ✓ |
| 1d_mirror_47 | `paint(paint(x, scan(x)), segment(x))` | 123.4 | ✗ |
| 1d_mirror_48 | `shift(shift(reflect(x)))` | 136.9 | ✗ |
| 1d_mirror_49 | `paint(x, segment(x))` | 146.2 | ✗ |
| 1d_mirror_5 | `paint(paint(x, scan(x)), segment(x))` | 177.5 | ✗ |
| 1d_mirror_6 | `paint(x, local(reflect(x)))` | 96.7 | ✗ |
| 1d_mirror_7 | `paint(x, local(paint(shift(x), local(x))))` | 97.7 | ✗ |
| 1d_mirror_8 | `paint(x, segment(x))` | 147.2 | ✗ |
| 1d_mirror_9 | `paint(paint(x, scan(x)), segment(x))` | 149.6 | ✗ |
| 1d_move_1p_0 | `paint(shift(paint(x, scan(x))), local(x))` | 48.8 | ✓ |
| 1d_move_1p_1 | `paint(shift(paint(x, scan(x))), local(x))` | 42.1 | ✓ |
| 1d_move_1p_10 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_11 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_12 | `paint(shift(paint(x, scan(x))), local(x))` | 46.0 | ✓ |
| 1d_move_1p_13 | `paint(shift(x), local(recolour(x)))` | 48.1 | ✓ |
| 1d_move_1p_14 | `shift(x)` | 53.5 | ✓ |
| 1d_move_1p_15 | `paint(shift(x), local(x))` | 51.6 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 53.0 | ✓ |
| 1d_move_1p_17 | `paint(shift(paint(x, scan(x))), local(x))` | 49.1 | ✓ |
| 1d_move_1p_18 | `paint(paint(shift(x), segment(x)), local(x))` | 48.9 | ✗ |
| 1d_move_1p_19 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_2 | `paint(shift(x), local(x))` | 47.2 | ✓ |
| 1d_move_1p_20 | `paint(shift(shift(x)), local(x))` | 49.9 | ✓ |
| 1d_move_1p_21 | `paint(paint(shift(x), segment(x)), local(x))` | 44.7 | ✓ |
| 1d_move_1p_22 | `paint(shift(x), local(x))` | 51.5 | ✓ |
| 1d_move_1p_23 | `paint(shift(x), local(x))` | 47.6 | ✓ |
| 1d_move_1p_24 | `shift(x)` | 51.8 | ✓ |
| 1d_move_1p_25 | `paint(shift(x), scan(x))` | 43.3 | ✓ |
| 1d_move_1p_26 | `paint(paint(shift(x), segment(x)), local(x))` | 37.2 | ✓ |
| 1d_move_1p_27 | `shift(x)` | 56.0 | ✓ |
| 1d_move_1p_28 | `paint(recolour(shift(x)), scan(x))` | 40.2 | ✓ |
| 1d_move_1p_29 | `paint(shift(x), local(x))` | 53.6 | ✓ |
| 1d_move_1p_3 | `paint(recolour(shift(x)), local(x))` | 46.7 | ✓ |
| 1d_move_1p_30 | `shift(x)` | 54.3 | ✓ |
| 1d_move_1p_31 | `paint(shift(x), local(x))` | 48.9 | ✓ |
| 1d_move_1p_32 | `paint(shift(x), scan(x))` | 53.9 | ✓ |
| 1d_move_1p_33 | `shift(x)` | 52.1 | ✓ |
| 1d_move_1p_34 | `shift(x)` | 53.7 | ✓ |
| 1d_move_1p_35 | `shift(x)` | 52.0 | ✓ |
| 1d_move_1p_36 | `paint(shift(paint(x, scan(x))), local(x))` | 47.2 | ✓ |
| 1d_move_1p_37 | `paint(shift(x), local(x))` | 38.3 | ✓ |
| 1d_move_1p_38 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_39 | `shift(x)` | 55.6 | ✓ |
| 1d_move_1p_4 | `paint(shift(x), local(x))` | 45.4 | ✓ |
| 1d_move_1p_40 | `paint(shift(paint(x, scan(x))), local(x))` | 46.6 | ✓ |
| 1d_move_1p_41 | `paint(shift(paint(x, local(x))), local(x))` | 47.3 | ✓ |
| 1d_move_1p_42 | `paint(shift(paint(x, scan(x))), local(x))` | 40.7 | ✓ |
| 1d_move_1p_43 | `paint(shift(paint(x, local(x))), local(x))` | 53.6 | ✓ |
| 1d_move_1p_44 | `paint(shift(x), segment(x))` | 50.5 | ✗ |
| 1d_move_1p_45 | `paint(paint(shift(x), segment(x)), local(x))` | 48.0 | ✓ |
| 1d_move_1p_46 | `paint(shift(x), local(x))` | 50.1 | ✓ |
| 1d_move_1p_47 | `paint(shift(paint(x, scan(x))), local(x))` | 53.0 | ✓ |
| 1d_move_1p_48 | `shift(x)` | 54.0 | ✓ |
| 1d_move_1p_49 | `paint(paint(shift(x), segment(x)), local(x))` | 50.4 | ✓ |
| 1d_move_1p_5 | `shift(x)` | 50.9 | ✓ |
| 1d_move_1p_6 | `paint(paint(shift(x), segment(x)), local(x))` | 45.4 | ✓ |
| 1d_move_1p_7 | `paint(shift(x), local(paint(x, segment(x))))` | 49.9 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_9 | `paint(paint(shift(x), segment(x)), local(x))` | 45.6 | ✓ |
| 1d_move_2p_0 | `paint(shift(paint(x, local(x))), local(x))` | 40.2 | ✓ |
| 1d_move_2p_1 | `shift(x)` | 46.0 | ✓ |
| 1d_move_2p_10 | `shift(x)` | 46.3 | ✓ |
| 1d_move_2p_11 | `shift(x)` | 46.3 | ✓ |
| 1d_move_2p_12 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_13 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_14 | `shift(x)` | 47.0 | ✓ |
| 1d_move_2p_15 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_16 | `shift(x)` | 46.9 | ✓ |
| 1d_move_2p_17 | `paint(shift(paint(x, local(x))), local(x))` | 46.6 | ✓ |
| 1d_move_2p_18 | `paint(paint(x, local(x)), scan(shift(x)))` | 47.6 | ✗ |
| 1d_move_2p_19 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_2 | `shift(x)` | 46.0 | ✓ |
| 1d_move_2p_20 | `shift(x)` | 46.9 | ✓ |
| 1d_move_2p_21 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_22 | `shift(x)` | 47.4 | ✓ |
| 1d_move_2p_23 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_24 | `shift(x)` | 45.6 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_26 | `shift(x)` | 46.0 | ✓ |
| 1d_move_2p_27 | `shift(x)` | 48.6 | ✓ |
| 1d_move_2p_28 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_29 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_3 | `paint(shift(paint(x, local(x))), local(x))` | 39.9 | ✓ |
| 1d_move_2p_30 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_31 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_32 | `shift(x)` | 47.6 | ✓ |
| 1d_move_2p_33 | `shift(x)` | 46.1 | ✓ |
| 1d_move_2p_34 | `shift(x)` | 47.3 | ✓ |
| 1d_move_2p_35 | `shift(x)` | 46.0 | ✓ |
| 1d_move_2p_36 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_37 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_38 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_39 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_4 | `shift(x)` | 46.0 | ✓ |
| 1d_move_2p_40 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.0 | ✓ |
| 1d_move_2p_42 | `paint(shift(paint(x, local(x))), local(x))` | 47.1 | ✓ |
| 1d_move_2p_43 | `paint(paint(shift(x), local(x)), segment(x))` | 42.6 | ✓ |
| 1d_move_2p_44 | `shift(x)` | 53.7 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 47.4 | ✓ |
| 1d_move_2p_46 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.0 | ✓ |
| 1d_move_2p_48 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_49 | `paint(paint(shift(x), segment(x)), local(x))` | 40.4 | ✓ |
| 1d_move_2p_5 | `shift(x)` | 44.8 | ✓ |
| 1d_move_2p_6 | `paint(paint(shift(x), local(x)), segment(x))` | 43.7 | ✓ |
| 1d_move_2p_7 | `shift(x)` | 52.9 | ✓ |
| 1d_move_2p_8 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_9 | `paint(paint(shift(x), local(x)), segment(x))` | 43.3 | ✓ |
| 1d_move_2p_dp_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 55.7 | ✗ |
| 1d_move_2p_dp_1 | `paint(shift(paint(x, scan(x))), local(x))` | 72.6 | ✓ |
| 1d_move_2p_dp_10 | `paint(shift(x), local(x))` | 71.0 | ✓ |
| 1d_move_2p_dp_11 | `paint(paint(x, local(x)), scan(shift(x)))` | 58.6 | ✓ |
| 1d_move_2p_dp_12 | `paint(paint(shift(x), segment(x)), local(x))` | 62.2 | ✓ |
| 1d_move_2p_dp_13 | `paint(paint(shift(x), segment(x)), local(x))` | 53.5 | ✓ |
| 1d_move_2p_dp_14 | `paint(paint(x, local(x)), segment(shift(x)))` | 56.5 | ✓ |
| 1d_move_2p_dp_15 | `paint(paint(x, local(x)), local(shift(x)))` | 53.9 | ✓ |
| 1d_move_2p_dp_16 | `paint(paint(x, local(x)), local(shift(x)))` | 60.1 | ✓ |
| 1d_move_2p_dp_17 | `paint(paint(x, local(x)), local(shift(x)))` | 61.8 | ✓ |
| 1d_move_2p_dp_18 | `paint(x, local(paint(x, scan(shift(x)))))` | 67.1 | ✓ |
| 1d_move_2p_dp_19 | `paint(paint(x, local(x)), local(shift(x)))` | 51.0 | ✓ |
| 1d_move_2p_dp_2 | `paint(paint(x, local(x)), segment(shift(x)))` | 56.0 | ✓ |
| 1d_move_2p_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 56.6 | ✗ |
| 1d_move_2p_dp_21 | `paint(shift(x), local(paint(x, local(x))))` | 72.8 | ✗ |
| 1d_move_2p_dp_22 | `paint(shift(paint(x, scan(x))), local(x))` | 74.8 | ✓ |
| 1d_move_2p_dp_23 | `paint(paint(shift(x), segment(x)), local(x))` | 66.9 | ✓ |
| 1d_move_2p_dp_24 | `paint(x, local(shift(paint(x, segment(x)))))` | 57.0 | ✓ |
| 1d_move_2p_dp_25 | `paint(paint(shift(x), local(x)), scan(x))` | 58.9 | ✓ |
| 1d_move_2p_dp_26 | `paint(paint(x, local(x)), segment(shift(x)))` | 47.0 | ✓ |
| 1d_move_2p_dp_27 | `paint(paint(x, scan(x)), local(x))` | 55.3 | ✓ |
| 1d_move_2p_dp_28 | `paint(paint(x, local(x)), scan(shift(x)))` | 60.4 | ✓ |
| 1d_move_2p_dp_29 | `paint(paint(x, local(x)), segment(x))` | 74.5 | ✓ |
| 1d_move_2p_dp_3 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.9 | ✓ |
| 1d_move_2p_dp_30 | `paint(paint(x, local(x)), local(shift(x)))` | 54.9 | ✓ |
| 1d_move_2p_dp_31 | `paint(paint(x, local(x)), segment(x))` | 63.1 | ✓ |
| 1d_move_2p_dp_32 | `shift(paint(x, local(recolour(x))))` | 77.1 | ✗ |
| 1d_move_2p_dp_33 | `paint(x, local(x))` | 62.4 | ✓ |
| 1d_move_2p_dp_34 | `shift(paint(paint(x, local(x)), local(x)))` | 76.3 | ✗ |
| 1d_move_2p_dp_35 | `paint(shift(x), local(x))` | 78.6 | ✓ |
| 1d_move_2p_dp_36 | `paint(paint(x, local(x)), local(shift(x)))` | 59.9 | ✓ |
| 1d_move_2p_dp_37 | `shift(paint(x, local(recolour(x))))` | 75.6 | ✗ |
| 1d_move_2p_dp_38 | `paint(paint(x, local(x)), segment(shift(x)))` | 53.9 | ✓ |
| 1d_move_2p_dp_39 | `paint(paint(x, local(x)), scan(x))` | 54.0 | ✓ |
| 1d_move_2p_dp_4 | `paint(shift(x), local(x))` | 75.9 | ✓ |
| 1d_move_2p_dp_40 | `paint(paint(x, local(x)), segment(shift(x)))` | 57.5 | ✓ |
| 1d_move_2p_dp_41 | `paint(shift(paint(x, scan(x))), local(x))` | 82.4 | ✓ |
| 1d_move_2p_dp_42 | `paint(paint(x, local(x)), local(shift(x)))` | 62.5 | ✓ |
| 1d_move_2p_dp_43 | `paint(shift(x), local(x))` | 63.0 | ✓ |
| 1d_move_2p_dp_44 | `paint(paint(shift(x), scan(x)), local(x))` | 53.8 | ✓ |
| 1d_move_2p_dp_45 | `paint(x, local(paint(x, local(x))))` | 55.5 | ✓ |
| 1d_move_2p_dp_46 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.9 | ✓ |
| 1d_move_2p_dp_47 | `paint(paint(x, local(x)), scan(shift(x)))` | 68.7 | ✗ |
| 1d_move_2p_dp_48 | `paint(paint(x, local(x)), local(shift(x)))` | 52.8 | ✓ |
| 1d_move_2p_dp_49 | `paint(paint(x, local(x)), local(shift(x)))` | 56.3 | ✓ |
| 1d_move_2p_dp_5 | `paint(paint(x, local(x)), local(shift(x)))` | 58.4 | ✗ |
| 1d_move_2p_dp_6 | `paint(paint(x, local(x)), local(shift(x)))` | 57.1 | ✓ |
| 1d_move_2p_dp_7 | `shift(paint(paint(x, local(x)), local(x)))` | 79.0 | ✗ |
| 1d_move_2p_dp_8 | `recolour(paint(x, local(x)))` | 55.1 | ✗ |
| 1d_move_2p_dp_9 | `paint(paint(x, local(x)), segment(shift(x)))` | 42.5 | ✓ |
| 1d_move_3p_0 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_1 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_10 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_11 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_12 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_13 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_14 | `paint(shift(x), local(x))` | 51.3 | ✓ |
| 1d_move_3p_15 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_16 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_17 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_18 | `paint(paint(x, local(x)), local(shift(x)))` | 53.4 | ✗ |
| 1d_move_3p_19 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_2 | `paint(shift(x), local(x))` | 45.8 | ✓ |
| 1d_move_3p_20 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_21 | `paint(paint(shift(x), local(x)), scan(x))` | 41.8 | ✓ |
| 1d_move_3p_22 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_23 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.1 | ✓ |
| 1d_move_3p_24 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_25 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_26 | `paint(paint(shift(x), scan(x)), local(x))` | 53.2 | ✓ |
| 1d_move_3p_27 | `shift(x)` | 54.1 | ✓ |
| 1d_move_3p_28 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_29 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_3 | `paint(shift(x), local(x))` | 52.0 | ✓ |
| 1d_move_3p_30 | `paint(recolour(shift(x)), local(x))` | 45.8 | ✓ |
| 1d_move_3p_31 | `paint(paint(x, local(x)), segment(shift(x)))` | 45.9 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_35 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_36 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_37 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_38 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_39 | `shift(x)` | 52.7 | ✓ |
| 1d_move_3p_4 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_40 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_41 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_43 | `paint(paint(x, local(x)), scan(shift(x)))` | 48.8 | ✓ |
| 1d_move_3p_44 | `paint(recolour(shift(x)), local(x))` | 55.5 | ✓ |
| 1d_move_3p_45 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_46 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_47 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_48 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_49 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_5 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_6 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_7 | `shift(x)` | 56.5 | ✓ |
| 1d_move_3p_8 | `shift(x)` | 52.3 | ✓ |
| 1d_move_3p_9 | `shift(x)` | 54.0 | ✓ |
| 1d_move_dp_0 | `paint(x, local(reflect(x)))` | 95.9 | ✗ |
| 1d_move_dp_1 | `paint(x, scan(paint(x, local(x))))` | 138.6 | ✗ |
| 1d_move_dp_10 | `shift(shift(x))` | 119.5 | ✗ |
| 1d_move_dp_11 | `shift(shift(x))` | 118.7 | ✗ |
| 1d_move_dp_12 | `paint(reflect(x), local(x))` | 100.4 | ✗ |
| 1d_move_dp_13 | `paint(paint(x, scan(x)), segment(x))` | 98.2 | ✗ |
| 1d_move_dp_14 | `paint(paint(x, local(x)), local(shift(x)))` | 59.7 | ✗ |
| 1d_move_dp_15 | `paint(paint(x, local(x)), scan(x))` | 125.2 | ✗ |
| 1d_move_dp_16 | `shift(recolour(paint(x, local(x))))` | 115.9 | ✗ |
| 1d_move_dp_17 | `paint(x, local(reflect(x)))` | 105.4 | ✓ |
| 1d_move_dp_18 | `shift(x)` | 105.2 | ✗ |
| 1d_move_dp_19 | `paint(x, local(reflect(x)))` | 90.1 | ✗ |
| 1d_move_dp_2 | `paint(paint(x, scan(x)), local(x))` | 146.0 | ✗ |
| 1d_move_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 67.7 | ✗ |
| 1d_move_dp_21 | `paint(x, scan(x))` | 131.5 | ✗ |
| 1d_move_dp_22 | `paint(x, local(shift(x)))` | 115.3 | ✗ |
| 1d_move_dp_23 | `paint(x, scan(paint(x, local(shift(x)))))` | 129.5 | ✗ |
| 1d_move_dp_24 | `paint(x, scan(reflect(x)))` | 125.7 | ✗ |
| 1d_move_dp_25 | `paint(paint(x, scan(x)), segment(x))` | 105.7 | ✗ |
| 1d_move_dp_26 | `paint(paint(x, scan(x)), segment(x))` | 126.2 | ✗ |
| 1d_move_dp_27 | `shift(paint(x, scan(x)))` | 80.8 | ✗ |
| 1d_move_dp_28 | `paint(paint(x, local(x)), scan(x))` | 109.4 | ✗ |
| 1d_move_dp_29 | `reflect(paint(x, local(x)))` | 117.3 | ✗ |
| 1d_move_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 101.3 | ✗ |
| 1d_move_dp_30 | `paint(paint(x, local(x)), segment(x))` | 70.8 | ✗ |
| 1d_move_dp_31 | `paint(shift(x), scan(paint(x, local(x))))` | 129.7 | ✗ |
| 1d_move_dp_32 | `paint(paint(x, scan(x)), local(x))` | 137.7 | ✗ |
| 1d_move_dp_33 | `recolour(paint(x, local(shift(x))))` | 99.2 | ✗ |
| 1d_move_dp_34 | `paint(paint(x, local(shift(x))), scan(x))` | 98.4 | ✗ |
| 1d_move_dp_35 | `paint(paint(x, scan(x)), local(x))` | 127.4 | ✗ |
| 1d_move_dp_36 | `paint(paint(x, scan(x)), local(x))` | 112.8 | ✗ |
| 1d_move_dp_37 | `shift(paint(x, local(recolour(x))))` | 71.7 | ✗ |
| 1d_move_dp_38 | `recolour(paint(x, scan(x)))` | 138.4 | ✗ |
| 1d_move_dp_39 | `shift(shift(x))` | 116.6 | ✗ |
| 1d_move_dp_4 | `shift(recolour(paint(x, local(x))))` | 111.5 | ✗ |
| 1d_move_dp_40 | `paint(reflect(x), local(x))` | 83.4 | ✗ |
| 1d_move_dp_41 | `paint(paint(x, local(x)), segment(shift(x)))` | 64.7 | ✗ |
| 1d_move_dp_42 | `paint(paint(shift(x), scan(x)), local(x))` | 161.0 | ✗ |
| 1d_move_dp_43 | `paint(paint(shift(x), local(x)), segment(x))` | 73.1 | ✗ |
| 1d_move_dp_44 | `paint(paint(shift(x), local(x)), local(x))` | 64.9 | ✓ |
| 1d_move_dp_45 | `paint(x, local(paint(x, local(x))))` | 55.5 | ✗ |
| 1d_move_dp_46 | `paint(x, local(reflect(x)))` | 80.3 | ✗ |
| 1d_move_dp_47 | `shift(paint(paint(x, scan(x)), local(x)))` | 125.1 | ✗ |
| 1d_move_dp_48 | `paint(x, local(shift(x)))` | 110.9 | ✓ |
| 1d_move_dp_49 | `paint(x, local(reflect(x)))` | 121.4 | ✗ |
| 1d_move_dp_5 | `paint(paint(x, scan(x)), segment(x))` | 118.5 | ✗ |
| 1d_move_dp_6 | `paint(paint(x, scan(x)), segment(x))` | 120.2 | ✗ |
| 1d_move_dp_7 | `paint(paint(shift(x), local(x)), local(x))` | 55.3 | ✓ |
| 1d_move_dp_8 | `paint(paint(x, local(x)), local(shift(x)))` | 60.1 | ✗ |
| 1d_move_dp_9 | `paint(paint(x, scan(x)), segment(x))` | 128.2 | ✗ |
| 1d_padded_fill_0 | `paint(paint(x, scan(x)), segment(x))` | 58.2 | ✓ |
| 1d_padded_fill_1 | `paint(paint(x, scan(x)), segment(x))` | 47.6 | ✓ |
| 1d_padded_fill_10 | `recolour(paint(x, scan(x)))` | 74.8 | ✓ |
| 1d_padded_fill_11 | `paint(paint(x, scan(x)), segment(x))` | 48.6 | ✓ |
| 1d_padded_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 56.4 | ✓ |
| 1d_padded_fill_13 | `paint(paint(x, scan(x)), segment(x))` | 61.9 | ✓ |
| 1d_padded_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 39.4 | ✓ |
| 1d_padded_fill_15 | `paint(paint(x, scan(x)), local(x))` | 41.9 | ✓ |
| 1d_padded_fill_16 | `recolour(paint(x, scan(x)))` | 46.7 | ✓ |
| 1d_padded_fill_17 | `paint(paint(x, scan(x)), segment(x))` | 59.1 | ✓ |
| 1d_padded_fill_18 | `paint(paint(x, scan(x)), local(x))` | 47.0 | ✓ |
| 1d_padded_fill_19 | `paint(paint(shift(x), scan(x)), local(x))` | 62.1 | ✗ |
| 1d_padded_fill_2 | `paint(paint(shift(x), scan(x)), local(x))` | 55.6 | ✓ |
| 1d_padded_fill_20 | `paint(paint(x, scan(x)), segment(x))` | 53.4 | ✓ |
| 1d_padded_fill_21 | `paint(x, scan(paint(x, scan(x))))` | 65.1 | ✓ |
| 1d_padded_fill_22 | `paint(paint(x, local(x)), scan(x))` | 54.8 | ✓ |
| 1d_padded_fill_23 | `paint(paint(x, scan(x)), segment(x))` | 44.7 | ✓ |
| 1d_padded_fill_24 | `paint(paint(x, scan(x)), segment(x))` | 40.0 | ✓ |
| 1d_padded_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 47.0 | ✓ |
| 1d_padded_fill_26 | `recolour(paint(x, scan(x)))` | 84.3 | ✓ |
| 1d_padded_fill_27 | `paint(x, scan(paint(x, scan(x))))` | 59.0 | ✓ |
| 1d_padded_fill_28 | `paint(paint(x, scan(x)), segment(x))` | 45.3 | ✓ |
| 1d_padded_fill_29 | `paint(paint(x, scan(x)), segment(x))` | 48.8 | ✓ |
| 1d_padded_fill_3 | `recolour(paint(x, scan(x)))` | 50.7 | ✓ |
| 1d_padded_fill_30 | `recolour(paint(x, scan(x)))` | 61.3 | ✓ |
| 1d_padded_fill_31 | `paint(paint(x, scan(x)), local(x))` | 54.2 | ✓ |
| 1d_padded_fill_32 | `paint(paint(x, scan(x)), local(shift(x)))` | 54.5 | ✓ |
| 1d_padded_fill_33 | `recolour(paint(x, scan(x)))` | 54.0 | ✓ |
| 1d_padded_fill_34 | `paint(paint(x, scan(x)), local(shift(x)))` | 33.2 | ✓ |
| 1d_padded_fill_35 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.0 | ✓ |
| 1d_padded_fill_36 | `paint(x, scan(paint(x, scan(x))))` | 65.5 | ✓ |
| 1d_padded_fill_37 | `paint(paint(shift(x), scan(x)), local(x))` | 48.0 | ✓ |
| 1d_padded_fill_38 | `paint(paint(x, scan(x)), segment(x))` | 40.7 | ✓ |
| 1d_padded_fill_39 | `recolour(paint(x, scan(x)))` | 63.3 | ✓ |
| 1d_padded_fill_4 | `paint(paint(x, scan(x)), local(x))` | 44.1 | ✓ |
| 1d_padded_fill_40 | `paint(paint(x, scan(x)), local(x))` | 54.0 | ✓ |
| 1d_padded_fill_41 | `paint(paint(x, scan(x)), local(x))` | 41.2 | ✓ |
| 1d_padded_fill_42 | `paint(paint(x, local(x)), scan(x))` | 58.5 | ✓ |
| 1d_padded_fill_43 | `recolour(paint(x, scan(x)))` | 50.5 | ✓ |
| 1d_padded_fill_44 | `paint(paint(x, scan(x)), local(shift(x)))` | 51.9 | ✓ |
| 1d_padded_fill_45 | `paint(paint(x, scan(x)), segment(x))` | 53.0 | ✓ |
| 1d_padded_fill_46 | `paint(paint(x, scan(x)), segment(x))` | 81.7 | ✗ |
| 1d_padded_fill_47 | `paint(paint(x, local(shift(x))), scan(x))` | 53.2 | ✗ |
| 1d_padded_fill_48 | `paint(paint(x, scan(x)), local(x))` | 35.0 | ✓ |
| 1d_padded_fill_49 | `paint(paint(x, scan(x)), segment(x))` | 48.9 | ✓ |
| 1d_padded_fill_5 | `paint(paint(x, scan(x)), segment(x))` | 45.9 | ✓ |
| 1d_padded_fill_6 | `paint(paint(x, scan(x)), local(x))` | 66.2 | ✓ |
| 1d_padded_fill_7 | `recolour(paint(x, scan(x)))` | 58.6 | ✓ |
| 1d_padded_fill_8 | `paint(paint(x, scan(x)), segment(x))` | 51.1 | ✓ |
| 1d_padded_fill_9 | `paint(x, scan(paint(x, scan(x))))` | 50.9 | ✓ |
| 1d_pcopy_1c_0 | `paint(x, local(paint(x, local(x))))` | 80.3 | ✓ |
| 1d_pcopy_1c_1 | `paint(paint(x, local(x)), scan(shift(x)))` | 67.0 | ✓ |
| 1d_pcopy_1c_10 | `paint(paint(shift(x), scan(x)), local(x))` | 69.3 | ✗ |
| 1d_pcopy_1c_11 | `paint(paint(x, segment(x)), local(x))` | 71.9 | ✗ |
| 1d_pcopy_1c_12 | `paint(x, local(paint(x, local(x))))` | 57.8 | ✓ |
| 1d_pcopy_1c_13 | `paint(paint(x, scan(x)), local(x))` | 71.4 | ✗ |
| 1d_pcopy_1c_14 | `paint(paint(x, scan(x)), scan(x))` | 68.4 | ✗ |
| 1d_pcopy_1c_15 | `paint(paint(x, local(x)), scan(shift(x)))` | 54.5 | ✗ |
| 1d_pcopy_1c_16 | `paint(paint(x, segment(x)), local(x))` | 56.4 | ✗ |
| 1d_pcopy_1c_17 | `paint(paint(x, local(x)), scan(shift(x)))` | 63.0 | ✓ |
| 1d_pcopy_1c_18 | `paint(paint(x, scan(x)), local(x))` | 67.3 | ✗ |
| 1d_pcopy_1c_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 72.5 | ✗ |
| 1d_pcopy_1c_2 | `paint(paint(x, scan(x)), local(x))` | 56.6 | ✓ |
| 1d_pcopy_1c_20 | `paint(paint(x, segment(x)), local(x))` | 72.7 | ✗ |
| 1d_pcopy_1c_21 | `paint(paint(x, segment(x)), local(x))` | 72.2 | ✓ |
| 1d_pcopy_1c_22 | `paint(shift(shift(x)), local(x))` | 88.9 | ✓ |
| 1d_pcopy_1c_23 | `paint(paint(x, segment(x)), local(x))` | 70.4 | ✓ |
| 1d_pcopy_1c_24 | `paint(paint(x, local(shift(x))), local(x))` | 73.8 | ✗ |
| 1d_pcopy_1c_25 | `paint(paint(x, scan(x)), local(x))` | 60.5 | ✓ |
| 1d_pcopy_1c_26 | `paint(paint(x, scan(x)), local(x))` | 63.4 | ✗ |
| 1d_pcopy_1c_27 | `paint(paint(x, local(x)), scan(shift(x)))` | 56.7 | ✓ |
| 1d_pcopy_1c_28 | `paint(x, local(paint(x, scan(shift(x)))))` | 88.2 | ✓ |
| 1d_pcopy_1c_29 | `paint(paint(x, segment(x)), local(x))` | 61.0 | ✓ |
| 1d_pcopy_1c_3 | `paint(x, local(paint(x, local(x))))` | 78.2 | ✓ |
| 1d_pcopy_1c_30 | `paint(recolour(x), local(x))` | 77.1 | ✓ |
| 1d_pcopy_1c_31 | `paint(paint(x, local(x)), scan(shift(x)))` | 61.0 | ✓ |
| 1d_pcopy_1c_32 | `paint(x, local(paint(x, scan(x))))` | 70.3 | ✓ |
| 1d_pcopy_1c_33 | `paint(paint(x, local(x)), local(x))` | 85.0 | ✓ |
| 1d_pcopy_1c_34 | `paint(paint(x, segment(x)), local(x))` | 86.2 | ✓ |
| 1d_pcopy_1c_35 | `paint(paint(x, segment(x)), local(x))` | 59.6 | ✗ |
| 1d_pcopy_1c_36 | `paint(paint(x, segment(x)), local(x))` | 77.4 | ✓ |
| 1d_pcopy_1c_37 | `paint(paint(x, segment(x)), local(x))` | 70.8 | ✗ |
| 1d_pcopy_1c_38 | `paint(shift(x), local(x))` | 91.4 | ✓ |
| 1d_pcopy_1c_39 | `paint(recolour(x), local(x))` | 88.0 | ✓ |
| 1d_pcopy_1c_4 | `paint(paint(x, segment(x)), local(x))` | 68.0 | ✗ |
| 1d_pcopy_1c_40 | `paint(x, local(paint(x, scan(x))))` | 77.7 | ✗ |
| 1d_pcopy_1c_41 | `paint(paint(x, local(x)), scan(shift(x)))` | 62.5 | ✗ |
| 1d_pcopy_1c_42 | `paint(x, local(paint(x, scan(x))))` | 68.4 | ✓ |
| 1d_pcopy_1c_43 | `paint(paint(x, segment(x)), local(x))` | 84.4 | ✗ |
| 1d_pcopy_1c_44 | `paint(paint(x, segment(x)), local(x))` | 81.7 | ✗ |
| 1d_pcopy_1c_45 | `paint(x, local(paint(x, scan(x))))` | 74.3 | ✓ |
| 1d_pcopy_1c_46 | `paint(paint(x, local(x)), scan(shift(x)))` | 63.5 | ✗ |
| 1d_pcopy_1c_47 | `paint(paint(x, segment(x)), local(x))` | 72.5 | ✗ |
| 1d_pcopy_1c_48 | `paint(x, local(paint(x, scan(x))))` | 65.5 | ✓ |
| 1d_pcopy_1c_49 | `paint(paint(x, local(x)), scan(shift(x)))` | 68.0 | ✗ |
| 1d_pcopy_1c_5 | `paint(paint(x, segment(x)), local(x))` | 54.3 | ✗ |
| 1d_pcopy_1c_6 | `paint(x, local(x))` | 90.4 | ✗ |
| 1d_pcopy_1c_7 | `paint(paint(x, segment(x)), local(x))` | 89.0 | ✗ |
| 1d_pcopy_1c_8 | `paint(paint(x, segment(x)), local(x))` | 60.8 | ✓ |
| 1d_pcopy_1c_9 | `paint(paint(x, scan(x)), local(x))` | 65.6 | ✓ |
| 1d_pcopy_mc_0 | `paint(paint(x, segment(shift(x))), local(x))` | 44.9 | ✓ |
| 1d_pcopy_mc_1 | `paint(paint(x, segment(x)), local(x))` | 47.4 | ✗ |
| 1d_pcopy_mc_10 | `paint(shift(shift(x)), local(x))` | 75.6 | ✓ |
| 1d_pcopy_mc_11 | `paint(paint(x, segment(x)), local(x))` | 47.5 | ✓ |
| 1d_pcopy_mc_12 | `paint(paint(x, scan(x)), local(x))` | 59.7 | ✓ |
| 1d_pcopy_mc_13 | `paint(paint(x, segment(x)), local(x))` | 65.0 | ✓ |
| 1d_pcopy_mc_14 | `paint(x, local(paint(x, segment(x))))` | 84.5 | ✓ |
| 1d_pcopy_mc_15 | `paint(x, local(paint(x, scan(shift(x)))))` | 66.1 | ✓ |
| 1d_pcopy_mc_16 | `paint(paint(x, segment(shift(x))), local(x))` | 46.1 | ✓ |
| 1d_pcopy_mc_17 | `paint(paint(x, segment(shift(x))), local(x))` | 59.6 | ✓ |
| 1d_pcopy_mc_18 | `paint(paint(x, segment(x)), local(x))` | 38.5 | ✗ |
| 1d_pcopy_mc_19 | `paint(paint(x, segment(x)), local(x))` | 46.2 | ✓ |
| 1d_pcopy_mc_2 | `paint(paint(x, local(shift(x))), local(x))` | 57.6 | ✓ |
| 1d_pcopy_mc_20 | `paint(shift(paint(x, segment(x))), local(x))` | 79.0 | ✓ |
| 1d_pcopy_mc_21 | `paint(paint(x, segment(shift(x))), local(x))` | 49.9 | ✓ |
| 1d_pcopy_mc_22 | `paint(paint(x, segment(shift(x))), local(x))` | 48.2 | ✓ |
| 1d_pcopy_mc_23 | `paint(paint(x, segment(x)), local(x))` | 50.9 | ✓ |
| 1d_pcopy_mc_24 | `paint(shift(x), local(x))` | 89.3 | ✓ |
| 1d_pcopy_mc_25 | `paint(x, local(paint(x, segment(x))))` | 65.0 | ✓ |
| 1d_pcopy_mc_26 | `paint(paint(x, segment(shift(x))), local(x))` | 48.8 | ✓ |
| 1d_pcopy_mc_27 | `paint(paint(x, segment(x)), local(x))` | 65.7 | ✓ |
| 1d_pcopy_mc_28 | `paint(paint(x, segment(x)), local(x))` | 54.7 | ✓ |
| 1d_pcopy_mc_29 | `paint(x, local(paint(x, segment(shift(x)))))` | 56.5 | ✓ |
| 1d_pcopy_mc_3 | `paint(paint(x, segment(x)), local(x))` | 41.9 | ✓ |
| 1d_pcopy_mc_30 | `paint(paint(x, segment(x)), local(x))` | 45.8 | ✗ |
| 1d_pcopy_mc_31 | `paint(paint(x, scan(x)), local(x))` | 54.6 | ✓ |
| 1d_pcopy_mc_32 | `paint(x, local(paint(shift(x), segment(x))))` | 85.4 | ✓ |
| 1d_pcopy_mc_33 | `paint(paint(x, scan(x)), local(x))` | 77.1 | ✓ |
| 1d_pcopy_mc_34 | `paint(paint(x, segment(x)), local(x))` | 74.2 | ✓ |
| 1d_pcopy_mc_35 | `paint(paint(x, segment(shift(x))), local(x))` | 44.1 | ✓ |
| 1d_pcopy_mc_36 | `paint(x, local(paint(x, scan(shift(x)))))` | 57.1 | ✓ |
| 1d_pcopy_mc_37 | `paint(paint(x, scan(x)), local(x))` | 48.9 | ✓ |
| 1d_pcopy_mc_38 | `paint(paint(x, local(shift(x))), local(x))` | 45.9 | ✓ |
| 1d_pcopy_mc_39 | `paint(paint(x, segment(x)), local(x))` | 47.3 | ✓ |
| 1d_pcopy_mc_4 | `paint(paint(x, scan(x)), local(x))` | 59.1 | ✓ |
| 1d_pcopy_mc_40 | `paint(paint(x, segment(x)), local(x))` | 58.4 | ✓ |
| 1d_pcopy_mc_41 | `paint(paint(x, segment(x)), local(x))` | 46.4 | ✓ |
| 1d_pcopy_mc_42 | `paint(paint(x, segment(shift(x))), local(x))` | 53.3 | ✓ |
| 1d_pcopy_mc_43 | `paint(paint(x, segment(x)), local(x))` | 45.6 | ✓ |
| 1d_pcopy_mc_44 | `paint(paint(x, segment(shift(x))), local(x))` | 42.8 | ✓ |
| 1d_pcopy_mc_45 | `paint(paint(x, segment(shift(x))), local(x))` | 44.3 | ✓ |
| 1d_pcopy_mc_46 | `paint(paint(x, local(shift(x))), local(x))` | 52.8 | ✓ |
| 1d_pcopy_mc_47 | `paint(paint(x, scan(x)), local(x))` | 45.5 | ✓ |
| 1d_pcopy_mc_48 | `paint(paint(x, segment(x)), local(x))` | 49.2 | ✓ |
| 1d_pcopy_mc_49 | `paint(x, local(x))` | 66.1 | ✓ |
| 1d_pcopy_mc_5 | `paint(paint(x, segment(x)), local(x))` | 45.6 | ✓ |
| 1d_pcopy_mc_6 | `paint(x, local(paint(x, scan(shift(x)))))` | 51.0 | ✓ |
| 1d_pcopy_mc_7 | `paint(x, local(paint(x, segment(shift(x)))))` | 63.4 | ✓ |
| 1d_pcopy_mc_8 | `paint(paint(x, segment(x)), local(x))` | 46.8 | ✓ |
| 1d_pcopy_mc_9 | `paint(paint(x, scan(x)), local(x))` | 42.2 | ✓ |
| 1d_recolor_cmp_0 | `paint(paint(x, local(x)), segment(x))` | 39.1 | ✓ |
| 1d_recolor_cmp_1 | `recolour(paint(x, segment(x)))` | 58.8 | ✓ |
| 1d_recolor_cmp_10 | `paint(paint(x, segment(x)), segment(x))` | 45.5 | ✓ |
| 1d_recolor_cmp_11 | `paint(paint(x, local(shift(x))), segment(x))` | 45.7 | ✓ |
| 1d_recolor_cmp_12 | `paint(x, segment(recolour(x)))` | 64.0 | ✓ |
| 1d_recolor_cmp_13 | `paint(paint(x, segment(x)), local(x))` | 42.2 | ✓ |
| 1d_recolor_cmp_14 | `recolour(paint(x, segment(x)))` | 62.3 | ✓ |
| 1d_recolor_cmp_15 | `paint(paint(x, scan(x)), segment(x))` | 63.6 | ✓ |
| 1d_recolor_cmp_16 | `paint(paint(x, local(shift(x))), segment(x))` | 46.7 | ✓ |
| 1d_recolor_cmp_17 | `paint(paint(x, scan(x)), segment(x))` | 45.6 | ✓ |
| 1d_recolor_cmp_18 | `paint(paint(x, scan(x)), segment(x))` | 44.8 | ✓ |
| 1d_recolor_cmp_19 | `paint(paint(x, segment(x)), segment(x))` | 41.3 | ✓ |
| 1d_recolor_cmp_2 | `paint(paint(x, local(shift(x))), segment(x))` | 57.1 | ✓ |
| 1d_recolor_cmp_20 | `paint(paint(x, segment(x)), local(x))` | 32.2 | ✓ |
| 1d_recolor_cmp_21 | `paint(paint(x, segment(x)), scan(x))` | 40.2 | ✓ |
| 1d_recolor_cmp_22 | `paint(paint(x, scan(x)), segment(x))` | 50.8 | ✓ |
| 1d_recolor_cmp_23 | `paint(paint(x, segment(x)), segment(x))` | 43.6 | ✓ |
| 1d_recolor_cmp_24 | `recolour(paint(x, segment(x)))` | 46.8 | ✓ |
| 1d_recolor_cmp_25 | `paint(paint(x, scan(x)), segment(x))` | 43.0 | ✓ |
| 1d_recolor_cmp_26 | `paint(paint(x, scan(x)), segment(x))` | 55.0 | ✓ |
| 1d_recolor_cmp_27 | `paint(paint(x, scan(x)), segment(x))` | 45.5 | ✓ |
| 1d_recolor_cmp_28 | `paint(paint(x, segment(x)), segment(x))` | 45.1 | ✓ |
| 1d_recolor_cmp_29 | `paint(paint(x, scan(x)), segment(x))` | 29.4 | ✓ |
| 1d_recolor_cmp_3 | `paint(paint(x, local(shift(x))), segment(x))` | 68.0 | ✓ |
| 1d_recolor_cmp_30 | `paint(x, segment(paint(x, local(x))))` | 93.6 | ✓ |
| 1d_recolor_cmp_31 | `paint(paint(x, segment(x)), local(x))` | 51.7 | ✓ |
| 1d_recolor_cmp_32 | `paint(paint(x, scan(x)), segment(x))` | 53.0 | ✓ |
| 1d_recolor_cmp_33 | `recolour(paint(x, segment(x)))` | 67.0 | ✓ |
| 1d_recolor_cmp_34 | `paint(paint(x, segment(x)), segment(x))` | 43.8 | ✓ |
| 1d_recolor_cmp_35 | `paint(paint(x, scan(x)), segment(x))` | 82.0 | ✓ |
| 1d_recolor_cmp_36 | `paint(paint(x, scan(x)), segment(x))` | 38.6 | ✓ |
| 1d_recolor_cmp_37 | `paint(paint(x, segment(x)), scan(x))` | 30.0 | ✓ |
| 1d_recolor_cmp_38 | `paint(paint(x, scan(x)), segment(x))` | 45.4 | ✓ |
| 1d_recolor_cmp_39 | `paint(paint(x, scan(x)), segment(x))` | 42.3 | ✓ |
| 1d_recolor_cmp_4 | `paint(paint(x, segment(x)), segment(x))` | 59.5 | ✓ |
| 1d_recolor_cmp_40 | `paint(paint(x, scan(x)), segment(x))` | 59.5 | ✓ |
| 1d_recolor_cmp_41 | `paint(paint(x, scan(x)), segment(x))` | 46.5 | ✓ |
| 1d_recolor_cmp_42 | `paint(paint(x, segment(x)), scan(x))` | 63.0 | ✓ |
| 1d_recolor_cmp_43 | `paint(paint(x, scan(x)), segment(x))` | 55.0 | ✓ |
| 1d_recolor_cmp_44 | `paint(paint(x, scan(x)), segment(x))` | 37.1 | ✓ |
| 1d_recolor_cmp_45 | `paint(paint(x, segment(x)), local(shift(x)))` | 60.9 | ✓ |
| 1d_recolor_cmp_46 | `paint(paint(x, segment(x)), scan(x))` | 52.3 | ✓ |
| 1d_recolor_cmp_47 | `paint(paint(x, scan(x)), segment(x))` | 51.3 | ✓ |
| 1d_recolor_cmp_48 | `paint(paint(x, local(x)), scan(x))` | 65.0 | ✗ |
| 1d_recolor_cmp_49 | `paint(paint(x, segment(x)), scan(x))` | 64.0 | ✓ |
| 1d_recolor_cmp_5 | `paint(paint(x, segment(x)), segment(x))` | 44.1 | ✓ |
| 1d_recolor_cmp_6 | `paint(paint(x, scan(x)), segment(x))` | 67.9 | ✓ |
| 1d_recolor_cmp_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 54.8 | ✓ |
| 1d_recolor_cmp_8 | `paint(paint(x, scan(x)), segment(x))` | 35.0 | ✓ |
| 1d_recolor_cmp_9 | `paint(paint(x, segment(x)), scan(x))` | 43.8 | ✓ |
| 1d_recolor_cnt_0 | `paint(paint(x, scan(x)), segment(x))` | 83.3 | ✓ |
| 1d_recolor_cnt_1 | `paint(paint(x, segment(x)), local(x))` | 104.2 | ✓ |
| 1d_recolor_cnt_10 | `paint(paint(x, segment(x)), local(shift(x)))` | 100.0 | ✓ |
| 1d_recolor_cnt_11 | `paint(paint(x, segment(x)), segment(x))` | 111.0 | ✓ |
| 1d_recolor_cnt_12 | `paint(paint(x, segment(x)), local(x))` | 79.6 | ✓ |
| 1d_recolor_cnt_13 | `paint(paint(x, segment(x)), segment(x))` | 92.9 | ✓ |
| 1d_recolor_cnt_14 | `paint(paint(x, segment(x)), local(x))` | 100.2 | ✓ |
| 1d_recolor_cnt_15 | `paint(paint(x, segment(x)), local(x))` | 80.0 | ✓ |
| 1d_recolor_cnt_16 | `paint(paint(x, segment(x)), local(x))` | 72.3 | ✓ |
| 1d_recolor_cnt_17 | `paint(paint(x, segment(x)), local(x))` | 64.3 | ✓ |
| 1d_recolor_cnt_18 | `paint(paint(shift(x), segment(x)), local(x))` | 113.4 | ✓ |
| 1d_recolor_cnt_19 | `paint(x, segment(x))` | 83.2 | ✓ |
| 1d_recolor_cnt_2 | `paint(paint(x, segment(x)), local(x))` | 70.8 | ✓ |
| 1d_recolor_cnt_20 | `paint(paint(x, segment(x)), scan(x))` | 88.2 | ✓ |
| 1d_recolor_cnt_21 | `paint(paint(x, segment(x)), local(x))` | 68.5 | ✓ |
| 1d_recolor_cnt_22 | `paint(paint(x, segment(x)), local(x))` | 63.5 | ✓ |
| 1d_recolor_cnt_23 | `paint(paint(x, segment(x)), local(x))` | 75.8 | ✓ |
| 1d_recolor_cnt_24 | `paint(paint(x, segment(x)), local(x))` | 90.9 | ✓ |
| 1d_recolor_cnt_25 | `paint(x, segment(paint(x, local(x))))` | 78.8 | ✓ |
| 1d_recolor_cnt_26 | `paint(paint(x, segment(x)), local(x))` | 76.5 | ✓ |
| 1d_recolor_cnt_27 | `paint(paint(x, segment(x)), local(shift(x)))` | 77.5 | ✓ |
| 1d_recolor_cnt_28 | `paint(x, segment(x))` | 78.8 | ✓ |
| 1d_recolor_cnt_29 | `paint(paint(x, segment(x)), segment(x))` | 107.3 | ✓ |
| 1d_recolor_cnt_3 | `paint(paint(x, local(shift(x))), segment(x))` | 99.8 | ✓ |
| 1d_recolor_cnt_30 | `paint(paint(x, segment(x)), local(x))` | 76.5 | ✓ |
| 1d_recolor_cnt_31 | `paint(paint(x, segment(x)), scan(x))` | 76.1 | ✓ |
| 1d_recolor_cnt_32 | `paint(paint(x, segment(x)), local(x))` | 83.2 | ✓ |
| 1d_recolor_cnt_33 | `paint(paint(x, segment(x)), segment(x))` | 98.8 | ✓ |
| 1d_recolor_cnt_34 | `paint(x, segment(paint(x, segment(x))))` | 91.6 | ✓ |
| 1d_recolor_cnt_35 | `paint(x, segment(paint(x, segment(x))))` | 81.7 | ✓ |
| 1d_recolor_cnt_36 | `paint(paint(x, scan(x)), segment(x))` | 124.1 | ✓ |
| 1d_recolor_cnt_37 | `paint(paint(x, segment(x)), local(x))` | 67.1 | ✓ |
| 1d_recolor_cnt_38 | `paint(paint(x, scan(x)), segment(x))` | 73.6 | ✓ |
| 1d_recolor_cnt_39 | `paint(paint(x, segment(x)), segment(x))` | 69.9 | ✓ |
| 1d_recolor_cnt_4 | `paint(paint(x, segment(x)), local(x))` | 77.6 | ✓ |
| 1d_recolor_cnt_40 | `paint(paint(x, segment(x)), segment(x))` | 80.7 | ✓ |
| 1d_recolor_cnt_41 | `recolour(paint(x, segment(x)))` | 97.2 | ✓ |
| 1d_recolor_cnt_42 | `paint(paint(x, scan(x)), segment(x))` | 63.7 | ✓ |
| 1d_recolor_cnt_43 | `paint(paint(shift(x), segment(x)), local(x))` | 84.5 | ✓ |
| 1d_recolor_cnt_44 | `paint(paint(x, scan(x)), segment(x))` | 56.2 | ✓ |
| 1d_recolor_cnt_45 | `paint(paint(x, segment(x)), local(x))` | 103.7 | ✓ |
| 1d_recolor_cnt_46 | `paint(paint(x, segment(x)), local(x))` | 84.8 | ✓ |
| 1d_recolor_cnt_47 | `paint(paint(x, local(x)), segment(x))` | 114.0 | ✓ |
| 1d_recolor_cnt_48 | `paint(paint(x, segment(x)), local(x))` | 90.0 | ✓ |
| 1d_recolor_cnt_49 | `paint(paint(x, scan(x)), segment(x))` | 83.8 | ✓ |
| 1d_recolor_cnt_5 | `paint(paint(x, segment(x)), local(x))` | 85.4 | ✓ |
| 1d_recolor_cnt_6 | `paint(x, segment(x))` | 86.5 | ✓ |
| 1d_recolor_cnt_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 72.1 | ✓ |
| 1d_recolor_cnt_8 | `paint(x, segment(x))` | 78.0 | ✓ |
| 1d_recolor_cnt_9 | `paint(paint(x, scan(x)), segment(x))` | 89.4 | ✓ |
| 1d_recolor_oe_0 | `paint(paint(x, scan(x)), segment(x))` | 79.8 | ✗ |
| 1d_recolor_oe_1 | `paint(paint(x, segment(x)), local(x))` | 62.0 | ✓ |
| 1d_recolor_oe_10 | `paint(paint(x, segment(x)), local(x))` | 103.5 | ✓ |
| 1d_recolor_oe_11 | `paint(paint(x, segment(x)), local(x))` | 83.2 | ✓ |
| 1d_recolor_oe_12 | `paint(paint(x, segment(x)), local(x))` | 105.7 | ✓ |
| 1d_recolor_oe_13 | `paint(paint(x, segment(x)), segment(x))` | 68.8 | ✓ |
| 1d_recolor_oe_14 | `paint(paint(x, segment(x)), local(x))` | 67.0 | ✓ |
| 1d_recolor_oe_15 | `paint(paint(x, segment(x)), scan(x))` | 75.6 | ✓ |
| 1d_recolor_oe_16 | `paint(paint(x, segment(x)), local(shift(x)))` | 94.7 | ✓ |
| 1d_recolor_oe_17 | `paint(paint(x, segment(x)), local(x))` | 99.1 | ✓ |
| 1d_recolor_oe_18 | `paint(paint(x, segment(x)), segment(x))` | 76.3 | ✓ |
| 1d_recolor_oe_19 | `paint(paint(x, segment(x)), local(x))` | 76.2 | ✓ |
| 1d_recolor_oe_2 | `paint(x, segment(x))` | 60.8 | ✓ |
| 1d_recolor_oe_20 | `paint(paint(x, segment(x)), segment(x))` | 90.7 | ✓ |
| 1d_recolor_oe_21 | `paint(paint(x, segment(x)), local(x))` | 68.8 | ✓ |
| 1d_recolor_oe_22 | `paint(paint(x, segment(x)), scan(x))` | 80.7 | ✓ |
| 1d_recolor_oe_23 | `paint(paint(x, segment(x)), segment(x))` | 62.7 | ✓ |
| 1d_recolor_oe_24 | `paint(paint(x, segment(x)), segment(x))` | 65.9 | ✓ |
| 1d_recolor_oe_25 | `paint(paint(x, segment(x)), scan(x))` | 92.7 | ✓ |
| 1d_recolor_oe_26 | `paint(x, segment(paint(x, scan(x))))` | 59.3 | ✓ |
| 1d_recolor_oe_27 | `paint(paint(x, segment(x)), local(x))` | 79.9 | ✓ |
| 1d_recolor_oe_28 | `paint(paint(x, segment(x)), local(x))` | 82.0 | ✗ |
| 1d_recolor_oe_29 | `paint(x, segment(paint(x, scan(x))))` | 69.1 | ✗ |
| 1d_recolor_oe_3 | `paint(paint(x, segment(x)), local(shift(x)))` | 69.6 | ✓ |
| 1d_recolor_oe_30 | `paint(x, segment(x))` | 69.1 | ✓ |
| 1d_recolor_oe_31 | `paint(x, segment(x))` | 60.6 | ✗ |
| 1d_recolor_oe_32 | `paint(paint(x, segment(x)), local(shift(x)))` | 110.7 | ✓ |
| 1d_recolor_oe_33 | `paint(paint(x, segment(x)), segment(x))` | 76.1 | ✓ |
| 1d_recolor_oe_34 | `recolour(paint(x, segment(x)))` | 78.7 | ✗ |
| 1d_recolor_oe_35 | `paint(paint(x, segment(x)), scan(x))` | 118.9 | ✓ |
| 1d_recolor_oe_36 | `paint(x, segment(x))` | 54.8 | ✓ |
| 1d_recolor_oe_37 | `paint(paint(x, segment(x)), segment(x))` | 81.2 | ✓ |
| 1d_recolor_oe_38 | `paint(paint(x, segment(x)), segment(x))` | 101.3 | ✓ |
| 1d_recolor_oe_39 | `paint(x, segment(x))` | 58.8 | ✓ |
| 1d_recolor_oe_4 | `paint(paint(x, segment(x)), local(x))` | 74.0 | ✓ |
| 1d_recolor_oe_40 | `paint(paint(x, segment(x)), scan(x))` | 75.3 | ✗ |
| 1d_recolor_oe_41 | `recolour(paint(x, segment(x)))` | 69.1 | ✓ |
| 1d_recolor_oe_42 | `recolour(paint(x, segment(x)))` | 62.1 | ✓ |
| 1d_recolor_oe_43 | `paint(x, segment(paint(x, scan(x))))` | 82.2 | ✓ |
| 1d_recolor_oe_44 | `paint(paint(x, segment(x)), segment(x))` | 91.8 | ✓ |
| 1d_recolor_oe_45 | `paint(recolour(x), segment(x))` | 104.3 | ✗ |
| 1d_recolor_oe_46 | `paint(paint(x, local(shift(x))), segment(x))` | 99.3 | ✓ |
| 1d_recolor_oe_47 | `paint(paint(x, segment(x)), segment(x))` | 69.6 | ✓ |
| 1d_recolor_oe_48 | `paint(paint(x, segment(x)), local(shift(x)))` | 86.5 | ✓ |
| 1d_recolor_oe_49 | `paint(paint(x, segment(x)), segment(x))` | 98.1 | ✓ |
| 1d_recolor_oe_5 | `paint(paint(x, segment(x)), segment(x))` | 64.9 | ✓ |
| 1d_recolor_oe_6 | `recolour(paint(x, segment(x)))` | 73.6 | ✓ |
| 1d_recolor_oe_7 | `paint(paint(x, segment(x)), scan(x))` | 87.0 | ✓ |
| 1d_recolor_oe_8 | `paint(paint(x, segment(x)), segment(x))` | 56.5 | ✓ |
| 1d_recolor_oe_9 | `paint(paint(x, segment(x)), local(x))` | 68.3 | ✓ |
| 1d_scale_dp_0 | `paint(paint(x, scan(x)), segment(x))` | 35.1 | ✓ |
| 1d_scale_dp_1 | `paint(paint(x, scan(x)), scan(x))` | 53.4 | ✓ |
| 1d_scale_dp_10 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.1 | ✓ |
| 1d_scale_dp_11 | `paint(paint(x, scan(x)), scan(x))` | 38.4 | ✓ |
| 1d_scale_dp_12 | `paint(paint(x, local(shift(x))), segment(x))` | 52.0 | ✓ |
| 1d_scale_dp_13 | `paint(paint(x, local(x)), scan(shift(x)))` | 52.3 | ✗ |
| 1d_scale_dp_14 | `paint(x, scan(x))` | 55.2 | ✓ |
| 1d_scale_dp_15 | `paint(x, scan(x))` | 77.6 | ✓ |
| 1d_scale_dp_16 | `paint(paint(x, scan(x)), scan(x))` | 63.1 | ✗ |
| 1d_scale_dp_17 | `paint(paint(x, scan(x)), local(x))` | 59.7 | ✓ |
| 1d_scale_dp_18 | `paint(paint(x, local(x)), scan(x))` | 27.9 | ✓ |
| 1d_scale_dp_19 | `paint(paint(x, scan(x)), scan(x))` | 44.0 | ✗ |
| 1d_scale_dp_2 | `paint(paint(x, scan(x)), scan(x))` | 64.2 | ✗ |
| 1d_scale_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 44.4 | ✗ |
| 1d_scale_dp_21 | `paint(paint(x, local(x)), scan(x))` | 60.2 | ✓ |
| 1d_scale_dp_22 | `paint(x, local(x))` | 47.6 | ✓ |
| 1d_scale_dp_23 | `paint(paint(x, local(x)), local(shift(x)))` | 68.5 | ✗ |
| 1d_scale_dp_24 | `paint(paint(x, scan(x)), scan(x))` | 30.2 | ✓ |
| 1d_scale_dp_25 | `paint(paint(x, scan(x)), scan(x))` | 42.7 | ✓ |
| 1d_scale_dp_26 | `paint(paint(x, scan(x)), scan(x))` | 36.4 | ✓ |
| 1d_scale_dp_27 | `paint(paint(x, local(x)), scan(x))` | 62.2 | ✓ |
| 1d_scale_dp_28 | `paint(x, local(paint(x, local(x))))` | 51.9 | ✓ |
| 1d_scale_dp_29 | `paint(paint(x, scan(x)), scan(x))` | 70.1 | ✓ |
| 1d_scale_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 35.2 | ✓ |
| 1d_scale_dp_30 | `paint(paint(x, local(shift(x))), scan(x))` | 62.9 | ✓ |
| 1d_scale_dp_31 | `paint(paint(shift(x), local(x)), scan(x))` | 58.0 | ✗ |
| 1d_scale_dp_32 | `paint(paint(x, scan(x)), scan(x))` | 38.6 | ✓ |
| 1d_scale_dp_33 | `paint(x, scan(paint(x, local(shift(x)))))` | 51.6 | ✓ |
| 1d_scale_dp_34 | `paint(paint(x, local(shift(x))), scan(x))` | 34.1 | ✓ |
| 1d_scale_dp_35 | `paint(paint(x, local(shift(x))), scan(x))` | 48.2 | ✓ |
| 1d_scale_dp_36 | `paint(paint(x, local(x)), local(shift(x)))` | 58.1 | ✗ |
| 1d_scale_dp_37 | `paint(x, scan(paint(x, local(x))))` | 48.3 | ✓ |
| 1d_scale_dp_38 | `paint(paint(x, scan(x)), scan(x))` | 81.5 | ✓ |
| 1d_scale_dp_39 | `paint(paint(x, scan(x)), segment(x))` | 47.4 | ✓ |
| 1d_scale_dp_4 | `paint(x, scan(x))` | 41.8 | ✗ |
| 1d_scale_dp_40 | `paint(paint(x, scan(x)), scan(x))` | 47.7 | ✓ |
| 1d_scale_dp_41 | `paint(paint(x, scan(x)), local(shift(x)))` | 69.2 | ✓ |
| 1d_scale_dp_42 | `paint(paint(x, scan(x)), local(shift(x)))` | 34.8 | ✓ |
| 1d_scale_dp_43 | `paint(paint(x, scan(x)), scan(x))` | 49.3 | ✓ |
| 1d_scale_dp_44 | `paint(shift(x), local(x))` | 35.3 | ✓ |
| 1d_scale_dp_45 | `recolour(paint(shift(x), local(x)))` | 41.1 | ✗ |
| 1d_scale_dp_46 | `paint(paint(x, scan(x)), scan(x))` | 61.1 | ✓ |
| 1d_scale_dp_47 | `paint(shift(x), scan(x))` | 72.9 | ✓ |
| 1d_scale_dp_48 | `paint(paint(x, scan(x)), scan(x))` | 35.7 | ✓ |
| 1d_scale_dp_49 | `paint(paint(x, scan(x)), scan(x))` | 44.3 | ✓ |
| 1d_scale_dp_5 | `paint(x, scan(x))` | 68.5 | ✓ |
| 1d_scale_dp_50 | `paint(x, scan(paint(x, local(x))))` | 50.8 | ✓ |
| 1d_scale_dp_6 | `paint(paint(x, local(shift(x))), scan(x))` | 64.9 | ✓ |
| 1d_scale_dp_7 | `paint(shift(shift(x)), local(x))` | 42.7 | ✓ |
| 1d_scale_dp_8 | `paint(x, local(paint(x, segment(x))))` | 55.4 | ✓ |
| 1d_scale_dp_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 51.2 | ✓ |
