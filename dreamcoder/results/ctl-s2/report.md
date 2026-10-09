# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 901 (50 per family, drawn with seed 2), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/ctl-s2/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 660/901 (73%) | 722/901 | 792/901 | 65.9 | 7 | 150 | 1862s |
| 1 | 666/901 (74%) | 725/901 | 781/901 | 66.8 | 7 | 150 | 2021s |
| 2 | 669/901 (74%) | 721/901 | 788/901 | 64.9 | 7 | 150 | 2049s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 46/50 | 47/50 | 45/50 |
| denoising_mc | 39/50 | 41/50 | 43/50 |
| fill | 47/50 | 44/50 | 43/50 |
| flip | 5/50 | 7/50 | 6/50 |
| hollow | 50/50 | 45/50 | 47/50 |
| mirror | 0/50 | 2/50 | 3/50 |
| move_1p | 45/50 | 48/50 | 49/50 |
| move_2p | 50/50 | 50/50 | 50/50 |
| move_2p_dp | 40/50 | 41/50 | 42/50 |
| move_3p | 50/50 | 50/50 | 50/50 |
| move_dp | 3/50 | 5/50 | 4/50 |
| padded_fill | 45/50 | 45/50 | 45/50 |
| pcopy_1c | 18/50 | 16/50 | 19/50 |
| pcopy_mc | 38/50 | 44/50 | 39/50 |
| recolor_cmp | 49/50 | 46/50 | 49/50 |
| recolor_cnt | 49/50 | 50/50 | 49/50 |
| recolor_oe | 41/50 | 43/50 | 43/50 |
| scale_dp | 45/51 | 42/51 | 43/51 |

## Library growth

- no fragment had support in two tasks

## Examples from the last iteration

### Solved: `1d_denoising_mc_22`

`paint(paint(x, local(x)), local(shift(x)))`, DL 49.3 = 10.9 structure + 38.3 parameters + 0.1 data bits, fits its training pairs exactly.

![1d_denoising_mc_22](figures/1d_denoising_mc_22.png)

| pair | input | output |
|---|---|---|
| train 0 | `....555555555555556595655.......` | `....555555555555555555555.......` |
| train 1 | `.........11562111117111111111...` | `.........11111111111111111111...` |
| train 2 | `.......999999959999999692999....` | `.......999999999999999999999....` |
| **test** | `.....2222222222292227222222.....` | `.....2222222222222222222222.....` |
| predicted | | `.....2222222222222222222222.....` |

### Solved: `1d_fill_13`

`paint(x, scan(paint(x, local(x))))`, DL 69.7 = 9.0 structure + 60.4 parameters + 0.3 data bits, fits its training pairs exactly.

![1d_fill_13](figures/1d_fill_13.png)

| pair | input | output |
|---|---|---|
| train 0 | `................7.....7.` | `................7777777.` |
| train 1 | `..7...............7.....` | `..77777777777777777.....` |
| train 2 | `8.....8.................` | `8888888.................` |
| **test** | `....7...........7.......` | `....7777777777777.......` |
| predicted | | `....7777777777777.......` |

### Solved: `1d_move_3p_46`

`shift(x)`, DL 53.2 = 4.0 structure + 43.2 parameters + 6.0 data bits, fits its training pairs exactly.

![1d_move_3p_46](figures/1d_move_3p_46.png)

| pair | input | output |
|---|---|---|
| train 0 | `4444444444444444....` | `...4444444444444444.` |
| train 1 | `888888888888888.....` | `...888888888888888..` |
| train 2 | `....66666...........` | `.......66666........` |
| **test** | `..77777777..........` | `.....77777777.......` |
| predicted | | `.....77777777.......` |

### Failed: `1d_move_2p_dp_5`

`paint(paint(x, local(x)), local(shift(x)))`, DL 58.1 = 10.9 structure + 47.0 parameters + 0.2 data bits, fits its training pairs exactly.

![1d_move_2p_dp_5](figures/1d_move_2p_dp_5.png)

| pair | input | output |
|---|---|---|
| train 0 | `.........222222222..5....` | `...........2222222225....` |
| train 1 | `.......33333333333..5....` | `.........333333333335....` |
| train 2 | `.........444444..5.......` | `...........4444445.......` |
| **test** | `...........222..5........` | `.............2225........` |
| predicted | | `...........222225........` |

### Failed: `1d_move_dp_11`

`paint(x, scan(paint(x, local(x))))`, DL 119.4 = 9.0 structure + 100.9 parameters + 9.5 data bits, does not fit its training pairs exactly.

![1d_move_dp_11](figures/1d_move_dp_11.png)

| pair | input | output |
|---|---|---|
| train 0 | `......8888.....6........` | `...........88886........` |
| train 1 | `..33333333333333333....6` | `......333333333333333336` |
| train 2 | `............777......6..` | `..................7776..` |
| **test** | `55555555555555555555...6` | `...555555555555555555556` |
| predicted | | `5...55555555555555555556` |

### Failed: `1d_pcopy_1c_43`

`paint(x, local(x))`, DL 77.7 = 4.5 structure + 72.2 parameters + 1.0 data bits, fits its training pairs exactly.

![1d_pcopy_1c_43](figures/1d_pcopy_1c_43.png)

