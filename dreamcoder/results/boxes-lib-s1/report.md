# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 901 (50 per family, drawn with seed 1), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/boxes-lib-s1/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 837/901 (93%) | 855/901 | 885/901 | 47.1 | 10 | 150 | 1625s |
| 1 | 842/901 (93%) | 852/901 | 883/901 | 45.6 | 12 | 150 | 1904s |
| 2 | 805/901 (89%) | 870/901 | 850/901 | 47.9 | 14 | 150 | 2227s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 50/50 | 49/50 | 49/50 |
| denoising_mc | 44/50 | 48/50 | 47/50 |
| fill | 48/50 | 47/50 | 48/50 |
| flip | 50/50 | 50/50 | 50/50 |
| hollow | 49/50 | 49/50 | 50/50 |
| mirror | 50/50 | 50/50 | 12/50 |
| move_1p | 50/50 | 49/50 | 50/50 |
| move_2p | 50/50 | 50/50 | 50/50 |
| move_2p_dp | 50/50 | 50/50 | 50/50 |
| move_3p | 50/50 | 50/50 | 50/50 |
| move_dp | 50/50 | 50/50 | 48/50 |
| padded_fill | 49/50 | 49/50 | 50/50 |
| pcopy_1c | 15/50 | 19/50 | 15/50 |
| pcopy_mc | 42/50 | 41/50 | 44/50 |
| recolor_cmp | 50/50 | 50/50 | 50/50 |
| recolor_cnt | 50/50 | 50/50 | 50/50 |
| recolor_oe | 43/50 | 41/50 | 43/50 |
| scale_dp | 47/51 | 50/51 | 49/51 |

## Library growth

- after iteration 0: `f0a : Grid -> Grid` := `paint(shift(x), local(x))` (6 trained weight tensors inherited)
- after iteration 0: `f0b : Grid -> Grid` := `paint(paint(x, scan(x)), local(x))` (10 trained weight tensors inherited)
- after iteration 1: `f1a : Grid -> Grid` := `paint(paint(x, scan(x)), segment(x))` (10 trained weight tensors inherited)
- after iteration 1: `f1b : Grid -> Grid` := `paint(x, scan(x))` (5 trained weight tensors inherited)

`f0a`'s body:

![f0a](figures/box-f0a.png)

`f0b`'s body:

![f0b](figures/box-f0b.png)

`f1a`'s body:

![f1a](figures/box-f1a.png)

`f1b`'s body:

![f1b](figures/box-f1b.png)

## Examples from the last iteration

### Solved: `1d_fill_48`

`f1b(paint(x, scan(x)))`, DL 62.5 = 10.0 structure + 52.1 parameters + 0.3 data bits, fits its training pairs exactly.

![1d_fill_48](figures/1d_fill_48.png)

| pair | input | output |
|---|---|---|
| train 0 | `2......2..............` | `22222222..............` |
| train 1 | `.........8......8.....` | `.........88888888.....` |
| train 2 | `7........7............` | `7777777777............` |
| **test** | `.1...............1....` | `.11111111111111111....` |
| predicted | | `.11111111111111111....` |

### Solved: `1d_pcopy_mc_22`

`paint(paint(x, local(x)), local(x))`, DL 43.2 = 9.8 structure + 32.3 parameters + 1.1 data bits, fits its training pairs exactly.

![1d_pcopy_mc_22](figures/1d_pcopy_mc_22.png)

| pair | input | output |
|---|---|---|
| train 0 | `..444...5.....3...2.............` | `..444..555...333.222............` |
| train 1 | `.555...1....7...4...............` | `.555..111..777.444..............` |
| train 2 | `.444....5.....2....1............` | `.444...555...222..111...........` |
| **test** | `..999..6.....9...6..............` | `..999.666...999.666.............` |
| predicted | | `..999.666...999.666.............` |

### Solved: `1d_scale_dp_34`

`paint(paint(x, scan(x)), scan(x))`, DL 58.9 = 10.0 structure + 48.8 parameters + 0.1 data bits, fits its training pairs exactly.

![1d_scale_dp_34](figures/1d_scale_dp_34.png)

| pair | input | output |
|---|---|---|
| train 0 | `......6666..1..` | `......6666661..` |
| train 1 | `.222..1........` | `.222221........` |
| train 2 | `.88888...1.....` | `.888888881.....` |
| **test** | `..88888.....1..` | `..88888888881..` |
| predicted | | `..88888888881..` |

### Failed: `1d_mirror_36`

`paint(f1b(x), scan(x))`, DL 168.1 = 10.0 structure + 102.6 parameters + 55.5 data bits, does not fit its training pairs exactly.

![1d_mirror_36](figures/1d_mirror_36.png)

| pair | input | output |
|---|---|---|
| train 0 | `......4444444..9..........` | `...............9..4444444.` |
| train 1 | `..7777777..9..............` | `...........9..7777777.....` |
| train 2 | `666666....9...............` | `..........9....666666.....` |
| **test** | `.666666...9...............` | `..........9...666666......` |
| predicted | | `..........9...............` |

### Failed: `1d_pcopy_1c_6`

`paint(x, local(x))`, DL 74.9 = 5.4 structure + 69.0 parameters + 0.5 data bits, fits its training pairs exactly.

![1d_pcopy_1c_6](figures/1d_pcopy_1c_6.png)

| pair | input | output |
|---|---|---|
| train 0 | `.999....9...9.....9..............` | `.999...999.999...999.............` |
| train 1 | `..999...9...9....9...............` | `..999..999.999..999..............` |
| train 2 | `.777..7.....7....................` | `.777.777...777...................` |
| **test** | `.555..5.....5....5...............` | `.555.555...555..555..............` |
| predicted | | `.555..55...555..555..............` |

### Failed: `1d_recolor_oe_34`

`paint(paint(x, local(x)), segment(x))`, DL 92.0 = 10.2 structure + 81.3 parameters + 0.6 data bits, fits its training pairs exactly.

![1d_recolor_oe_34](figures/1d_recolor_oe_34.png)

