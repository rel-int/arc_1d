# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 901 (50 per family, drawn with seed 0), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/lib-s0/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 662/901 (73%) | 723/901 | 799/901 | 65.0 | 7 | 150 | 1871s |
| 1 | 687/901 (76%) | 735/901 | 790/901 | 65.0 | 9 | 150 | 2283s |
| 2 | 689/901 (76%) | 745/901 | 793/901 | 62.1 | 11 | 150 | 2557s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 45/50 | 47/50 | 47/50 |
| denoising_mc | 39/50 | 44/50 | 46/50 |
| fill | 39/50 | 47/50 | 46/50 |
| flip | 7/50 | 6/50 | 4/50 |
| hollow | 49/50 | 47/50 | 49/50 |
| mirror | 2/50 | 5/50 | 4/50 |
| move_1p | 47/50 | 48/50 | 48/50 |
| move_2p | 49/50 | 49/50 | 49/50 |
| move_2p_dp | 42/50 | 44/50 | 45/50 |
| move_3p | 49/50 | 50/50 | 50/50 |
| move_dp | 3/50 | 2/50 | 4/50 |
| padded_fill | 45/50 | 47/50 | 45/50 |
| pcopy_1c | 25/50 | 23/50 | 23/50 |
| pcopy_mc | 39/50 | 39/50 | 45/50 |
| recolor_cmp | 48/50 | 49/50 | 48/50 |
| recolor_cnt | 49/50 | 50/50 | 50/50 |
| recolor_oe | 41/50 | 45/50 | 41/50 |
| scale_dp | 44/51 | 45/51 | 45/51 |

## Library growth

- after iteration 0: `f0a : Grid -> Grid` := `paint(paint(x, scan(x)), local(x))` (10 trained weight tensors inherited)
- after iteration 0: `f0b : Grid -> Grid` := `paint(shift(x), local(x))` (6 trained weight tensors inherited)
- after iteration 1: `f1a : Grid -> Grid` := `paint(x, scan(x))` (5 trained weight tensors inherited)
- after iteration 1: `f1b : Grid -> Grid` := `paint(x, local(x))` (5 trained weight tensors inherited)

`f0a`'s body:

![f0a](figures/box-f0a.png)

`f0b`'s body:

![f0b](figures/box-f0b.png)

`f1a`'s body:

![f1a](figures/box-f1a.png)

`f1b`'s body:

![f1b](figures/box-f1b.png)

## Examples from the last iteration

### Solved: `1d_denoising_1c_49`

`f0a(paint(x, local(x)))`, DL 29.3 = 10.9 structure + 17.6 parameters + 0.8 data bits, fits its training pairs exactly.

![1d_denoising_1c_49](figures/1d_denoising_1c_49.png)

| pair | input | output |
|---|---|---|
| train 0 | `.4444444444444....4..............` | `.4444444444444...................` |
| train 1 | `...2....2222222222222...2...2..2.` | `........2222222222222............` |
| train 2 | `....5......55555555555555..5...5.` | `...........55555555555555........` |
| **test** | `..5..5...5.......555555555555....` | `.................555555555555....` |
| predicted | | `.................555555555555....` |

### Solved: `1d_move_2p_28`

`shift(x)`, DL 48.1 = 4.4 structure + 39.8 parameters + 3.9 data bits, fits its training pairs exactly.

![1d_move_2p_28](figures/1d_move_2p_28.png)

| pair | input | output |
|---|---|---|
| train 0 | `.......666666666.............` | `.........666666666...........` |
| train 1 | `8888888888888888888888888....` | `..8888888888888888888888888..` |
| train 2 | `.................777.........` | `...................777.......` |
| **test** | `.22222222222222222222222.....` | `...22222222222222222222222...` |
| predicted | | `...22222222222222222222222...` |

### Solved: `1d_padded_fill_11`

`f1a(f1b(x))`, DL 44.8 = 10.3 structure + 31.2 parameters + 3.4 data bits, fits its training pairs exactly.

![1d_padded_fill_11](figures/1d_padded_fill_11.png)

| pair | input | output |
|---|---|---|
| train 0 | `...........1..1.............1..1.............1..1..` | `...........1111.............1111.............1111..` |
| train 1 | `5......5.........5......5.........5......5.........` | `55555555.........55555555.........55555555.........` |
| train 2 | `.....1........1.......1........1.......1........1..` | `.....1111111111.......1111111111.......1111111111..` |
| **test** | `.............1.1..............1.1..............1.1.` | `.............111..............111..............111.` |
| predicted | | `.............111..............111..............111.` |

### Failed: `1d_flip_26`

`f1a(paint(shift(x), local(x)))`, DL 80.4 = 13.1 structure + 60.8 parameters + 6.5 data bits, does not fit its training pairs exactly.

![1d_flip_26](figures/1d_flip_26.png)

| pair | input | output |
|---|---|---|
| train 0 | `..........622222222222..` | `..........222222222226..` |
| train 1 | `.........45555555.......` | `.........55555554.......` |
| train 2 | `14444444................` | `44444441................` |
| **test** | `.........2888888888.....` | `.........8888888882.....` |
| predicted | | `.........8888888881.....` |

### Failed: `1d_mirror_38`

`paint(x, scan(shift(x)))`, DL 187.4 = 9.0 structure + 125.8 parameters + 52.6 data bits, does not fit its training pairs exactly.

![1d_mirror_38](figures/1d_mirror_38.png)

| pair | input | output |
|---|---|---|
| train 0 | `......4444444...9.............` | `................9...4444444...` |
| train 1 | `.555555555.9..................` | `...........9.555555555........` |
| train 2 | `.111111111...9................` | `.............9...111111111....` |
| **test** | `......666666666..9............` | `.................9..666666666.` |
| predicted | | `..............6..9............` |

### Failed: `1d_move_dp_18`

`f1b(paint(shift(x), local(x)))`, DL 119.4 = 13.2 structure + 104.7 parameters + 1.6 data bits, fits its training pairs exactly.

![1d_move_dp_18](figures/1d_move_dp_18.png)