| pair | input | output |
|---|---|---|
| train 0 | `.222....2.....2...2.............` | `.222...222...222.222............` |
| train 1 | `.555...5........................` | `.555..555.......................` |
| train 2 | `..999..9.....9..................` | `..999.999...999.................` |
| **test** | `..777...7.......................` | `..777..777......................` |
| predicted | | `..777...7.......................` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_0 | `paint(x, local(paint(x, scan(x))))` | 35.5 | ✓ |
| 1d_denoising_1c_1 | `paint(x, local(x))` | 44.8 | ✓ |
| 1d_denoising_1c_10 | `paint(paint(x, scan(x)), segment(x))` | 48.1 | ✓ |
| 1d_denoising_1c_11 | `paint(paint(x, local(x)), segment(shift(x)))` | 35.3 | ✓ |
| 1d_denoising_1c_12 | `paint(x, local(paint(x, scan(x))))` | 38.1 | ✓ |
| 1d_denoising_1c_13 | `paint(x, local(paint(x, scan(x))))` | 37.9 | ✓ |
| 1d_denoising_1c_14 | `paint(paint(shift(x), local(x)), segment(x))` | 33.1 | ✗ |
| 1d_denoising_1c_15 | `paint(recolour(x), local(x))` | 40.7 | ✓ |
| 1d_denoising_1c_16 | `paint(shift(x), local(x))` | 42.9 | ✓ |
| 1d_denoising_1c_17 | `paint(x, local(paint(x, scan(x))))` | 39.0 | ✓ |
| 1d_denoising_1c_18 | `paint(x, local(paint(x, scan(x))))` | 37.4 | ✓ |
| 1d_denoising_1c_19 | `paint(x, local(recolour(x)))` | 46.6 | ✗ |
| 1d_denoising_1c_2 | `paint(x, local(paint(x, local(x))))` | 44.3 | ✓ |
| 1d_denoising_1c_20 | `paint(shift(x), local(x))` | 34.3 | ✓ |
| 1d_denoising_1c_21 | `paint(x, local(paint(x, scan(x))))` | 34.2 | ✓ |
| 1d_denoising_1c_22 | `paint(paint(shift(x), scan(x)), local(x))` | 38.2 | ✓ |
| 1d_denoising_1c_23 | `paint(paint(x, local(shift(x))), segment(x))` | 36.9 | ✓ |
| 1d_denoising_1c_24 | `paint(x, local(recolour(x)))` | 44.0 | ✓ |
| 1d_denoising_1c_25 | `paint(paint(x, scan(x)), local(x))` | 49.2 | ✓ |
| 1d_denoising_1c_26 | `paint(x, local(recolour(x)))` | 41.9 | ✗ |
| 1d_denoising_1c_27 | `paint(paint(x, scan(x)), segment(x))` | 39.1 | ✓ |
| 1d_denoising_1c_28 | `paint(x, local(paint(x, scan(shift(x)))))` | 42.7 | ✓ |
| 1d_denoising_1c_29 | `paint(x, local(paint(x, local(x))))` | 38.2 | ✓ |
| 1d_denoising_1c_3 | `paint(x, local(paint(x, scan(x))))` | 40.2 | ✓ |
| 1d_denoising_1c_30 | `paint(paint(shift(x), scan(x)), local(x))` | 40.0 | ✓ |
| 1d_denoising_1c_31 | `paint(paint(shift(x), scan(x)), local(x))` | 29.4 | ✗ |
| 1d_denoising_1c_32 | `paint(x, local(paint(x, scan(x))))` | 31.4 | ✓ |
| 1d_denoising_1c_33 | `paint(shift(x), local(x))` | 29.4 | ✓ |
| 1d_denoising_1c_34 | `paint(x, local(paint(x, scan(x))))` | 31.1 | ✓ |
| 1d_denoising_1c_35 | `paint(shift(paint(x, local(x))), segment(x))` | 41.6 | ✓ |
| 1d_denoising_1c_36 | `paint(paint(x, local(shift(x))), segment(x))` | 40.3 | ✓ |
| 1d_denoising_1c_37 | `paint(paint(x, scan(x)), segment(x))` | 47.4 | ✓ |
| 1d_denoising_1c_38 | `paint(x, local(paint(x, scan(x))))` | 40.8 | ✓ |
| 1d_denoising_1c_39 | `paint(x, local(paint(x, scan(x))))` | 32.3 | ✓ |
| 1d_denoising_1c_4 | `paint(x, local(paint(x, scan(x))))` | 32.5 | ✓ |
| 1d_denoising_1c_40 | `paint(x, local(recolour(x)))` | 43.7 | ✓ |
| 1d_denoising_1c_41 | `paint(paint(shift(x), scan(x)), local(x))` | 31.9 | ✓ |
| 1d_denoising_1c_42 | `paint(shift(x), local(x))` | 48.7 | ✓ |
| 1d_denoising_1c_43 | `paint(x, local(recolour(x)))` | 48.1 | ✗ |
| 1d_denoising_1c_44 | `paint(x, local(paint(x, local(x))))` | 44.9 | ✓ |
| 1d_denoising_1c_45 | `paint(x, local(paint(x, scan(x))))` | 33.5 | ✓ |
| 1d_denoising_1c_46 | `paint(x, local(paint(x, scan(x))))` | 32.9 | ✓ |
| 1d_denoising_1c_47 | `paint(recolour(x), local(x))` | 43.6 | ✓ |
| 1d_denoising_1c_48 | `paint(x, local(paint(x, scan(x))))` | 35.5 | ✓ |
| 1d_denoising_1c_49 | `paint(x, local(paint(x, scan(x))))` | 31.1 | ✓ |
| 1d_denoising_1c_5 | `paint(x, local(paint(x, scan(x))))` | 37.4 | ✓ |
| 1d_denoising_1c_6 | `paint(x, local(paint(x, scan(x))))` | 42.1 | ✓ |
| 1d_denoising_1c_7 | `paint(x, local(paint(x, scan(x))))` | 36.2 | ✓ |
| 1d_denoising_1c_8 | `paint(paint(x, scan(x)), segment(x))` | 43.6 | ✓ |
| 1d_denoising_1c_9 | `paint(paint(x, local(shift(x))), local(x))` | 45.9 | ✓ |
| 1d_denoising_mc_0 | `paint(shift(x), local(x))` | 50.4 | ✓ |
| 1d_denoising_mc_1 | `paint(paint(shift(x), local(x)), segment(x))` | 40.9 | ✓ |
| 1d_denoising_mc_10 | `recolour(paint(shift(x), local(x)))` | 38.5 | ✗ |
| 1d_denoising_mc_11 | `paint(paint(shift(x), local(x)), segment(x))` | 38.0 | ✓ |
| 1d_denoising_mc_12 | `paint(paint(shift(x), local(x)), scan(x))` | 29.2 | ✗ |
| 1d_denoising_mc_13 | `paint(paint(shift(x), local(x)), segment(x))` | 31.6 | ✓ |
| 1d_denoising_mc_14 | `paint(shift(x), local(x))` | 33.1 | ✓ |
| 1d_denoising_mc_15 | `paint(paint(shift(x), local(x)), local(x))` | 18.9 | ✓ |
| 1d_denoising_mc_16 | `paint(paint(shift(x), local(x)), local(x))` | 24.1 | ✓ |
| 1d_denoising_mc_17 | `paint(paint(shift(x), local(x)), local(x))` | 18.7 | ✓ |
| 1d_denoising_mc_18 | `paint(paint(shift(x), local(x)), segment(x))` | 29.7 | ✓ |
| 1d_denoising_mc_19 | `paint(paint(shift(x), local(x)), segment(x))` | 40.5 | ✗ |
| 1d_denoising_mc_2 | `paint(paint(shift(x), local(x)), segment(x))` | 37.2 | ✓ |
| 1d_denoising_mc_20 | `paint(paint(shift(x), local(x)), segment(x))` | 26.5 | ✓ |
| 1d_denoising_mc_21 | `paint(shift(x), local(paint(x, scan(x))))` | 50.1 | ✓ |
| 1d_denoising_mc_22 | `paint(paint(x, local(x)), local(shift(x)))` | 49.3 | ✓ |
| 1d_denoising_mc_23 | `paint(paint(shift(x), local(x)), scan(x))` | 19.6 | ✓ |
| 1d_denoising_mc_24 | `paint(paint(shift(x), local(x)), segment(x))` | 27.1 | ✓ |
| 1d_denoising_mc_25 | `paint(paint(shift(x), local(x)), scan(x))` | 39.8 | ✓ |
| 1d_denoising_mc_26 | `paint(paint(x, local(x)), local(shift(x)))` | 52.3 | ✓ |
| 1d_denoising_mc_27 | `paint(shift(paint(x, local(x))), local(x))` | 56.5 | ✗ |
| 1d_denoising_mc_28 | `paint(shift(x), local(paint(x, segment(x))))` | 27.8 | ✓ |
| 1d_denoising_mc_29 | `paint(paint(shift(x), local(x)), scan(x))` | 21.9 | ✓ |
| 1d_denoising_mc_3 | `paint(paint(shift(x), local(x)), local(x))` | 44.2 | ✓ |
| 1d_denoising_mc_30 | `paint(paint(shift(x), scan(x)), local(x))` | 37.2 | ✓ |
| 1d_denoising_mc_31 | `paint(paint(shift(x), local(x)), segment(x))` | 39.3 | ✓ |
| 1d_denoising_mc_32 | `paint(paint(shift(x), local(x)), local(x))` | 30.6 | ✓ |
| 1d_denoising_mc_33 | `paint(paint(shift(x), local(x)), segment(x))` | 37.9 | ✗ |
| 1d_denoising_mc_34 | `paint(paint(shift(x), local(x)), segment(x))` | 63.1 | ✓ |
| 1d_denoising_mc_35 | `paint(shift(x), local(x))` | 27.1 | ✓ |
| 1d_denoising_mc_36 | `paint(paint(shift(x), local(x)), segment(x))` | 56.1 | ✓ |
| 1d_denoising_mc_37 | `paint(shift(paint(x, local(x))), local(x))` | 45.0 | ✓ |
| 1d_denoising_mc_38 | `paint(paint(shift(x), local(x)), segment(x))` | 36.0 | ✓ |
| 1d_denoising_mc_39 | `paint(shift(paint(x, scan(x))), local(x))` | 52.3 | ✓ |
| 1d_denoising_mc_4 | `paint(paint(shift(x), local(x)), segment(x))` | 12.1 | ✗ |
| 1d_denoising_mc_40 | `paint(paint(shift(x), local(x)), segment(x))` | 23.2 | ✓ |
| 1d_denoising_mc_41 | `paint(shift(x), local(x))` | 37.2 | ✓ |
| 1d_denoising_mc_42 | `paint(paint(shift(x), local(x)), segment(x))` | 26.8 | ✓ |
| 1d_denoising_mc_43 | `paint(paint(shift(x), local(x)), segment(x))` | 28.7 | ✗ |
| 1d_denoising_mc_44 | `paint(shift(paint(x, scan(x))), local(x))` | 47.1 | ✓ |
| 1d_denoising_mc_45 | `paint(paint(shift(x), scan(x)), local(x))` | 51.6 | ✓ |
| 1d_denoising_mc_46 | `paint(paint(shift(x), scan(x)), local(x))` | 27.9 | ✓ |
| 1d_denoising_mc_47 | `paint(shift(paint(x, local(x))), local(x))` | 44.7 | ✓ |
| 1d_denoising_mc_48 | `paint(paint(shift(x), local(x)), scan(x))` | 32.9 | ✓ |
| 1d_denoising_mc_49 | `paint(paint(shift(x), local(x)), segment(x))` | 27.8 | ✓ |
| 1d_denoising_mc_5 | `paint(paint(shift(x), local(x)), scan(x))` | 13.2 | ✓ |
| 1d_denoising_mc_6 | `paint(paint(shift(x), local(x)), scan(x))` | 32.2 | ✓ |
| 1d_denoising_mc_7 | `paint(paint(shift(x), local(x)), local(x))` | 35.0 | ✓ |
| 1d_denoising_mc_8 | `paint(paint(shift(x), local(x)), segment(x))` | 18.8 | ✓ |
| 1d_denoising_mc_9 | `paint(paint(shift(x), local(x)), segment(x))` | 44.8 | ✓ |
| 1d_fill_0 | `paint(paint(x, scan(x)), segment(x))` | 78.7 | ✓ |
| 1d_fill_1 | `paint(x, scan(paint(x, segment(x))))` | 73.2 | ✓ |
| 1d_fill_10 | `paint(x, local(paint(x, scan(x))))` | 78.9 | ✓ |
| 1d_fill_11 | `paint(x, scan(paint(x, local(x))))` | 71.0 | ✓ |
| 1d_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 41.5 | ✓ |
| 1d_fill_13 | `paint(x, scan(paint(x, local(x))))` | 69.7 | ✓ |
| 1d_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 68.1 | ✓ |
| 1d_fill_15 | `paint(x, scan(paint(x, segment(x))))` | 68.6 | ✓ |
| 1d_fill_16 | `paint(shift(paint(x, scan(x))), local(x))` | 82.6 | ✓ |
| 1d_fill_17 | `paint(paint(x, scan(x)), local(shift(x)))` | 69.1 | ✓ |
| 1d_fill_18 | `paint(x, scan(paint(x, scan(x))))` | 64.0 | ✓ |
| 1d_fill_19 | `paint(paint(shift(x), scan(x)), local(x))` | 48.2 | ✗ |
| 1d_fill_2 | `paint(x, local(paint(shift(x), scan(x))))` | 62.9 | ✓ |
| 1d_fill_20 | `paint(paint(shift(x), scan(x)), local(x))` | 73.8 | ✓ |
| 1d_fill_21 | `paint(paint(x, local(x)), scan(x))` | 64.0 | ✓ |
| 1d_fill_22 | `paint(paint(x, local(x)), scan(x))` | 58.0 | ✓ |
| 1d_fill_23 | `paint(paint(x, local(x)), scan(x))` | 60.8 | ✓ |
| 1d_fill_24 | `paint(x, local(paint(shift(x), scan(x))))` | 50.1 | ✗ |
| 1d_fill_25 | `paint(paint(x, local(shift(x))), scan(x))` | 50.3 | ✓ |
| 1d_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 77.7 | ✓ |
| 1d_fill_27 | `paint(x, scan(paint(x, segment(x))))` | 58.5 | ✓ |
| 1d_fill_28 | `paint(paint(shift(x), scan(x)), local(x))` | 58.5 | ✓ |
| 1d_fill_29 | `paint(paint(shift(x), scan(x)), local(x))` | 71.6 | ✗ |
| 1d_fill_3 | `paint(shift(paint(x, scan(x))), local(x))` | 79.0 | ✓ |
| 1d_fill_30 | `paint(paint(shift(x), scan(x)), local(x))` | 89.7 | ✓ |
| 1d_fill_31 | `paint(paint(shift(x), scan(x)), local(x))` | 68.9 | ✓ |
| 1d_fill_32 | `paint(x, scan(paint(x, segment(x))))` | 63.1 | ✓ |
| 1d_fill_33 | `paint(x, local(paint(shift(x), scan(x))))` | 45.5 | ✓ |
| 1d_fill_34 | `paint(shift(paint(x, scan(x))), local(x))` | 75.4 | ✓ |
| 1d_fill_35 | `paint(x, scan(paint(x, segment(x))))` | 50.5 | ✓ |
| 1d_fill_36 | `paint(x, scan(paint(x, segment(x))))` | 44.2 | ✓ |
| 1d_fill_37 | `paint(paint(x, scan(x)), local(x))` | 48.4 | ✗ |
| 1d_fill_38 | `paint(x, scan(paint(x, segment(x))))` | 58.1 | ✗ |
| 1d_fill_39 | `paint(x, local(paint(x, scan(x))))` | 75.4 | ✓ |
| 1d_fill_4 | `paint(paint(x, scan(x)), local(shift(x)))` | 75.7 | ✓ |
| 1d_fill_40 | `paint(paint(shift(x), scan(x)), local(x))` | 49.2 | ✓ |
| 1d_fill_41 | `paint(paint(x, scan(x)), local(shift(x)))` | 70.5 | ✓ |
| 1d_fill_42 | `paint(paint(x, scan(x)), local(shift(x)))` | 56.7 | ✓ |
| 1d_fill_43 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.9 | ✓ |
| 1d_fill_44 | `paint(paint(x, segment(x)), local(x))` | 61.1 | ✓ |
| 1d_fill_45 | `paint(shift(paint(x, scan(x))), local(x))` | 87.3 | ✓ |
| 1d_fill_46 | `paint(paint(shift(x), scan(x)), local(x))` | 52.7 | ✓ |
| 1d_fill_47 | `paint(paint(shift(x), local(x)), local(x))` | 60.2 | ✗ |
| 1d_fill_48 | `paint(shift(paint(x, scan(x))), local(x))` | 61.1 | ✓ |
| 1d_fill_49 | `paint(paint(shift(x), scan(x)), local(x))` | 67.2 | ✓ |
| 1d_fill_5 | `paint(paint(shift(x), scan(x)), local(x))` | 56.1 | ✓ |
| 1d_fill_6 | `paint(paint(x, scan(x)), segment(x))` | 54.5 | ✓ |
| 1d_fill_7 | `paint(paint(x, scan(x)), local(x))` | 61.0 | ✓ |
| 1d_fill_8 | `paint(x, local(paint(shift(x), scan(x))))` | 67.6 | ✗ |
| 1d_fill_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.3 | ✓ |
| 1d_flip_0 | `paint(paint(x, local(shift(x))), local(x))` | 68.5 | ✗ |
| 1d_flip_1 | `paint(shift(x), local(x))` | 83.2 | ✗ |
| 1d_flip_10 | `paint(x, local(x))` | 86.3 | ✓ |
| 1d_flip_11 | `paint(paint(shift(x), local(x)), scan(x))` | 76.7 | ✗ |
| 1d_flip_12 | `paint(x, local(x))` | 90.4 | ✗ |
| 1d_flip_13 | `paint(paint(shift(x), local(x)), scan(x))` | 91.3 | ✗ |
| 1d_flip_14 | `paint(shift(paint(x, local(x))), local(x))` | 74.8 | ✗ |
| 1d_flip_15 | `paint(shift(shift(x)), scan(x))` | 92.5 | ✗ |
| 1d_flip_16 | `paint(shift(x), local(paint(x, scan(x))))` | 87.1 | ✗ |
| 1d_flip_17 | `paint(paint(shift(x), local(x)), segment(x))` | 91.4 | ✗ |
| 1d_flip_18 | `paint(x, local(x))` | 86.1 | ✗ |
| 1d_flip_19 | `paint(x, local(x))` | 78.9 | ✓ |
| 1d_flip_2 | `paint(shift(shift(x)), local(x))` | 63.7 | ✗ |
| 1d_flip_20 | `paint(paint(shift(x), local(x)), scan(x))` | 91.2 | ✗ |
| 1d_flip_21 | `paint(shift(shift(x)), local(x))` | 75.4 | ✗ |
| 1d_flip_22 | `paint(x, local(x))` | 91.5 | ✗ |
| 1d_flip_23 | `paint(paint(shift(x), local(x)), local(x))` | 82.2 | ✗ |
| 1d_flip_24 | `paint(shift(recolour(x)), local(x))` | 85.5 | ✗ |
| 1d_flip_25 | `paint(shift(paint(x, local(x))), local(x))` | 82.0 | ✗ |
| 1d_flip_26 | `paint(paint(x, segment(x)), local(x))` | 82.3 | ✗ |
| 1d_flip_27 | `paint(paint(shift(x), local(x)), segment(x))` | 75.7 | ✗ |
| 1d_flip_28 | `paint(paint(x, local(x)), local(x))` | 77.6 | ✓ |
| 1d_flip_29 | `paint(shift(x), local(paint(x, local(x))))` | 72.3 | ✗ |
| 1d_flip_3 | `paint(paint(shift(x), local(x)), local(x))` | 81.7 | ✓ |
| 1d_flip_30 | `paint(paint(shift(x), local(x)), scan(x))` | 79.4 | ✗ |
| 1d_flip_31 | `paint(reflect(x), local(x))` | 106.1 | ✗ |
| 1d_flip_32 | `paint(x, scan(paint(x, local(x))))` | 83.4 | ✗ |
| 1d_flip_33 | `paint(paint(shift(x), local(x)), scan(x))` | 66.5 | ✗ |
| 1d_flip_34 | `paint(paint(shift(x), local(x)), local(x))` | 70.4 | ✗ |
| 1d_flip_35 | `paint(paint(x, scan(x)), segment(x))` | 87.4 | ✗ |
| 1d_flip_36 | `paint(shift(x), local(paint(x, scan(x))))` | 95.9 | ✗ |
| 1d_flip_37 | `paint(shift(shift(x)), local(x))` | 93.3 | ✗ |
| 1d_flip_38 | `paint(shift(shift(x)), scan(x))` | 91.9 | ✗ |
| 1d_flip_39 | `paint(paint(x, local(x)), segment(shift(x)))` | 56.0 | ✗ |
| 1d_flip_4 | `paint(x, local(reflect(x)))` | 65.5 | ✗ |
| 1d_flip_40 | `paint(paint(shift(x), local(x)), segment(x))` | 96.8 | ✗ |
| 1d_flip_41 | `paint(paint(x, local(shift(x))), local(x))` | 70.2 | ✗ |
| 1d_flip_42 | `paint(paint(shift(x), local(x)), scan(x))` | 86.1 | ✗ |
| 1d_flip_43 | `paint(paint(shift(x), local(x)), local(x))` | 109.4 | ✗ |
| 1d_flip_44 | `paint(paint(x, local(shift(x))), local(x))` | 87.8 | ✗ |
| 1d_flip_45 | `paint(x, scan(x))` | 103.9 | ✗ |
| 1d_flip_46 | `paint(reflect(x), local(x))` | 85.5 | ✗ |
| 1d_flip_47 | `paint(paint(x, local(shift(x))), local(x))` | 62.6 | ✗ |
| 1d_flip_48 | `paint(paint(shift(x), local(x)), segment(x))` | 81.9 | ✗ |
| 1d_flip_49 | `paint(paint(x, segment(x)), scan(x))` | 71.5 | ✗ |
| 1d_flip_5 | `paint(paint(x, local(shift(x))), segment(x))` | 91.9 | ✗ |
| 1d_flip_6 | `paint(shift(shift(x)), local(x))` | 90.7 | ✗ |
| 1d_flip_7 | `paint(paint(shift(x), local(x)), local(x))` | 81.8 | ✓ |
| 1d_flip_8 | `paint(paint(x, segment(x)), local(x))` | 64.4 | ✓ |
| 1d_flip_9 | `paint(shift(shift(x)), local(x))` | 82.4 | ✗ |
| 1d_hollow_0 | `paint(paint(x, segment(x)), segment(x))` | 59.2 | ✗ |
| 1d_hollow_1 | `paint(paint(x, local(x)), segment(x))` | 39.4 | ✓ |
| 1d_hollow_10 | `paint(paint(x, segment(shift(x))), local(x))` | 50.1 | ✓ |
| 1d_hollow_11 | `paint(x, scan(paint(x, segment(x))))` | 67.8 | ✓ |
| 1d_hollow_12 | `paint(paint(x, segment(shift(x))), local(x))` | 52.5 | ✓ |
| 1d_hollow_13 | `paint(paint(x, local(x)), segment(x))` | 44.4 | ✓ |
| 1d_hollow_14 | `paint(paint(shift(x), scan(x)), local(x))` | 54.5 | ✓ |
| 1d_hollow_15 | `paint(recolour(x), local(x))` | 61.9 | ✓ |
| 1d_hollow_16 | `paint(x, local(x))` | 58.1 | ✓ |
| 1d_hollow_17 | `paint(paint(shift(x), scan(x)), local(x))` | 40.0 | ✓ |
| 1d_hollow_18 | `paint(paint(x, local(x)), segment(shift(x)))` | 42.8 | ✓ |
| 1d_hollow_19 | `paint(paint(x, scan(x)), local(shift(x)))` | 48.0 | ✓ |
| 1d_hollow_2 | `paint(x, scan(paint(x, local(x))))` | 53.0 | ✓ |
| 1d_hollow_20 | `paint(paint(x, local(x)), local(x))` | 56.3 | ✓ |
| 1d_hollow_21 | `paint(paint(x, segment(x)), scan(x))` | 68.5 | ✓ |
| 1d_hollow_22 | `paint(paint(x, segment(x)), segment(x))` | 72.6 | ✓ |
| 1d_hollow_23 | `paint(paint(x, segment(x)), scan(x))` | 62.3 | ✓ |
| 1d_hollow_24 | `paint(paint(x, local(x)), segment(x))` | 70.8 | ✓ |
| 1d_hollow_25 | `paint(paint(x, local(shift(x))), scan(x))` | 66.7 | ✓ |
| 1d_hollow_26 | `paint(paint(x, local(x)), segment(x))` | 51.6 | ✓ |
| 1d_hollow_27 | `paint(x, local(x))` | 47.4 | ✓ |
| 1d_hollow_28 | `paint(x, local(paint(shift(x), local(x))))` | 69.2 | ✗ |
| 1d_hollow_29 | `paint(paint(shift(x), local(x)), scan(x))` | 62.2 | ✓ |
| 1d_hollow_3 | `recolour(paint(x, local(x)))` | 65.1 | ✓ |
| 1d_hollow_30 | `recolour(paint(x, local(x)))` | 59.5 | ✓ |
| 1d_hollow_31 | `paint(paint(x, scan(x)), local(shift(x)))` | 50.6 | ✗ |
| 1d_hollow_32 | `paint(paint(x, local(x)), segment(x))` | 53.3 | ✓ |
| 1d_hollow_33 | `paint(paint(x, segment(x)), segment(x))` | 53.2 | ✓ |
| 1d_hollow_34 | `paint(paint(x, local(x)), segment(shift(x)))` | 36.9 | ✓ |
| 1d_hollow_35 | `paint(paint(x, local(x)), segment(x))` | 40.8 | ✓ |
| 1d_hollow_36 | `paint(paint(x, local(x)), local(x))` | 53.2 | ✓ |
| 1d_hollow_37 | `paint(x, local(paint(x, local(x))))` | 59.6 | ✓ |
| 1d_hollow_38 | `paint(paint(x, segment(x)), segment(x))` | 60.6 | ✓ |
| 1d_hollow_39 | `paint(paint(x, segment(shift(x))), local(x))` | 54.8 | ✓ |
| 1d_hollow_4 | `paint(paint(x, local(x)), segment(x))` | 44.3 | ✓ |
| 1d_hollow_40 | `paint(paint(x, local(x)), segment(shift(x)))` | 49.8 | ✓ |
| 1d_hollow_41 | `paint(paint(x, segment(x)), scan(x))` | 50.6 | ✓ |
| 1d_hollow_42 | `paint(x, local(x))` | 71.5 | ✓ |
| 1d_hollow_43 | `paint(paint(x, segment(x)), scan(x))` | 51.0 | ✓ |
| 1d_hollow_44 | `paint(paint(x, scan(x)), local(shift(x)))` | 56.4 | ✓ |
| 1d_hollow_45 | `paint(paint(x, local(x)), segment(shift(x)))` | 41.0 | ✓ |
| 1d_hollow_46 | `paint(paint(x, segment(x)), scan(x))` | 64.5 | ✓ |
| 1d_hollow_47 | `paint(paint(x, segment(x)), scan(x))` | 68.3 | ✓ |
| 1d_hollow_48 | `paint(paint(x, local(x)), segment(shift(x)))` | 40.8 | ✓ |
| 1d_hollow_49 | `paint(paint(x, segment(x)), scan(x))` | 69.6 | ✓ |
| 1d_hollow_5 | `paint(paint(x, local(x)), segment(shift(x)))` | 47.4 | ✓ |
| 1d_hollow_6 | `paint(paint(x, segment(x)), segment(x))` | 37.7 | ✓ |
| 1d_hollow_7 | `recolour(paint(x, local(x)))` | 50.8 | ✓ |
| 1d_hollow_8 | `paint(paint(x, local(x)), local(x))` | 48.0 | ✓ |
| 1d_hollow_9 | `paint(paint(x, local(x)), segment(shift(x)))` | 51.5 | ✓ |
| 1d_mirror_0 | `paint(recolour(x), scan(x))` | 178.4 | ✗ |
| 1d_mirror_1 | `shift(reflect(x))` | 87.0 | ✗ |
| 1d_mirror_10 | `shift(reflect(shift(x)))` | 111.9 | ✗ |
| 1d_mirror_11 | `paint(paint(x, scan(x)), scan(x))` | 169.1 | ✗ |
| 1d_mirror_12 | `shift(reflect(shift(x)))` | 131.5 | ✗ |
| 1d_mirror_13 | `paint(paint(x, scan(x)), scan(x))` | 151.6 | ✗ |
| 1d_mirror_14 | `shift(reflect(shift(x)))` | 111.0 | ✗ |
| 1d_mirror_15 | `shift(reflect(x))` | 96.8 | ✗ |
| 1d_mirror_16 | `paint(paint(x, scan(x)), scan(x))` | 153.4 | ✗ |
| 1d_mirror_17 | `shift(reflect(x))` | 69.9 | ✗ |
| 1d_mirror_18 | `shift(reflect(x))` | 86.8 | ✗ |
| 1d_mirror_19 | `shift(reflect(x))` | 88.3 | ✗ |
| 1d_mirror_2 | `paint(paint(x, local(x)), segment(x))` | 136.4 | ✗ |
| 1d_mirror_20 | `recolour(paint(x, local(shift(x))))` | 136.6 | ✗ |
| 1d_mirror_21 | `reflect(shift(x))` | 83.7 | ✗ |
| 1d_mirror_22 | `paint(paint(x, scan(x)), scan(x))` | 134.0 | ✗ |
| 1d_mirror_23 | `shift(reflect(shift(x)))` | 116.5 | ✗ |
| 1d_mirror_24 | `paint(paint(x, scan(x)), segment(x))` | 145.9 | ✗ |
| 1d_mirror_25 | `paint(paint(x, segment(x)), scan(x))` | 169.3 | ✗ |
| 1d_mirror_26 | `paint(paint(x, scan(x)), segment(x))` | 131.8 | ✗ |
| 1d_mirror_27 | `shift(shift(paint(x, segment(x))))` | 152.5 | ✗ |
| 1d_mirror_28 | `shift(reflect(x))` | 87.1 | ✓ |
| 1d_mirror_29 | `paint(paint(x, local(shift(x))), segment(x))` | 136.5 | ✗ |
| 1d_mirror_3 | `paint(paint(x, scan(x)), segment(x))` | 137.9 | ✗ |
| 1d_mirror_30 | `paint(recolour(x), scan(x))` | 162.8 | ✗ |
| 1d_mirror_31 | `shift(reflect(x))` | 67.9 | ✗ |
| 1d_mirror_32 | `shift(reflect(x))` | 76.8 | ✗ |
| 1d_mirror_33 | `shift(reflect(shift(x)))` | 123.6 | ✗ |
| 1d_mirror_34 | `reflect(shift(x))` | 76.8 | ✗ |
| 1d_mirror_35 | `paint(paint(x, local(x)), scan(x))` | 160.5 | ✗ |
| 1d_mirror_36 | `reflect(shift(shift(x)))` | 143.0 | ✗ |
| 1d_mirror_37 | `paint(paint(x, segment(x)), local(shift(x)))` | 96.3 | ✗ |
| 1d_mirror_38 | `paint(paint(x, local(x)), scan(x))` | 160.0 | ✗ |
| 1d_mirror_39 | `shift(reflect(shift(x)))` | 145.3 | ✗ |
| 1d_mirror_4 | `paint(paint(x, scan(x)), segment(x))` | 171.9 | ✗ |
| 1d_mirror_40 | `shift(reflect(x))` | 89.3 | ✗ |
| 1d_mirror_41 | `reflect(shift(x))` | 77.0 | ✗ |
| 1d_mirror_42 | `paint(x, scan(paint(x, local(shift(x)))))` | 150.3 | ✗ |
| 1d_mirror_43 | `shift(reflect(x))` | 89.3 | ✗ |
| 1d_mirror_44 | `shift(reflect(x))` | 89.8 | ✗ |
| 1d_mirror_45 | `paint(paint(x, local(x)), local(shift(x)))` | 108.5 | ✗ |
| 1d_mirror_46 | `paint(x, local(paint(shift(x), segment(x))))` | 104.7 | ✓ |
| 1d_mirror_47 | `paint(paint(x, scan(x)), segment(x))` | 123.6 | ✗ |
| 1d_mirror_48 | `paint(recolour(x), scan(x))` | 132.0 | ✗ |
| 1d_mirror_49 | `paint(recolour(x), scan(x))` | 147.8 | ✗ |
| 1d_mirror_5 | `paint(paint(x, scan(x)), segment(x))` | 177.7 | ✗ |
| 1d_mirror_6 | `paint(x, local(reflect(x)))` | 101.8 | ✗ |
| 1d_mirror_7 | `paint(x, local(recolour(shift(x))))` | 107.5 | ✓ |
| 1d_mirror_8 | `paint(paint(x, scan(x)), scan(x))` | 127.2 | ✗ |
| 1d_mirror_9 | `paint(paint(x, scan(x)), segment(x))` | 149.8 | ✗ |
| 1d_move_1p_0 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_1 | `paint(shift(paint(x, local(x))), segment(x))` | 52.2 | ✓ |
| 1d_move_1p_10 | `shift(x)` | 52.5 | ✓ |
| 1d_move_1p_11 | `paint(shift(x), local(x))` | 52.5 | ✓ |
| 1d_move_1p_12 | `paint(shift(shift(x)), local(x))` | 52.4 | ✓ |
| 1d_move_1p_13 | `paint(shift(paint(x, local(x))), local(x))` | 51.5 | ✓ |
| 1d_move_1p_14 | `paint(shift(x), scan(paint(x, local(x))))` | 44.2 | ✓ |
| 1d_move_1p_15 | `paint(shift(x), local(x))` | 44.9 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 53.1 | ✓ |
| 1d_move_1p_17 | `paint(shift(shift(x)), local(x))` | 51.4 | ✓ |
| 1d_move_1p_18 | `paint(shift(x), local(x))` | 50.0 | ✗ |
| 1d_move_1p_19 | `shift(x)` | 54.7 | ✓ |
| 1d_move_1p_2 | `paint(shift(paint(x, local(x))), segment(x))` | 50.5 | ✓ |
| 1d_move_1p_20 | `paint(shift(paint(x, local(x))), segment(x))` | 49.6 | ✓ |
| 1d_move_1p_21 | `paint(shift(paint(x, local(x))), segment(x))` | 52.5 | ✓ |
| 1d_move_1p_22 | `paint(shift(x), local(x))` | 51.5 | ✓ |
| 1d_move_1p_23 | `paint(shift(x), local(x))` | 47.5 | ✓ |
| 1d_move_1p_24 | `shift(x)` | 51.9 | ✓ |
| 1d_move_1p_25 | `paint(shift(paint(x, local(x))), local(x))` | 53.3 | ✓ |
| 1d_move_1p_26 | `paint(shift(shift(x)), scan(x))` | 35.7 | ✓ |
| 1d_move_1p_27 | `shift(x)` | 56.1 | ✓ |
| 1d_move_1p_28 | `paint(shift(shift(x)), scan(x))` | 50.7 | ✓ |
| 1d_move_1p_29 | `paint(shift(x), local(x))` | 46.4 | ✓ |
| 1d_move_1p_3 | `paint(shift(shift(x)), local(x))` | 52.3 | ✓ |
| 1d_move_1p_30 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_31 | `paint(shift(paint(x, local(x))), local(x))` | 53.3 | ✓ |
| 1d_move_1p_32 | `paint(shift(shift(x)), scan(x))` | 52.4 | ✓ |
| 1d_move_1p_33 | `paint(paint(shift(x), segment(x)), local(x))` | 49.7 | ✓ |
| 1d_move_1p_34 | `shift(x)` | 53.8 | ✓ |
| 1d_move_1p_35 | `shift(x)` | 52.1 | ✓ |
| 1d_move_1p_36 | `paint(shift(shift(x)), local(x))` | 51.5 | ✓ |
| 1d_move_1p_37 | `shift(x)` | 54.8 | ✓ |
| 1d_move_1p_38 | `shift(x)` | 54.7 | ✓ |
| 1d_move_1p_39 | `shift(x)` | 55.7 | ✓ |
| 1d_move_1p_4 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_40 | `paint(shift(x), local(x))` | 50.0 | ✓ |
| 1d_move_1p_41 | `shift(x)` | 53.4 | ✓ |
| 1d_move_1p_42 | `paint(shift(x), local(x))` | 53.4 | ✓ |
| 1d_move_1p_43 | `paint(shift(paint(x, local(x))), segment(x))` | 48.6 | ✓ |
| 1d_move_1p_44 | `paint(paint(shift(x), local(x)), segment(x))` | 45.5 | ✓ |
| 1d_move_1p_45 | `shift(x)` | 53.7 | ✓ |
| 1d_move_1p_46 | `paint(shift(paint(x, local(x))), segment(x))` | 47.2 | ✓ |
| 1d_move_1p_47 | `paint(shift(x), scan(paint(x, local(x))))` | 52.3 | ✓ |
| 1d_move_1p_48 | `shift(x)` | 54.1 | ✓ |
| 1d_move_1p_49 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_5 | `shift(x)` | 51.0 | ✓ |
| 1d_move_1p_6 | `paint(shift(shift(x)), local(x))` | 51.5 | ✓ |
| 1d_move_1p_7 | `paint(shift(x), scan(shift(x)))` | 48.7 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 54.8 | ✓ |
| 1d_move_1p_9 | `shift(x)` | 51.0 | ✓ |
| 1d_move_2p_0 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_1 | `shift(x)` | 46.8 | ✓ |
| 1d_move_2p_10 | `shift(x)` | 47.0 | ✓ |
| 1d_move_2p_11 | `shift(x)` | 47.0 | ✓ |
| 1d_move_2p_12 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_13 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_14 | `shift(x)` | 47.6 | ✓ |
| 1d_move_2p_15 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_16 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_17 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_18 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_19 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_2 | `shift(x)` | 46.8 | ✓ |
| 1d_move_2p_20 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_21 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_22 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_23 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_24 | `shift(x)` | 46.5 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_26 | `shift(x)` | 46.8 | ✓ |
| 1d_move_2p_27 | `shift(x)` | 48.9 | ✓ |
| 1d_move_2p_28 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_29 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_3 | `paint(paint(shift(x), local(x)), segment(x))` | 40.5 | ✓ |
| 1d_move_2p_30 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_31 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_32 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_33 | `shift(x)` | 46.8 | ✓ |
| 1d_move_2p_34 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_35 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_36 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_37 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_38 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_39 | `shift(x)` | 48.7 | ✓ |
| 1d_move_2p_4 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_40 | `paint(paint(shift(x), local(x)), segment(x))` | 44.1 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.6 | ✓ |
| 1d_move_2p_42 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_43 | `paint(paint(shift(x), local(x)), segment(x))` | 42.6 | ✓ |
| 1d_move_2p_44 | `shift(x)` | 54.1 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_46 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_48 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_49 | `shift(x)` | 46.8 | ✓ |
| 1d_move_2p_5 | `shift(x)` | 45.8 | ✓ |
| 1d_move_2p_6 | `paint(paint(shift(x), local(x)), segment(x))` | 43.6 | ✓ |
| 1d_move_2p_7 | `shift(x)` | 53.3 | ✓ |
| 1d_move_2p_8 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_9 | `paint(paint(shift(x), local(x)), segment(x))` | 43.2 | ✓ |
| 1d_move_2p_dp_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 55.6 | ✗ |
| 1d_move_2p_dp_1 | `paint(x, local(x))` | 63.2 | ✗ |
| 1d_move_2p_dp_10 | `paint(paint(x, local(x)), segment(shift(x)))` | 67.7 | ✓ |
| 1d_move_2p_dp_11 | `paint(paint(x, local(x)), local(shift(x)))` | 61.5 | ✓ |
| 1d_move_2p_dp_12 | `paint(paint(shift(x), local(x)), scan(x))` | 64.8 | ✓ |
| 1d_move_2p_dp_13 | `paint(paint(x, local(x)), local(shift(x)))` | 57.2 | ✓ |
| 1d_move_2p_dp_14 | `paint(paint(shift(x), local(x)), scan(x))` | 69.4 | ✓ |
| 1d_move_2p_dp_15 | `paint(paint(x, local(x)), local(shift(x)))` | 53.6 | ✓ |
| 1d_move_2p_dp_16 | `paint(paint(x, local(x)), local(shift(x)))` | 59.8 | ✓ |
| 1d_move_2p_dp_17 | `paint(x, local(paint(x, local(shift(x)))))` | 63.3 | ✓ |
| 1d_move_2p_dp_18 | `paint(paint(x, local(x)), segment(x))` | 60.0 | ✗ |
| 1d_move_2p_dp_19 | `paint(paint(x, local(x)), local(shift(x)))` | 50.7 | ✓ |
| 1d_move_2p_dp_2 | `paint(paint(x, local(x)), local(shift(x)))` | 64.7 | ✓ |
| 1d_move_2p_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 67.8 | ✗ |
| 1d_move_2p_dp_21 | `paint(paint(x, local(x)), scan(shift(x)))` | 68.3 | ✓ |
| 1d_move_2p_dp_22 | `paint(paint(x, segment(shift(x))), local(x))` | 66.4 | ✓ |
| 1d_move_2p_dp_23 | `paint(paint(x, local(x)), segment(x))` | 81.2 | ✓ |
| 1d_move_2p_dp_24 | `paint(paint(x, scan(x)), local(x))` | 56.8 | ✓ |
| 1d_move_2p_dp_25 | `paint(paint(x, local(x)), scan(shift(x)))` | 59.3 | ✓ |
| 1d_move_2p_dp_26 | `paint(paint(x, local(x)), local(shift(x)))` | 56.6 | ✓ |
| 1d_move_2p_dp_27 | `paint(paint(x, segment(shift(x))), local(x))` | 74.9 | ✓ |
| 1d_move_2p_dp_28 | `paint(paint(x, local(x)), scan(x))` | 51.5 | ✓ |
| 1d_move_2p_dp_29 | `paint(shift(x), local(paint(x, local(x))))` | 81.5 | ✓ |
| 1d_move_2p_dp_3 | `paint(paint(x, local(x)), local(shift(x)))` | 56.9 | ✓ |
| 1d_move_2p_dp_30 | `paint(paint(x, local(x)), segment(shift(x)))` | 68.3 | ✓ |
| 1d_move_2p_dp_31 | `paint(paint(x, local(x)), segment(x))` | 63.0 | ✓ |
| 1d_move_2p_dp_32 | `paint(paint(x, local(x)), local(shift(x)))` | 61.8 | ✓ |
| 1d_move_2p_dp_33 | `paint(paint(x, local(shift(x))), local(x))` | 71.4 | ✓ |
| 1d_move_2p_dp_34 | `paint(paint(x, segment(shift(x))), local(x))` | 72.6 | ✓ |
| 1d_move_2p_dp_35 | `paint(shift(x), local(paint(x, scan(x))))` | 78.7 | ✓ |
| 1d_move_2p_dp_36 | `paint(paint(x, local(x)), local(shift(x)))` | 59.6 | ✓ |
| 1d_move_2p_dp_37 | `paint(paint(shift(x), local(x)), segment(x))` | 62.7 | ✓ |
| 1d_move_2p_dp_38 | `paint(paint(x, local(x)), local(shift(x)))` | 63.0 | ✗ |
| 1d_move_2p_dp_39 | `paint(paint(x, local(x)), local(shift(x)))` | 58.1 | ✓ |
| 1d_move_2p_dp_4 | `paint(paint(x, scan(x)), local(x))` | 74.0 | ✓ |
| 1d_move_2p_dp_40 | `paint(paint(shift(x), local(x)), scan(x))` | 57.8 | ✓ |
| 1d_move_2p_dp_41 | `paint(paint(x, local(x)), scan(shift(x)))` | 62.8 | ✓ |
| 1d_move_2p_dp_42 | `paint(shift(recolour(x)), local(x))` | 73.1 | ✓ |
| 1d_move_2p_dp_43 | `paint(paint(x, local(x)), segment(shift(x)))` | 58.7 | ✓ |
| 1d_move_2p_dp_44 | `paint(paint(shift(x), scan(x)), local(x))` | 53.8 | ✓ |
| 1d_move_2p_dp_45 | `paint(paint(x, local(x)), local(shift(x)))` | 55.4 | ✗ |
| 1d_move_2p_dp_46 | `paint(paint(x, local(x)), segment(shift(x)))` | 52.9 | ✓ |
| 1d_move_2p_dp_47 | `paint(paint(x, local(x)), segment(shift(x)))` | 58.5 | ✗ |
| 1d_move_2p_dp_48 | `paint(paint(x, local(x)), local(shift(x)))` | 52.5 | ✓ |
| 1d_move_2p_dp_49 | `paint(paint(x, local(x)), local(shift(x)))` | 55.2 | ✓ |
| 1d_move_2p_dp_5 | `paint(paint(x, local(x)), local(shift(x)))` | 58.1 | ✗ |
| 1d_move_2p_dp_6 | `paint(paint(x, local(x)), segment(x))` | 46.1 | ✓ |
| 1d_move_2p_dp_7 | `paint(shift(x), scan(shift(x)))` | 71.5 | ✓ |
| 1d_move_2p_dp_8 | `paint(paint(x, local(x)), segment(shift(x)))` | 72.4 | ✓ |
| 1d_move_2p_dp_9 | `paint(paint(x, local(x)), local(shift(x)))` | 55.2 | ✓ |
| 1d_move_3p_0 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_1 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_10 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_11 | `shift(x)` | 52.7 | ✓ |
| 1d_move_3p_12 | `paint(paint(x, local(x)), local(shift(x)))` | 47.5 | ✓ |
| 1d_move_3p_13 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_14 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_15 | `shift(x)` | 52.3 | ✓ |
| 1d_move_3p_16 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_17 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_18 | `paint(shift(paint(x, scan(x))), local(x))` | 45.3 | ✓ |
| 1d_move_3p_19 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_2 | `paint(paint(x, local(x)), segment(x))` | 34.6 | ✓ |
| 1d_move_3p_20 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_21 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_22 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_23 | `shift(x)` | 52.8 | ✓ |
| 1d_move_3p_24 | `paint(paint(x, local(x)), local(shift(x)))` | 45.7 | ✓ |
| 1d_move_3p_25 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_26 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_27 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_28 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_29 | `shift(x)` | 52.6 | ✓ |
| 1d_move_3p_3 | `paint(paint(x, local(x)), scan(x))` | 53.0 | ✓ |
| 1d_move_3p_30 | `shift(x)` | 52.6 | ✓ |
| 1d_move_3p_31 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 52.3 | ✓ |
| 1d_move_3p_35 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_36 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_37 | `shift(x)` | 52.4 | ✓ |
| 1d_move_3p_38 | `shift(x)` | 52.3 | ✓ |
| 1d_move_3p_39 | `shift(x)` | 52.5 | ✓ |
| 1d_move_3p_4 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_40 | `paint(paint(x, local(x)), local(shift(x)))` | 40.3 | ✓ |
| 1d_move_3p_41 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_43 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_44 | `shift(x)` | 57.0 | ✓ |
| 1d_move_3p_45 | `shift(x)` | 52.3 | ✓ |
| 1d_move_3p_46 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_47 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_48 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_49 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_5 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_6 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_7 | `shift(x)` | 56.7 | ✓ |
| 1d_move_3p_8 | `shift(x)` | 52.6 | ✓ |
| 1d_move_3p_9 | `shift(x)` | 53.8 | ✓ |
| 1d_move_dp_0 | `paint(x, local(reflect(x)))` | 106.1 | ✗ |
| 1d_move_dp_1 | `paint(x, local(paint(shift(x), local(x))))` | 95.1 | ✗ |
| 1d_move_dp_10 | `paint(paint(x, scan(x)), local(shift(x)))` | 123.5 | ✗ |
| 1d_move_dp_11 | `paint(x, scan(paint(x, local(x))))` | 119.4 | ✗ |
| 1d_move_dp_12 | `paint(reflect(x), local(x))` | 100.0 | ✗ |
| 1d_move_dp_13 | `shift(paint(recolour(x), scan(x)))` | 146.3 | ✗ |
| 1d_move_dp_14 | `paint(paint(x, local(x)), segment(shift(x)))` | 62.8 | ✗ |
| 1d_move_dp_15 | `paint(x, scan(x))` | 129.9 | ✗ |
| 1d_move_dp_16 | `paint(x, local(paint(shift(x), scan(x))))` | 138.5 | ✗ |
| 1d_move_dp_17 | `paint(x, local(reflect(x)))` | 100.7 | ✗ |
| 1d_move_dp_18 | `shift(shift(x))` | 105.3 | ✗ |
| 1d_move_dp_19 | `paint(x, local(reflect(x)))` | 79.9 | ✗ |
| 1d_move_dp_2 | `paint(x, scan(paint(x, segment(x))))` | 178.1 | ✗ |
| 1d_move_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 67.8 | ✗ |
| 1d_move_dp_21 | `paint(x, scan(x))` | 141.9 | ✗ |
| 1d_move_dp_22 | `paint(x, local(paint(shift(x), segment(x))))` | 79.4 | ✗ |
| 1d_move_dp_23 | `paint(reflect(x), scan(x))` | 121.6 | ✗ |
| 1d_move_dp_24 | `paint(x, scan(reflect(x)))` | 118.7 | ✗ |
| 1d_move_dp_25 | `paint(paint(shift(x), scan(x)), local(x))` | 132.1 | ✗ |
| 1d_move_dp_26 | `paint(paint(x, scan(x)), local(x))` | 111.3 | ✗ |
| 1d_move_dp_27 | `shift(x)` | 63.1 | ✗ |
| 1d_move_dp_28 | `paint(paint(x, local(x)), scan(x))` | 109.3 | ✗ |
| 1d_move_dp_29 | `reflect(paint(x, local(x)))` | 100.3 | ✗ |
| 1d_move_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 86.6 | ✗ |
| 1d_move_dp_30 | `paint(paint(shift(x), local(x)), local(x))` | 96.5 | ✓ |
| 1d_move_dp_31 | `paint(paint(x, scan(x)), local(shift(x)))` | 158.5 | ✗ |
| 1d_move_dp_32 | `paint(paint(x, scan(x)), local(x))` | 122.8 | ✗ |
| 1d_move_dp_33 | `recolour(paint(x, local(shift(x))))` | 99.3 | ✗ |
| 1d_move_dp_34 | `paint(paint(x, segment(x)), scan(x))` | 90.8 | ✗ |
| 1d_move_dp_35 | `paint(recolour(x), scan(x))` | 119.7 | ✗ |
| 1d_move_dp_36 | `paint(paint(x, scan(x)), local(x))` | 112.8 | ✗ |
| 1d_move_dp_37 | `paint(paint(x, local(x)), segment(x))` | 62.3 | ✓ |
| 1d_move_dp_38 | `paint(paint(x, local(x)), scan(shift(x)))` | 149.5 | ✗ |
| 1d_move_dp_39 | `shift(paint(x, local(paint(x, scan(x)))))` | 110.8 | ✗ |
| 1d_move_dp_4 | `paint(x, scan(paint(shift(x), local(x))))` | 99.6 | ✗ |
| 1d_move_dp_40 | `paint(reflect(x), local(x))` | 83.0 | ✗ |
| 1d_move_dp_41 | `paint(paint(x, local(x)), segment(shift(x)))` | 66.7 | ✗ |
| 1d_move_dp_42 | `paint(reflect(x), scan(x))` | 126.7 | ✗ |
| 1d_move_dp_43 | `paint(paint(shift(x), local(x)), local(x))` | 84.1 | ✗ |
| 1d_move_dp_44 | `paint(paint(shift(x), local(x)), local(x))` | 64.6 | ✓ |
| 1d_move_dp_45 | `paint(paint(x, local(x)), local(shift(x)))` | 55.4 | ✗ |
| 1d_move_dp_46 | `paint(x, local(reflect(x)))` | 75.0 | ✗ |
| 1d_move_dp_47 | `shift(paint(paint(x, scan(x)), local(x)))` | 125.2 | ✗ |
| 1d_move_dp_48 | `paint(paint(x, local(x)), segment(shift(x)))` | 92.1 | ✗ |
| 1d_move_dp_49 | `paint(x, local(reflect(x)))` | 129.1 | ✗ |
| 1d_move_dp_5 | `paint(x, scan(reflect(x)))` | 133.2 | ✗ |
| 1d_move_dp_6 | `paint(x, scan(paint(x, segment(x))))` | 142.1 | ✗ |
| 1d_move_dp_7 | `paint(paint(shift(x), local(x)), local(x))` | 55.0 | ✓ |
| 1d_move_dp_8 | `paint(paint(x, local(x)), local(shift(x)))` | 59.8 | ✗ |
| 1d_move_dp_9 | `paint(shift(paint(x, local(x))), scan(x))` | 144.1 | ✗ |
| 1d_padded_fill_0 | `paint(paint(x, scan(x)), segment(x))` | 55.5 | ✓ |
| 1d_padded_fill_1 | `paint(x, scan(paint(x, scan(x))))` | 37.1 | ✓ |
| 1d_padded_fill_10 | `paint(paint(x, scan(x)), local(x))` | 69.5 | ✓ |
| 1d_padded_fill_11 | `paint(x, scan(paint(x, scan(x))))` | 43.5 | ✓ |
| 1d_padded_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 47.8 | ✓ |
| 1d_padded_fill_13 | `paint(x, scan(paint(x, local(x))))` | 40.9 | ✓ |
| 1d_padded_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 37.2 | ✓ |
| 1d_padded_fill_15 | `paint(paint(x, scan(x)), segment(x))` | 52.6 | ✓ |
| 1d_padded_fill_16 | `recolour(paint(x, scan(x)))` | 47.0 | ✓ |
| 1d_padded_fill_17 | `paint(paint(x, scan(x)), local(shift(x)))` | 64.3 | ✓ |
| 1d_padded_fill_18 | `paint(paint(x, scan(x)), local(x))` | 74.3 | ✓ |
| 1d_padded_fill_19 | `paint(paint(x, scan(x)), local(x))` | 29.9 | ✓ |
| 1d_padded_fill_2 | `paint(paint(shift(x), scan(x)), local(x))` | 67.7 | ✓ |
| 1d_padded_fill_20 | `paint(paint(x, scan(x)), segment(x))` | 68.3 | ✓ |
| 1d_padded_fill_21 | `paint(paint(x, local(x)), scan(x))` | 54.0 | ✓ |
| 1d_padded_fill_22 | `paint(paint(x, local(x)), scan(x))` | 43.5 | ✓ |
| 1d_padded_fill_23 | `paint(paint(x, scan(x)), local(x))` | 32.7 | ✓ |
| 1d_padded_fill_24 | `paint(paint(x, scan(x)), local(shift(x)))` | 47.4 | ✓ |
| 1d_padded_fill_25 | `paint(paint(shift(x), scan(x)), local(x))` | 49.4 | ✓ |
| 1d_padded_fill_26 | `paint(paint(x, scan(x)), local(x))` | 51.7 | ✓ |
| 1d_padded_fill_27 | `paint(recolour(x), scan(x))` | 57.6 | ✓ |
| 1d_padded_fill_28 | `recolour(paint(x, scan(x)))` | 68.8 | ✓ |
| 1d_padded_fill_29 | `paint(paint(x, scan(x)), local(x))` | 50.2 | ✓ |
| 1d_padded_fill_3 | `paint(paint(x, scan(x)), local(x))` | 45.0 | ✓ |
| 1d_padded_fill_30 | `recolour(paint(x, scan(x)))` | 61.7 | ✓ |
| 1d_padded_fill_31 | `paint(paint(x, scan(x)), segment(x))` | 51.4 | ✓ |
| 1d_padded_fill_32 | `paint(paint(x, scan(x)), local(shift(x)))` | 54.5 | ✓ |
| 1d_padded_fill_33 | `paint(paint(x, local(x)), scan(x))` | 44.5 | ✓ |
| 1d_padded_fill_34 | `paint(paint(x, scan(x)), local(x))` | 65.4 | ✓ |
| 1d_padded_fill_35 | `paint(paint(shift(x), scan(x)), local(x))` | 46.8 | ✓ |
| 1d_padded_fill_36 | `paint(paint(x, local(x)), scan(x))` | 40.7 | ✓ |
| 1d_padded_fill_37 | `paint(x, local(paint(x, scan(x))))` | 58.3 | ✓ |
| 1d_padded_fill_38 | `paint(x, scan(paint(x, segment(x))))` | 44.5 | ✓ |
| 1d_padded_fill_39 | `recolour(paint(x, scan(x)))` | 76.1 | ✓ |
| 1d_padded_fill_4 | `paint(paint(x, scan(x)), local(x))` | 56.2 | ✓ |
| 1d_padded_fill_40 | `paint(paint(x, scan(x)), segment(x))` | 58.7 | ✓ |
| 1d_padded_fill_41 | `paint(paint(x, scan(x)), local(x))` | 64.5 | ✓ |
| 1d_padded_fill_42 | `paint(paint(shift(x), scan(x)), local(x))` | 61.4 | ✗ |
| 1d_padded_fill_43 | `paint(paint(x, local(x)), scan(x))` | 46.9 | ✗ |
| 1d_padded_fill_44 | `paint(x, local(paint(shift(x), scan(x))))` | 67.9 | ✓ |
| 1d_padded_fill_45 | `paint(paint(x, scan(x)), segment(x))` | 51.0 | ✓ |
| 1d_padded_fill_46 | `recolour(paint(x, scan(x)))` | 67.2 | ✗ |
| 1d_padded_fill_47 | `paint(paint(x, local(x)), scan(x))` | 48.4 | ✗ |
| 1d_padded_fill_48 | `paint(paint(x, scan(x)), local(shift(x)))` | 38.4 | ✓ |
| 1d_padded_fill_49 | `recolour(paint(x, scan(x)))` | 73.7 | ✓ |
| 1d_padded_fill_5 | `paint(paint(x, scan(x)), segment(x))` | 54.4 | ✓ |
| 1d_padded_fill_6 | `paint(paint(x, scan(x)), segment(x))` | 42.0 | ✓ |
| 1d_padded_fill_7 | `paint(paint(x, scan(x)), segment(x))` | 45.5 | ✓ |
| 1d_padded_fill_8 | `paint(paint(x, scan(x)), segment(x))` | 51.3 | ✓ |
| 1d_padded_fill_9 | `paint(paint(x, local(x)), scan(x))` | 48.7 | ✗ |
| 1d_pcopy_1c_0 | `paint(x, local(paint(x, scan(shift(x)))))` | 83.0 | ✗ |
| 1d_pcopy_1c_1 | `paint(x, scan(paint(x, segment(x))))` | 69.1 | ✗ |
| 1d_pcopy_1c_10 | `paint(x, local(x))` | 66.3 | ✓ |
| 1d_pcopy_1c_11 | `paint(x, local(paint(x, scan(shift(x)))))` | 75.1 | ✗ |
| 1d_pcopy_1c_12 | `paint(paint(x, scan(x)), local(x))` | 57.5 | ✗ |
| 1d_pcopy_1c_13 | `paint(x, scan(paint(x, segment(x))))` | 74.3 | ✗ |
| 1d_pcopy_1c_14 | `paint(x, local(paint(x, local(shift(x)))))` | 75.6 | ✗ |
| 1d_pcopy_1c_15 | `paint(paint(x, local(x)), scan(shift(x)))` | 54.6 | ✗ |
| 1d_pcopy_1c_16 | `paint(paint(x, segment(x)), local(x))` | 59.7 | ✗ |
| 1d_pcopy_1c_17 | `paint(paint(x, local(shift(x))), local(x))` | 69.7 | ✗ |
| 1d_pcopy_1c_18 | `paint(paint(x, segment(x)), local(x))` | 65.3 | ✓ |
| 1d_pcopy_1c_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 84.2 | ✓ |
| 1d_pcopy_1c_2 | `paint(x, local(paint(x, scan(x))))` | 56.1 | ✓ |
| 1d_pcopy_1c_20 | `paint(shift(paint(x, scan(x))), local(x))` | 85.5 | ✗ |
| 1d_pcopy_1c_21 | `paint(paint(x, local(x)), scan(shift(x)))` | 79.1 | ✗ |
| 1d_pcopy_1c_22 | `paint(shift(shift(x)), local(x))` | 88.9 | ✓ |
| 1d_pcopy_1c_23 | `paint(x, local(paint(x, local(shift(x)))))` | 70.8 | ✓ |
| 1d_pcopy_1c_24 | `paint(paint(x, scan(x)), local(x))` | 57.1 | ✗ |
| 1d_pcopy_1c_25 | `paint(recolour(x), scan(x))` | 77.9 | ✗ |
| 1d_pcopy_1c_26 | `paint(shift(paint(x, scan(x))), local(x))` | 96.8 | ✗ |
| 1d_pcopy_1c_27 | `paint(paint(x, scan(x)), local(x))` | 58.1 | ✗ |
| 1d_pcopy_1c_28 | `paint(x, local(paint(x, scan(shift(x)))))` | 80.3 | ✓ |
| 1d_pcopy_1c_29 | `paint(paint(x, segment(x)), local(x))` | 90.0 | ✓ |
| 1d_pcopy_1c_3 | `paint(recolour(x), local(x))` | 88.6 | ✓ |
| 1d_pcopy_1c_30 | `paint(shift(paint(x, scan(x))), local(x))` | 85.6 | ✗ |
| 1d_pcopy_1c_31 | `paint(x, local(paint(x, local(x))))` | 79.5 | ✓ |
| 1d_pcopy_1c_32 | `paint(x, local(paint(x, segment(x))))` | 90.9 | ✓ |
| 1d_pcopy_1c_33 | `paint(paint(x, local(x)), local(x))` | 84.6 | ✓ |
| 1d_pcopy_1c_34 | `paint(shift(paint(x, scan(x))), local(x))` | 92.8 | ✗ |
| 1d_pcopy_1c_35 | `paint(paint(x, segment(x)), local(x))` | 78.2 | ✗ |
| 1d_pcopy_1c_36 | `paint(paint(x, local(x)), local(x))` | 86.9 | ✓ |
| 1d_pcopy_1c_37 | `paint(recolour(x), local(x))` | 89.8 | ✗ |
| 1d_pcopy_1c_38 | `paint(x, local(paint(x, segment(x))))` | 81.5 | ✓ |
| 1d_pcopy_1c_39 | `paint(paint(x, segment(x)), local(x))` | 63.4 | ✓ |
| 1d_pcopy_1c_4 | `paint(paint(x, scan(x)), local(x))` | 61.8 | ✗ |
| 1d_pcopy_1c_40 | `paint(x, local(paint(x, scan(shift(x)))))` | 71.7 | ✗ |
| 1d_pcopy_1c_41 | `paint(paint(x, local(x)), scan(shift(x)))` | 59.5 | ✗ |
| 1d_pcopy_1c_42 | `paint(x, scan(x))` | 71.8 | ✗ |
| 1d_pcopy_1c_43 | `paint(x, local(x))` | 77.7 | ✗ |
| 1d_pcopy_1c_44 | `paint(paint(x, segment(x)), local(x))` | 64.6 | ✓ |
| 1d_pcopy_1c_45 | `paint(paint(x, local(x)), scan(shift(x)))` | 72.5 | ✗ |
| 1d_pcopy_1c_46 | `paint(paint(x, scan(x)), local(x))` | 64.4 | ✗ |
| 1d_pcopy_1c_47 | `paint(paint(x, segment(x)), local(x))` | 86.2 | ✓ |
| 1d_pcopy_1c_48 | `paint(paint(x, scan(x)), local(x))` | 60.1 | ✗ |
| 1d_pcopy_1c_49 | `paint(paint(x, local(x)), scan(shift(x)))` | 71.0 | ✗ |
| 1d_pcopy_1c_5 | `paint(paint(x, segment(shift(x))), local(x))` | 74.3 | ✗ |
| 1d_pcopy_1c_6 | `paint(paint(x, scan(x)), local(x))` | 66.1 | ✗ |
| 1d_pcopy_1c_7 | `paint(x, local(x))` | 85.3 | ✓ |
| 1d_pcopy_1c_8 | `paint(x, local(x))` | 81.3 | ✗ |
| 1d_pcopy_1c_9 | `paint(paint(x, local(x)), scan(shift(x)))` | 60.7 | ✓ |
| 1d_pcopy_mc_0 | `paint(shift(x), local(x))` | 70.4 | ✓ |
| 1d_pcopy_mc_1 | `paint(x, local(x))` | 38.5 | ✗ |
| 1d_pcopy_mc_10 | `paint(shift(shift(x)), local(x))` | 75.6 | ✓ |
| 1d_pcopy_mc_11 | `paint(shift(shift(x)), local(x))` | 77.0 | ✓ |
| 1d_pcopy_mc_12 | `paint(paint(x, scan(x)), local(x))` | 45.0 | ✓ |
| 1d_pcopy_mc_13 | `paint(paint(x, segment(x)), local(x))` | 56.9 | ✓ |
| 1d_pcopy_mc_14 | `paint(x, local(paint(x, segment(x))))` | 75.0 | ✓ |
| 1d_pcopy_mc_15 | `paint(shift(paint(x, scan(x))), local(x))` | 67.8 | ✓ |
| 1d_pcopy_mc_16 | `paint(x, local(x))` | 54.6 | ✓ |
| 1d_pcopy_mc_17 | `paint(paint(x, segment(x)), local(x))` | 42.0 | ✓ |
| 1d_pcopy_mc_18 | `paint(x, local(x))` | 37.5 | ✗ |
| 1d_pcopy_mc_19 | `paint(x, local(x))` | 36.9 | ✗ |
| 1d_pcopy_mc_2 | `paint(paint(x, local(x)), local(shift(x)))` | 54.0 | ✓ |
| 1d_pcopy_mc_20 | `paint(shift(x), local(x))` | 83.0 | ✓ |
| 1d_pcopy_mc_21 | `paint(paint(x, segment(x)), local(x))` | 40.5 | ✓ |
| 1d_pcopy_mc_22 | `paint(x, local(x))` | 43.5 | ✓ |
| 1d_pcopy_mc_23 | `paint(x, local(paint(x, local(x))))` | 46.9 | ✓ |
| 1d_pcopy_mc_24 | `paint(paint(x, segment(x)), local(x))` | 66.3 | ✓ |
| 1d_pcopy_mc_25 | `paint(x, local(paint(x, local(x))))` | 78.3 | ✗ |
| 1d_pcopy_mc_26 | `paint(paint(x, segment(x)), local(x))` | 43.3 | ✓ |
| 1d_pcopy_mc_27 | `paint(x, local(x))` | 58.4 | ✗ |
| 1d_pcopy_mc_28 | `paint(x, local(x))` | 52.4 | ✓ |
| 1d_pcopy_mc_29 | `paint(x, local(paint(x, scan(shift(x)))))` | 50.2 | ✓ |
| 1d_pcopy_mc_3 | `paint(paint(x, segment(x)), local(x))` | 40.5 | ✓ |
| 1d_pcopy_mc_30 | `paint(paint(x, segment(x)), local(x))` | 37.3 | ✗ |
| 1d_pcopy_mc_31 | `paint(paint(x, local(shift(x))), local(x))` | 50.7 | ✓ |
| 1d_pcopy_mc_32 | `paint(x, local(paint(shift(x), segment(x))))` | 85.4 | ✓ |
| 1d_pcopy_mc_33 | `paint(paint(x, scan(x)), local(x))` | 77.1 | ✓ |
| 1d_pcopy_mc_34 | `paint(x, local(paint(x, segment(x))))` | 71.4 | ✓ |
| 1d_pcopy_mc_35 | `paint(x, local(x))` | 55.1 | ✓ |
| 1d_pcopy_mc_36 | `paint(paint(x, scan(x)), local(x))` | 52.9 | ✗ |
| 1d_pcopy_mc_37 | `paint(x, local(paint(x, segment(x))))` | 54.4 | ✓ |
| 1d_pcopy_mc_38 | `paint(paint(x, segment(x)), local(x))` | 54.4 | ✓ |
| 1d_pcopy_mc_39 | `paint(x, local(x))` | 73.1 | ✓ |
| 1d_pcopy_mc_4 | `paint(paint(x, scan(x)), local(x))` | 50.4 | ✓ |
| 1d_pcopy_mc_40 | `paint(paint(x, scan(x)), local(x))` | 66.3 | ✗ |
| 1d_pcopy_mc_41 | `paint(paint(x, scan(x)), local(x))` | 51.9 | ✓ |
| 1d_pcopy_mc_42 | `paint(x, local(paint(x, scan(shift(x)))))` | 78.3 | ✗ |
| 1d_pcopy_mc_43 | `paint(x, local(x))` | 43.2 | ✓ |
| 1d_pcopy_mc_44 | `paint(paint(x, scan(x)), local(x))` | 54.7 | ✓ |
| 1d_pcopy_mc_45 | `paint(shift(x), local(x))` | 71.6 | ✓ |
| 1d_pcopy_mc_46 | `paint(paint(x, local(x)), local(x))` | 42.6 | ✓ |
| 1d_pcopy_mc_47 | `paint(x, local(paint(x, segment(x))))` | 50.8 | ✓ |
| 1d_pcopy_mc_48 | `paint(paint(x, segment(x)), local(x))` | 43.9 | ✓ |
| 1d_pcopy_mc_49 | `paint(x, local(x))` | 37.7 | ✓ |
| 1d_pcopy_mc_5 | `paint(paint(x, scan(x)), local(x))` | 59.7 | ✗ |
| 1d_pcopy_mc_6 | `paint(paint(x, local(x)), local(x))` | 52.7 | ✗ |
| 1d_pcopy_mc_7 | `paint(paint(x, local(shift(x))), local(x))` | 46.0 | ✓ |
| 1d_pcopy_mc_8 | `paint(x, local(x))` | 35.5 | ✓ |
| 1d_pcopy_mc_9 | `paint(paint(x, scan(x)), local(x))` | 43.3 | ✓ |
| 1d_recolor_cmp_0 | `paint(paint(x, scan(x)), segment(x))` | 43.9 | ✓ |
| 1d_recolor_cmp_1 | `paint(paint(x, segment(x)), local(shift(x)))` | 30.3 | ✓ |
| 1d_recolor_cmp_10 | `paint(paint(x, local(shift(x))), segment(x))` | 59.4 | ✓ |
| 1d_recolor_cmp_11 | `paint(paint(x, segment(x)), local(shift(x)))` | 48.2 | ✓ |
| 1d_recolor_cmp_12 | `paint(x, segment(recolour(x)))` | 81.7 | ✓ |
| 1d_recolor_cmp_13 | `paint(paint(x, segment(x)), local(x))` | 38.8 | ✓ |
| 1d_recolor_cmp_14 | `recolour(paint(x, segment(x)))` | 61.3 | ✓ |
| 1d_recolor_cmp_15 | `paint(paint(x, scan(x)), segment(x))` | 51.6 | ✓ |
| 1d_recolor_cmp_16 | `paint(paint(x, scan(x)), segment(x))` | 38.3 | ✓ |
| 1d_recolor_cmp_17 | `paint(paint(x, scan(x)), segment(x))` | 70.6 | ✓ |
| 1d_recolor_cmp_18 | `paint(paint(x, scan(x)), segment(x))` | 50.9 | ✓ |
| 1d_recolor_cmp_19 | `paint(paint(x, scan(x)), segment(x))` | 37.7 | ✓ |
| 1d_recolor_cmp_2 | `paint(paint(x, local(x)), segment(x))` | 53.4 | ✓ |
| 1d_recolor_cmp_20 | `paint(paint(x, segment(x)), local(x))` | 45.7 | ✓ |
| 1d_recolor_cmp_21 | `paint(paint(x, segment(x)), segment(x))` | 43.3 | ✓ |
| 1d_recolor_cmp_22 | `paint(paint(x, segment(x)), scan(x))` | 33.1 | ✓ |
| 1d_recolor_cmp_23 | `paint(paint(x, segment(x)), local(x))` | 41.9 | ✓ |
| 1d_recolor_cmp_24 | `paint(paint(x, local(x)), segment(x))` | 37.7 | ✓ |
| 1d_recolor_cmp_25 | `paint(paint(x, scan(x)), segment(x))` | 46.9 | ✓ |
| 1d_recolor_cmp_26 | `paint(paint(x, scan(x)), segment(x))` | 38.6 | ✓ |
| 1d_recolor_cmp_27 | `paint(paint(x, scan(x)), segment(x))` | 51.4 | ✓ |
| 1d_recolor_cmp_28 | `paint(paint(x, local(shift(x))), segment(x))` | 53.2 | ✓ |
| 1d_recolor_cmp_29 | `paint(paint(x, local(x)), segment(x))` | 46.9 | ✓ |
| 1d_recolor_cmp_3 | `paint(paint(x, segment(x)), segment(x))` | 34.5 | ✓ |
| 1d_recolor_cmp_30 | `paint(x, segment(paint(x, segment(x))))` | 86.4 | ✓ |
| 1d_recolor_cmp_31 | `paint(paint(x, local(x)), segment(x))` | 27.7 | ✓ |
| 1d_recolor_cmp_32 | `paint(paint(x, segment(x)), local(x))` | 59.7 | ✓ |
| 1d_recolor_cmp_33 | `paint(paint(x, segment(x)), segment(x))` | 40.4 | ✓ |
| 1d_recolor_cmp_34 | `recolour(paint(x, segment(x)))` | 48.7 | ✓ |
| 1d_recolor_cmp_35 | `paint(paint(x, scan(x)), segment(x))` | 67.1 | ✓ |
| 1d_recolor_cmp_36 | `paint(paint(x, segment(x)), scan(x))` | 35.1 | ✓ |
| 1d_recolor_cmp_37 | `paint(paint(x, segment(x)), local(x))` | 53.8 | ✓ |
| 1d_recolor_cmp_38 | `paint(paint(x, local(x)), segment(x))` | 40.4 | ✓ |
| 1d_recolor_cmp_39 | `paint(paint(x, local(shift(x))), segment(x))` | 59.4 | ✓ |
| 1d_recolor_cmp_4 | `paint(paint(x, scan(x)), segment(x))` | 35.1 | ✓ |
| 1d_recolor_cmp_40 | `paint(paint(x, scan(x)), segment(x))` | 47.0 | ✓ |
| 1d_recolor_cmp_41 | `paint(paint(x, segment(x)), scan(x))` | 29.4 | ✓ |
| 1d_recolor_cmp_42 | `paint(paint(x, segment(x)), scan(x))` | 42.4 | ✓ |
| 1d_recolor_cmp_43 | `paint(paint(x, segment(x)), scan(x))` | 54.9 | ✓ |
| 1d_recolor_cmp_44 | `paint(paint(x, scan(x)), segment(x))` | 52.6 | ✓ |
| 1d_recolor_cmp_45 | `paint(paint(x, segment(x)), local(x))` | 44.2 | ✓ |
| 1d_recolor_cmp_46 | `paint(paint(x, segment(x)), local(shift(x)))` | 32.2 | ✓ |
| 1d_recolor_cmp_47 | `paint(paint(x, segment(x)), segment(x))` | 60.3 | ✓ |
| 1d_recolor_cmp_48 | `paint(paint(x, segment(shift(x))), local(x))` | 54.1 | ✗ |
| 1d_recolor_cmp_49 | `paint(paint(x, segment(x)), scan(x))` | 44.3 | ✓ |
| 1d_recolor_cmp_5 | `paint(paint(x, scan(x)), segment(x))` | 70.0 | ✓ |
| 1d_recolor_cmp_6 | `paint(paint(x, segment(x)), scan(x))` | 59.1 | ✓ |
| 1d_recolor_cmp_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 43.9 | ✓ |
| 1d_recolor_cmp_8 | `paint(paint(x, scan(x)), segment(x))` | 42.0 | ✓ |
| 1d_recolor_cmp_9 | `paint(paint(x, segment(x)), local(x))` | 38.9 | ✓ |
| 1d_recolor_cnt_0 | `paint(paint(x, segment(x)), local(shift(x)))` | 79.2 | ✓ |
| 1d_recolor_cnt_1 | `paint(x, segment(paint(x, local(x))))` | 92.3 | ✓ |
| 1d_recolor_cnt_10 | `paint(paint(x, segment(x)), scan(x))` | 76.9 | ✓ |
| 1d_recolor_cnt_11 | `paint(paint(x, segment(x)), local(x))` | 79.2 | ✓ |
| 1d_recolor_cnt_12 | `paint(paint(x, segment(x)), local(x))` | 79.4 | ✓ |
| 1d_recolor_cnt_13 | `paint(paint(x, local(x)), segment(x))` | 101.9 | ✓ |
| 1d_recolor_cnt_14 | `paint(paint(x, segment(x)), local(x))` | 100.0 | ✓ |
| 1d_recolor_cnt_15 | `paint(paint(x, segment(x)), segment(x))` | 105.2 | ✓ |
| 1d_recolor_cnt_16 | `paint(paint(x, segment(x)), scan(x))` | 82.6 | ✓ |
| 1d_recolor_cnt_17 | `paint(paint(x, segment(x)), segment(x))` | 92.7 | ✓ |
| 1d_recolor_cnt_18 | `paint(x, segment(paint(x, segment(x))))` | 99.0 | ✓ |
| 1d_recolor_cnt_19 | `paint(paint(x, segment(x)), local(shift(x)))` | 87.3 | ✓ |
| 1d_recolor_cnt_2 | `paint(x, segment(paint(x, segment(x))))` | 92.6 | ✓ |
| 1d_recolor_cnt_20 | `paint(x, segment(recolour(x)))` | 81.6 | ✓ |
| 1d_recolor_cnt_21 | `paint(shift(x), segment(x))` | 104.4 | ✓ |
| 1d_recolor_cnt_22 | `paint(paint(x, segment(x)), local(x))` | 111.4 | ✓ |
| 1d_recolor_cnt_23 | `paint(x, segment(x))` | 81.0 | ✓ |
| 1d_recolor_cnt_24 | `paint(paint(x, segment(x)), local(x))` | 85.3 | ✓ |
| 1d_recolor_cnt_25 | `paint(x, segment(x))` | 88.5 | ✓ |
| 1d_recolor_cnt_26 | `paint(paint(x, scan(x)), segment(x))` | 70.0 | ✓ |
| 1d_recolor_cnt_27 | `paint(x, segment(x))` | 93.7 | ✓ |
| 1d_recolor_cnt_28 | `paint(paint(x, segment(x)), local(x))` | 105.7 | ✓ |
| 1d_recolor_cnt_29 | `paint(x, segment(paint(x, segment(x))))` | 87.1 | ✓ |
| 1d_recolor_cnt_3 | `paint(paint(x, segment(x)), local(x))` | 97.9 | ✓ |
| 1d_recolor_cnt_30 | `paint(paint(x, local(x)), segment(x))` | 102.1 | ✓ |
| 1d_recolor_cnt_31 | `paint(paint(x, segment(x)), scan(x))` | 89.0 | ✓ |
| 1d_recolor_cnt_32 | `paint(paint(x, segment(x)), local(x))` | 88.3 | ✓ |
| 1d_recolor_cnt_33 | `paint(paint(x, segment(x)), local(shift(x)))` | 70.0 | ✓ |
| 1d_recolor_cnt_34 | `paint(x, segment(paint(x, segment(x))))` | 103.2 | ✓ |
| 1d_recolor_cnt_35 | `paint(paint(x, segment(x)), local(x))` | 97.8 | ✓ |
| 1d_recolor_cnt_36 | `paint(paint(x, segment(x)), local(x))` | 57.9 | ✓ |
| 1d_recolor_cnt_37 | `paint(x, segment(recolour(x)))` | 103.4 | ✓ |
| 1d_recolor_cnt_38 | `paint(paint(x, local(x)), segment(x))` | 76.6 | ✓ |
| 1d_recolor_cnt_39 | `paint(paint(x, segment(x)), local(x))` | 89.8 | ✓ |
| 1d_recolor_cnt_4 | `paint(paint(x, segment(x)), local(x))` | 91.9 | ✓ |
| 1d_recolor_cnt_40 | `paint(paint(x, segment(x)), segment(x))` | 108.0 | ✓ |
| 1d_recolor_cnt_41 | `paint(paint(x, segment(x)), local(x))` | 95.4 | ✓ |
| 1d_recolor_cnt_42 | `paint(x, segment(paint(x, local(x))))` | 88.9 | ✓ |
| 1d_recolor_cnt_43 | `paint(paint(x, segment(x)), local(x))` | 79.8 | ✓ |
| 1d_recolor_cnt_44 | `paint(paint(x, segment(x)), local(shift(x)))` | 90.5 | ✓ |
| 1d_recolor_cnt_45 | `paint(x, segment(recolour(x)))` | 100.7 | ✓ |
| 1d_recolor_cnt_46 | `paint(paint(x, segment(x)), local(shift(x)))` | 107.4 | ✓ |
| 1d_recolor_cnt_47 | `paint(x, segment(x))` | 87.7 | ✓ |
| 1d_recolor_cnt_48 | `paint(shift(x), segment(x))` | 88.1 | ✗ |
| 1d_recolor_cnt_49 | `paint(x, segment(recolour(x)))` | 96.2 | ✓ |
| 1d_recolor_cnt_5 | `paint(paint(x, segment(x)), local(shift(x)))` | 90.4 | ✓ |
| 1d_recolor_cnt_6 | `paint(shift(shift(x)), segment(x))` | 124.5 | ✓ |
| 1d_recolor_cnt_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 84.8 | ✓ |
| 1d_recolor_cnt_8 | `paint(paint(x, scan(x)), segment(x))` | 95.4 | ✓ |
| 1d_recolor_cnt_9 | `paint(paint(x, segment(x)), local(x))` | 104.2 | ✓ |
| 1d_recolor_oe_0 | `paint(paint(x, segment(x)), scan(x))` | 70.9 | ✗ |
| 1d_recolor_oe_1 | `recolour(paint(x, segment(x)))` | 73.2 | ✓ |
| 1d_recolor_oe_10 | `paint(paint(x, segment(x)), segment(x))` | 95.7 | ✓ |
| 1d_recolor_oe_11 | `paint(paint(x, segment(x)), local(x))` | 89.2 | ✓ |
| 1d_recolor_oe_12 | `paint(paint(x, segment(x)), local(x))` | 78.5 | ✓ |
| 1d_recolor_oe_13 | `paint(paint(x, segment(x)), segment(x))` | 68.5 | ✓ |
| 1d_recolor_oe_14 | `paint(paint(x, segment(x)), segment(x))` | 67.7 | ✓ |
| 1d_recolor_oe_15 | `paint(paint(x, segment(x)), scan(x))` | 63.7 | ✓ |
| 1d_recolor_oe_16 | `paint(paint(x, segment(x)), local(x))` | 96.6 | ✓ |
| 1d_recolor_oe_17 | `paint(paint(x, segment(x)), local(shift(x)))` | 85.8 | ✓ |
| 1d_recolor_oe_18 | `paint(paint(x, segment(x)), segment(x))` | 62.5 | ✓ |
| 1d_recolor_oe_19 | `paint(paint(x, segment(x)), local(x))` | 85.4 | ✓ |
| 1d_recolor_oe_2 | `paint(paint(x, segment(x)), segment(x))` | 99.3 | ✓ |
| 1d_recolor_oe_20 | `paint(paint(x, segment(x)), segment(x))` | 70.0 | ✓ |
| 1d_recolor_oe_21 | `paint(paint(x, segment(x)), local(x))` | 83.2 | ✓ |
| 1d_recolor_oe_22 | `paint(x, segment(paint(x, segment(x))))` | 59.9 | ✓ |
| 1d_recolor_oe_23 | `paint(x, segment(x))` | 55.9 | ✓ |
| 1d_recolor_oe_24 | `paint(x, segment(paint(x, scan(x))))` | 65.3 | ✓ |
| 1d_recolor_oe_25 | `paint(paint(x, segment(x)), local(x))` | 68.2 | ✓ |
| 1d_recolor_oe_26 | `paint(x, segment(paint(x, local(x))))` | 83.5 | ✗ |
| 1d_recolor_oe_27 | `paint(paint(x, segment(x)), local(x))` | 75.0 | ✓ |
| 1d_recolor_oe_28 | `paint(paint(x, segment(x)), local(x))` | 81.9 | ✗ |
| 1d_recolor_oe_29 | `paint(paint(x, local(x)), segment(x))` | 78.8 | ✗ |
| 1d_recolor_oe_3 | `paint(paint(x, segment(x)), local(shift(x)))` | 95.5 | ✓ |
| 1d_recolor_oe_30 | `recolour(paint(x, segment(x)))` | 60.9 | ✓ |
| 1d_recolor_oe_31 | `paint(paint(x, local(shift(x))), segment(x))` | 73.5 | ✓ |
| 1d_recolor_oe_32 | `paint(paint(x, segment(x)), local(shift(x)))` | 89.3 | ✓ |
| 1d_recolor_oe_33 | `paint(paint(x, local(shift(x))), segment(x))` | 52.0 | ✓ |
| 1d_recolor_oe_34 | `paint(x, segment(recolour(x)))` | 65.3 | ✗ |
| 1d_recolor_oe_35 | `recolour(paint(x, segment(x)))` | 80.6 | ✓ |
| 1d_recolor_oe_36 | `paint(paint(x, segment(x)), segment(x))` | 70.8 | ✓ |
| 1d_recolor_oe_37 | `paint(paint(x, local(x)), segment(x))` | 67.8 | ✓ |
| 1d_recolor_oe_38 | `paint(recolour(x), segment(x))` | 96.2 | ✓ |
| 1d_recolor_oe_39 | `paint(paint(x, segment(x)), scan(x))` | 75.5 | ✓ |
| 1d_recolor_oe_4 | `paint(paint(x, segment(x)), segment(x))` | 72.0 | ✓ |
| 1d_recolor_oe_40 | `paint(x, segment(x))` | 58.0 | ✓ |
| 1d_recolor_oe_41 | `recolour(paint(x, segment(x)))` | 110.0 | ✓ |
| 1d_recolor_oe_42 | `paint(paint(x, segment(x)), scan(x))` | 65.9 | ✓ |
| 1d_recolor_oe_43 | `paint(x, segment(paint(x, local(x))))` | 75.8 | ✓ |
| 1d_recolor_oe_44 | `paint(x, segment(recolour(x)))` | 64.0 | ✓ |
| 1d_recolor_oe_45 | `paint(recolour(x), segment(x))` | 104.6 | ✗ |
| 1d_recolor_oe_46 | `paint(paint(x, local(shift(x))), segment(x))` | 87.9 | ✓ |
| 1d_recolor_oe_47 | `paint(paint(x, segment(x)), local(shift(x)))` | 62.9 | ✓ |
| 1d_recolor_oe_48 | `paint(paint(x, segment(x)), segment(x))` | 97.4 | ✓ |
| 1d_recolor_oe_49 | `paint(paint(x, segment(x)), segment(x))` | 98.2 | ✓ |
| 1d_recolor_oe_5 | `paint(paint(x, segment(x)), segment(x))` | 75.5 | ✓ |
| 1d_recolor_oe_6 | `paint(paint(x, local(shift(x))), segment(x))` | 88.3 | ✓ |
| 1d_recolor_oe_7 | `paint(paint(x, local(x)), segment(x))` | 68.1 | ✗ |
| 1d_recolor_oe_8 | `paint(paint(x, segment(x)), segment(x))` | 74.0 | ✓ |
| 1d_recolor_oe_9 | `paint(paint(x, segment(x)), local(shift(x)))` | 68.0 | ✓ |
| 1d_scale_dp_0 | `paint(paint(x, local(shift(x))), scan(x))` | 50.7 | ✓ |
| 1d_scale_dp_1 | `paint(x, scan(paint(x, scan(x))))` | 55.4 | ✓ |
| 1d_scale_dp_10 | `paint(paint(x, scan(x)), local(x))` | 44.9 | ✓ |
| 1d_scale_dp_11 | `paint(x, scan(x))` | 44.5 | ✓ |
| 1d_scale_dp_12 | `paint(x, scan(paint(x, scan(x))))` | 44.2 | ✓ |
| 1d_scale_dp_13 | `paint(paint(x, local(x)), scan(shift(x)))` | 49.3 | ✗ |
| 1d_scale_dp_14 | `paint(x, scan(x))` | 46.8 | ✓ |
| 1d_scale_dp_15 | `paint(x, scan(x))` | 54.7 | ✓ |
| 1d_scale_dp_16 | `paint(paint(x, segment(x)), scan(x))` | 46.9 | ✓ |
| 1d_scale_dp_17 | `paint(x, scan(paint(x, segment(x))))` | 46.5 | ✓ |
| 1d_scale_dp_18 | `paint(x, scan(x))` | 53.3 | ✓ |
| 1d_scale_dp_19 | `paint(x, scan(paint(x, segment(x))))` | 55.0 | ✓ |
| 1d_scale_dp_2 | `paint(paint(x, scan(x)), scan(x))` | 64.4 | ✓ |
| 1d_scale_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 44.5 | ✗ |
| 1d_scale_dp_21 | `paint(paint(x, local(x)), scan(x))` | 60.1 | ✓ |
| 1d_scale_dp_22 | `paint(paint(x, scan(shift(x))), local(x))` | 53.3 | ✓ |
| 1d_scale_dp_23 | `paint(paint(x, local(shift(x))), scan(x))` | 40.0 | ✓ |
| 1d_scale_dp_24 | `paint(paint(x, scan(x)), scan(x))` | 61.8 | ✓ |
| 1d_scale_dp_25 | `paint(x, scan(x))` | 52.6 | ✓ |
| 1d_scale_dp_26 | `paint(x, scan(x))` | 40.4 | ✓ |
| 1d_scale_dp_27 | `paint(x, scan(paint(x, local(x))))` | 52.6 | ✓ |
| 1d_scale_dp_28 | `paint(paint(x, scan(x)), local(shift(x)))` | 37.3 | ✓ |
| 1d_scale_dp_29 | `paint(paint(x, scan(x)), scan(x))` | 58.8 | ✓ |
| 1d_scale_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 67.2 | ✓ |
| 1d_scale_dp_30 | `paint(x, scan(x))` | 52.5 | ✓ |
| 1d_scale_dp_31 | `paint(paint(shift(x), local(x)), scan(x))` | 58.1 | ✗ |
| 1d_scale_dp_32 | `paint(x, scan(x))` | 37.0 | ✓ |
| 1d_scale_dp_33 | `paint(x, scan(paint(x, segment(x))))` | 36.8 | ✓ |
| 1d_scale_dp_34 | `paint(x, scan(x))` | 44.7 | ✓ |
| 1d_scale_dp_35 | `paint(paint(x, segment(x)), scan(x))` | 40.7 | ✓ |
| 1d_scale_dp_36 | `paint(x, scan(paint(x, segment(x))))` | 46.2 | ✓ |
| 1d_scale_dp_37 | `paint(x, local(paint(x, scan(shift(x)))))` | 52.5 | ✗ |
| 1d_scale_dp_38 | `paint(x, scan(x))` | 48.9 | ✓ |
| 1d_scale_dp_39 | `paint(x, scan(x))` | 45.2 | ✓ |
| 1d_scale_dp_4 | `paint(x, scan(paint(x, scan(x))))` | 47.4 | ✓ |
| 1d_scale_dp_40 | `paint(paint(x, scan(x)), local(x))` | 74.2 | ✗ |
| 1d_scale_dp_41 | `paint(x, scan(x))` | 46.7 | ✓ |
| 1d_scale_dp_42 | `paint(paint(x, local(x)), scan(x))` | 72.6 | ✓ |
| 1d_scale_dp_43 | `paint(x, local(shift(x)))` | 62.9 | ✗ |
| 1d_scale_dp_44 | `paint(x, scan(x))` | 46.2 | ✓ |
| 1d_scale_dp_45 | `recolour(paint(shift(x), local(x)))` | 41.3 | ✗ |
| 1d_scale_dp_46 | `paint(x, scan(paint(x, segment(x))))` | 60.2 | ✓ |
| 1d_scale_dp_47 | `paint(paint(x, local(x)), scan(x))` | 65.6 | ✗ |
| 1d_scale_dp_48 | `paint(paint(x, local(x)), scan(x))` | 49.5 | ✓ |
| 1d_scale_dp_49 | `paint(recolour(x), scan(x))` | 49.3 | ✓ |
| 1d_scale_dp_5 | `paint(x, scan(x))` | 81.2 | ✓ |
| 1d_scale_dp_50 | `paint(x, scan(paint(x, segment(x))))` | 41.7 | ✓ |
| 1d_scale_dp_6 | `paint(paint(x, local(shift(x))), scan(x))` | 55.1 | ✓ |
| 1d_scale_dp_7 | `paint(shift(shift(x)), local(x))` | 42.7 | ✓ |
| 1d_scale_dp_8 | `paint(x, local(paint(x, local(x))))` | 37.7 | ✓ |
| 1d_scale_dp_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.3 | ✓ |