| pair | input | output |
|---|---|---|
| train 0 | `.333333.333..33...3..33......` | `.111111.555..11...5..11......` |
| train 1 | `.333333..333.3.3..33.........` | `.111111..555.5.5..11.........` |
| train 2 | `...3333.333..3.3333...3......` | `...1111.555..5.1111...5......` |
| **test** | `...33..33333..33333...3......` | `...11..55555..55555...5......` |
| predicted | | `...11..11111..11111...5......` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_0 | `f1a(x)` | 9.0 | ✓ |
| 1d_denoising_1c_1 | `f1a(x)` | 14.1 | ✓ |
| 1d_denoising_1c_10 | `paint(shift(x), local(x))` | 35.9 | ✓ |
| 1d_denoising_1c_11 | `f1a(x)` | 19.9 | ✓ |
| 1d_denoising_1c_12 | `paint(x, local(x))` | 37.7 | ✓ |
| 1d_denoising_1c_13 | `f1a(x)` | 18.4 | ✓ |
| 1d_denoising_1c_14 | `paint(x, local(paint(x, scan(x))))` | 45.1 | ✗ |
| 1d_denoising_1c_15 | `f1a(x)` | 14.1 | ✓ |
| 1d_denoising_1c_16 | `f1a(x)` | 12.4 | ✓ |
| 1d_denoising_1c_17 | `f1a(x)` | 10.3 | ✓ |
| 1d_denoising_1c_18 | `f1a(x)` | 11.1 | ✓ |
| 1d_denoising_1c_19 | `paint(shift(x), local(x))` | 39.1 | ✓ |
| 1d_denoising_1c_2 | `f1a(x)` | 9.1 | ✓ |
| 1d_denoising_1c_20 | `f1a(x)` | 20.3 | ✓ |
| 1d_denoising_1c_21 | `f1a(x)` | 27.2 | ✓ |
| 1d_denoising_1c_22 | `f1a(x)` | 9.4 | ✓ |
| 1d_denoising_1c_23 | `f1a(x)` | 11.3 | ✓ |
| 1d_denoising_1c_24 | `f1a(x)` | 9.6 | ✓ |
| 1d_denoising_1c_25 | `f1a(x)` | 9.1 | ✓ |
| 1d_denoising_1c_26 | `f1a(x)` | 10.0 | ✓ |
| 1d_denoising_1c_27 | `f1a(x)` | 27.0 | ✓ |
| 1d_denoising_1c_28 | `paint(shift(x), local(x))` | 33.7 | ✓ |
| 1d_denoising_1c_29 | `f1a(x)` | 9.3 | ✓ |
| 1d_denoising_1c_3 | `f1a(x)` | 20.6 | ✓ |
| 1d_denoising_1c_30 | `f1a(x)` | 16.8 | ✓ |
| 1d_denoising_1c_31 | `f1b(paint(x, segment(x)))` | 39.6 | ✓ |
| 1d_denoising_1c_32 | `f1a(x)` | 12.0 | ✓ |
| 1d_denoising_1c_33 | `f1a(x)` | 18.9 | ✓ |
| 1d_denoising_1c_34 | `f1a(x)` | 18.8 | ✓ |
| 1d_denoising_1c_35 | `f1a(x)` | 9.6 | ✓ |
| 1d_denoising_1c_36 | `f1a(x)` | 24.8 | ✓ |
| 1d_denoising_1c_37 | `f1a(x)` | 20.2 | ✓ |
| 1d_denoising_1c_38 | `f1a(x)` | 14.2 | ✓ |
| 1d_denoising_1c_39 | `f1a(x)` | 13.9 | ✓ |
| 1d_denoising_1c_4 | `f1a(x)` | 18.5 | ✓ |
| 1d_denoising_1c_40 | `f1a(x)` | 18.8 | ✓ |
| 1d_denoising_1c_41 | `paint(x, local(paint(x, scan(x))))` | 39.7 | ✓ |
| 1d_denoising_1c_42 | `f1a(x)` | 20.1 | ✓ |
| 1d_denoising_1c_43 | `f1a(x)` | 17.6 | ✓ |
| 1d_denoising_1c_44 | `f1a(x)` | 10.1 | ✓ |
| 1d_denoising_1c_45 | `paint(f1b(x), segment(x))` | 43.3 | ✓ |
| 1d_denoising_1c_46 | `f1a(x)` | 9.7 | ✓ |
| 1d_denoising_1c_47 | `f1a(x)` | 13.9 | ✓ |
| 1d_denoising_1c_48 | `f1a(x)` | 9.8 | ✓ |
| 1d_denoising_1c_49 | `f1a(x)` | 15.1 | ✓ |
| 1d_denoising_1c_5 | `f1a(x)` | 8.6 | ✓ |
| 1d_denoising_1c_6 | `f1a(x)` | 13.8 | ✓ |
| 1d_denoising_1c_7 | `f1a(x)` | 9.6 | ✓ |
| 1d_denoising_1c_8 | `f1a(x)` | 10.0 | ✓ |
| 1d_denoising_1c_9 | `f1a(x)` | 12.0 | ✓ |
| 1d_denoising_mc_0 | `paint(paint(shift(x), local(x)), local(x))` | 22.7 | ✓ |
| 1d_denoising_mc_1 | `paint(paint(shift(x), local(x)), scan(x))` | 40.6 | ✓ |
| 1d_denoising_mc_10 | `paint(shift(x), local(x))` | 31.7 | ✓ |
| 1d_denoising_mc_11 | `paint(shift(x), local(x))` | 34.4 | ✓ |
| 1d_denoising_mc_12 | `paint(shift(x), local(x))` | 31.1 | ✓ |
| 1d_denoising_mc_13 | `paint(shift(x), local(x))` | 45.3 | ✓ |
| 1d_denoising_mc_14 | `paint(shift(x), local(x))` | 27.5 | ✓ |
| 1d_denoising_mc_15 | `paint(shift(x), local(x))` | 22.9 | ✓ |
| 1d_denoising_mc_16 | `paint(shift(x), local(x))` | 27.2 | ✓ |
| 1d_denoising_mc_17 | `paint(paint(shift(x), local(x)), scan(x))` | 21.1 | ✓ |
| 1d_denoising_mc_18 | `paint(shift(x), local(x))` | 36.0 | ✓ |
| 1d_denoising_mc_19 | `paint(shift(x), local(x))` | 27.8 | ✓ |
| 1d_denoising_mc_2 | `paint(shift(x), local(x))` | 26.0 | ✓ |
| 1d_denoising_mc_20 | `paint(paint(shift(x), local(x)), scan(x))` | 33.5 | ✓ |
| 1d_denoising_mc_21 | `paint(shift(x), local(x))` | 33.6 | ✓ |
| 1d_denoising_mc_22 | `paint(paint(shift(x), local(x)), scan(x))` | 46.8 | ✓ |
| 1d_denoising_mc_23 | `paint(shift(x), scan(x))` | 33.8 | ✓ |
| 1d_denoising_mc_24 | `f1a(shift(x))` | 34.7 | ✓ |
| 1d_denoising_mc_25 | `paint(shift(x), scan(x))` | 35.4 | ✓ |
| 1d_denoising_mc_26 | `paint(shift(x), local(shift(x)))` | 49.4 | ✓ |
| 1d_denoising_mc_27 | `paint(shift(x), local(x))` | 41.8 | ✓ |
| 1d_denoising_mc_28 | `paint(paint(shift(x), scan(x)), local(x))` | 21.5 | ✓ |
| 1d_denoising_mc_29 | `paint(paint(shift(x), local(x)), scan(x))` | 15.4 | ✓ |
| 1d_denoising_mc_3 | `paint(paint(shift(x), local(x)), local(x))` | 30.3 | ✓ |
| 1d_denoising_mc_30 | `paint(paint(shift(x), scan(x)), scan(x))` | 41.9 | ✓ |
| 1d_denoising_mc_31 | `paint(paint(shift(x), local(x)), scan(x))` | 28.7 | ✓ |
| 1d_denoising_mc_32 | `paint(paint(shift(x), local(x)), scan(x))` | 27.0 | ✓ |
| 1d_denoising_mc_33 | `paint(paint(shift(x), local(x)), local(x))` | 33.3 | ✗ |
| 1d_denoising_mc_34 | `paint(shift(x), local(x))` | 49.6 | ✓ |
| 1d_denoising_mc_35 | `paint(shift(x), local(x))` | 34.5 | ✓ |
| 1d_denoising_mc_36 | `paint(shift(x), local(x))` | 38.8 | ✓ |
| 1d_denoising_mc_37 | `paint(shift(x), local(x))` | 36.1 | ✓ |
| 1d_denoising_mc_38 | `paint(shift(x), local(x))` | 26.6 | ✓ |
| 1d_denoising_mc_39 | `paint(shift(x), local(x))` | 32.9 | ✓ |
| 1d_denoising_mc_4 | `paint(paint(shift(x), local(x)), scan(x))` | 31.8 | ✗ |
| 1d_denoising_mc_40 | `paint(paint(shift(x), local(x)), scan(x))` | 15.3 | ✓ |
| 1d_denoising_mc_41 | `paint(paint(shift(x), local(x)), local(x))` | 20.0 | ✓ |
| 1d_denoising_mc_42 | `paint(shift(x), local(x))` | 34.4 | ✓ |
| 1d_denoising_mc_43 | `paint(shift(x), local(x))` | 28.2 | ✓ |
| 1d_denoising_mc_44 | `paint(paint(x, local(x)), scan(shift(x)))` | 48.2 | ✗ |
| 1d_denoising_mc_45 | `paint(paint(shift(x), scan(x)), scan(x))` | 32.6 | ✓ |
| 1d_denoising_mc_46 | `paint(paint(shift(x), local(x)), scan(x))` | 14.7 | ✓ |
| 1d_denoising_mc_47 | `paint(shift(x), local(x))` | 37.4 | ✓ |
| 1d_denoising_mc_48 | `paint(paint(shift(x), local(x)), scan(x))` | 28.3 | ✓ |
| 1d_denoising_mc_49 | `paint(shift(x), local(x))` | 34.8 | ✓ |
| 1d_denoising_mc_5 | `paint(paint(shift(x), local(x)), scan(x))` | 20.5 | ✓ |
| 1d_denoising_mc_6 | `paint(shift(x), local(x))` | 33.2 | ✓ |
| 1d_denoising_mc_7 | `paint(shift(x), local(x))` | 33.3 | ✓ |
| 1d_denoising_mc_8 | `paint(shift(x), local(x))` | 51.4 | ✓ |
| 1d_denoising_mc_9 | `paint(f1b(shift(x)), local(x))` | 37.3 | ✓ |
| 1d_fill_0 | `paint(f1b(x), local(shift(x)))` | 68.5 | ✓ |
| 1d_fill_1 | `paint(x, scan(paint(x, segment(x))))` | 70.7 | ✓ |
| 1d_fill_10 | `paint(f1b(x), scan(shift(x)))` | 48.4 | ✓ |
| 1d_fill_11 | `f1b(paint(x, segment(x)))` | 46.9 | ✓ |
| 1d_fill_12 | `f1b(f1b(x))` | 69.9 | ✓ |
| 1d_fill_13 | `paint(paint(x, scan(x)), scan(shift(x)))` | 52.0 | ✓ |
| 1d_fill_14 | `paint(paint(x, scan(x)), local(shift(x)))` | 63.3 | ✓ |
| 1d_fill_15 | `paint(x, scan(paint(x, local(shift(x)))))` | 65.9 | ✓ |
| 1d_fill_16 | `paint(f1b(x), local(x))` | 47.3 | ✓ |
| 1d_fill_17 | `paint(f1b(x), segment(x))` | 51.2 | ✓ |
| 1d_fill_18 | `f0b(x)` | 61.2 | ✓ |
| 1d_fill_19 | `paint(x, scan(paint(x, segment(x))))` | 62.4 | ✓ |
| 1d_fill_2 | `paint(f1b(x), local(x))` | 60.0 | ✗ |
| 1d_fill_20 | `paint(paint(x, scan(x)), scan(shift(x)))` | 45.6 | ✓ |
| 1d_fill_21 | `paint(paint(x, local(x)), scan(x))` | 50.3 | ✓ |
| 1d_fill_22 | `f1b(paint(x, local(x)))` | 46.6 | ✓ |
| 1d_fill_23 | `paint(f1b(x), segment(x))` | 62.6 | ✓ |
| 1d_fill_24 | `slide(paint(x, scan(x)))` | 70.9 | ✓ |
| 1d_fill_25 | `paint(x, scan(shift(paint(x, local(x)))))` | 51.3 | ✗ |
| 1d_fill_26 | `paint(paint(x, scan(x)), local(shift(x)))` | 67.8 | ✓ |
| 1d_fill_27 | `paint(paint(shift(x), scan(x)), scan(x))` | 59.6 | ✓ |
| 1d_fill_28 | `paint(paint(x, scan(x)), segment(x))` | 43.7 | ✓ |
| 1d_fill_29 | `paint(x, scan(paint(x, local(shift(x)))))` | 56.1 | ✓ |
| 1d_fill_3 | `paint(f1b(x), scan(shift(x)))` | 39.8 | ✓ |
| 1d_fill_30 | `f0b(x)` | 60.9 | ✓ |
| 1d_fill_31 | `paint(paint(shift(x), scan(x)), local(x))` | 50.8 | ✓ |
| 1d_fill_32 | `f0b(x)` | 52.3 | ✓ |
| 1d_fill_33 | `paint(f1b(x), scan(x))` | 40.8 | ✓ |
| 1d_fill_34 | `paint(shift(f1b(x)), local(x))` | 68.9 | ✓ |
| 1d_fill_35 | `f0b(x)` | 52.2 | ✓ |
| 1d_fill_36 | `paint(x, scan(paint(x, segment(x))))` | 61.2 | ✓ |
| 1d_fill_37 | `paint(paint(x, scan(x)), scan(shift(x)))` | 56.2 | ✓ |
| 1d_fill_38 | `f0b(x)` | 64.3 | ✓ |
| 1d_fill_39 | `paint(f1b(x), local(x))` | 67.0 | ✓ |
| 1d_fill_4 | `paint(f1b(x), scan(shift(x)))` | 53.7 | ✓ |
| 1d_fill_40 | `paint(x, local(paint(x, scan(x))))` | 64.9 | ✓ |
| 1d_fill_41 | `f0b(x)` | 59.5 | ✓ |
| 1d_fill_42 | `paint(paint(x, local(x)), scan(x))` | 47.1 | ✓ |
| 1d_fill_43 | `paint(x, scan(f1b(x)))` | 39.2 | ✓ |
| 1d_fill_44 | `paint(x, local(paint(shift(x), scan(x))))` | 50.0 | ✓ |
| 1d_fill_45 | `paint(f1b(x), local(shift(x)))` | 43.8 | ✓ |
| 1d_fill_46 | `paint(x, scan(paint(x, local(shift(x)))))` | 46.9 | ✓ |
| 1d_fill_47 | `paint(x, local(paint(shift(x), scan(x))))` | 40.6 | ✓ |
| 1d_fill_48 | `f1b(paint(x, scan(x)))` | 62.5 | ✓ |
| 1d_fill_49 | `paint(paint(shift(x), scan(x)), local(x))` | 62.8 | ✓ |
| 1d_fill_5 | `f1b(paint(x, scan(x)))` | 56.8 | ✓ |
| 1d_fill_6 | `f0b(x)` | 57.7 | ✓ |
| 1d_fill_7 | `paint(f1b(x), scan(shift(x)))` | 40.0 | ✓ |
| 1d_fill_8 | `paint(paint(x, scan(x)), local(shift(x)))` | 49.2 | ✓ |
| 1d_fill_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 44.9 | ✓ |
| 1d_flip_0 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_1 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_10 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_11 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_12 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_13 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_14 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_15 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_16 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_17 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_18 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_19 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_2 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_20 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_21 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_22 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_23 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_24 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_25 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_26 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_27 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_28 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_29 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_3 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_30 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_31 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_32 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_33 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_34 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_35 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_36 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_37 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_38 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_39 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_4 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_40 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_41 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_42 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_43 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_44 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_45 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_46 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_47 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_48 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_49 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_5 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_6 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_7 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_8 | `reverse(x)` | 5.8 | ✓ |
| 1d_flip_9 | `reverse(x)` | 5.8 | ✓ |
| 1d_hollow_0 | `paint(reverse(x), scan(x))` | 64.7 | ✓ |
| 1d_hollow_1 | `paint(f1b(x), local(x))` | 44.2 | ✓ |
| 1d_hollow_10 | `paint(paint(x, segment(x)), scan(x))` | 50.3 | ✓ |
| 1d_hollow_11 | `paint(reverse(x), scan(x))` | 59.4 | ✓ |
| 1d_hollow_12 | `paint(reverse(x), scan(x))` | 57.7 | ✓ |
| 1d_hollow_13 | `f1b(reverse(x))` | 54.8 | ✓ |
| 1d_hollow_14 | `paint(paint(shift(x), local(x)), scan(x))` | 57.0 | ✓ |
| 1d_hollow_15 | `paint(paint(x, segment(x)), segment(x))` | 54.6 | ✓ |
| 1d_hollow_16 | `paint(paint(x, segment(x)), segment(x))` | 55.8 | ✓ |
| 1d_hollow_17 | `paint(reverse(x), scan(x))` | 66.7 | ✓ |
| 1d_hollow_18 | `paint(f1b(shift(x)), local(x))` | 39.9 | ✓ |
| 1d_hollow_19 | `paint(x, scan(reverse(x)))` | 68.2 | ✓ |
| 1d_hollow_2 | `f1b(paint(x, segment(x)))` | 66.9 | ✓ |
| 1d_hollow_20 | `paint(f1b(shift(x)), local(x))` | 43.8 | ✓ |
| 1d_hollow_21 | `paint(x, scan(paint(x, segment(x))))` | 41.2 | ✓ |
| 1d_hollow_22 | `paint(paint(x, segment(x)), scan(x))` | 61.2 | ✓ |
| 1d_hollow_23 | `paint(reverse(x), scan(x))` | 60.5 | ✓ |
| 1d_hollow_24 | `paint(reverse(x), scan(x))` | 63.6 | ✓ |
| 1d_hollow_25 | `f1b(paint(x, scan(x)))` | 54.8 | ✓ |
| 1d_hollow_26 | `paint(paint(x, scan(shift(x))), local(x))` | 47.3 | ✓ |
| 1d_hollow_27 | `paint(reverse(x), scan(x))` | 49.9 | ✓ |
| 1d_hollow_28 | `paint(x, scan(reverse(x)))` | 58.8 | ✓ |
| 1d_hollow_29 | `f1a(x)` | 48.1 | ✓ |
| 1d_hollow_3 | `f1b(paint(x, scan(x)))` | 35.9 | ✓ |
| 1d_hollow_30 | `paint(paint(shift(x), local(x)), scan(x))` | 55.6 | ✓ |
| 1d_hollow_31 | `paint(paint(x, local(x)), segment(x))` | 65.5 | ✓ |
| 1d_hollow_32 | `paint(f1b(x), scan(x))` | 55.5 | ✓ |
| 1d_hollow_33 | `paint(paint(shift(x), local(x)), scan(x))` | 56.4 | ✓ |
| 1d_hollow_34 | `paint(paint(shift(x), scan(x)), local(x))` | 37.1 | ✓ |
| 1d_hollow_35 | `paint(paint(x, scan(shift(x))), local(x))` | 51.7 | ✓ |
| 1d_hollow_36 | `paint(paint(x, segment(x)), local(x))` | 55.2 | ✓ |
| 1d_hollow_37 | `f1a(x)` | 37.0 | ✓ |
| 1d_hollow_38 | `f1a(x)` | 42.6 | ✓ |
| 1d_hollow_39 | `paint(paint(x, segment(x)), local(x))` | 52.9 | ✓ |
| 1d_hollow_4 | `paint(paint(x, scan(x)), local(shift(x)))` | 51.2 | ✓ |
| 1d_hollow_40 | `paint(paint(shift(x), local(x)), scan(x))` | 54.6 | ✓ |
| 1d_hollow_41 | `f1b(paint(x, local(x)))` | 53.2 | ✓ |
| 1d_hollow_42 | `paint(paint(x, segment(x)), local(x))` | 55.5 | ✓ |
| 1d_hollow_43 | `paint(paint(shift(x), local(x)), scan(x))` | 57.6 | ✓ |
| 1d_hollow_44 | `paint(x, scan(f1b(x)))` | 60.0 | ✓ |
| 1d_hollow_45 | `paint(paint(shift(x), local(x)), scan(x))` | 56.2 | ✓ |
| 1d_hollow_46 | `paint(reverse(x), scan(x))` | 62.6 | ✓ |
| 1d_hollow_47 | `paint(x, scan(reverse(x)))` | 45.3 | ✓ |
| 1d_hollow_48 | `paint(paint(x, local(x)), segment(x))` | 47.7 | ✓ |
| 1d_hollow_49 | `f1b(paint(x, scan(x)))` | 49.6 | ✓ |
| 1d_hollow_5 | `f1a(x)` | 34.0 | ✓ |
| 1d_hollow_6 | `paint(paint(x, scan(x)), local(x))` | 62.1 | ✓ |
| 1d_hollow_7 | `f1b(paint(x, scan(x)))` | 62.3 | ✓ |
| 1d_hollow_8 | `paint(paint(x, local(shift(x))), local(x))` | 51.9 | ✓ |
| 1d_hollow_9 | `f1a(x)` | 47.3 | ✓ |
| 1d_mirror_0 | `paint(paint(x, scan(x)), segment(x))` | 180.7 | ✗ |
| 1d_mirror_1 | `paint(paint(x, scan(x)), scan(shift(x)))` | 138.9 | ✗ |
| 1d_mirror_10 | `paint(paint(x, scan(x)), segment(x))` | 155.1 | ✗ |
| 1d_mirror_11 | `paint(paint(x, scan(x)), segment(x))` | 178.8 | ✗ |
| 1d_mirror_12 | `paint(paint(x, scan(x)), segment(x))` | 133.3 | ✗ |
| 1d_mirror_13 | `paint(f1b(x), scan(x))` | 164.6 | ✗ |
| 1d_mirror_14 | `paint(x, scan(paint(shift(x), local(x))))` | 129.8 | ✗ |
| 1d_mirror_15 | `f1b(paint(x, scan(x)))` | 155.4 | ✗ |
| 1d_mirror_16 | `reverse(paint(x, local(x)))` | 167.9 | ✗ |
| 1d_mirror_17 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_18 | `paint(f1b(x), scan(x))` | 138.2 | ✗ |
| 1d_mirror_19 | `paint(f1b(x), segment(x))` | 174.9 | ✗ |
| 1d_mirror_2 | `paint(f1b(x), segment(x))` | 113.3 | ✗ |
| 1d_mirror_20 | `paint(f1b(x), scan(shift(x)))` | 124.0 | ✗ |
| 1d_mirror_21 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_22 | `paint(paint(x, scan(x)), scan(x))` | 142.8 | ✗ |
| 1d_mirror_23 | `paint(paint(x, scan(x)), scan(x))` | 142.7 | ✗ |
| 1d_mirror_24 | `paint(paint(x, scan(x)), segment(x))` | 146.1 | ✗ |
| 1d_mirror_25 | `paint(paint(x, scan(x)), scan(x))` | 173.1 | ✗ |
| 1d_mirror_26 | `paint(paint(x, scan(x)), segment(x))` | 132.0 | ✗ |
| 1d_mirror_27 | `f1a(x)` | 144.7 | ✗ |
| 1d_mirror_28 | `paint(paint(x, scan(x)), scan(x))` | 158.4 | ✗ |
| 1d_mirror_29 | `paint(f1b(x), scan(x))` | 129.5 | ✗ |
| 1d_mirror_3 | `paint(paint(x, scan(x)), segment(x))` | 138.1 | ✗ |
| 1d_mirror_30 | `paint(paint(x, scan(x)), scan(x))` | 159.3 | ✗ |
| 1d_mirror_31 | `f1b(x)` | 131.4 | ✗ |
| 1d_mirror_32 | `paint(paint(x, scan(x)), scan(x))` | 170.0 | ✗ |
| 1d_mirror_33 | `paint(f1b(x), scan(x))` | 172.0 | ✗ |
| 1d_mirror_34 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_35 | `paint(shift(paint(x, local(x))), scan(x))` | 167.1 | ✗ |
| 1d_mirror_36 | `paint(f1b(x), scan(x))` | 168.1 | ✗ |
| 1d_mirror_37 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_38 | `paint(f1b(x), scan(x))` | 177.5 | ✗ |
| 1d_mirror_39 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_4 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_40 | `paint(paint(x, scan(x)), segment(x))` | 136.8 | ✗ |
| 1d_mirror_41 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_42 | `f1b(paint(x, local(x)))` | 143.4 | ✗ |
| 1d_mirror_43 | `paint(paint(x, scan(x)), segment(x))` | 131.9 | ✗ |
| 1d_mirror_44 | `paint(f1b(x), scan(x))` | 127.7 | ✗ |
| 1d_mirror_45 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_46 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_47 | `paint(paint(x, scan(x)), segment(x))` | 123.8 | ✗ |
| 1d_mirror_48 | `f1b(reverse(x))` | 145.0 | ✗ |
| 1d_mirror_49 | `paint(f1b(x), segment(x))` | 147.1 | ✗ |
| 1d_mirror_5 | `paint(paint(x, scan(shift(x))), scan(x))` | 170.9 | ✗ |
| 1d_mirror_6 | `paint(paint(x, scan(x)), segment(x))` | 162.8 | ✗ |
| 1d_mirror_7 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_8 | `pivot(x)` | 7.0 | ✓ |
| 1d_mirror_9 | `pivot(x)` | 7.0 | ✓ |
| 1d_move_1p_0 | `paint(shift(paint(x, local(x))), scan(x))` | 52.7 | ✓ |
| 1d_move_1p_1 | `shift(x)` | 49.9 | ✓ |
| 1d_move_1p_10 | `shift(x)` | 50.5 | ✓ |
| 1d_move_1p_11 | `shift(x)` | 50.5 | ✓ |
| 1d_move_1p_12 | `paint(paint(shift(x), scan(x)), local(x))` | 43.4 | ✓ |
| 1d_move_1p_13 | `paint(shift(x), local(x))` | 50.4 | ✓ |
| 1d_move_1p_14 | `shift(x)` | 52.3 | ✓ |
| 1d_move_1p_15 | `shift(x)` | 54.7 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 51.8 | ✓ |
| 1d_move_1p_17 | `paint(shift(x), local(x))` | 53.1 | ✓ |
| 1d_move_1p_18 | `paint(shift(x), scan(shift(x)))` | 52.5 | ✓ |
| 1d_move_1p_19 | `shift(x)` | 54.3 | ✓ |
| 1d_move_1p_2 | `shift(x)` | 49.3 | ✓ |
| 1d_move_1p_20 | `shift(x)` | 51.9 | ✓ |
| 1d_move_1p_21 | `paint(shift(x), scan(shift(x)))` | 52.0 | ✓ |
| 1d_move_1p_22 | `paint(paint(shift(x), scan(x)), local(x))` | 49.8 | ✓ |
| 1d_move_1p_23 | `paint(shift(x), local(x))` | 49.2 | ✓ |
| 1d_move_1p_24 | `paint(paint(shift(x), local(x)), scan(x))` | 32.8 | ✓ |
| 1d_move_1p_25 | `paint(shift(paint(x, scan(x))), local(x))` | 44.9 | ✓ |
| 1d_move_1p_26 | `shift(x)` | 49.3 | ✓ |
| 1d_move_1p_27 | `shift(x)` | 56.5 | ✓ |
| 1d_move_1p_28 | `paint(shift(shift(x)), scan(x))` | 52.7 | ✓ |
| 1d_move_1p_29 | `paint(shift(paint(x, scan(x))), local(x))` | 48.7 | ✓ |
| 1d_move_1p_3 | `paint(shift(shift(x)), local(x))` | 46.6 | ✓ |
| 1d_move_1p_30 | `shift(x)` | 54.1 | ✓ |
| 1d_move_1p_31 | `f1a(shift(x))` | 28.9 | ✓ |
| 1d_move_1p_32 | `shift(x)` | 53.7 | ✓ |
| 1d_move_1p_33 | `shift(x)` | 49.8 | ✓ |
| 1d_move_1p_34 | `shift(x)` | 53.0 | ✓ |
| 1d_move_1p_35 | `shift(x)` | 49.7 | ✓ |
| 1d_move_1p_36 | `shift(x)` | 53.6 | ✓ |
| 1d_move_1p_37 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_38 | `shift(x)` | 54.3 | ✓ |
| 1d_move_1p_39 | `shift(x)` | 55.8 | ✓ |
| 1d_move_1p_4 | `shift(x)` | 50.0 | ✓ |
| 1d_move_1p_40 | `paint(shift(x), local(x))` | 49.2 | ✓ |
| 1d_move_1p_41 | `shift(x)` | 52.2 | ✓ |
| 1d_move_1p_42 | `paint(paint(shift(x), local(x)), scan(x))` | 34.9 | ✓ |
| 1d_move_1p_43 | `paint(shift(paint(x, scan(x))), local(x))` | 47.8 | ✓ |
| 1d_move_1p_44 | `f1a(shift(x))` | 36.0 | ✓ |
| 1d_move_1p_45 | `shift(x)` | 52.8 | ✓ |
| 1d_move_1p_46 | `paint(paint(shift(x), scan(x)), local(x))` | 51.3 | ✓ |
| 1d_move_1p_47 | `shift(x)` | 52.3 | ✓ |
| 1d_move_1p_48 | `shift(x)` | 53.4 | ✓ |
| 1d_move_1p_49 | `paint(shift(shift(x)), local(x))` | 48.5 | ✓ |
| 1d_move_1p_5 | `paint(shift(x), local(x))` | 47.2 | ✓ |
| 1d_move_1p_6 | `paint(shift(shift(x)), scan(x))` | 50.8 | ✓ |
| 1d_move_1p_7 | `f1a(shift(x))` | 41.1 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 54.4 | ✓ |
| 1d_move_1p_9 | `shift(x)` | 49.0 | ✓ |
| 1d_move_2p_0 | `paint(shift(x), local(x))` | 39.6 | ✓ |
| 1d_move_2p_1 | `paint(shift(x), local(x))` | 42.2 | ✓ |
| 1d_move_2p_10 | `paint(shift(x), local(x))` | 45.3 | ✓ |
| 1d_move_2p_11 | `shift(x)` | 47.1 | ✓ |
| 1d_move_2p_12 | `shift(x)` | 47.3 | ✓ |
| 1d_move_2p_13 | `shift(x)` | 48.0 | ✓ |
| 1d_move_2p_14 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_15 | `shift(x)` | 48.7 | ✓ |
| 1d_move_2p_16 | `paint(shift(x), local(x))` | 34.9 | ✓ |
| 1d_move_2p_17 | `paint(shift(x), local(x))` | 36.4 | ✓ |
| 1d_move_2p_18 | `paint(shift(x), local(x))` | 40.4 | ✓ |
| 1d_move_2p_19 | `paint(shift(x), local(x))` | 40.3 | ✓ |
| 1d_move_2p_2 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_20 | `paint(shift(x), local(x))` | 44.2 | ✓ |
| 1d_move_2p_21 | `paint(shift(x), local(x))` | 41.4 | ✓ |
| 1d_move_2p_22 | `paint(shift(x), local(x))` | 41.0 | ✓ |
| 1d_move_2p_23 | `paint(shift(x), local(x))` | 40.3 | ✓ |
| 1d_move_2p_24 | `shift(x)` | 46.2 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 48.5 | ✓ |
| 1d_move_2p_26 | `paint(shift(x), local(x))` | 37.7 | ✓ |
| 1d_move_2p_27 | `shift(x)` | 49.4 | ✓ |
| 1d_move_2p_28 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_29 | `paint(shift(x), local(x))` | 41.6 | ✓ |
| 1d_move_2p_3 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_30 | `shift(x)` | 48.7 | ✓ |
| 1d_move_2p_31 | `shift(x)` | 48.8 | ✓ |
| 1d_move_2p_32 | `paint(shift(x), local(x))` | 37.0 | ✓ |
| 1d_move_2p_33 | `paint(shift(x), local(x))` | 43.1 | ✓ |
| 1d_move_2p_34 | `shift(x)` | 48.1 | ✓ |
| 1d_move_2p_35 | `shift(x)` | 46.7 | ✓ |
| 1d_move_2p_36 | `paint(shift(x), local(x))` | 37.6 | ✓ |
| 1d_move_2p_37 | `shift(x)` | 48.6 | ✓ |
| 1d_move_2p_38 | `paint(shift(x), local(x))` | 44.4 | ✓ |
| 1d_move_2p_39 | `shift(x)` | 49.3 | ✓ |
| 1d_move_2p_4 | `shift(x)` | 46.6 | ✓ |
| 1d_move_2p_40 | `paint(shift(x), local(paint(x, scan(x))))` | 44.4 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_42 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_43 | `paint(shift(x), local(x))` | 38.7 | ✓ |
| 1d_move_2p_44 | `f0a(x)` | 53.2 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_46 | `shift(x)` | 48.9 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.7 | ✓ |
| 1d_move_2p_48 | `paint(shift(x), local(x))` | 37.8 | ✓ |
| 1d_move_2p_49 | `paint(shift(x), local(x))` | 42.2 | ✓ |
| 1d_move_2p_5 | `f1b(paint(shift(x), local(x)))` | 44.6 | ✓ |
| 1d_move_2p_6 | `paint(shift(x), local(x))` | 47.2 | ✓ |
| 1d_move_2p_7 | `shift(x)` | 53.5 | ✓ |
| 1d_move_2p_8 | `paint(shift(x), local(x))` | 44.5 | ✓ |
| 1d_move_2p_9 | `paint(shift(x), local(x))` | 43.7 | ✓ |
| 1d_move_2p_dp_0 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_1 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_10 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_11 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_12 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_13 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_14 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_15 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_16 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_17 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_18 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_19 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_2 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_20 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_21 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_22 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_23 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_24 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_25 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_26 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_27 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_28 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_29 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_3 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_30 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_31 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_32 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_33 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_34 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_35 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_36 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_37 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_38 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_39 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_4 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_40 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_41 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_42 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_43 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_44 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_45 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_46 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_47 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_48 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_49 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_5 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_6 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_7 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_8 | `slide(x)` | 6.0 | ✓ |
| 1d_move_2p_dp_9 | `slide(x)` | 6.0 | ✓ |
| 1d_move_3p_0 | `paint(shift(x), local(x))` | 52.2 | ✓ |
| 1d_move_3p_1 | `paint(shift(x), local(x))` | 48.7 | ✓ |
| 1d_move_3p_10 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_11 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_12 | `paint(paint(x, local(x)), scan(x))` | 38.8 | ✓ |
| 1d_move_3p_13 | `shift(x)` | 54.7 | ✓ |
| 1d_move_3p_14 | `shift(x)` | 54.7 | ✓ |
| 1d_move_3p_15 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_16 | `paint(shift(x), local(x))` | 43.9 | ✓ |
| 1d_move_3p_17 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_18 | `paint(shift(x), local(x))` | 38.9 | ✓ |
| 1d_move_3p_19 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_2 | `paint(shift(x), local(x))` | 45.8 | ✓ |
| 1d_move_3p_20 | `shift(x)` | 54.7 | ✓ |
| 1d_move_3p_21 | `f0a(x)` | 45.8 | ✓ |
| 1d_move_3p_22 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_23 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_24 | `paint(shift(x), local(x))` | 47.7 | ✓ |
| 1d_move_3p_25 | `shift(x)` | 54.6 | ✓ |
| 1d_move_3p_26 | `paint(shift(x), local(x))` | 36.2 | ✓ |
| 1d_move_3p_27 | `paint(shift(x), local(x))` | 33.8 | ✓ |
| 1d_move_3p_28 | `paint(shift(x), local(x))` | 32.9 | ✓ |
| 1d_move_3p_29 | `paint(shift(x), local(x))` | 43.1 | ✓ |
| 1d_move_3p_3 | `paint(paint(x, local(x)), scan(x))` | 45.9 | ✓ |
| 1d_move_3p_30 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_31 | `shift(x)` | 54.5 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 54.0 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 53.3 | ✓ |
| 1d_move_3p_35 | `paint(shift(x), local(x))` | 38.3 | ✓ |
| 1d_move_3p_36 | `paint(shift(x), local(x))` | 34.0 | ✓ |
| 1d_move_3p_37 | `paint(shift(x), local(x))` | 42.0 | ✓ |
| 1d_move_3p_38 | `shift(x)` | 53.5 | ✓ |
| 1d_move_3p_39 | `shift(x)` | 53.6 | ✓ |
| 1d_move_3p_4 | `paint(shift(x), local(x))` | 51.4 | ✓ |
| 1d_move_3p_40 | `paint(paint(x, local(x)), scan(x))` | 37.2 | ✓ |
| 1d_move_3p_41 | `paint(shift(x), local(x))` | 39.6 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_43 | `paint(shift(x), local(x))` | 46.3 | ✓ |
| 1d_move_3p_44 | `shift(x)` | 57.6 | ✓ |
| 1d_move_3p_45 | `shift(x)` | 53.4 | ✓ |
| 1d_move_3p_46 | `shift(x)` | 54.3 | ✓ |
| 1d_move_3p_47 | `paint(shift(x), local(x))` | 54.1 | ✓ |
| 1d_move_3p_48 | `paint(shift(x), local(x))` | 31.2 | ✓ |
| 1d_move_3p_49 | `paint(shift(x), local(x))` | 40.1 | ✓ |
| 1d_move_3p_5 | `shift(x)` | 55.0 | ✓ |
| 1d_move_3p_6 | `shift(x)` | 54.4 | ✓ |
| 1d_move_3p_7 | `shift(x)` | 57.3 | ✓ |
| 1d_move_3p_8 | `shift(x)` | 53.2 | ✓ |
| 1d_move_3p_9 | `paint(shift(x), local(x))` | 49.1 | ✓ |
| 1d_move_dp_0 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_1 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_10 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_11 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_12 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_13 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_14 | `paint(x, local(x))` | 54.1 | ✗ |
| 1d_move_dp_15 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_16 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_17 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_18 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_19 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_2 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_20 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_21 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_22 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_23 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_24 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_25 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_26 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_27 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_28 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_29 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_3 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_30 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_31 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_32 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_33 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_34 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_35 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_36 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_37 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_38 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_39 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_4 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_40 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_41 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_42 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_43 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_44 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_45 | `paint(x, local(x))` | 58.9 | ✗ |
| 1d_move_dp_46 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_47 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_48 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_49 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_5 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_6 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_7 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_8 | `slide(x)` | 6.0 | ✓ |
| 1d_move_dp_9 | `slide(x)` | 6.0 | ✓ |
| 1d_padded_fill_0 | `paint(paint(x, scan(x)), scan(shift(x)))` | 57.2 | ✓ |
| 1d_padded_fill_1 | `paint(paint(x, scan(x)), local(x))` | 39.3 | ✓ |
| 1d_padded_fill_10 | `f0b(x)` | 30.3 | ✓ |
| 1d_padded_fill_11 | `paint(paint(shift(x), scan(x)), local(x))` | 52.7 | ✓ |
| 1d_padded_fill_12 | `paint(paint(x, scan(x)), segment(x))` | 48.6 | ✓ |
| 1d_padded_fill_13 | `paint(f1b(x), scan(shift(x)))` | 46.4 | ✓ |
| 1d_padded_fill_14 | `paint(f1b(x), local(shift(x)))` | 27.6 | ✓ |
| 1d_padded_fill_15 | `paint(paint(x, scan(x)), segment(x))` | 52.8 | ✓ |
| 1d_padded_fill_16 | `paint(paint(x, scan(x)), segment(x))` | 52.5 | ✓ |
| 1d_padded_fill_17 | `paint(f1b(x), segment(x))` | 50.6 | ✓ |
| 1d_padded_fill_18 | `f0b(x)` | 37.3 | ✓ |
| 1d_padded_fill_19 | `paint(reverse(x), scan(x))` | 30.0 | ✓ |
| 1d_padded_fill_2 | `f0b(x)` | 45.4 | ✓ |
| 1d_padded_fill_20 | `paint(paint(x, scan(x)), segment(x))` | 48.2 | ✓ |
| 1d_padded_fill_21 | `paint(x, scan(f1b(x)))` | 38.0 | ✓ |
| 1d_padded_fill_22 | `f1b(paint(x, scan(x)))` | 47.0 | ✓ |
| 1d_padded_fill_23 | `paint(f1b(x), scan(shift(x)))` | 33.5 | ✓ |
| 1d_padded_fill_24 | `f0b(x)` | 26.6 | ✓ |
| 1d_padded_fill_25 | `paint(paint(x, scan(x)), segment(x))` | 38.5 | ✓ |
| 1d_padded_fill_26 | `f0b(x)` | 33.7 | ✓ |
| 1d_padded_fill_27 | `paint(reverse(x), scan(x))` | 51.6 | ✓ |
| 1d_padded_fill_28 | `paint(paint(x, scan(x)), segment(x))` | 43.0 | ✓ |
| 1d_padded_fill_29 | `paint(reverse(x), scan(x))` | 31.1 | ✓ |
| 1d_padded_fill_3 | `paint(paint(x, scan(x)), local(shift(x)))` | 54.2 | ✓ |
| 1d_padded_fill_30 | `f0b(x)` | 32.3 | ✓ |
| 1d_padded_fill_31 | `f0b(x)` | 46.4 | ✓ |
| 1d_padded_fill_32 | `f0b(x)` | 38.2 | ✓ |
| 1d_padded_fill_33 | `paint(x, scan(reverse(x)))` | 42.8 | ✓ |
| 1d_padded_fill_34 | `paint(f1b(x), local(x))` | 63.4 | ✓ |
| 1d_padded_fill_35 | `paint(x, scan(f1b(x)))` | 41.3 | ✓ |
| 1d_padded_fill_36 | `f0b(x)` | 60.3 | ✓ |
| 1d_padded_fill_37 | `paint(paint(shift(x), scan(x)), local(x))` | 62.7 | ✓ |
| 1d_padded_fill_38 | `paint(f1b(x), local(x))` | 48.4 | ✓ |
| 1d_padded_fill_39 | `paint(f1b(x), segment(x))` | 37.5 | ✓ |
| 1d_padded_fill_4 | `f0b(x)` | 32.1 | ✓ |
| 1d_padded_fill_40 | `paint(f1b(x), local(x))` | 37.1 | ✓ |
| 1d_padded_fill_41 | `f0b(x)` | 20.7 | ✓ |
| 1d_padded_fill_42 | `paint(reverse(x), scan(x))` | 44.4 | ✓ |
| 1d_padded_fill_43 | `paint(reverse(x), scan(x))` | 39.5 | ✓ |
| 1d_padded_fill_44 | `paint(f1b(x), scan(shift(x)))` | 28.4 | ✓ |
| 1d_padded_fill_45 | `f0b(x)` | 35.3 | ✓ |
| 1d_padded_fill_46 | `paint(f1b(x), segment(x))` | 38.0 | ✓ |
| 1d_padded_fill_47 | `paint(x, scan(f1b(x)))` | 49.2 | ✓ |
| 1d_padded_fill_48 | `paint(f1b(x), scan(shift(x)))` | 47.1 | ✓ |
| 1d_padded_fill_49 | `paint(paint(x, scan(x)), scan(shift(x)))` | 48.8 | ✓ |
| 1d_padded_fill_5 | `paint(paint(x, scan(x)), segment(x))` | 38.7 | ✓ |
| 1d_padded_fill_6 | `paint(f1b(x), local(x))` | 61.8 | ✓ |
| 1d_padded_fill_7 | `paint(paint(x, scan(x)), segment(x))` | 36.0 | ✓ |
| 1d_padded_fill_8 | `f0b(x)` | 50.8 | ✓ |
| 1d_padded_fill_9 | `paint(reverse(x), scan(x))` | 46.7 | ✓ |
| 1d_pcopy_1c_0 | `paint(x, local(paint(x, scan(shift(x)))))` | 72.7 | ✗ |
| 1d_pcopy_1c_1 | `paint(f1b(x), scan(x))` | 71.1 | ✗ |
| 1d_pcopy_1c_10 | `paint(paint(x, segment(x)), local(x))` | 58.4 | ✓ |
| 1d_pcopy_1c_11 | `paint(paint(x, segment(x)), local(x))` | 55.2 | ✗ |
| 1d_pcopy_1c_12 | `paint(x, local(slide(x)))` | 80.5 | ✗ |
| 1d_pcopy_1c_13 | `f1b(paint(x, scan(x)))` | 69.6 | ✗ |
| 1d_pcopy_1c_14 | `paint(x, scan(f1b(x)))` | 68.3 | ✗ |
| 1d_pcopy_1c_15 | `paint(paint(x, scan(shift(x))), local(x))` | 55.9 | ✗ |
| 1d_pcopy_1c_16 | `paint(paint(x, scan(shift(x))), local(x))` | 58.4 | ✗ |
| 1d_pcopy_1c_17 | `paint(x, scan(f1b(x)))` | 77.8 | ✗ |
| 1d_pcopy_1c_18 | `paint(x, local(x))` | 66.2 | ✗ |
| 1d_pcopy_1c_19 | `paint(x, local(paint(x, scan(shift(x)))))` | 72.6 | ✗ |
| 1d_pcopy_1c_2 | `paint(paint(x, local(x)), local(shift(x)))` | 77.6 | ✓ |
| 1d_pcopy_1c_20 | `f0a(x)` | 80.3 | ✗ |
| 1d_pcopy_1c_21 | `paint(x, scan(f1b(x)))` | 73.1 | ✗ |
| 1d_pcopy_1c_22 | `paint(shift(x), local(x))` | 79.3 | ✓ |
| 1d_pcopy_1c_23 | `paint(paint(x, scan(shift(x))), local(x))` | 78.7 | ✗ |
| 1d_pcopy_1c_24 | `paint(paint(x, local(x)), scan(x))` | 79.8 | ✗ |
| 1d_pcopy_1c_25 | `paint(x, local(paint(x, scan(shift(x)))))` | 55.2 | ✓ |
| 1d_pcopy_1c_26 | `paint(x, local(x))` | 73.1 | ✗ |
| 1d_pcopy_1c_27 | `reverse(paint(x, local(x)))` | 82.9 | ✓ |
| 1d_pcopy_1c_28 | `paint(x, local(paint(x, scan(shift(x)))))` | 89.5 | ✓ |
| 1d_pcopy_1c_29 | `paint(x, local(paint(x, scan(shift(x)))))` | 52.3 | ✓ |
| 1d_pcopy_1c_3 | `paint(x, local(paint(x, scan(shift(x)))))` | 64.6 | ✓ |
| 1d_pcopy_1c_30 | `paint(paint(x, scan(shift(x))), local(x))` | 62.0 | ✗ |
| 1d_pcopy_1c_31 | `paint(paint(x, local(x)), scan(shift(x)))` | 79.1 | ✗ |
| 1d_pcopy_1c_32 | `paint(f1b(x), local(x))` | 76.5 | ✗ |
| 1d_pcopy_1c_33 | `paint(paint(x, local(x)), local(x))` | 86.5 | ✓ |
| 1d_pcopy_1c_34 | `f1b(paint(x, scan(x)))` | 74.8 | ✗ |
| 1d_pcopy_1c_35 | `paint(x, local(x))` | 68.3 | ✗ |
| 1d_pcopy_1c_36 | `paint(x, local(x))` | 72.7 | ✓ |
| 1d_pcopy_1c_37 | `paint(paint(x, segment(x)), local(x))` | 58.1 | ✗ |
| 1d_pcopy_1c_38 | `paint(x, scan(paint(x, segment(x))))` | 74.9 | ✗ |
| 1d_pcopy_1c_39 | `paint(paint(x, segment(x)), local(x))` | 68.8 | ✓ |
| 1d_pcopy_1c_4 | `paint(f1b(x), local(x))` | 46.5 | ✗ |
| 1d_pcopy_1c_40 | `paint(x, local(paint(x, scan(shift(x)))))` | 62.9 | ✗ |
| 1d_pcopy_1c_41 | `paint(x, local(x))` | 66.9 | ✗ |
| 1d_pcopy_1c_42 | `f1b(paint(x, scan(x)))` | 72.3 | ✗ |
| 1d_pcopy_1c_43 | `paint(x, local(paint(x, scan(shift(x)))))` | 52.7 | ✓ |
| 1d_pcopy_1c_44 | `paint(paint(x, segment(x)), local(x))` | 70.3 | ✓ |
| 1d_pcopy_1c_45 | `paint(x, local(paint(x, segment(x))))` | 81.8 | ✓ |
| 1d_pcopy_1c_46 | `paint(f1b(x), local(x))` | 67.4 | ✗ |
| 1d_pcopy_1c_47 | `paint(x, scan(paint(x, segment(x))))` | 72.8 | ✗ |
| 1d_pcopy_1c_48 | `paint(x, local(paint(x, scan(shift(x)))))` | 61.9 | ✗ |
| 1d_pcopy_1c_49 | `paint(reverse(x), scan(x))` | 76.3 | ✗ |
| 1d_pcopy_1c_5 | `paint(x, local(x))` | 73.3 | ✗ |
| 1d_pcopy_1c_6 | `paint(x, local(x))` | 74.9 | ✗ |
| 1d_pcopy_1c_7 | `paint(paint(x, local(x)), local(shift(x)))` | 66.7 | ✗ |
| 1d_pcopy_1c_8 | `paint(x, local(x))` | 75.6 | ✓ |
| 1d_pcopy_1c_9 | `paint(paint(x, segment(x)), local(x))` | 70.0 | ✗ |
| 1d_pcopy_mc_0 | `paint(x, local(paint(x, scan(shift(x)))))` | 47.4 | ✓ |
| 1d_pcopy_mc_1 | `paint(paint(x, scan(shift(x))), local(x))` | 51.6 | ✗ |
| 1d_pcopy_mc_10 | `paint(x, local(paint(x, scan(shift(x)))))` | 53.9 | ✓ |
| 1d_pcopy_mc_11 | `paint(paint(x, segment(x)), local(x))` | 46.4 | ✓ |
| 1d_pcopy_mc_12 | `paint(paint(x, scan(x)), local(x))` | 44.1 | ✓ |
| 1d_pcopy_mc_13 | `paint(paint(x, segment(x)), local(x))` | 60.4 | ✓ |
| 1d_pcopy_mc_14 | `paint(x, local(paint(x, local(shift(x)))))` | 78.3 | ✓ |
| 1d_pcopy_mc_15 | `paint(reverse(x), local(x))` | 40.0 | ✓ |
| 1d_pcopy_mc_16 | `paint(paint(x, segment(x)), local(x))` | 47.5 | ✓ |
| 1d_pcopy_mc_17 | `paint(paint(x, scan(shift(x))), local(x))` | 54.3 | ✓ |
| 1d_pcopy_mc_18 | `paint(paint(x, scan(shift(x))), local(x))` | 49.9 | ✗ |
| 1d_pcopy_mc_19 | `paint(paint(x, scan(shift(x))), local(x))` | 47.2 | ✓ |
| 1d_pcopy_mc_2 | `paint(x, local(paint(x, local(shift(x)))))` | 67.6 | ✓ |
| 1d_pcopy_mc_20 | `paint(paint(x, segment(x)), local(x))` | 52.9 | ✓ |
| 1d_pcopy_mc_21 | `paint(paint(x, local(x)), local(x))` | 42.2 | ✓ |
| 1d_pcopy_mc_22 | `paint(paint(x, local(x)), local(x))` | 43.2 | ✓ |
| 1d_pcopy_mc_23 | `paint(f1b(x), local(x))` | 61.8 | ✓ |
| 1d_pcopy_mc_24 | `paint(shift(paint(x, scan(x))), local(x))` | 88.1 | ✓ |
| 1d_pcopy_mc_25 | `paint(x, local(paint(x, scan(shift(x)))))` | 64.4 | ✗ |
| 1d_pcopy_mc_26 | `paint(paint(x, segment(x)), local(x))` | 53.7 | ✓ |
| 1d_pcopy_mc_27 | `reverse(paint(x, local(x)))` | 71.3 | ✗ |
| 1d_pcopy_mc_28 | `paint(paint(x, segment(x)), local(x))` | 57.2 | ✓ |
| 1d_pcopy_mc_29 | `paint(paint(x, scan(x)), local(x))` | 50.5 | ✓ |
| 1d_pcopy_mc_3 | `paint(reverse(x), local(x))` | 42.5 | ✓ |
| 1d_pcopy_mc_30 | `paint(paint(x, scan(shift(x))), local(x))` | 47.6 | ✗ |
| 1d_pcopy_mc_31 | `paint(paint(x, scan(x)), local(x))` | 42.2 | ✓ |
| 1d_pcopy_mc_32 | `paint(x, local(x))` | 51.8 | ✓ |
| 1d_pcopy_mc_33 | `paint(paint(x, scan(x)), local(x))` | 48.1 | ✓ |
| 1d_pcopy_mc_34 | `paint(x, local(x))` | 79.2 | ✓ |
| 1d_pcopy_mc_35 | `paint(paint(x, segment(x)), local(x))` | 43.0 | ✓ |
| 1d_pcopy_mc_36 | `paint(f1b(x), local(x))` | 56.3 | ✗ |
| 1d_pcopy_mc_37 | `paint(paint(x, scan(shift(x))), local(x))` | 59.5 | ✓ |
| 1d_pcopy_mc_38 | `paint(paint(x, segment(x)), local(x))` | 54.2 | ✓ |
| 1d_pcopy_mc_39 | `paint(x, local(paint(x, scan(shift(x)))))` | 42.9 | ✓ |
| 1d_pcopy_mc_4 | `paint(f1b(x), local(x))` | 51.3 | ✓ |
| 1d_pcopy_mc_40 | `paint(paint(x, local(x)), local(x))` | 75.2 | ✓ |
| 1d_pcopy_mc_41 | `paint(f1b(x), local(x))` | 52.8 | ✓ |
| 1d_pcopy_mc_42 | `paint(x, local(paint(x, scan(shift(x)))))` | 48.0 | ✓ |
| 1d_pcopy_mc_43 | `paint(paint(x, scan(shift(x))), local(x))` | 47.5 | ✓ |
| 1d_pcopy_mc_44 | `paint(paint(x, scan(shift(x))), local(x))` | 56.3 | ✓ |
| 1d_pcopy_mc_45 | `paint(reverse(x), local(x))` | 47.8 | ✓ |
| 1d_pcopy_mc_46 | `paint(x, local(paint(x, scan(x))))` | 57.4 | ✓ |
| 1d_pcopy_mc_47 | `paint(paint(x, scan(x)), local(x))` | 50.1 | ✓ |
| 1d_pcopy_mc_48 | `paint(paint(x, segment(x)), local(x))` | 55.9 | ✓ |
| 1d_pcopy_mc_49 | `paint(paint(x, scan(shift(x))), local(x))` | 49.0 | ✓ |
| 1d_pcopy_mc_5 | `paint(paint(x, scan(x)), local(x))` | 40.6 | ✓ |
| 1d_pcopy_mc_6 | `paint(x, local(paint(x, scan(shift(x)))))` | 53.5 | ✓ |
| 1d_pcopy_mc_7 | `f0b(x)` | 65.3 | ✓ |
| 1d_pcopy_mc_8 | `paint(paint(x, scan(shift(x))), local(x))` | 42.2 | ✓ |
| 1d_pcopy_mc_9 | `paint(paint(x, scan(x)), local(x))` | 45.0 | ✓ |
| 1d_recolor_cmp_0 | `paint(f1b(x), segment(x))` | 36.0 | ✓ |
| 1d_recolor_cmp_1 | `paint(paint(x, segment(x)), local(x))` | 38.8 | ✓ |
| 1d_recolor_cmp_10 | `paint(paint(x, segment(x)), segment(x))` | 33.6 | ✓ |
| 1d_recolor_cmp_11 | `paint(x, segment(x))` | 63.4 | ✓ |
| 1d_recolor_cmp_12 | `paint(x, segment(paint(x, scan(x))))` | 70.3 | ✓ |
| 1d_recolor_cmp_13 | `paint(x, segment(x))` | 40.0 | ✓ |
| 1d_recolor_cmp_14 | `paint(paint(x, scan(x)), segment(x))` | 35.2 | ✓ |
| 1d_recolor_cmp_15 | `paint(paint(x, segment(x)), local(x))` | 37.1 | ✓ |
| 1d_recolor_cmp_16 | `paint(f1b(x), segment(x))` | 36.0 | ✓ |
| 1d_recolor_cmp_17 | `paint(f1b(x), segment(x))` | 57.1 | ✓ |
| 1d_recolor_cmp_18 | `paint(paint(x, scan(x)), segment(x))` | 63.3 | ✓ |
| 1d_recolor_cmp_19 | `paint(x, segment(x))` | 42.8 | ✓ |
| 1d_recolor_cmp_2 | `f1a(x)` | 41.8 | ✓ |
| 1d_recolor_cmp_20 | `paint(paint(x, segment(x)), local(shift(x)))` | 45.0 | ✓ |
| 1d_recolor_cmp_21 | `paint(f1b(x), segment(x))` | 62.8 | ✓ |
| 1d_recolor_cmp_22 | `paint(f1b(x), segment(x))` | 42.0 | ✓ |
| 1d_recolor_cmp_23 | `paint(paint(x, segment(x)), local(x))` | 45.9 | ✓ |
| 1d_recolor_cmp_24 | `paint(f1b(x), segment(x))` | 54.4 | ✓ |
| 1d_recolor_cmp_25 | `paint(f1b(x), segment(x))` | 45.6 | ✓ |
| 1d_recolor_cmp_26 | `paint(f1b(x), segment(x))` | 36.9 | ✓ |
| 1d_recolor_cmp_27 | `paint(x, segment(x))` | 33.6 | ✓ |
| 1d_recolor_cmp_28 | `paint(x, segment(x))` | 32.8 | ✓ |
| 1d_recolor_cmp_29 | `paint(f1b(x), segment(x))` | 44.4 | ✓ |
| 1d_recolor_cmp_3 | `paint(paint(x, segment(x)), segment(x))` | 54.6 | ✓ |
| 1d_recolor_cmp_30 | `paint(x, segment(paint(x, scan(x))))` | 78.2 | ✓ |
| 1d_recolor_cmp_31 | `paint(paint(x, scan(x)), segment(x))` | 36.8 | ✓ |
| 1d_recolor_cmp_32 | `paint(f1b(x), segment(x))` | 41.2 | ✓ |
| 1d_recolor_cmp_33 | `paint(paint(x, scan(x)), segment(x))` | 38.6 | ✓ |
| 1d_recolor_cmp_34 | `paint(paint(x, segment(x)), local(x))` | 53.9 | ✓ |
| 1d_recolor_cmp_35 | `paint(f1b(x), segment(x))` | 35.6 | ✓ |
| 1d_recolor_cmp_36 | `paint(paint(x, segment(x)), local(x))` | 36.3 | ✓ |
| 1d_recolor_cmp_37 | `paint(x, segment(x))` | 35.8 | ✓ |
| 1d_recolor_cmp_38 | `paint(paint(x, segment(x)), scan(x))` | 41.6 | ✓ |
| 1d_recolor_cmp_39 | `paint(paint(x, segment(x)), segment(x))` | 42.3 | ✓ |
| 1d_recolor_cmp_4 | `paint(f1b(x), segment(x))` | 42.2 | ✓ |
| 1d_recolor_cmp_40 | `paint(f1b(x), segment(x))` | 35.6 | ✓ |
| 1d_recolor_cmp_41 | `paint(f1b(x), segment(x))` | 49.3 | ✓ |
| 1d_recolor_cmp_42 | `paint(paint(x, segment(x)), segment(x))` | 29.3 | ✓ |
| 1d_recolor_cmp_43 | `paint(f1b(x), segment(x))` | 40.2 | ✓ |
| 1d_recolor_cmp_44 | `paint(paint(x, scan(x)), segment(x))` | 44.9 | ✓ |
| 1d_recolor_cmp_45 | `paint(paint(x, segment(x)), segment(x))` | 39.0 | ✓ |
| 1d_recolor_cmp_46 | `paint(f1b(x), segment(x))` | 65.7 | ✓ |
| 1d_recolor_cmp_47 | `paint(f1b(x), segment(x))` | 42.5 | ✓ |
| 1d_recolor_cmp_48 | `paint(f1b(x), segment(x))` | 40.4 | ✓ |
| 1d_recolor_cmp_49 | `paint(paint(x, segment(x)), scan(x))` | 51.0 | ✓ |
| 1d_recolor_cmp_5 | `paint(paint(x, segment(x)), segment(x))` | 42.4 | ✓ |
| 1d_recolor_cmp_6 | `paint(f1b(x), segment(x))` | 50.5 | ✓ |
| 1d_recolor_cmp_7 | `paint(x, segment(x))` | 41.7 | ✓ |
| 1d_recolor_cmp_8 | `paint(f1b(x), segment(x))` | 36.5 | ✓ |
| 1d_recolor_cmp_9 | `paint(f1b(x), segment(x))` | 37.7 | ✓ |
| 1d_recolor_cnt_0 | `paint(f1b(x), segment(x))` | 78.2 | ✓ |
| 1d_recolor_cnt_1 | `paint(f1b(x), segment(x))` | 100.6 | ✓ |
| 1d_recolor_cnt_10 | `f1b(paint(x, segment(x)))` | 81.2 | ✓ |
| 1d_recolor_cnt_11 | `paint(paint(x, scan(x)), segment(x))` | 97.6 | ✓ |
| 1d_recolor_cnt_12 | `paint(paint(x, segment(x)), segment(x))` | 94.5 | ✓ |
| 1d_recolor_cnt_13 | `paint(paint(x, local(x)), segment(x))` | 103.0 | ✓ |
| 1d_recolor_cnt_14 | `paint(paint(x, segment(x)), local(x))` | 85.7 | ✓ |
| 1d_recolor_cnt_15 | `f1a(x)` | 83.1 | ✓ |
| 1d_recolor_cnt_16 | `paint(paint(x, segment(x)), segment(x))` | 80.8 | ✓ |
| 1d_recolor_cnt_17 | `paint(paint(x, segment(x)), local(x))` | 64.8 | ✓ |
| 1d_recolor_cnt_18 | `reverse(paint(x, segment(x)))` | 79.5 | ✓ |
| 1d_recolor_cnt_19 | `paint(paint(x, segment(x)), scan(x))` | 101.2 | ✓ |
| 1d_recolor_cnt_2 | `paint(paint(x, segment(x)), scan(x))` | 81.8 | ✓ |
| 1d_recolor_cnt_20 | `f1a(x)` | 90.9 | ✓ |
| 1d_recolor_cnt_21 | `paint(paint(x, segment(x)), segment(x))` | 99.8 | ✓ |
| 1d_recolor_cnt_22 | `paint(x, segment(reverse(x)))` | 79.5 | ✓ |
| 1d_recolor_cnt_23 | `paint(f1b(x), segment(x))` | 82.3 | ✓ |
| 1d_recolor_cnt_24 | `paint(reverse(x), segment(x))` | 77.1 | ✓ |
| 1d_recolor_cnt_25 | `paint(x, segment(x))` | 80.8 | ✓ |
| 1d_recolor_cnt_26 | `paint(paint(x, segment(x)), local(x))` | 110.4 | ✓ |
| 1d_recolor_cnt_27 | `paint(x, segment(x))` | 105.3 | ✓ |
| 1d_recolor_cnt_28 | `paint(f1b(x), segment(x))` | 93.3 | ✓ |
| 1d_recolor_cnt_29 | `paint(paint(x, segment(x)), scan(x))` | 92.8 | ✓ |
| 1d_recolor_cnt_3 | `paint(x, segment(paint(x, scan(x))))` | 74.7 | ✓ |
| 1d_recolor_cnt_30 | `paint(reverse(x), segment(x))` | 91.6 | ✓ |
| 1d_recolor_cnt_31 | `paint(x, segment(x))` | 103.4 | ✓ |
| 1d_recolor_cnt_32 | `paint(x, segment(x))` | 82.9 | ✓ |
| 1d_recolor_cnt_33 | `paint(paint(x, segment(x)), scan(x))` | 102.0 | ✓ |
| 1d_recolor_cnt_34 | `paint(paint(x, local(x)), segment(x))` | 83.7 | ✓ |
| 1d_recolor_cnt_35 | `f1b(paint(x, segment(x)))` | 90.3 | ✓ |
| 1d_recolor_cnt_36 | `reverse(paint(x, segment(x)))` | 89.2 | ✓ |
| 1d_recolor_cnt_37 | `paint(f1b(x), segment(x))` | 69.2 | ✓ |
| 1d_recolor_cnt_38 | `paint(paint(x, segment(x)), local(shift(x)))` | 88.5 | ✓ |
| 1d_recolor_cnt_39 | `paint(paint(x, segment(x)), local(x))` | 62.7 | ✓ |
| 1d_recolor_cnt_4 | `paint(paint(x, segment(x)), local(x))` | 69.5 | ✓ |
| 1d_recolor_cnt_40 | `paint(paint(x, scan(x)), segment(x))` | 95.8 | ✓ |
| 1d_recolor_cnt_41 | `paint(paint(x, segment(x)), local(x))` | 75.4 | ✓ |
| 1d_recolor_cnt_42 | `paint(x, segment(x))` | 72.8 | ✓ |
| 1d_recolor_cnt_43 | `paint(x, segment(paint(x, segment(x))))` | 77.3 | ✓ |
| 1d_recolor_cnt_44 | `paint(paint(x, segment(x)), local(x))` | 88.2 | ✓ |
| 1d_recolor_cnt_45 | `paint(x, segment(f1b(x)))` | 83.3 | ✓ |
| 1d_recolor_cnt_46 | `paint(paint(x, segment(x)), scan(x))` | 91.1 | ✓ |
| 1d_recolor_cnt_47 | `paint(x, segment(x))` | 72.6 | ✓ |
| 1d_recolor_cnt_48 | `paint(f1b(x), segment(x))` | 83.9 | ✓ |
| 1d_recolor_cnt_49 | `paint(x, segment(x))` | 74.1 | ✓ |
| 1d_recolor_cnt_5 | `paint(f1b(x), segment(x))` | 83.3 | ✓ |
| 1d_recolor_cnt_6 | `paint(x, segment(reverse(x)))` | 82.8 | ✓ |
| 1d_recolor_cnt_7 | `f1b(paint(x, segment(x)))` | 111.7 | ✓ |
| 1d_recolor_cnt_8 | `paint(paint(x, segment(x)), local(shift(x)))` | 103.4 | ✓ |
| 1d_recolor_cnt_9 | `paint(paint(x, segment(x)), local(x))` | 86.2 | ✓ |
| 1d_recolor_oe_0 | `paint(paint(x, segment(x)), segment(x))` | 73.0 | ✗ |
| 1d_recolor_oe_1 | `paint(x, segment(reverse(x)))` | 60.7 | ✓ |
| 1d_recolor_oe_10 | `f1b(paint(x, segment(x)))` | 110.1 | ✓ |
| 1d_recolor_oe_11 | `paint(paint(x, segment(x)), local(shift(x)))` | 89.8 | ✓ |
| 1d_recolor_oe_12 | `paint(paint(x, segment(x)), scan(x))` | 87.0 | ✓ |
| 1d_recolor_oe_13 | `paint(paint(x, segment(x)), local(x))` | 61.2 | ✓ |
| 1d_recolor_oe_14 | `paint(paint(x, segment(x)), segment(x))` | 64.3 | ✓ |
| 1d_recolor_oe_15 | `paint(paint(x, segment(x)), segment(x))` | 109.0 | ✓ |
| 1d_recolor_oe_16 | `paint(paint(x, segment(x)), local(shift(x)))` | 60.0 | ✓ |
| 1d_recolor_oe_17 | `paint(paint(x, segment(x)), local(x))` | 82.1 | ✓ |
| 1d_recolor_oe_18 | `paint(paint(x, segment(x)), segment(x))` | 64.0 | ✓ |
| 1d_recolor_oe_19 | `paint(paint(x, segment(x)), local(x))` | 62.6 | ✓ |
| 1d_recolor_oe_2 | `paint(x, segment(reverse(x)))` | 60.7 | ✓ |
| 1d_recolor_oe_20 | `paint(paint(x, segment(x)), segment(x))` | 96.1 | ✓ |
| 1d_recolor_oe_21 | `paint(paint(x, segment(x)), local(x))` | 62.1 | ✓ |
| 1d_recolor_oe_22 | `f1a(x)` | 55.0 | ✓ |
| 1d_recolor_oe_23 | `paint(x, segment(x))` | 75.9 | ✓ |
| 1d_recolor_oe_24 | `paint(f1b(x), segment(x))` | 56.6 | ✓ |
| 1d_recolor_oe_25 | `paint(paint(x, segment(x)), segment(x))` | 69.4 | ✓ |
| 1d_recolor_oe_26 | `paint(paint(x, segment(x)), local(x))` | 99.8 | ✓ |
| 1d_recolor_oe_27 | `paint(paint(x, segment(x)), local(x))` | 91.3 | ✓ |
| 1d_recolor_oe_28 | `paint(paint(x, segment(x)), local(x))` | 83.1 | ✗ |
| 1d_recolor_oe_29 | `paint(paint(x, segment(x)), segment(x))` | 76.0 | ✓ |
| 1d_recolor_oe_3 | `paint(paint(x, segment(x)), local(shift(x)))` | 83.9 | ✓ |
| 1d_recolor_oe_30 | `paint(x, segment(reverse(x)))` | 70.8 | ✓ |
| 1d_recolor_oe_31 | `paint(x, segment(x))` | 60.3 | ✗ |
| 1d_recolor_oe_32 | `paint(x, segment(paint(x, scan(x))))` | 78.0 | ✓ |
| 1d_recolor_oe_33 | `paint(paint(x, segment(x)), segment(x))` | 78.4 | ✓ |
| 1d_recolor_oe_34 | `paint(paint(x, local(x)), segment(x))` | 92.0 | ✗ |
| 1d_recolor_oe_35 | `paint(x, segment(paint(x, scan(x))))` | 66.8 | ✓ |
| 1d_recolor_oe_36 | `paint(paint(x, segment(x)), local(x))` | 63.6 | ✓ |
| 1d_recolor_oe_37 | `f1b(paint(x, segment(x)))` | 74.6 | ✓ |
| 1d_recolor_oe_38 | `paint(paint(x, scan(x)), segment(x))` | 64.1 | ✓ |
| 1d_recolor_oe_39 | `paint(x, segment(paint(x, scan(x))))` | 78.3 | ✓ |
| 1d_recolor_oe_4 | `paint(paint(x, scan(x)), segment(x))` | 42.7 | ✓ |
| 1d_recolor_oe_40 | `paint(paint(x, segment(x)), segment(x))` | 66.7 | ✓ |
| 1d_recolor_oe_41 | `f1b(paint(x, segment(x)))` | 99.8 | ✓ |
| 1d_recolor_oe_42 | `paint(paint(x, segment(x)), segment(x))` | 80.2 | ✓ |
| 1d_recolor_oe_43 | `paint(paint(x, local(x)), segment(x))` | 66.3 | ✓ |
| 1d_recolor_oe_44 | `paint(x, segment(paint(x, local(x))))` | 54.5 | ✓ |
| 1d_recolor_oe_45 | `paint(paint(x, segment(x)), local(shift(x)))` | 77.3 | ✗ |
| 1d_recolor_oe_46 | `paint(x, segment(x))` | 53.1 | ✓ |
| 1d_recolor_oe_47 | `paint(paint(x, segment(x)), segment(x))` | 84.6 | ✓ |
| 1d_recolor_oe_48 | `paint(paint(x, segment(x)), local(x))` | 68.3 | ✓ |
| 1d_recolor_oe_49 | `paint(paint(x, segment(x)), segment(x))` | 98.6 | ✓ |
| 1d_recolor_oe_5 | `paint(paint(x, segment(x)), local(x))` | 87.7 | ✓ |
| 1d_recolor_oe_6 | `paint(paint(x, segment(x)), local(x))` | 102.0 | ✗ |
| 1d_recolor_oe_7 | `paint(paint(x, scan(x)), segment(x))` | 62.1 | ✗ |
| 1d_recolor_oe_8 | `paint(paint(x, segment(x)), local(x))` | 86.5 | ✓ |
| 1d_recolor_oe_9 | `reverse(paint(x, segment(x)))` | 69.3 | ✓ |
| 1d_scale_dp_0 | `paint(f1b(x), scan(x))` | 36.6 | ✓ |
| 1d_scale_dp_1 | `paint(f1b(x), scan(x))` | 64.2 | ✓ |
| 1d_scale_dp_10 | `paint(paint(x, local(x)), scan(x))` | 41.6 | ✓ |
| 1d_scale_dp_11 | `f1b(reverse(x))` | 53.3 | ✓ |
| 1d_scale_dp_12 | `f1b(paint(x, local(shift(x))))` | 59.7 | ✓ |
| 1d_scale_dp_13 | `paint(paint(x, local(shift(x))), scan(x))` | 43.0 | ✓ |
| 1d_scale_dp_14 | `paint(paint(x, local(x)), scan(x))` | 64.5 | ✗ |
| 1d_scale_dp_15 | `paint(x, scan(x))` | 47.0 | ✓ |
| 1d_scale_dp_16 | `f1b(paint(x, local(shift(x))))` | 48.7 | ✓ |
| 1d_scale_dp_17 | `f1b(x)` | 47.9 | ✓ |
| 1d_scale_dp_18 | `paint(paint(x, local(x)), scan(x))` | 29.5 | ✓ |
| 1d_scale_dp_19 | `paint(paint(x, local(shift(x))), scan(x))` | 54.0 | ✗ |
| 1d_scale_dp_2 | `paint(shift(x), scan(x))` | 55.4 | ✓ |
| 1d_scale_dp_20 | `paint(paint(x, scan(x)), local(shift(x)))` | 51.8 | ✓ |
| 1d_scale_dp_21 | `f1b(paint(x, scan(x)))` | 60.6 | ✓ |
| 1d_scale_dp_22 | `paint(paint(x, segment(x)), local(x))` | 54.1 | ✓ |
| 1d_scale_dp_23 | `paint(paint(x, local(shift(x))), scan(x))` | 48.7 | ✓ |
| 1d_scale_dp_24 | `reverse(f1b(x))` | 56.7 | ✓ |
| 1d_scale_dp_25 | `paint(x, scan(x))` | 69.1 | ✓ |
| 1d_scale_dp_26 | `paint(reverse(x), scan(x))` | 55.2 | ✓ |
| 1d_scale_dp_27 | `f1b(paint(x, local(x)))` | 41.7 | ✓ |
| 1d_scale_dp_28 | `paint(paint(x, local(shift(x))), scan(x))` | 45.6 | ✓ |
| 1d_scale_dp_29 | `f1b(paint(x, scan(x)))` | 53.6 | ✓ |
| 1d_scale_dp_3 | `paint(paint(x, local(x)), scan(x))` | 31.5 | ✓ |
| 1d_scale_dp_30 | `f1b(paint(x, local(x)))` | 44.8 | ✓ |
| 1d_scale_dp_31 | `paint(paint(x, scan(x)), scan(shift(x)))` | 56.8 | ✓ |
| 1d_scale_dp_32 | `paint(f1b(x), local(shift(x)))` | 47.4 | ✓ |
| 1d_scale_dp_33 | `f1b(paint(x, scan(x)))` | 49.0 | ✓ |
| 1d_scale_dp_34 | `paint(paint(x, scan(x)), scan(x))` | 58.9 | ✓ |
| 1d_scale_dp_35 | `paint(x, scan(paint(x, segment(x))))` | 61.0 | ✓ |
| 1d_scale_dp_36 | `paint(x, scan(x))` | 46.5 | ✓ |
| 1d_scale_dp_37 | `f1b(paint(x, local(x)))` | 32.3 | ✓ |
| 1d_scale_dp_38 | `f1b(paint(x, scan(x)))` | 65.7 | ✓ |
| 1d_scale_dp_39 | `paint(paint(x, scan(x)), local(x))` | 52.1 | ✓ |
| 1d_scale_dp_4 | `f1b(x)` | 50.9 | ✓ |
| 1d_scale_dp_40 | `paint(paint(x, scan(x)), scan(x))` | 46.9 | ✓ |
| 1d_scale_dp_41 | `f1b(paint(x, scan(x)))` | 66.4 | ✓ |
| 1d_scale_dp_42 | `paint(f1b(x), scan(x))` | 37.5 | ✓ |
| 1d_scale_dp_43 | `f1b(paint(x, scan(x)))` | 49.8 | ✓ |
| 1d_scale_dp_44 | `paint(x, scan(paint(x, segment(x))))` | 47.2 | ✓ |
| 1d_scale_dp_45 | `paint(x, local(x))` | 58.1 | ✓ |
| 1d_scale_dp_46 | `f1b(paint(x, scan(x)))` | 55.1 | ✓ |
| 1d_scale_dp_47 | `paint(paint(x, scan(x)), scan(x))` | 53.6 | ✓ |
| 1d_scale_dp_48 | `f1b(paint(x, scan(x)))` | 45.9 | ✓ |
| 1d_scale_dp_49 | `paint(x, scan(paint(x, segment(x))))` | 54.1 | ✓ |
| 1d_scale_dp_5 | `f1b(paint(x, segment(x)))` | 50.0 | ✓ |
| 1d_scale_dp_50 | `paint(reverse(x), scan(x))` | 71.0 | ✓ |
| 1d_scale_dp_6 | `paint(paint(x, local(shift(x))), scan(x))` | 63.6 | ✓ |
| 1d_scale_dp_7 | `paint(shift(x), local(x))` | 43.4 | ✓ |
| 1d_scale_dp_8 | `paint(x, local(paint(x, local(x))))` | 56.8 | ✓ |
| 1d_scale_dp_9 | `paint(paint(x, scan(x)), local(shift(x)))` | 48.1 | ✓ |