| pair | input | output |
|---|---|---|
| train 0 | `......7777777..8.` | `........77777778.` |
| train 1 | `666666....8......` | `....6666668......` |
| train 2 | `5555555555555..8.` | `..55555555555558.` |
| **test** | `..........444...8` | `.............4448` |
| predicted | | `.............4..8` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_0 | `f0a(paint(x, local(x)))` | 26.6 | ✓ |
| 1d_denoising_1c_1 | `paint(f0a(x), local(x))` | 36.4 | ✓ |
| 1d_denoising_1c_10 | `f0a(paint(x, local(x)))` | 37.8 | ✓ |
| 1d_denoising_1c_11 | `f0a(paint(x, local(x)))` | 31.6 | ✓ |
| 1d_denoising_1c_12 | `f0a(paint(x, local(x)))` | 22.2 | ✓ |
| 1d_denoising_1c_13 | `f0a(paint(x, local(x)))` | 20.1 | ✓ |
| 1d_denoising_1c_14 | `f0a(paint(x, local(x)))` | 27.0 | ✓ |
| 1d_denoising_1c_15 | `f0a(paint(x, local(x)))` | 24.5 | ✓ |
| 1d_denoising_1c_16 | `f0a(paint(x, local(x)))` | 34.3 | ✓ |
| 1d_denoising_1c_17 | `paint(paint(x, scan(x)), segment(x))` | 38.3 | ✓ |
| 1d_denoising_1c_18 | `f0a(paint(x, local(x)))` | 40.6 | ✓ |
| 1d_denoising_1c_19 | `f0a(paint(x, local(x)))` | 19.0 | ✓ |
| 1d_denoising_1c_2 | `f0a(shift(x))` | 30.7 | ✗ |
| 1d_denoising_1c_20 | `f0a(paint(x, local(x)))` | 27.3 | ✓ |
| 1d_denoising_1c_21 | `f0a(shift(x))` | 20.4 | ✓ |
| 1d_denoising_1c_22 | `paint(f0a(x), local(x))` | 23.9 | ✓ |
| 1d_denoising_1c_23 | `f0a(paint(x, local(x)))` | 22.8 | ✓ |
| 1d_denoising_1c_24 | `f0a(shift(x))` | 30.1 | ✗ |
| 1d_denoising_1c_25 | `paint(paint(shift(x), scan(x)), local(x))` | 31.0 | ✓ |
| 1d_denoising_1c_26 | `f0a(paint(x, local(x)))` | 29.7 | ✓ |
| 1d_denoising_1c_27 | `f0a(paint(x, local(x)))` | 17.4 | ✓ |
| 1d_denoising_1c_28 | `f0a(paint(x, local(x)))` | 18.6 | ✓ |
| 1d_denoising_1c_29 | `f0a(paint(x, local(x)))` | 21.7 | ✓ |
| 1d_denoising_1c_3 | `f0a(paint(x, local(x)))` | 32.1 | ✓ |
| 1d_denoising_1c_30 | `f0a(paint(x, local(x)))` | 45.0 | ✓ |
| 1d_denoising_1c_31 | `f0a(shift(x))` | 16.5 | ✗ |
| 1d_denoising_1c_32 | `f0a(paint(x, local(x)))` | 27.8 | ✓ |
| 1d_denoising_1c_33 | `f0a(paint(x, local(x)))` | 31.9 | ✓ |
| 1d_denoising_1c_34 | `f0a(paint(x, local(x)))` | 23.2 | ✓ |
| 1d_denoising_1c_35 | `f0a(paint(x, local(x)))` | 35.4 | ✓ |
| 1d_denoising_1c_36 | `f0a(shift(x))` | 21.0 | ✓ |
| 1d_denoising_1c_37 | `paint(f0a(x), local(x))` | 20.3 | ✓ |
| 1d_denoising_1c_38 | `f0a(paint(x, local(x)))` | 35.7 | ✓ |
| 1d_denoising_1c_39 | `paint(f0a(x), local(x))` | 27.7 | ✓ |
| 1d_denoising_1c_4 | `f0a(paint(x, local(x)))` | 24.5 | ✓ |
| 1d_denoising_1c_40 | `f0a(paint(x, local(x)))` | 22.2 | ✓ |
| 1d_denoising_1c_41 | `f0a(paint(x, local(x)))` | 19.9 | ✓ |
| 1d_denoising_1c_42 | `f0a(paint(x, local(x)))` | 32.0 | ✓ |
| 1d_denoising_1c_43 | `f0a(paint(x, local(x)))` | 16.3 | ✓ |
| 1d_denoising_1c_44 | `f0a(paint(x, local(x)))` | 22.7 | ✓ |
| 1d_denoising_1c_45 | `f0a(paint(x, local(x)))` | 22.8 | ✓ |
| 1d_denoising_1c_46 | `paint(paint(x, scan(x)), segment(x))` | 38.2 | ✓ |
| 1d_denoising_1c_47 | `f0a(paint(x, local(x)))` | 33.9 | ✓ |
| 1d_denoising_1c_48 | `f0a(paint(x, local(x)))` | 21.3 | ✓ |
| 1d_denoising_1c_49 | `f0a(paint(x, local(x)))` | 29.3 | ✓ |
| 1d_denoising_1c_5 | `paint(paint(shift(x), local(x)), local(x))` | 42.4 | ✓ |
| 1d_denoising_1c_6 | `f0a(shift(x))` | 16.5 | ✓ |
| 1d_denoising_1c_7 | `f0a(paint(x, local(x)))` | 33.7 | ✓ |
| 1d_denoising_1c_8 | `f0a(paint(x, local(x)))` | 22.2 | ✓ |
| 1d_denoising_1c_9 | `f0a(shift(x))` | 21.2 | ✓ |
| 1d_denoising_mc_0 | `paint(f1a(shift(x)), local(x))` | 27.7 | ✓ |
| 1d_denoising_mc_1 | `paint(paint(shift(x), segment(x)), local(x))` | 41.8 | ✓ |
| 1d_denoising_mc_10 | `paint(paint(shift(x), segment(x)), local(x))` | 27.6 | ✗ |
| 1d_denoising_mc_11 | `paint(shift(paint(x, scan(x))), local(x))` | 32.0 | ✓ |
| 1d_denoising_mc_12 | `f1a(paint(shift(x), local(x)))` | 35.1 | ✓ |
| 1d_denoising_mc_13 | `paint(shift(paint(x, scan(x))), local(x))` | 52.3 | ✓ |
| 1d_denoising_mc_14 | `f0a(shift(x))` | 24.1 | ✗ |
| 1d_denoising_mc_15 | `paint(paint(shift(x), local(x)), segment(x))` | 34.8 | ✓ |
| 1d_denoising_mc_16 | `paint(shift(paint(x, scan(x))), local(x))` | 29.6 | ✓ |
| 1d_denoising_mc_17 | `paint(paint(shift(x), local(x)), scan(x))` | 18.1 | ✓ |
| 1d_denoising_mc_18 | `paint(f1a(shift(x)), local(x))` | 22.6 | ✓ |
| 1d_denoising_mc_19 | `f1a(paint(shift(x), local(x)))` | 30.0 | ✓ |
| 1d_denoising_mc_2 | `paint(paint(shift(x), local(x)), segment(x))` | 31.0 | ✓ |
| 1d_denoising_mc_20 | `paint(shift(paint(x, local(x))), local(x))` | 49.1 | ✓ |
| 1d_denoising_mc_21 | `paint(paint(shift(x), local(x)), segment(x))` | 36.1 | ✓ |
| 1d_denoising_mc_22 | `paint(paint(x, local(x)), local(shift(x)))` | 55.1 | ✓ |
| 1d_denoising_mc_23 | `f1b(paint(shift(x), local(x)))` | 25.5 | ✓ |
| 1d_denoising_mc_24 | `f1a(paint(shift(x), local(x)))` | 29.6 | ✓ |
| 1d_denoising_mc_25 | `f0b(paint(x, local(x)))` | 41.7 | ✓ |
| 1d_denoising_mc_26 | `paint(shift(x), scan(x))` | 39.8 | ✓ |
| 1d_denoising_mc_27 | `f1b(paint(shift(x), local(x)))` | 24.2 | ✓ |
| 1d_denoising_mc_28 | `f1b(paint(shift(x), local(x)))` | 26.4 | ✓ |
| 1d_denoising_mc_29 | `f1a(paint(shift(x), local(x)))` | 17.8 | ✓ |
| 1d_denoising_mc_3 | `paint(paint(shift(x), local(x)), local(x))` | 25.0 | ✓ |
| 1d_denoising_mc_30 | `paint(paint(shift(x), local(x)), segment(x))` | 38.7 | ✓ |
| 1d_denoising_mc_31 | `paint(paint(shift(x), local(x)), scan(x))` | 38.9 | ✓ |
| 1d_denoising_mc_32 | `paint(paint(shift(x), local(x)), scan(x))` | 26.8 | ✓ |
| 1d_denoising_mc_33 | `paint(shift(paint(x, scan(x))), local(x))` | 25.6 | ✓ |
| 1d_denoising_mc_34 | `paint(shift(paint(x, scan(x))), local(x))` | 50.6 | ✓ |
| 1d_denoising_mc_35 | `f0b(paint(x, local(x)))` | 47.3 | ✓ |
| 1d_denoising_mc_36 | `paint(shift(x), local(paint(x, local(x))))` | 45.9 | ✓ |
| 1d_denoising_mc_37 | `paint(shift(paint(x, scan(x))), local(x))` | 31.1 | ✓ |
| 1d_denoising_mc_38 | `paint(paint(shift(x), scan(x)), local(x))` | 29.5 | ✓ |
| 1d_denoising_mc_39 | `paint(f0b(x), local(x))` | 40.9 | ✓ |
| 1d_denoising_mc_4 | `f1b(paint(shift(x), local(x)))` | 26.0 | ✗ |
| 1d_denoising_mc_40 | `paint(paint(shift(x), local(x)), scan(x))` | 17.7 | ✓ |
| 1d_denoising_mc_41 | `f1b(paint(shift(x), local(x)))` | 28.1 | ✓ |
| 1d_denoising_mc_42 | `paint(shift(paint(x, scan(x))), local(x))` | 34.7 | ✓ |
| 1d_denoising_mc_43 | `f1a(paint(shift(x), local(x)))` | 30.2 | ✗ |
| 1d_denoising_mc_44 | `paint(paint(x, local(x)), local(shift(x)))` | 35.3 | ✓ |
| 1d_denoising_mc_45 | `paint(shift(paint(x, scan(x))), local(x))` | 39.1 | ✓ |
| 1d_denoising_mc_46 | `f1b(paint(shift(x), local(x)))` | 23.8 | ✓ |
| 1d_denoising_mc_47 | `paint(shift(paint(x, scan(x))), local(x))` | 39.7 | ✓ |
| 1d_denoising_mc_48 | `paint(paint(shift(x), local(x)), scan(x))` | 39.3 | ✓ |
| 1d_denoising_mc_49 | `paint(paint(shift(x), local(x)), segment(x))` | 28.7 | ✓ |
| 1d_denoising_mc_5 | `paint(paint(shift(x), local(x)), local(x))` | 17.2 | ✓ |
| 1d_denoising_mc_6 | `paint(shift(paint(x, scan(x))), local(x))` | 40.0 | ✓ |
| 1d_denoising_mc_7 | `f0b(paint(x, local(x)))` | 50.9 | ✓ |
| 1d_denoising_mc_8 | `f1b(paint(shift(x), local(x)))` | 38.3 | ✓ |
| 1d_denoising_mc_9 | `paint(paint(shift(x), local(x)), segment(x))` | 30.2 | ✓ |
| 1d_fill_0 | `paint(paint(x, scan(x)), local(shift(x)))` | 61.8 | ✓ |
| 1d_fill_1 | `paint(paint(x, scan(x)), segment(x))` | 49.1 | ✓ |
| 1d_fill_10 | `paint(shift(f1a(x)), local(x))` | 46.6 | ✓ |
| 1d_fill_11 | `f1b(paint(x, scan(x)))` | 48.2 | ✓ |
| 1d_fill_12 | `f1a(f1a(x))` | 63.7 | ✓ |
| 1d_fill_13 | `paint(x, scan(paint(x, local(x))))` | 71.7 | ✓ |
| 1d_fill_14 | `paint(f1a(x), local(shift(x)))` | 53.3 | ✓ |
| 1d_fill_15 | `paint(paint(x, scan(x)), local(x))` | 32.2 | ✗ |
| 1d_fill_16 | `f1b(f1a(x))` | 43.0 | ✓ |
| 1d_fill_17 | `paint(paint(x, scan(x)), local(shift(x)))` | 41.0 | ✓ |
| 1d_fill_18 | `f1b(f1a(x))` | 61.8 | ✓ |
| 1d_fill_19 | `paint(paint(x, scan(x)), local(x))` | 48.9 | ✓ |
| 1d_fill_2 | `f1b(f1a(x))` | 29.3 | ✓ |
| 1d_fill_20 | `paint(paint(shift(x), scan(x)), local(x))` | 42.8 | ✓ |
| 1d_fill_21 | `f1b(f1a(x))` | 36.9 | ✓ |
| 1d_fill_22 | `paint(paint(shift(x), scan(x)), local(x))` | 42.2 | ✗ |
| 1d_fill_23 | `f1a(f1a(x))` | 64.6 | ✓ |
| 1d_fill_24 | `f1b(paint(x, scan(x)))` | 42.4 | ✓ |
| 1d_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 51.8 | ✓ |
| 1d_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 38.9 | ✓ |
| 1d_fill_27 | `f1b(f1a(x))` | 35.3 | ✓ |
| 1d_fill_28 | `paint(f1a(x), local(shift(x)))` | 60.2 | ✗ |
| 1d_fill_29 | `f1b(paint(x, scan(x)))` | 45.4 | ✓ |
| 1d_fill_3 | `f1b(f1a(x))` | 54.5 | ✓ |
| 1d_fill_30 | `paint(shift(f1a(x)), local(x))` | 52.6 | ✓ |
| 1d_fill_31 | `f1b(f1a(x))` | 54.8 | ✓ |
| 1d_fill_32 | `paint(paint(x, scan(x)), local(x))` | 44.6 | ✓ |
| 1d_fill_33 | `paint(f1a(x), local(shift(x)))` | 45.1 | ✓ |
| 1d_fill_34 | `f1b(paint(x, scan(x)))` | 56.3 | ✓ |
| 1d_fill_35 | `paint(x, scan(paint(x, segment(x))))` | 65.7 | ✓ |
| 1d_fill_36 | `paint(x, scan(paint(x, local(x))))` | 57.6 | ✓ |
| 1d_fill_37 | `f1a(f1b(x))` | 50.6 | ✓ |
| 1d_fill_38 | `f1b(paint(x, scan(x)))` | 49.4 | ✓ |
| 1d_fill_39 | `paint(paint(x, scan(x)), local(shift(x)))` | 42.7 | ✓ |
| 1d_fill_4 | `f1b(paint(x, scan(x)))` | 52.2 | ✓ |
| 1d_fill_40 | `f1b(paint(x, scan(x)))` | 38.7 | ✓ |
| 1d_fill_41 | `f1b(f1a(x))` | 57.2 | ✓ |
| 1d_fill_42 | `f1a(paint(x, local(x)))` | 56.4 | ✓ |
| 1d_fill_43 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.0 | ✓ |
| 1d_fill_44 | `paint(f1b(x), local(x))` | 65.0 | ✓ |
| 1d_fill_45 | `f1b(f1a(x))` | 64.2 | ✓ |
| 1d_fill_46 | `paint(paint(x, scan(x)), local(shift(x)))` | 37.6 | ✓ |
| 1d_fill_47 | `paint(x, scan(paint(x, scan(x))))` | 48.1 | ✓ |
| 1d_fill_48 | `f1b(f1a(x))` | 40.5 | ✓ |
| 1d_fill_49 | `paint(paint(shift(x), scan(x)), local(x))` | 48.0 | ✗ |
| 1d_fill_5 | `f1b(f1a(x))` | 41.4 | ✓ |
| 1d_fill_6 | `f1b(f1a(x))` | 54.0 | ✓ |
| 1d_fill_7 | `paint(paint(x, scan(x)), local(x))` | 28.7 | ✓ |
| 1d_fill_8 | `paint(paint(x, scan(x)), local(shift(x)))` | 49.3 | ✓ |
| 1d_fill_9 | `f1b(paint(x, scan(x)))` | 42.3 | ✓ |
| 1d_flip_0 | `paint(f0b(x), local(x))` | 71.2 | ✗ |
| 1d_flip_1 | `paint(paint(shift(x), local(x)), scan(x))` | 84.8 | ✗ |
| 1d_flip_10 | `paint(paint(x, local(x)), local(x))` | 73.8 | ✓ |
| 1d_flip_11 | `f0a(paint(x, local(x)))` | 70.7 | ✗ |
| 1d_flip_12 | `paint(f0b(x), local(x))` | 70.7 | ✗ |
| 1d_flip_13 | `f1a(shift(paint(x, local(x))))` | 97.7 | ✗ |
| 1d_flip_14 | `paint(f0b(x), local(x))` | 73.4 | ✗ |
| 1d_flip_15 | `paint(f1b(x), scan(x))` | 103.1 | ✗ |
| 1d_flip_16 | `f1a(paint(shift(x), local(x)))` | 77.6 | ✗ |
| 1d_flip_17 | `f1a(paint(shift(x), local(x)))` | 70.6 | ✗ |
| 1d_flip_18 | `f1a(paint(shift(x), local(x)))` | 76.8 | ✗ |
| 1d_flip_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 91.9 | ✓ |
| 1d_flip_2 | `paint(f0b(x), local(x))` | 72.6 | ✗ |
| 1d_flip_20 | `f1a(paint(x, local(x)))` | 75.1 | ✗ |
| 1d_flip_21 | `f1a(paint(shift(x), local(x)))` | 69.2 | ✗ |
| 1d_flip_22 | `f1a(paint(shift(x), local(x)))` | 80.5 | ✗ |
| 1d_flip_23 | `f1a(paint(shift(x), local(x)))` | 69.9 | ✗ |
| 1d_flip_24 | `f1b(x)` | 83.4 | ✗ |
| 1d_flip_25 | `f0a(paint(x, local(x)))` | 76.5 | ✗ |
| 1d_flip_26 | `f1a(paint(shift(x), local(x)))` | 80.4 | ✗ |
| 1d_flip_27 | `paint(f1a(shift(x)), local(x))` | 77.6 | ✗ |
| 1d_flip_28 | `paint(shift(x), local(paint(x, segment(x))))` | 85.1 | ✗ |
| 1d_flip_29 | `paint(shift(x), local(paint(x, segment(x))))` | 75.1 | ✗ |
| 1d_flip_3 | `paint(paint(shift(x), scan(x)), local(x))` | 71.3 | ✓ |
| 1d_flip_30 | `paint(paint(shift(x), local(x)), scan(x))` | 79.4 | ✗ |
| 1d_flip_31 | `paint(shift(x), local(paint(x, segment(x))))` | 80.3 | ✗ |
| 1d_flip_32 | `paint(shift(f1a(x)), local(x))` | 72.9 | ✗ |
| 1d_flip_33 | `f1a(paint(shift(x), local(x)))` | 90.3 | ✗ |
| 1d_flip_34 | `paint(f0b(x), local(x))` | 83.1 | ✗ |
| 1d_flip_35 | `f0b(shift(x))` | 67.9 | ✗ |
| 1d_flip_36 | `paint(f1a(shift(x)), local(x))` | 65.0 | ✗ |
| 1d_flip_37 | `paint(shift(x), local(x))` | 91.9 | ✗ |
| 1d_flip_38 | `paint(paint(shift(x), local(x)), scan(x))` | 81.9 | ✗ |
| 1d_flip_39 | `paint(f0b(x), local(x))` | 55.3 | ✗ |
| 1d_flip_4 | `f1b(f1b(x))` | 71.5 | ✗ |
| 1d_flip_40 | `paint(f1b(x), segment(x))` | 86.0 | ✗ |
| 1d_flip_41 | `f1b(paint(x, local(x)))` | 72.5 | ✗ |
| 1d_flip_42 | `f1a(paint(shift(x), local(x)))` | 71.2 | ✗ |
| 1d_flip_43 | `paint(f1a(x), local(x))` | 87.9 | ✗ |
| 1d_flip_44 | `f0a(paint(x, local(x)))` | 80.1 | ✗ |
| 1d_flip_45 | `paint(x, scan(paint(x, local(shift(x)))))` | 90.2 | ✗ |
| 1d_flip_46 | `f1b(paint(x, local(x)))` | 87.8 | ✗ |
| 1d_flip_47 | `paint(x, local(paint(x, scan(x))))` | 68.7 | ✗ |
| 1d_flip_48 | `f1b(x)` | 79.7 | ✗ |
| 1d_flip_49 | `f1b(paint(shift(x), local(x)))` | 67.9 | ✗ |
| 1d_flip_5 | `paint(paint(x, local(x)), local(x))` | 80.0 | ✗ |
| 1d_flip_6 | `f1b(f1b(x))` | 81.8 | ✗ |
| 1d_flip_7 | `f1a(paint(shift(x), local(x)))` | 78.0 | ✗ |
| 1d_flip_8 | `paint(paint(shift(x), segment(x)), local(x))` | 69.8 | ✓ |
| 1d_flip_9 | `f0a(paint(x, local(x)))` | 85.8 | ✗ |
| 1d_hollow_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 43.1 | ✓ |
| 1d_hollow_1 | `paint(paint(x, local(x)), segment(x))` | 44.2 | ✓ |
| 1d_hollow_10 | `paint(paint(shift(x), segment(x)), local(x))` | 63.7 | ✓ |
| 1d_hollow_11 | `paint(paint(x, local(x)), segment(shift(x)))` | 38.1 | ✓ |
| 1d_hollow_12 | `paint(f1a(x), local(x))` | 63.2 | ✓ |
| 1d_hollow_13 | `paint(paint(x, scan(x)), segment(x))` | 41.9 | ✓ |
| 1d_hollow_14 | `paint(paint(x, segment(x)), local(x))` | 40.4 | ✓ |
| 1d_hollow_15 | `f1a(paint(x, local(x)))` | 61.4 | ✓ |
| 1d_hollow_16 | `paint(x, segment(f1b(x)))` | 48.3 | ✓ |
| 1d_hollow_17 | `paint(paint(x, segment(x)), local(x))` | 44.0 | ✓ |
| 1d_hollow_18 | `paint(paint(x, local(x)), segment(shift(x)))` | 50.9 | ✓ |
| 1d_hollow_19 | `paint(f1a(x), scan(x))` | 58.5 | ✓ |
| 1d_hollow_2 | `paint(paint(x, segment(x)), scan(x))` | 57.3 | ✓ |
| 1d_hollow_20 | `f1a(paint(x, local(x)))` | 40.1 | ✓ |
| 1d_hollow_21 | `paint(paint(x, scan(x)), scan(x))` | 44.6 | ✓ |
| 1d_hollow_22 | `f1a(paint(x, local(shift(x))))` | 67.8 | ✓ |
| 1d_hollow_23 | `f1a(x)` | 70.9 | ✓ |
| 1d_hollow_24 | `paint(f1a(x), local(shift(x)))` | 62.0 | ✓ |
| 1d_hollow_25 | `paint(f0a(x), local(x))` | 59.7 | ✓ |
| 1d_hollow_26 | `f1b(f1b(x))` | 35.7 | ✓ |
| 1d_hollow_27 | `f1a(paint(x, local(x)))` | 46.3 | ✓ |
| 1d_hollow_28 | `paint(paint(x, local(x)), scan(shift(x)))` | 58.6 | ✓ |
| 1d_hollow_29 | `paint(paint(x, scan(x)), segment(x))` | 48.5 | ✓ |
| 1d_hollow_3 | `paint(paint(x, local(x)), scan(x))` | 46.0 | ✓ |
| 1d_hollow_30 | `paint(paint(x, scan(x)), local(shift(x)))` | 57.7 | ✓ |
| 1d_hollow_31 | `f1b(paint(x, scan(x)))` | 51.9 | ✓ |
| 1d_hollow_32 | `paint(f1b(x), segment(x))` | 42.9 | ✓ |
| 1d_hollow_33 | `paint(paint(x, local(x)), segment(shift(x)))` | 41.0 | ✓ |
| 1d_hollow_34 | `f0a(paint(x, local(x)))` | 50.4 | ✓ |
| 1d_hollow_35 | `paint(paint(x, local(x)), segment(shift(x)))` | 48.3 | ✓ |
| 1d_hollow_36 | `paint(paint(x, local(x)), scan(x))` | 68.1 | ✓ |
| 1d_hollow_37 | `paint(paint(x, segment(x)), local(x))` | 51.0 | ✓ |
| 1d_hollow_38 | `paint(paint(x, local(x)), segment(shift(x)))` | 53.9 | ✓ |
| 1d_hollow_39 | `paint(paint(x, local(x)), segment(shift(x)))` | 58.1 | ✓ |
| 1d_hollow_4 | `paint(f1b(x), segment(x))` | 37.4 | ✓ |
| 1d_hollow_40 | `paint(paint(x, local(x)), segment(shift(x)))` | 41.7 | ✓ |
| 1d_hollow_41 | `f1a(x)` | 59.9 | ✓ |
| 1d_hollow_42 | `paint(f1a(shift(x)), local(x))` | 51.2 | ✓ |
| 1d_hollow_43 | `paint(f1b(x), scan(x))` | 65.9 | ✗ |
| 1d_hollow_44 | `paint(f1b(x), scan(x))` | 64.5 | ✓ |
| 1d_hollow_45 | `paint(f1b(x), segment(x))` | 44.7 | ✓ |
| 1d_hollow_46 | `f1a(paint(x, local(shift(x))))` | 56.0 | ✓ |
| 1d_hollow_47 | `f1a(x)` | 55.7 | ✓ |
| 1d_hollow_48 | `paint(paint(shift(x), scan(x)), local(x))` | 45.5 | ✓ |
| 1d_hollow_49 | `f1a(paint(x, local(x)))` | 56.3 | ✓ |
| 1d_hollow_5 | `paint(paint(x, local(x)), segment(shift(x)))` | 46.5 | ✓ |
| 1d_hollow_6 | `f1a(f1a(x))` | 44.7 | ✓ |
| 1d_hollow_7 | `f1a(paint(x, local(shift(x))))` | 59.4 | ✓ |
| 1d_hollow_8 | `paint(f1b(x), scan(x))` | 57.3 | ✓ |
| 1d_hollow_9 | `paint(paint(x, local(x)), segment(shift(x)))` | 30.3 | ✓ |
| 1d_mirror_0 | `f1a(f1a(x))` | 185.2 | ✗ |
| 1d_mirror_1 | `paint(paint(x, scan(x)), segment(x))` | 150.1 | ✗ |
| 1d_mirror_10 | `paint(paint(x, scan(x)), segment(x))` | 159.7 | ✗ |
| 1d_mirror_11 | `paint(paint(x, scan(x)), segment(x))` | 179.0 | ✗ |
| 1d_mirror_12 | `paint(paint(x, scan(x)), segment(x))` | 133.5 | ✗ |
| 1d_mirror_13 | `paint(f1a(x), segment(x))` | 146.9 | ✗ |
| 1d_mirror_14 | `paint(paint(x, scan(x)), segment(x))` | 144.5 | ✗ |
| 1d_mirror_15 | `paint(paint(x, scan(x)), segment(x))` | 158.4 | ✗ |
| 1d_mirror_16 | `paint(f1b(x), scan(x))` | 162.6 | ✗ |
| 1d_mirror_17 | `paint(f1a(x), scan(x))` | 175.9 | ✗ |
| 1d_mirror_18 | `f1a(f1a(x))` | 145.2 | ✗ |
| 1d_mirror_19 | `paint(paint(x, local(x)), segment(shift(x)))` | 177.4 | ✗ |
| 1d_mirror_2 | `f1a(paint(x, segment(x)))` | 134.3 | ✗ |
| 1d_mirror_20 | `paint(x, local(shift(shift(x))))` | 138.1 | ✗ |
| 1d_mirror_21 | `paint(paint(x, local(shift(x))), local(x))` | 94.9 | ✓ |
| 1d_mirror_22 | `paint(x, local(shift(shift(x))))` | 147.7 | ✓ |
| 1d_mirror_23 | `paint(paint(x, scan(x)), segment(x))` | 141.2 | ✗ |
| 1d_mirror_24 | `paint(paint(x, scan(x)), segment(x))` | 146.3 | ✗ |
| 1d_mirror_25 | `paint(paint(x, segment(x)), scan(x))` | 171.6 | ✗ |
| 1d_mirror_26 | `paint(paint(x, scan(x)), segment(x))` | 132.2 | ✗ |
| 1d_mirror_27 | `paint(x, segment(paint(x, segment(x))))` | 144.3 | ✗ |
| 1d_mirror_28 | `paint(x, scan(paint(shift(x), local(x))))` | 156.8 | ✗ |
| 1d_mirror_29 | `paint(f1a(x), scan(x))` | 130.0 | ✗ |
| 1d_mirror_3 | `f1a(f1a(x))` | 129.6 | ✗ |
| 1d_mirror_30 | `paint(x, scan(shift(x)))` | 173.8 | ✗ |
| 1d_mirror_31 | `f1a(f1a(x))` | 122.0 | ✗ |
| 1d_mirror_32 | `paint(paint(x, local(x)), scan(shift(x)))` | 176.8 | ✗ |
| 1d_mirror_33 | `paint(paint(x, local(x)), segment(x))` | 168.7 | ✗ |
| 1d_mirror_34 | `paint(x, local(paint(shift(x), segment(x))))` | 98.4 | ✗ |
| 1d_mirror_35 | `f1a(paint(x, scan(x)))` | 164.7 | ✗ |
| 1d_mirror_36 | `paint(paint(x, scan(x)), segment(x))` | 158.5 | ✗ |
| 1d_mirror_37 | `paint(paint(x, local(x)), local(shift(x)))` | 110.3 | ✗ |
| 1d_mirror_38 | `paint(x, scan(shift(x)))` | 187.4 | ✗ |
| 1d_mirror_39 | `paint(shift(x), scan(x))` | 189.5 | ✗ |
| 1d_mirror_4 | `paint(paint(x, scan(x)), segment(x))` | 172.3 | ✗ |
| 1d_mirror_40 | `paint(paint(x, local(x)), segment(x))` | 135.2 | ✗ |
| 1d_mirror_41 | `paint(paint(x, local(shift(x))), local(x))` | 94.9 | ✓ |
| 1d_mirror_42 | `paint(paint(x, local(x)), scan(shift(x)))` | 138.4 | ✗ |
| 1d_mirror_43 | `paint(paint(x, scan(x)), segment(x))` | 132.1 | ✗ |
| 1d_mirror_44 | `paint(f1a(x), segment(x))` | 107.1 | ✗ |
| 1d_mirror_45 | `paint(paint(x, local(x)), local(shift(x)))` | 110.2 | ✗ |
| 1d_mirror_46 | `paint(paint(x, local(shift(x))), local(x))` | 87.7 | ✓ |
| 1d_mirror_47 | `paint(paint(x, scan(x)), segment(x))` | 124.0 | ✗ |
| 1d_mirror_48 | `paint(paint(x, scan(x)), segment(x))` | 139.5 | ✗ |
| 1d_mirror_49 | `paint(x, segment(x))` | 146.6 | ✗ |
| 1d_mirror_5 | `f1a(shift(x))` | 174.7 | ✗ |
| 1d_mirror_6 | `paint(paint(x, scan(x)), segment(x))` | 155.1 | ✗ |
| 1d_mirror_7 | `paint(x, local(paint(shift(x), local(x))))` | 99.0 | ✗ |
| 1d_mirror_8 | `paint(x, segment(x))` | 147.6 | ✗ |
| 1d_mirror_9 | `paint(paint(x, scan(x)), segment(x))` | 150.2 | ✗ |
| 1d_move_1p_0 | `paint(shift(paint(x, scan(x))), local(x))` | 50.0 | ✓ |
| 1d_move_1p_1 | `f0b(paint(x, local(x)))` | 41.0 | ✓ |
| 1d_move_1p_10 | `shift(x)` | 53.0 | ✓ |
| 1d_move_1p_11 | `shift(x)` | 52.9 | ✓ |
| 1d_move_1p_12 | `f0a(shift(x))` | 42.6 | ✓ |
| 1d_move_1p_13 | `f0b(paint(x, local(x)))` | 49.7 | ✓ |
| 1d_move_1p_14 | `f1b(paint(x, local(shift(x))))` | 51.5 | ✓ |
| 1d_move_1p_15 | `paint(shift(x), local(f1a(x)))` | 35.4 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 53.6 | ✓ |
| 1d_move_1p_17 | `paint(shift(x), local(f1a(x)))` | 49.7 | ✓ |
| 1d_move_1p_18 | `f0b(x)` | 49.1 | ✗ |
| 1d_move_1p_19 | `paint(f1b(x), local(x))` | 47.0 | ✓ |
| 1d_move_1p_2 | `f1b(paint(x, local(shift(x))))` | 48.0 | ✓ |
| 1d_move_1p_20 | `paint(shift(shift(x)), local(x))` | 51.5 | ✓ |
| 1d_move_1p_21 | `paint(paint(shift(x), segment(x)), local(x))` | 46.1 | ✓ |
| 1d_move_1p_22 | `f0b(x)` | 50.6 | ✓ |
| 1d_move_1p_23 | `f0b(x)` | 46.7 | ✓ |
| 1d_move_1p_24 | `f0b(paint(x, local(x)))` | 45.0 | ✓ |
| 1d_move_1p_25 | `paint(shift(x), scan(x))` | 44.1 | ✓ |
| 1d_move_1p_26 | `paint(paint(shift(x), segment(x)), local(x))` | 38.5 | ✓ |
| 1d_move_1p_27 | `shift(x)` | 56.5 | ✓ |
| 1d_move_1p_28 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_29 | `f0b(x)` | 52.6 | ✓ |
| 1d_move_1p_3 | `f1b(paint(x, local(shift(x))))` | 46.0 | ✓ |
| 1d_move_1p_30 | `shift(x)` | 54.9 | ✓ |
| 1d_move_1p_31 | `paint(shift(x), local(x))` | 49.9 | ✓ |
| 1d_move_1p_32 | `paint(shift(x), scan(x))` | 54.7 | ✓ |
| 1d_move_1p_33 | `f1b(paint(x, local(shift(x))))` | 52.2 | ✓ |
| 1d_move_1p_34 | `f0b(shift(x))` | 53.6 | ✓ |
| 1d_move_1p_35 | `f0b(x)` | 47.8 | ✓ |
| 1d_move_1p_36 | `paint(shift(paint(x, scan(x))), local(x))` | 48.3 | ✓ |
| 1d_move_1p_37 | `paint(shift(x), local(x))` | 39.3 | ✓ |
| 1d_move_1p_38 | `shift(x)` | 55.2 | ✓ |
| 1d_move_1p_39 | `shift(x)` | 56.2 | ✓ |
| 1d_move_1p_4 | `paint(shift(x), local(x))` | 46.4 | ✓ |
| 1d_move_1p_40 | `paint(shift(paint(x, scan(x))), local(x))` | 47.7 | ✓ |
| 1d_move_1p_41 | `paint(shift(paint(x, local(x))), local(x))` | 48.7 | ✓ |
| 1d_move_1p_42 | `paint(shift(paint(x, scan(x))), local(x))` | 41.8 | ✓ |
| 1d_move_1p_43 | `f0b(paint(x, local(x)))` | 52.9 | ✓ |
| 1d_move_1p_44 | `paint(shift(x), segment(x))` | 51.5 | ✗ |
| 1d_move_1p_45 | `paint(paint(shift(x), segment(x)), local(x))` | 49.4 | ✓ |
| 1d_move_1p_46 | `f0b(x)` | 49.1 | ✓ |
| 1d_move_1p_47 | `f1b(paint(x, local(shift(x))))` | 47.7 | ✓ |
| 1d_move_1p_48 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_49 | `f1b(paint(x, local(x)))` | 42.9 | ✓ |
| 1d_move_1p_5 | `f1b(paint(x, local(shift(x))))` | 46.9 | ✓ |
| 1d_move_1p_6 | `f1a(paint(shift(x), local(x)))` | 43.0 | ✓ |
| 1d_move_1p_7 | `paint(shift(x), local(paint(x, segment(x))))` | 51.2 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 55.2 | ✓ |
| 1d_move_1p_9 | `f0b(paint(x, local(x)))` | 45.7 | ✓ |
| 1d_move_2p_0 | `paint(shift(paint(x, local(x))), local(x))` | 41.6 | ✓ |
| 1d_move_2p_1 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_10 | `shift(x)` | 46.9 | ✓ |
| 1d_move_2p_11 | `shift(x)` | 46.9 | ✓ |
| 1d_move_2p_12 | `shift(x)` | 47.2 | ✓ |
| 1d_move_2p_13 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_14 | `f1b(f1a(x))` | 42.8 | ✓ |
| 1d_move_2p_15 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_16 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_17 | `f0b(paint(x, local(x)))` | 43.4 | ✓ |
| 1d_move_2p_18 | `shift(x)` | 48.6 | ✓ |
| 1d_move_2p_19 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_2 | `f0b(paint(x, local(x)))` | 43.6 | ✓ |
| 1d_move_2p_20 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_21 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_22 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_23 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_24 | `shift(x)` | 46.2 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_26 | `f0b(paint(x, local(x)))` | 43.1 | ✓ |
| 1d_move_2p_27 | `shift(x)` | 49.2 | ✓ |
| 1d_move_2p_28 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_29 | `shift(x)` | 48.8 | ✓ |
| 1d_move_2p_3 | `f0b(paint(x, local(x)))` | 37.2 | ✓ |
| 1d_move_2p_30 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_31 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_32 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_33 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_34 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_35 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_36 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_37 | `paint(shift(x), local(f1a(x)))` | 41.2 | ✓ |
| 1d_move_2p_38 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_39 | `shift(x)` | 49.1 | ✓ |
| 1d_move_2p_4 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_40 | `shift(x)` | 48.9 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.6 | ✓ |
| 1d_move_2p_42 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_43 | `paint(paint(shift(x), local(x)), segment(x))` | 44.0 | ✓ |
| 1d_move_2p_44 | `f1b(paint(x, scan(x)))` | 50.3 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_46 | `shift(x)` | 48.6 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.5 | ✓ |
| 1d_move_2p_48 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_49 | `f0b(paint(x, local(x)))` | 36.0 | ✓ |
| 1d_move_2p_5 | `f0b(paint(x, local(x)))` | 37.1 | ✗ |
| 1d_move_2p_6 | `paint(paint(shift(x), local(x)), segment(x))` | 45.1 | ✓ |
| 1d_move_2p_7 | `f1b(f1a(x))` | 44.9 | ✓ |
| 1d_move_2p_8 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_9 | `f0b(paint(x, local(x)))` | 36.7 | ✓ |
| 1d_move_2p_dp_0 | `paint(paint(x, local(x)), segment(shift(x)))` | 57.0 | ✗ |
| 1d_move_2p_dp_1 | `f1b(x)` | 70.4 | ✓ |
| 1d_move_2p_dp_10 | `f1b(f1b(x))` | 49.6 | ✓ |
| 1d_move_2p_dp_11 | `f1a(f1b(x))` | 64.0 | ✓ |
| 1d_move_2p_dp_12 | `f1b(paint(x, local(x)))` | 40.2 | ✓ |
| 1d_move_2p_dp_13 | `paint(paint(shift(x), segment(x)), local(x))` | 54.8 | ✓ |
| 1d_move_2p_dp_14 | `f1a(paint(x, local(x)))` | 57.4 | ✓ |
| 1d_move_2p_dp_15 | `paint(paint(x, local(x)), local(shift(x)))` | 55.2 | ✓ |
| 1d_move_2p_dp_16 | `f1a(paint(x, local(x)))` | 60.5 | ✓ |
| 1d_move_2p_dp_17 | `f1b(paint(x, scan(x)))` | 74.0 | ✓ |
| 1d_move_2p_dp_18 | `paint(x, local(paint(x, scan(shift(x)))))` | 68.3 | ✓ |
| 1d_move_2p_dp_19 | `f1b(f1a(x))` | 63.1 | ✗ |
| 1d_move_2p_dp_2 | `f1b(paint(x, scan(x)))` | 54.6 | ✓ |
| 1d_move_2p_dp_20 | `paint(f1b(x), segment(x))` | 50.6 | ✓ |
| 1d_move_2p_dp_21 | `f1b(paint(x, scan(x)))` | 66.4 | ✓ |
| 1d_move_2p_dp_22 | `paint(f1b(x), segment(x))` | 57.7 | ✓ |
| 1d_move_2p_dp_23 | `paint(paint(shift(x), segment(x)), local(x))` | 68.3 | ✓ |
| 1d_move_2p_dp_24 | `f1b(paint(x, scan(x)))` | 61.9 | ✓ |
| 1d_move_2p_dp_25 | `paint(paint(shift(x), local(x)), scan(x))` | 60.0 | ✓ |
| 1d_move_2p_dp_26 | `f1b(f1a(x))` | 38.8 | ✓ |
| 1d_move_2p_dp_27 | `f1b(shift(x))` | 72.0 | ✓ |
| 1d_move_2p_dp_28 | `f1b(paint(x, scan(x)))` | 71.0 | ✓ |
| 1d_move_2p_dp_29 | `paint(shift(x), local(f1a(x)))` | 64.6 | ✓ |
| 1d_move_2p_dp_3 | `paint(paint(x, local(x)), segment(shift(x)))` | 54.3 | ✓ |
| 1d_move_2p_dp_30 | `f1a(paint(x, local(x)))` | 58.8 | ✓ |
| 1d_move_2p_dp_31 | `paint(f1b(x), segment(x))` | 45.7 | ✓ |
| 1d_move_2p_dp_32 | `f1b(f1a(x))` | 58.9 | ✗ |
| 1d_move_2p_dp_33 | `f1b(f1b(x))` | 53.3 | ✓ |
| 1d_move_2p_dp_34 | `f1b(paint(x, segment(x)))` | 63.2 | ✓ |
| 1d_move_2p_dp_35 | `f1b(f1a(x))` | 61.6 | ✓ |
| 1d_move_2p_dp_36 | `f1b(paint(x, scan(x)))` | 59.2 | ✓ |
| 1d_move_2p_dp_37 | `paint(paint(x, local(x)), segment(x))` | 49.0 | ✓ |
| 1d_move_2p_dp_38 | `f1b(paint(x, local(shift(x))))` | 72.2 | ✓ |
| 1d_move_2p_dp_39 | `f1a(paint(x, local(x)))` | 42.2 | ✓ |
| 1d_move_2p_dp_4 | `f1b(paint(x, scan(x)))` | 61.5 | ✓ |
| 1d_move_2p_dp_40 | `f1a(f1b(x))` | 58.0 | ✓ |
| 1d_move_2p_dp_41 | `f1b(f1a(x))` | 62.5 | ✓ |
| 1d_move_2p_dp_42 | `paint(f1b(x), segment(x))` | 48.1 | ✓ |
| 1d_move_2p_dp_43 | `paint(shift(x), local(x))` | 64.0 | ✓ |
| 1d_move_2p_dp_44 | `paint(paint(shift(x), scan(x)), local(x))` | 55.0 | ✓ |
| 1d_move_2p_dp_45 | `f1b(paint(x, segment(x)))` | 60.8 | ✓ |
| 1d_move_2p_dp_46 | `paint(paint(x, local(x)), segment(shift(x)))` | 54.3 | ✓ |
| 1d_move_2p_dp_47 | `f0a(x)` | 65.7 | ✗ |
| 1d_move_2p_dp_48 | `f1b(paint(x, scan(x)))` | 65.1 | ✓ |
| 1d_move_2p_dp_49 | `f1b(f1b(x))` | 57.3 | ✓ |
| 1d_move_2p_dp_5 | `paint(paint(x, local(x)), local(shift(x)))` | 59.8 | ✗ |
| 1d_move_2p_dp_6 | `f1a(paint(x, local(x)))` | 48.9 | ✓ |
| 1d_move_2p_dp_7 | `paint(f1b(x), segment(x))` | 58.7 | ✓ |
| 1d_move_2p_dp_8 | `f1b(paint(x, local(shift(x))))` | 68.6 | ✓ |
| 1d_move_2p_dp_9 | `paint(f1b(x), segment(x))` | 41.0 | ✓ |
| 1d_move_3p_0 | `shift(x)` | 54.3 | ✓ |
| 1d_move_3p_1 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_10 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_11 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_12 | `shift(x)` | 54.4 | ✓ |
| 1d_move_3p_13 | `shift(x)` | 54.3 | ✓ |
| 1d_move_3p_14 | `paint(shift(x), local(x))` | 52.3 | ✓ |
| 1d_move_3p_15 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_16 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_17 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_18 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_19 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_2 | `f1b(f1a(x))` | 43.1 | ✓ |
| 1d_move_3p_20 | `shift(x)` | 54.4 | ✓ |
| 1d_move_3p_21 | `paint(paint(shift(x), local(x)), scan(x))` | 43.0 | ✓ |
| 1d_move_3p_22 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_23 | `paint(paint(x, local(x)), segment(shift(x)))` | 53.5 | ✓ |
| 1d_move_3p_24 | `shift(x)` | 54.5 | ✓ |
| 1d_move_3p_25 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_26 | `paint(paint(shift(x), scan(x)), local(x))` | 54.4 | ✓ |
| 1d_move_3p_27 | `shift(x)` | 54.6 | ✓ |
| 1d_move_3p_28 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_29 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_3 | `paint(shift(x), local(x))` | 52.9 | ✓ |
| 1d_move_3p_30 | `f1b(f1a(x))` | 42.0 | ✓ |
| 1d_move_3p_31 | `paint(paint(x, local(x)), segment(shift(x)))` | 47.3 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_35 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_36 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_37 | `f1b(f1a(x))` | 48.8 | ✓ |
| 1d_move_3p_38 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_39 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_4 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_40 | `shift(x)` | 54.1 | ✓ |
| 1d_move_3p_41 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_43 | `paint(paint(x, local(x)), scan(shift(x)))` | 50.0 | ✓ |
| 1d_move_3p_44 | `f1b(f1a(x))` | 53.9 | ✓ |
| 1d_move_3p_45 | `f1b(paint(x, local(shift(x))))` | 51.4 | ✓ |
| 1d_move_3p_46 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_47 | `paint(shift(x), local(f1a(x)))` | 52.6 | ✓ |
| 1d_move_3p_48 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_49 | `f1b(f1a(x))` | 48.3 | ✓ |
| 1d_move_3p_5 | `shift(x)` | 54.6 | ✓ |
| 1d_move_3p_6 | `f0b(paint(x, local(x)))` | 52.2 | ✓ |
| 1d_move_3p_7 | `f1b(f1a(x))` | 49.4 | ✓ |
| 1d_move_3p_8 | `shift(x)` | 52.9 | ✓ |
| 1d_move_3p_9 | `shift(x)` | 54.6 | ✓ |
| 1d_move_dp_0 | `paint(paint(x, scan(x)), segment(x))` | 149.4 | ✗ |
| 1d_move_dp_1 | `paint(x, scan(paint(x, local(x))))` | 139.2 | ✗ |
| 1d_move_dp_10 | `shift(shift(x))` | 120.7 | ✗ |
| 1d_move_dp_11 | `shift(shift(x))` | 119.9 | ✗ |
| 1d_move_dp_12 | `f1b(paint(shift(x), local(x)))` | 119.8 | ✗ |
| 1d_move_dp_13 | `paint(paint(x, scan(x)), segment(x))` | 98.7 | ✗ |
| 1d_move_dp_14 | `paint(paint(x, local(x)), local(shift(x)))` | 61.0 | ✗ |
| 1d_move_dp_15 | `f1b(paint(x, scan(x)))` | 122.8 | ✗ |
| 1d_move_dp_16 | `paint(paint(x, scan(x)), local(x))` | 120.5 | ✗ |
| 1d_move_dp_17 | `paint(x, segment(x))` | 137.6 | ✗ |
| 1d_move_dp_18 | `f1b(paint(shift(x), local(x)))` | 119.4 | ✗ |
| 1d_move_dp_19 | `f1b(paint(x, local(x)))` | 102.5 | ✗ |
| 1d_move_dp_2 | `f1a(x)` | 156.3 | ✗ |
| 1d_move_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 68.9 | ✗ |
| 1d_move_dp_21 | `f1a(x)` | 130.3 | ✗ |
| 1d_move_dp_22 | `paint(x, local(shift(x)))` | 116.3 | ✗ |
| 1d_move_dp_23 | `f1b(paint(x, local(x)))` | 107.8 | ✓ |
| 1d_move_dp_24 | `f1a(x)` | 124.4 | ✗ |
| 1d_move_dp_25 | `paint(paint(x, scan(x)), segment(x))` | 106.3 | ✗ |
| 1d_move_dp_26 | `f1b(paint(shift(x), local(x)))` | 120.3 | ✗ |
| 1d_move_dp_27 | `shift(paint(x, scan(x)))` | 81.5 | ✗ |
| 1d_move_dp_28 | `f1b(f1b(x))` | 116.5 | ✗ |
| 1d_move_dp_29 | `paint(paint(x, segment(x)), local(shift(x)))` | 130.0 | ✗ |
| 1d_move_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 102.5 | ✗ |
| 1d_move_dp_30 | `paint(paint(x, local(x)), segment(x))` | 71.6 | ✗ |
| 1d_move_dp_31 | `f1a(x)` | 94.3 | ✗ |
| 1d_move_dp_32 | `paint(paint(x, scan(x)), local(x))` | 138.3 | ✗ |
| 1d_move_dp_33 | `f0b(shift(x))` | 107.6 | ✗ |
| 1d_move_dp_34 | `paint(paint(x, local(shift(x))), scan(x))` | 99.6 | ✗ |
| 1d_move_dp_35 | `paint(x, scan(f1a(x)))` | 124.7 | ✗ |
| 1d_move_dp_36 | `paint(paint(x, scan(x)), local(x))` | 113.4 | ✗ |
| 1d_move_dp_37 | `f1b(shift(x))` | 69.1 | ✓ |
| 1d_move_dp_38 | `paint(x, segment(x))` | 140.5 | ✗ |
| 1d_move_dp_39 | `shift(shift(x))` | 117.7 | ✗ |
| 1d_move_dp_4 | `f1b(paint(x, local(x)))` | 111.8 | ✗ |
| 1d_move_dp_40 | `paint(paint(x, local(shift(x))), segment(x))` | 97.5 | ✗ |
| 1d_move_dp_41 | `paint(paint(x, local(x)), segment(shift(x)))` | 66.1 | ✗ |
| 1d_move_dp_42 | `paint(f1a(shift(x)), local(x))` | 161.7 | ✗ |
| 1d_move_dp_43 | `f1a(paint(x, local(x)))` | 72.5 | ✗ |
| 1d_move_dp_44 | `paint(f0b(x), local(x))` | 64.3 | ✓ |
| 1d_move_dp_45 | `f1b(paint(x, segment(x)))` | 60.8 | ✗ |
| 1d_move_dp_46 | `shift(f1a(paint(x, local(x))))` | 122.4 | ✗ |
| 1d_move_dp_47 | `shift(paint(paint(x, scan(x)), local(x)))` | 126.3 | ✗ |
| 1d_move_dp_48 | `paint(paint(x, local(x)), segment(shift(x)))` | 95.1 | ✗ |
| 1d_move_dp_49 | `paint(paint(x, local(shift(x))), scan(x))` | 125.9 | ✗ |
| 1d_move_dp_5 | `paint(paint(x, scan(x)), segment(x))` | 119.1 | ✗ |
| 1d_move_dp_6 | `f1a(x)` | 144.4 | ✗ |
| 1d_move_dp_7 | `f0b(shift(x))` | 63.7 | ✓ |
| 1d_move_dp_8 | `paint(paint(x, local(x)), local(shift(x)))` | 61.5 | ✗ |
| 1d_move_dp_9 | `paint(paint(x, scan(x)), segment(x))` | 128.8 | ✗ |
| 1d_padded_fill_0 | `paint(paint(x, scan(x)), segment(x))` | 58.7 | ✓ |
| 1d_padded_fill_1 | `paint(f1a(x), local(shift(x)))` | 47.6 | ✗ |
| 1d_padded_fill_10 | `f1b(paint(x, scan(x)))` | 66.6 | ✓ |
| 1d_padded_fill_11 | `f1a(f1b(x))` | 44.8 | ✓ |
| 1d_padded_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 56.9 | ✓ |
| 1d_padded_fill_13 | `f0a(x)` | 58.8 | ✓ |
| 1d_padded_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 40.6 | ✓ |
| 1d_padded_fill_15 | `paint(f1a(x), local(x))` | 38.3 | ✗ |
| 1d_padded_fill_16 | `paint(paint(x, scan(x)), segment(x))` | 52.7 | ✓ |
| 1d_padded_fill_17 | `f0a(x)` | 47.8 | ✓ |
| 1d_padded_fill_18 | `paint(paint(x, scan(x)), local(x))` | 47.6 | ✓ |
| 1d_padded_fill_19 | `f1a(paint(x, local(x)))` | 47.5 | ✗ |
| 1d_padded_fill_2 | `paint(paint(shift(x), scan(x)), local(x))` | 56.8 | ✓ |
| 1d_padded_fill_20 | `paint(paint(x, scan(x)), segment(x))` | 54.0 | ✓ |
| 1d_padded_fill_21 | `paint(x, scan(f1a(x)))` | 49.5 | ✓ |
| 1d_padded_fill_22 | `f1a(paint(x, local(x)))` | 44.1 | ✗ |
| 1d_padded_fill_23 | `paint(paint(x, scan(x)), segment(x))` | 45.3 | ✓ |
| 1d_padded_fill_24 | `f1a(paint(x, scan(x)))` | 36.9 | ✓ |
| 1d_padded_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 47.6 | ✓ |
| 1d_padded_fill_26 | `f0a(x)` | 55.5 | ✓ |
| 1d_padded_fill_27 | `f1a(f1b(x))` | 43.9 | ✓ |
| 1d_padded_fill_28 | `paint(paint(x, scan(x)), segment(x))` | 45.9 | ✓ |
| 1d_padded_fill_29 | `paint(paint(x, scan(x)), segment(x))` | 49.3 | ✓ |
| 1d_padded_fill_3 | `f1b(paint(x, scan(x)))` | 43.9 | ✓ |
| 1d_padded_fill_30 | `paint(f1a(x), segment(x))` | 53.3 | ✓ |
| 1d_padded_fill_31 | `paint(paint(x, scan(x)), local(x))` | 54.7 | ✓ |
| 1d_padded_fill_32 | `paint(f1a(x), segment(x))` | 54.0 | ✓ |
| 1d_padded_fill_33 | `f1a(f1a(x))` | 48.7 | ✓ |
| 1d_padded_fill_34 | `paint(paint(x, scan(x)), local(shift(x)))` | 34.4 | ✓ |
| 1d_padded_fill_35 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.1 | ✓ |
| 1d_padded_fill_36 | `f1b(f1a(x))` | 31.7 | ✓ |
| 1d_padded_fill_37 | `paint(paint(shift(x), scan(x)), local(x))` | 49.1 | ✓ |
| 1d_padded_fill_38 | `paint(paint(x, scan(x)), segment(x))` | 41.3 | ✓ |
| 1d_padded_fill_39 | `paint(paint(x, scan(x)), local(shift(x)))` | 45.6 | ✓ |
| 1d_padded_fill_4 | `f1a(paint(x, scan(x)))` | 54.6 | ✗ |
| 1d_padded_fill_40 | `f1b(paint(x, scan(x)))` | 30.8 | ✓ |
| 1d_padded_fill_41 | `paint(paint(x, scan(x)), local(x))` | 41.7 | ✓ |
| 1d_padded_fill_42 | `f1a(f1a(x))` | 42.7 | ✓ |
| 1d_padded_fill_43 | `paint(paint(x, scan(x)), segment(x))` | 53.4 | ✓ |
| 1d_padded_fill_44 | `paint(f1a(x), local(shift(x)))` | 43.5 | ✓ |
| 1d_padded_fill_45 | `f1b(f1a(x))` | 56.1 | ✓ |
| 1d_padded_fill_46 | `paint(x, scan(f1a(x)))` | 44.6 | ✓ |
| 1d_padded_fill_47 | `f1a(f1a(x))` | 41.5 | ✓ |
| 1d_padded_fill_48 | `paint(paint(x, scan(x)), local(x))` | 35.5 | ✓ |
| 1d_padded_fill_49 | `paint(paint(x, scan(x)), segment(x))` | 49.4 | ✓ |
| 1d_padded_fill_5 | `paint(paint(x, scan(x)), segment(x))` | 46.4 | ✓ |
| 1d_padded_fill_6 | `paint(f1a(x), local(x))` | 44.5 | ✓ |
| 1d_padded_fill_7 | `paint(paint(x, scan(x)), local(shift(x)))` | 29.1 | ✓ |
| 1d_padded_fill_8 | `paint(paint(x, scan(x)), segment(x))` | 51.6 | ✓ |
| 1d_padded_fill_9 | `paint(x, scan(paint(x, scan(x))))` | 51.3 | ✓ |
| 1d_pcopy_1c_0 | `f1b(f1b(x))` | 81.4 | ✗ |
| 1d_pcopy_1c_1 | `f1a(paint(x, local(shift(x))))` | 59.9 | ✗ |
| 1d_pcopy_1c_10 | `f1b(f1a(x))` | 61.6 | ✓ |
| 1d_pcopy_1c_11 | `f1b(paint(x, local(x)))` | 51.7 | ✗ |
| 1d_pcopy_1c_12 | `paint(x, local(paint(x, local(x))))` | 58.6 | ✓ |
| 1d_pcopy_1c_13 | `f1b(paint(x, local(x)))` | 66.3 | ✗ |
| 1d_pcopy_1c_14 | `f1b(paint(x, local(x)))` | 73.1 | ✗ |
| 1d_pcopy_1c_15 | `paint(paint(x, local(x)), scan(shift(x)))` | 55.7 | ✗ |
| 1d_pcopy_1c_16 | `f1b(f1a(x))` | 43.6 | ✗ |
| 1d_pcopy_1c_17 | `f1b(paint(x, local(x)))` | 57.8 | ✗ |
| 1d_pcopy_1c_18 | `f1b(f1a(x))` | 40.8 | ✓ |
| 1d_pcopy_1c_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 73.6 | ✗ |
| 1d_pcopy_1c_2 | `f1b(paint(x, scan(x)))` | 64.3 | ✓ |
| 1d_pcopy_1c_20 | `f1b(paint(x, scan(x)))` | 67.3 | ✗ |
| 1d_pcopy_1c_21 | `paint(paint(x, segment(x)), local(x))` | 73.0 | ✓ |
| 1d_pcopy_1c_22 | `f1b(f1a(x))` | 40.0 | ✓ |
| 1d_pcopy_1c_23 | `paint(paint(x, segment(x)), local(x))` | 71.2 | ✓ |
| 1d_pcopy_1c_24 | `f1b(f1a(x))` | 65.7 | ✓ |
| 1d_pcopy_1c_25 | `f1b(paint(x, scan(x)))` | 73.4 | ✓ |
| 1d_pcopy_1c_26 | `f1b(paint(x, scan(x)))` | 63.6 | ✗ |
| 1d_pcopy_1c_27 | `f1b(paint(x, scan(x)))` | 64.4 | ✓ |
| 1d_pcopy_1c_28 | `f1b(x)` | 74.7 | ✓ |
| 1d_pcopy_1c_29 | `paint(paint(x, segment(x)), local(x))` | 61.7 | ✓ |
| 1d_pcopy_1c_3 | `paint(x, local(paint(x, local(x))))` | 79.0 | ✓ |
| 1d_pcopy_1c_30 | `paint(x, local(f1b(x)))` | 55.7 | ✗ |
| 1d_pcopy_1c_31 | `f1b(paint(x, scan(x)))` | 61.0 | ✗ |
| 1d_pcopy_1c_32 | `paint(x, local(paint(x, scan(x))))` | 70.9 | ✓ |
| 1d_pcopy_1c_33 | `f1b(f1a(x))` | 57.9 | ✓ |
| 1d_pcopy_1c_34 | `f1a(paint(x, local(x)))` | 65.6 | ✗ |
| 1d_pcopy_1c_35 | `paint(paint(x, segment(x)), local(x))` | 60.4 | ✗ |
| 1d_pcopy_1c_36 | `paint(paint(x, segment(x)), local(x))` | 78.2 | ✓ |
| 1d_pcopy_1c_37 | `paint(paint(x, segment(x)), local(x))` | 71.6 | ✗ |
| 1d_pcopy_1c_38 | `paint(f1a(x), scan(x))` | 70.3 | ✗ |
| 1d_pcopy_1c_39 | `f1b(f1a(x))` | 44.6 | ✓ |
| 1d_pcopy_1c_4 | `f1b(f1b(x))` | 57.7 | ✗ |
| 1d_pcopy_1c_40 | `f1b(paint(x, scan(x)))` | 56.0 | ✗ |
| 1d_pcopy_1c_41 | `paint(paint(x, local(x)), scan(shift(x)))` | 63.6 | ✗ |
| 1d_pcopy_1c_42 | `paint(f1b(x), local(x))` | 62.8 | ✗ |
| 1d_pcopy_1c_43 | `f1b(f1a(x))` | 51.3 | ✓ |
| 1d_pcopy_1c_44 | `f1b(f1a(x))` | 72.0 | ✗ |
| 1d_pcopy_1c_45 | `paint(f0a(x), local(x))` | 78.1 | ✓ |
| 1d_pcopy_1c_46 | `paint(paint(x, local(x)), scan(shift(x)))` | 64.7 | ✗ |
| 1d_pcopy_1c_47 | `f1b(paint(x, scan(x)))` | 65.9 | ✓ |
| 1d_pcopy_1c_48 | `f1b(f1a(x))` | 66.0 | ✗ |
| 1d_pcopy_1c_49 | `paint(paint(x, local(x)), scan(shift(x)))` | 69.2 | ✗ |
| 1d_pcopy_1c_5 | `paint(paint(x, segment(x)), local(x))` | 55.1 | ✗ |
| 1d_pcopy_1c_6 | `f1b(paint(x, segment(x)))` | 67.9 | ✗ |
| 1d_pcopy_1c_7 | `f1b(paint(x, scan(x)))` | 52.4 | ✓ |
| 1d_pcopy_1c_8 | `f1b(paint(x, scan(x)))` | 51.8 | ✓ |
| 1d_pcopy_1c_9 | `paint(paint(x, scan(x)), local(x))` | 66.2 | ✓ |
| 1d_pcopy_mc_0 | `f1b(f1a(x))` | 41.5 | ✓ |
| 1d_pcopy_mc_1 | `f0a(x)` | 47.1 | ✗ |
| 1d_pcopy_mc_10 | `paint(paint(x, segment(x)), local(x))` | 55.8 | ✓ |
| 1d_pcopy_mc_11 | `paint(f1b(x), local(x))` | 44.9 | ✓ |
| 1d_pcopy_mc_12 | `f0a(x)` | 48.5 | ✓ |
| 1d_pcopy_mc_13 | `paint(paint(x, segment(x)), local(x))` | 65.8 | ✓ |
| 1d_pcopy_mc_14 | `paint(paint(x, local(shift(x))), local(x))` | 48.7 | ✓ |
| 1d_pcopy_mc_15 | `f0a(x)` | 45.4 | ✓ |
| 1d_pcopy_mc_16 | `paint(paint(x, segment(shift(x))), local(x))` | 47.5 | ✓ |
| 1d_pcopy_mc_17 | `paint(paint(x, segment(shift(x))), local(x))` | 61.0 | ✓ |
| 1d_pcopy_mc_18 | `paint(paint(x, segment(x)), local(x))` | 39.3 | ✗ |
| 1d_pcopy_mc_19 | `f1b(f1b(x))` | 48.5 | ✗ |
| 1d_pcopy_mc_2 | `f1b(x)` | 45.7 | ✓ |
| 1d_pcopy_mc_20 | `f1b(paint(x, local(x)))` | 43.8 | ✓ |
| 1d_pcopy_mc_21 | `paint(f1b(x), local(x))` | 41.2 | ✓ |
| 1d_pcopy_mc_22 | `paint(paint(x, segment(shift(x))), local(x))` | 49.6 | ✓ |
| 1d_pcopy_mc_23 | `f1b(paint(x, scan(x)))` | 42.7 | ✓ |
| 1d_pcopy_mc_24 | `f0a(x)` | 66.7 | ✓ |
| 1d_pcopy_mc_25 | `paint(x, local(paint(x, segment(x))))` | 65.8 | ✓ |
| 1d_pcopy_mc_26 | `paint(paint(x, segment(shift(x))), local(x))` | 50.1 | ✓ |
| 1d_pcopy_mc_27 | `paint(paint(x, segment(x)), local(x))` | 66.5 | ✓ |
| 1d_pcopy_mc_28 | `paint(paint(x, segment(x)), local(x))` | 55.5 | ✓ |
| 1d_pcopy_mc_29 | `f1b(paint(x, local(x)))` | 65.6 | ✓ |
| 1d_pcopy_mc_3 | `paint(paint(x, segment(x)), local(x))` | 42.7 | ✓ |
| 1d_pcopy_mc_30 | `paint(paint(x, segment(x)), local(x))` | 46.6 | ✗ |
| 1d_pcopy_mc_31 | `paint(f1a(x), local(x))` | 53.5 | ✓ |
| 1d_pcopy_mc_32 | `paint(paint(x, segment(shift(x))), local(x))` | 45.8 | ✓ |
| 1d_pcopy_mc_33 | `f1b(paint(x, scan(x)))` | 65.8 | ✓ |
| 1d_pcopy_mc_34 | `f1b(x)` | 72.0 | ✗ |
| 1d_pcopy_mc_35 | `f0a(x)` | 52.7 | ✓ |
| 1d_pcopy_mc_36 | `paint(f1a(x), local(x))` | 48.7 | ✓ |
| 1d_pcopy_mc_37 | `f1b(paint(x, scan(x)))` | 60.5 | ✓ |
| 1d_pcopy_mc_38 | `paint(paint(x, local(shift(x))), local(x))` | 47.3 | ✓ |
| 1d_pcopy_mc_39 | `paint(paint(x, segment(x)), local(x))` | 48.1 | ✓ |
| 1d_pcopy_mc_4 | `paint(f1a(x), local(x))` | 54.3 | ✓ |
| 1d_pcopy_mc_40 | `paint(paint(x, segment(x)), local(x))` | 59.2 | ✓ |
| 1d_pcopy_mc_41 | `paint(f1a(x), local(x))` | 50.6 | ✓ |
| 1d_pcopy_mc_42 | `f1b(f1a(x))` | 48.5 | ✓ |
| 1d_pcopy_mc_43 | `paint(paint(x, segment(x)), local(x))` | 46.4 | ✓ |
| 1d_pcopy_mc_44 | `paint(paint(x, scan(x)), local(x))` | 43.8 | ✓ |
| 1d_pcopy_mc_45 | `f1b(f1a(x))` | 57.9 | ✓ |
| 1d_pcopy_mc_46 | `paint(f1a(x), local(x))` | 42.4 | ✓ |
| 1d_pcopy_mc_47 | `f0a(x)` | 54.0 | ✓ |
| 1d_pcopy_mc_48 | `paint(paint(x, segment(x)), local(x))` | 50.0 | ✓ |
| 1d_pcopy_mc_49 | `f0a(x)` | 54.6 | ✓ |
| 1d_pcopy_mc_5 | `paint(paint(x, segment(x)), local(x))` | 46.3 | ✓ |
| 1d_pcopy_mc_6 | `f1b(f1a(x))` | 40.4 | ✓ |
| 1d_pcopy_mc_7 | `f1b(paint(x, local(x)))` | 64.2 | ✓ |
| 1d_pcopy_mc_8 | `paint(paint(x, segment(x)), local(x))` | 47.6 | ✓ |
| 1d_pcopy_mc_9 | `paint(paint(x, scan(x)), local(x))` | 42.7 | ✓ |
| 1d_recolor_cmp_0 | `paint(paint(x, local(x)), segment(x))` | 39.9 | ✓ |
| 1d_recolor_cmp_1 | `f1a(paint(x, segment(x)))` | 51.8 | ✓ |
| 1d_recolor_cmp_10 | `paint(paint(x, segment(x)), segment(x))` | 46.3 | ✓ |
| 1d_recolor_cmp_11 | `paint(paint(x, local(shift(x))), segment(x))` | 47.0 | ✓ |
| 1d_recolor_cmp_12 | `paint(x, segment(x))` | 75.5 | ✓ |
| 1d_recolor_cmp_13 | `paint(paint(x, segment(x)), local(x))` | 42.9 | ✓ |
| 1d_recolor_cmp_14 | `paint(f1a(x), segment(x))` | 28.3 | ✓ |
| 1d_recolor_cmp_15 | `paint(paint(x, scan(x)), segment(x))` | 64.2 | ✓ |
| 1d_recolor_cmp_16 | `paint(paint(x, local(shift(x))), segment(x))` | 48.1 | ✓ |
| 1d_recolor_cmp_17 | `paint(paint(x, scan(x)), segment(x))` | 46.1 | ✓ |
| 1d_recolor_cmp_18 | `paint(f1b(x), segment(x))` | 30.7 | ✓ |
| 1d_recolor_cmp_19 | `paint(paint(x, segment(x)), segment(x))` | 42.1 | ✓ |
| 1d_recolor_cmp_2 | `paint(f1b(x), segment(x))` | 44.7 | ✓ |
| 1d_recolor_cmp_20 | `paint(paint(x, segment(x)), local(x))` | 33.0 | ✓ |
| 1d_recolor_cmp_21 | `paint(paint(x, segment(x)), scan(x))` | 40.7 | ✓ |
| 1d_recolor_cmp_22 | `paint(f1a(x), segment(x))` | 44.0 | ✓ |
| 1d_recolor_cmp_23 | `paint(paint(x, segment(x)), segment(x))` | 44.3 | ✓ |
| 1d_recolor_cmp_24 | `paint(f1b(x), segment(x))` | 46.3 | ✓ |
| 1d_recolor_cmp_25 | `paint(f1b(x), segment(x))` | 27.3 | ✓ |
| 1d_recolor_cmp_26 | `paint(f1a(x), segment(x))` | 39.6 | ✓ |
| 1d_recolor_cmp_27 | `paint(paint(x, scan(x)), segment(x))` | 46.1 | ✓ |
| 1d_recolor_cmp_28 | `paint(f1b(x), segment(x))` | 44.6 | ✓ |
| 1d_recolor_cmp_29 | `paint(paint(x, scan(x)), segment(x))` | 30.0 | ✓ |
| 1d_recolor_cmp_3 | `paint(paint(x, local(shift(x))), segment(x))` | 69.4 | ✓ |
| 1d_recolor_cmp_30 | `paint(paint(x, segment(x)), local(x))` | 59.0 | ✓ |
| 1d_recolor_cmp_31 | `paint(f1b(x), segment(x))` | 32.5 | ✓ |
| 1d_recolor_cmp_32 | `paint(paint(x, scan(x)), segment(x))` | 53.6 | ✓ |
| 1d_recolor_cmp_33 | `paint(paint(x, scan(x)), segment(x))` | 72.9 | ✓ |
| 1d_recolor_cmp_34 | `paint(paint(x, segment(x)), segment(x))` | 44.5 | ✓ |
| 1d_recolor_cmp_35 | `paint(f1a(x), segment(x))` | 55.3 | ✓ |
| 1d_recolor_cmp_36 | `paint(paint(x, scan(x)), segment(x))` | 39.1 | ✓ |
| 1d_recolor_cmp_37 | `paint(paint(x, segment(x)), scan(x))` | 30.5 | ✓ |
| 1d_recolor_cmp_38 | `paint(paint(x, scan(x)), segment(x))` | 46.0 | ✓ |
| 1d_recolor_cmp_39 | `paint(paint(x, scan(x)), segment(x))` | 42.8 | ✓ |
| 1d_recolor_cmp_4 | `paint(f1a(x), segment(x))` | 48.7 | ✓ |
| 1d_recolor_cmp_40 | `paint(f1a(x), segment(x))` | 57.4 | ✗ |
| 1d_recolor_cmp_41 | `paint(f1a(x), segment(x))` | 38.5 | ✓ |
| 1d_recolor_cmp_42 | `paint(paint(x, segment(x)), scan(x))` | 63.5 | ✓ |
| 1d_recolor_cmp_43 | `paint(paint(x, scan(x)), segment(x))` | 55.6 | ✓ |
| 1d_recolor_cmp_44 | `paint(paint(x, scan(x)), segment(x))` | 37.6 | ✓ |
| 1d_recolor_cmp_45 | `paint(f1b(x), segment(x))` | 60.2 | ✓ |
| 1d_recolor_cmp_46 | `paint(paint(x, segment(x)), scan(x))` | 52.9 | ✓ |
| 1d_recolor_cmp_47 | `paint(paint(x, scan(x)), segment(x))` | 51.8 | ✓ |
| 1d_recolor_cmp_48 | `paint(paint(x, local(x)), scan(x))` | 65.5 | ✗ |
| 1d_recolor_cmp_49 | `paint(paint(x, segment(x)), scan(x))` | 64.5 | ✓ |
| 1d_recolor_cmp_5 | `paint(paint(x, segment(x)), segment(x))` | 44.8 | ✓ |
| 1d_recolor_cmp_6 | `paint(paint(x, scan(x)), segment(x))` | 68.4 | ✓ |
| 1d_recolor_cmp_7 | `paint(f1b(x), segment(x))` | 43.0 | ✓ |
| 1d_recolor_cmp_8 | `paint(paint(x, scan(x)), segment(x))` | 35.6 | ✓ |
| 1d_recolor_cmp_9 | `paint(paint(x, segment(x)), scan(x))` | 44.3 | ✓ |
| 1d_recolor_cnt_0 | `paint(paint(x, scan(x)), segment(x))` | 83.9 | ✓ |
| 1d_recolor_cnt_1 | `f1b(paint(x, segment(x)))` | 98.4 | ✓ |
| 1d_recolor_cnt_10 | `paint(paint(x, segment(x)), local(shift(x)))` | 101.3 | ✓ |
| 1d_recolor_cnt_11 | `paint(f1b(x), segment(x))` | 110.6 | ✓ |
| 1d_recolor_cnt_12 | `paint(paint(x, segment(x)), local(x))` | 80.4 | ✓ |
| 1d_recolor_cnt_13 | `paint(paint(x, segment(x)), segment(x))` | 93.7 | ✓ |
| 1d_recolor_cnt_14 | `paint(paint(x, segment(x)), local(x))` | 101.0 | ✓ |
| 1d_recolor_cnt_15 | `paint(paint(x, segment(x)), local(x))` | 80.8 | ✓ |
| 1d_recolor_cnt_16 | `paint(paint(x, segment(x)), local(x))` | 73.1 | ✓ |
| 1d_recolor_cnt_17 | `paint(paint(x, segment(x)), local(x))` | 65.0 | ✓ |
| 1d_recolor_cnt_18 | `paint(f1a(x), segment(x))` | 113.4 | ✓ |
| 1d_recolor_cnt_19 | `paint(x, segment(x))` | 83.5 | ✓ |
| 1d_recolor_cnt_2 | `paint(paint(x, segment(x)), local(x))` | 71.6 | ✓ |
| 1d_recolor_cnt_20 | `paint(paint(x, segment(x)), scan(x))` | 88.7 | ✓ |
| 1d_recolor_cnt_21 | `paint(paint(x, segment(x)), local(x))` | 69.2 | ✓ |
| 1d_recolor_cnt_22 | `paint(paint(x, segment(x)), local(x))` | 64.3 | ✓ |
| 1d_recolor_cnt_23 | `paint(paint(x, segment(x)), local(x))` | 76.6 | ✓ |
| 1d_recolor_cnt_24 | `paint(paint(x, segment(x)), local(x))` | 91.7 | ✓ |
| 1d_recolor_cnt_25 | `paint(x, segment(paint(x, local(x))))` | 79.6 | ✓ |
| 1d_recolor_cnt_26 | `paint(paint(x, segment(x)), local(x))` | 77.3 | ✓ |
| 1d_recolor_cnt_27 | `paint(paint(x, segment(x)), local(shift(x)))` | 78.8 | ✓ |
| 1d_recolor_cnt_28 | `paint(x, segment(x))` | 79.2 | ✓ |
| 1d_recolor_cnt_29 | `paint(paint(x, segment(x)), segment(x))` | 108.1 | ✓ |
| 1d_recolor_cnt_3 | `paint(f1a(x), segment(x))` | 64.0 | ✓ |
| 1d_recolor_cnt_30 | `paint(paint(x, segment(x)), local(x))` | 77.3 | ✓ |
| 1d_recolor_cnt_31 | `paint(paint(x, segment(x)), scan(x))` | 76.6 | ✓ |
| 1d_recolor_cnt_32 | `paint(paint(x, segment(x)), local(x))` | 84.0 | ✓ |
| 1d_recolor_cnt_33 | `paint(paint(x, segment(x)), segment(x))` | 99.6 | ✓ |
| 1d_recolor_cnt_34 | `paint(x, segment(paint(x, segment(x))))` | 92.4 | ✓ |
| 1d_recolor_cnt_35 | `paint(x, segment(paint(x, segment(x))))` | 82.5 | ✓ |
| 1d_recolor_cnt_36 | `f1a(paint(x, segment(x)))` | 110.4 | ✓ |
| 1d_recolor_cnt_37 | `paint(paint(x, segment(x)), local(x))` | 67.9 | ✓ |
| 1d_recolor_cnt_38 | `paint(paint(x, scan(x)), segment(x))` | 74.2 | ✓ |
| 1d_recolor_cnt_39 | `paint(paint(x, segment(x)), segment(x))` | 70.7 | ✓ |
| 1d_recolor_cnt_4 | `paint(paint(x, segment(x)), local(x))` | 78.4 | ✓ |
| 1d_recolor_cnt_40 | `paint(paint(x, segment(x)), segment(x))` | 81.5 | ✓ |
| 1d_recolor_cnt_41 | `f1a(paint(x, segment(x)))` | 100.2 | ✓ |
| 1d_recolor_cnt_42 | `paint(paint(x, scan(x)), segment(x))` | 64.2 | ✓ |
| 1d_recolor_cnt_43 | `paint(paint(shift(x), segment(x)), local(x))` | 85.9 | ✓ |
| 1d_recolor_cnt_44 | `paint(paint(x, scan(x)), segment(x))` | 56.8 | ✓ |
| 1d_recolor_cnt_45 | `f1b(paint(x, segment(x)))` | 96.8 | ✓ |
| 1d_recolor_cnt_46 | `paint(paint(x, segment(x)), local(x))` | 85.6 | ✓ |
| 1d_recolor_cnt_47 | `paint(x, segment(f1b(x)))` | 106.4 | ✓ |
| 1d_recolor_cnt_48 | `paint(paint(x, segment(x)), local(x))` | 90.8 | ✓ |
| 1d_recolor_cnt_49 | `paint(paint(x, scan(x)), segment(x))` | 84.4 | ✓ |
| 1d_recolor_cnt_5 | `paint(paint(x, segment(x)), local(x))` | 86.2 | ✓ |
| 1d_recolor_cnt_6 | `paint(x, segment(x))` | 86.9 | ✓ |
| 1d_recolor_cnt_7 | `paint(paint(x, segment(x)), local(shift(x)))` | 73.5 | ✓ |
| 1d_recolor_cnt_8 | `paint(x, segment(x))` | 78.4 | ✓ |
| 1d_recolor_cnt_9 | `paint(paint(x, scan(x)), segment(x))` | 90.0 | ✓ |
| 1d_recolor_oe_0 | `paint(paint(x, scan(x)), segment(x))` | 80.3 | ✗ |
| 1d_recolor_oe_1 | `paint(paint(x, segment(x)), local(x))` | 62.8 | ✓ |
| 1d_recolor_oe_10 | `f1b(paint(x, segment(x)))` | 85.8 | ✓ |
| 1d_recolor_oe_11 | `f1a(paint(x, segment(x)))` | 97.6 | ✗ |
| 1d_recolor_oe_12 | `paint(paint(x, segment(x)), local(x))` | 106.5 | ✓ |
| 1d_recolor_oe_13 | `paint(paint(x, segment(x)), segment(x))` | 69.6 | ✓ |
| 1d_recolor_oe_14 | `paint(paint(x, segment(x)), local(x))` | 67.8 | ✓ |
| 1d_recolor_oe_15 | `f1a(paint(x, segment(x)))` | 71.2 | ✓ |
| 1d_recolor_oe_16 | `paint(paint(x, segment(x)), local(shift(x)))` | 96.1 | ✓ |
| 1d_recolor_oe_17 | `paint(paint(x, segment(x)), local(x))` | 99.9 | ✓ |
| 1d_recolor_oe_18 | `f1b(paint(x, segment(x)))` | 59.2 | ✓ |
| 1d_recolor_oe_19 | `paint(paint(x, segment(x)), local(x))` | 77.0 | ✓ |
| 1d_recolor_oe_2 | `paint(x, segment(x))` | 61.2 | ✓ |
| 1d_recolor_oe_20 | `paint(paint(x, segment(x)), segment(x))` | 91.5 | ✓ |
| 1d_recolor_oe_21 | `paint(paint(x, segment(x)), local(x))` | 69.6 | ✓ |
| 1d_recolor_oe_22 | `paint(paint(x, segment(x)), scan(x))` | 81.3 | ✓ |
| 1d_recolor_oe_23 | `paint(paint(x, segment(x)), segment(x))` | 63.5 | ✓ |
| 1d_recolor_oe_24 | `paint(x, segment(f1b(x)))` | 65.7 | ✓ |
| 1d_recolor_oe_25 | `paint(paint(x, segment(x)), scan(x))` | 93.2 | ✓ |
| 1d_recolor_oe_26 | `paint(x, segment(paint(x, scan(x))))` | 59.9 | ✓ |
| 1d_recolor_oe_27 | `f1a(paint(x, segment(x)))` | 80.2 | ✓ |
| 1d_recolor_oe_28 | `paint(f1a(x), segment(x))` | 80.3 | ✗ |
| 1d_recolor_oe_29 | `f1a(paint(x, segment(x)))` | 62.4 | ✗ |
| 1d_recolor_oe_3 | `f1a(paint(x, segment(x)))` | 54.3 | ✓ |
| 1d_recolor_oe_30 | `paint(x, segment(x))` | 69.5 | ✓ |
| 1d_recolor_oe_31 | `paint(x, segment(x))` | 61.0 | ✗ |
| 1d_recolor_oe_32 | `paint(paint(x, segment(x)), local(shift(x)))` | 112.1 | ✓ |
| 1d_recolor_oe_33 | `paint(f1b(x), segment(x))` | 51.2 | ✓ |
| 1d_recolor_oe_34 | `paint(x, segment(f1b(x)))` | 74.0 | ✗ |
| 1d_recolor_oe_35 | `f1a(paint(x, segment(x)))` | 79.3 | ✗ |
| 1d_recolor_oe_36 | `f1b(paint(x, segment(x)))` | 93.0 | ✓ |
| 1d_recolor_oe_37 | `f1a(paint(x, segment(x)))` | 113.6 | ✓ |
| 1d_recolor_oe_38 | `paint(paint(x, segment(x)), segment(x))` | 102.1 | ✓ |
| 1d_recolor_oe_39 | `paint(x, segment(x))` | 59.2 | ✓ |
| 1d_recolor_oe_4 | `paint(paint(x, segment(x)), local(x))` | 74.8 | ✓ |
| 1d_recolor_oe_40 | `paint(paint(x, segment(x)), scan(x))` | 75.9 | ✗ |
| 1d_recolor_oe_41 | `paint(paint(x, segment(x)), local(shift(x)))` | 84.6 | ✓ |
| 1d_recolor_oe_42 | `paint(f1b(x), segment(x))` | 56.7 | ✗ |
| 1d_recolor_oe_43 | `paint(x, segment(paint(x, scan(x))))` | 82.8 | ✓ |
| 1d_recolor_oe_44 | `paint(paint(x, segment(x)), segment(x))` | 92.6 | ✓ |
| 1d_recolor_oe_45 | `paint(paint(x, local(x)), segment(x))` | 70.1 | ✓ |
| 1d_recolor_oe_46 | `paint(paint(x, local(shift(x))), segment(x))` | 100.6 | ✓ |
| 1d_recolor_oe_47 | `paint(paint(x, segment(x)), segment(x))` | 70.4 | ✓ |
| 1d_recolor_oe_48 | `paint(paint(x, segment(x)), local(shift(x)))` | 87.9 | ✓ |
| 1d_recolor_oe_49 | `paint(paint(x, segment(x)), segment(x))` | 98.9 | ✓ |
| 1d_recolor_oe_5 | `f1a(paint(x, segment(x)))` | 113.3 | ✓ |
| 1d_recolor_oe_6 | `f1b(paint(x, segment(x)))` | 83.7 | ✓ |
| 1d_recolor_oe_7 | `paint(paint(x, segment(x)), scan(x))` | 87.6 | ✓ |
| 1d_recolor_oe_8 | `paint(paint(x, segment(x)), segment(x))` | 57.3 | ✓ |
| 1d_recolor_oe_9 | `paint(paint(x, segment(x)), local(x))` | 69.0 | ✓ |
| 1d_scale_dp_0 | `f1b(paint(x, scan(x)))` | 30.2 | ✓ |
| 1d_scale_dp_1 | `paint(paint(x, scan(x)), scan(x))` | 53.8 | ✓ |
| 1d_scale_dp_10 | `paint(paint(x, scan(x)), local(shift(x)))` | 43.2 | ✓ |
| 1d_scale_dp_11 | `paint(paint(x, scan(x)), scan(x))` | 38.7 | ✓ |
| 1d_scale_dp_12 | `f1a(paint(x, local(x)))` | 38.2 | ✓ |
| 1d_scale_dp_13 | `f1a(f1b(x))` | 45.2 | ✓ |
| 1d_scale_dp_14 | `f1a(paint(x, local(x)))` | 31.1 | ✗ |
| 1d_scale_dp_15 | `paint(x, scan(f1b(x)))` | 38.2 | ✓ |
| 1d_scale_dp_16 | `f1a(f1b(x))` | 54.1 | ✓ |
| 1d_scale_dp_17 | `paint(paint(x, scan(x)), local(x))` | 60.3 | ✓ |
| 1d_scale_dp_18 | `paint(paint(x, local(x)), scan(x))` | 28.5 | ✓ |
| 1d_scale_dp_19 | `paint(paint(x, scan(x)), scan(x))` | 44.4 | ✗ |
| 1d_scale_dp_2 | `f1b(paint(x, scan(x)))` | 39.6 | ✓ |
| 1d_scale_dp_20 | `paint(paint(shift(x), local(x)), scan(x))` | 45.6 | ✗ |
| 1d_scale_dp_21 | `paint(paint(x, local(x)), scan(x))` | 60.8 | ✓ |
| 1d_scale_dp_22 | `paint(x, local(x))` | 48.0 | ✓ |
| 1d_scale_dp_23 | `f1a(f1a(x))` | 65.5 | ✓ |
| 1d_scale_dp_24 | `paint(paint(x, scan(x)), scan(x))` | 30.5 | ✓ |
| 1d_scale_dp_25 | `paint(paint(x, scan(x)), scan(x))` | 43.0 | ✓ |
| 1d_scale_dp_26 | `paint(paint(x, scan(x)), scan(x))` | 36.8 | ✓ |
| 1d_scale_dp_27 | `paint(paint(x, local(x)), scan(x))` | 62.8 | ✓ |
| 1d_scale_dp_28 | `paint(x, scan(f1b(x)))` | 50.2 | ✓ |
| 1d_scale_dp_29 | `paint(f1a(x), scan(x))` | 49.4 | ✓ |
| 1d_scale_dp_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 36.4 | ✓ |
| 1d_scale_dp_30 | `f1a(paint(x, local(x)))` | 52.1 | ✓ |
| 1d_scale_dp_31 | `paint(x, scan(f1a(x)))` | 57.1 | ✓ |
| 1d_scale_dp_32 | `paint(paint(x, scan(x)), scan(x))` | 38.9 | ✓ |
| 1d_scale_dp_33 | `f1a(f1a(x))` | 53.2 | ✓ |
| 1d_scale_dp_34 | `paint(paint(x, local(shift(x))), scan(x))` | 35.3 | ✓ |
| 1d_scale_dp_35 | `f1a(f1b(x))` | 39.7 | ✓ |
| 1d_scale_dp_36 | `f1a(paint(x, local(x)))` | 39.6 | ✗ |
| 1d_scale_dp_37 | `f1a(x)` | 42.4 | ✓ |
| 1d_scale_dp_38 | `f1a(paint(x, scan(x)))` | 49.1 | ✗ |
| 1d_scale_dp_39 | `f1a(x)` | 44.6 | ✓ |
| 1d_scale_dp_4 | `paint(x, scan(x))` | 42.0 | ✗ |
| 1d_scale_dp_40 | `paint(paint(x, scan(x)), scan(x))` | 48.0 | ✓ |
| 1d_scale_dp_41 | `f1a(paint(x, scan(x)))` | 66.5 | ✓ |
| 1d_scale_dp_42 | `f1b(f1a(x))` | 32.7 | ✓ |
| 1d_scale_dp_43 | `paint(paint(x, scan(x)), scan(x))` | 49.6 | ✓ |
| 1d_scale_dp_44 | `f0b(x)` | 34.3 | ✓ |
| 1d_scale_dp_45 | `f1b(x)` | 38.5 | ✓ |
| 1d_scale_dp_46 | `paint(paint(x, scan(x)), scan(x))` | 61.4 | ✓ |
| 1d_scale_dp_47 | `f1a(x)` | 57.0 | ✓ |
| 1d_scale_dp_48 | `paint(paint(x, scan(x)), scan(x))` | 36.1 | ✓ |
| 1d_scale_dp_49 | `paint(paint(x, scan(x)), scan(x))` | 44.6 | ✓ |
| 1d_scale_dp_5 | `f1a(x)` | 43.7 | ✓ |
| 1d_scale_dp_50 | `paint(x, scan(paint(x, local(x))))` | 51.3 | ✓ |
| 1d_scale_dp_6 | `paint(f1b(x), scan(x))` | 34.9 | ✓ |
| 1d_scale_dp_7 | `paint(shift(f1a(x)), local(x))` | 42.6 | ✓ |
| 1d_scale_dp_8 | `paint(x, local(paint(x, segment(x))))` | 56.2 | ✓ |
| 1d_scale_dp_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 52.4 | ✓ |
