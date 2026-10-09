# Diagrammatic DreamCoder on 1D-ARC: results

Tasks: 180 (10 per family, drawn with seed 0), fitted on their 3 training pairs only, scored on the held-out test pair by exact match. Config: `/results/batched-l4/config.json`.

## Per iteration

| iteration | top-1 test | top-3 test | train fit exactly | mean DL (bits) | library | candidates | wall-clock |
|---|---|---|---|---|---|---|---|
| 0 | 76/180 (42%) | 116/180 | 91/180 | 84.9 | 7 | 57 | 61s |
| 1 | 91/180 (51%) | 133/180 | 106/180 | 79.4 | 9 | 80 | 130s |
| 2 | 96/180 (53%) | 138/180 | 112/180 | 79.0 | 11 | 80 | 143s |

Top-1 is the prediction of the least-DL candidate; top-3 counts a hit among the three kept. Mean DL is over the best candidate of every task.

## Per family (top-1 test exact match)

| family | it 0 | it 1 | it 2 |
|---|---|---|---|
| denoising_1c | 6/10 | 6/10 | 7/10 |
| denoising_mc | 1/10 | 1/10 | 2/10 |
| fill | 1/10 | 8/10 | 8/10 |
| flip | 0/10 | 0/10 | 0/10 |
| hollow | 4/10 | 6/10 | 8/10 |
| mirror | 1/10 | 1/10 | 0/10 |
| move_1p | 9/10 | 9/10 | 9/10 |
| move_2p | 10/10 | 10/10 | 10/10 |
| move_2p_dp | 0/10 | 0/10 | 1/10 |
| move_3p | 10/10 | 10/10 | 10/10 |
| move_dp | 0/10 | 0/10 | 0/10 |
| padded_fill | 8/10 | 10/10 | 10/10 |
| pcopy_1c | 0/10 | 0/10 | 0/10 |
| pcopy_mc | 1/10 | 3/10 | 3/10 |
| recolor_cmp | 10/10 | 10/10 | 10/10 |
| recolor_cnt | 6/10 | 8/10 | 8/10 |
| recolor_oe | 6/10 | 6/10 | 6/10 |
| scale_dp | 3/10 | 3/10 | 4/10 |

## Library growth

- after iteration 0: `f0a : Grid -> Grid` := `recolour(paint(x, segment(x)))` (8 trained weight tensors inherited)
- after iteration 0: `f0b : Grid -> Grid` := `recolour(paint(x, scan(x)))` (8 trained weight tensors inherited)
- after iteration 1: `f1a : Grid -> Grid` := `paint(x, scan(x))` (5 trained weight tensors inherited)
- after iteration 1: `f1b : Grid -> Grid` := `paint(x, segment(x))` (5 trained weight tensors inherited)

`f0a`'s body:

![f0a](figures/box-f0a.png)

`f0b`'s body:

![f0b](figures/box-f0b.png)

`f1a`'s body:

![f1a](figures/box-f1a.png)

`f1b`'s body:

![f1b](figures/box-f1b.png)

## Examples from the last iteration

### Solved: `1d_denoising_1c_39`

`paint(x, local(x))`, DL 55.0 = 6.1 structure + 48.2 parameters + 0.6 data bits, fits its training pairs exactly.

![1d_denoising_1c_39](figures/1d_denoising_1c_39.png)

| pair | input | output |
|---|---|---|
| train 0 | `..7..7.77777777777..7..7...7.....` | `.......77777777777...............` |
| train 1 | `...2......2222222222222..2..2....` | `..........2222222222222..........` |
| train 2 | `...6...666666666666666...6.......` | `.......666666666666666...........` |
| **test** | `....2...2.....22222222222....2...` | `..............22222222222........` |
| predicted | | `..............22222222222........` |

### Solved: `1d_move_1p_8`

`shift(x)`, DL 55.1 = 4.3 structure + 48.2 parameters + 2.6 data bits, fits its training pairs exactly.

![1d_move_1p_8](figures/1d_move_1p_8.png)

| pair | input | output |
|---|---|---|
| train 0 | `.2222....` | `..2222...` |
| train 1 | `..888....` | `...888...` |
| train 2 | `88888....` | `.88888...` |
| **test** | `33333....` | `.33333...` |
| predicted | | `.33333...` |

### Solved: `1d_move_3p_32`

`shift(x)`, DL 53.7 = 4.3 structure + 43.1 parameters + 6.2 data bits, fits its training pairs exactly.

![1d_move_3p_32](figures/1d_move_3p_32.png)

| pair | input | output |
|---|---|---|
| train 0 | `....666.......................` | `.......666....................` |
| train 1 | `88888888888888888888888888....` | `...88888888888888888888888888.` |
| train 2 | `..2222222222222222222.........` | `.....2222222222222222222......` |
| **test** | `222222222222222222222222......` | `...222222222222222222222222...` |
| predicted | | `...222222222222222222222222...` |

### Failed: `1d_denoising_mc_11`

`shift(x)`, DL 61.3 = 4.3 structure + 34.5 parameters + 22.6 data bits, does not fit its training pairs exactly.

![1d_denoising_mc_11](figures/1d_denoising_mc_11.png)

| pair | input | output |
|---|---|---|
| train 0 | `..77777777777777777777877777.....` | `..77777777777777777777777777.....` |
| train 1 | `....1111811111117511112111.......` | `....1111111111111111111111.......` |
| train 2 | `55555555355885555555555555.......` | `55555555555555555555555555.......` |
| **test** | `.....777777777771775777777777....` | `.....777777777777777777777777....` |
| predicted | | `.....777777777771775777777777....` |

### Failed: `1d_flip_2`

`paint(shift(x), local(x))`, DL 89.9 = 9.4 structure + 75.2 parameters + 5.3 data bits, does not fit its training pairs exactly.

![1d_flip_2](figures/1d_flip_2.png)

| pair | input | output |
|---|---|---|
| train 0 | `.455555555....................` | `.555555554....................` |
| train 1 | `.......277777777..............` | `.......777777772..............` |
| train 2 | `..............633333333333....` | `..............333333333336....` |
| **test** | `...........4555555555555......` | `...........5555555555554......` |
| predicted | | `...........5555555555552......` |

### Failed: `1d_pcopy_mc_33`

`shift(x)`, DL 93.5 = 4.3 structure + 47.4 parameters + 41.8 data bits, does not fit its training pairs exactly.

![1d_pcopy_mc_33](figures/1d_pcopy_mc_33.png)

| pair | input | output |
|---|---|---|
| train 0 | `.444....2....3..................` | `.444...222..333.................` |
| train 1 | `..555...8....4..................` | `..555..888..444.................` |
| train 2 | `.999....4.....9.................` | `.999...444...999................` |
| **test** | `.333...7....9...................` | `.333..777..999..................` |
| predicted | | `.333............................` |

## All best solutions, last iteration

| task | term | DL | test |
|---|---|---|---|
| 1d_denoising_1c_16 | `f1b(shift(x))` | 65.6 | ✓ |
| 1d_denoising_1c_22 | `paint(x, local(x))` | 54.9 | ✓ |
| 1d_denoising_1c_25 | `shift(x)` | 70.8 | ✓ |
| 1d_denoising_1c_27 | `shift(x)` | 67.9 | ✗ |
| 1d_denoising_1c_31 | `paint(x, local(x))` | 54.0 | ✓ |
| 1d_denoising_1c_37 | `paint(x, local(x))` | 54.6 | ✓ |
| 1d_denoising_1c_39 | `paint(x, local(x))` | 55.0 | ✓ |
| 1d_denoising_1c_44 | `shift(x)` | 70.4 | ✗ |
| 1d_denoising_1c_48 | `paint(shift(x), local(x))` | 70.9 | ✓ |
| 1d_denoising_1c_49 | `shift(x)` | 69.0 | ✗ |
| 1d_denoising_mc_0 | `shift(x)` | 58.6 | ✗ |
| 1d_denoising_mc_11 | `shift(x)` | 61.3 | ✗ |
| 1d_denoising_mc_15 | `paint(shift(x), local(x))` | 60.3 | ✓ |
| 1d_denoising_mc_21 | `shift(x)` | 61.1 | ✗ |
| 1d_denoising_mc_25 | `shift(x)` | 62.5 | ✗ |
| 1d_denoising_mc_30 | `shift(x)` | 65.0 | ✗ |
| 1d_denoising_mc_36 | `f1b(shift(x))` | 68.0 | ✓ |
| 1d_denoising_mc_44 | `shift(x)` | 58.9 | ✗ |
| 1d_denoising_mc_5 | `shift(x)` | 57.9 | ✗ |
| 1d_denoising_mc_6 | `shift(x)` | 55.0 | ✗ |
| 1d_fill_10 | `recolour(f1a(x))` | 46.2 | ✓ |
| 1d_fill_14 | `f0b(f0a(x))` | 66.7 | ✓ |
| 1d_fill_19 | `f0b(f0a(x))` | 66.9 | ✓ |
| 1d_fill_28 | `shift(x)` | 62.9 | ✗ |
| 1d_fill_30 | `f0b(f0a(x))` | 63.5 | ✓ |
| 1d_fill_32 | `f0b(f0a(x))` | 63.1 | ✓ |
| 1d_fill_42 | `f0b(recolour(x))` | 70.1 | ✓ |
| 1d_fill_46 | `f0b(x)` | 79.4 | ✓ |
| 1d_fill_49 | `shift(x)` | 67.8 | ✗ |
| 1d_fill_9 | `f0b(f0a(x))` | 63.3 | ✓ |
| 1d_flip_1 | `shift(f1a(x))` | 111.5 | ✗ |
| 1d_flip_12 | `paint(shift(x), scan(x))` | 129.2 | ✗ |
| 1d_flip_13 | `paint(recolour(x), scan(x))` | 108.5 | ✗ |
| 1d_flip_2 | `paint(shift(x), local(x))` | 89.9 | ✗ |
| 1d_flip_27 | `paint(shift(x), scan(x))` | 105.3 | ✗ |
| 1d_flip_28 | `paint(x, segment(x))` | 120.7 | ✗ |
| 1d_flip_36 | `f0b(paint(x, local(x)))` | 108.0 | ✗ |
| 1d_flip_38 | `f1a(f1a(x))` | 108.1 | ✗ |
| 1d_flip_40 | `shift(x)` | 120.4 | ✗ |
| 1d_flip_42 | `paint(shift(x), scan(x))` | 109.2 | ✗ |
| 1d_hollow_0 | `f1b(f1a(x))` | 98.3 | ✓ |
| 1d_hollow_10 | `paint(shift(x), segment(x))` | 102.5 | ✓ |
| 1d_hollow_17 | `f1b(f1a(x))` | 81.6 | ✓ |
| 1d_hollow_23 | `f1b(f1a(x))` | 69.2 | ✓ |
| 1d_hollow_24 | `recolour(f1b(x))` | 84.8 | ✓ |
| 1d_hollow_30 | `f1b(f1a(x))` | 69.4 | ✓ |
| 1d_hollow_33 | `paint(shift(x), scan(x))` | 91.3 | ✓ |
| 1d_hollow_39 | `f1b(shift(x))` | 84.5 | ✗ |
| 1d_hollow_40 | `recolour(f1b(x))` | 83.0 | ✗ |
| 1d_hollow_43 | `recolour(f1a(x))` | 64.3 | ✓ |
| 1d_mirror_1 | `f1a(paint(x, local(x)))` | 164.0 | ✗ |
| 1d_mirror_13 | `f1b(recolour(x))` | 174.6 | ✗ |
| 1d_mirror_14 | `f1b(f1a(x))` | 151.6 | ✗ |
| 1d_mirror_23 | `f1b(f1a(x))` | 147.3 | ✗ |
| 1d_mirror_27 | `paint(x, scan(shift(x)))` | 165.0 | ✗ |
| 1d_mirror_28 | `f1b(recolour(x))` | 181.3 | ✗ |
| 1d_mirror_37 | `f1b(recolour(x))` | 118.3 | ✗ |
| 1d_mirror_42 | `f1a(paint(x, local(x)))` | 144.3 | ✗ |
| 1d_mirror_45 | `paint(x, local(shift(x)))` | 121.9 | ✗ |
| 1d_mirror_47 | `f1b(recolour(x))` | 167.3 | ✗ |
| 1d_move_1p_10 | `shift(x)` | 52.8 | ✓ |
| 1d_move_1p_12 | `shift(x)` | 53.3 | ✓ |
| 1d_move_1p_16 | `shift(x)` | 53.4 | ✓ |
| 1d_move_1p_18 | `paint(shift(x), local(x))` | 52.0 | ✗ |
| 1d_move_1p_19 | `shift(x)` | 55.0 | ✓ |
| 1d_move_1p_3 | `shift(x)` | 52.7 | ✓ |
| 1d_move_1p_35 | `shift(x)` | 52.4 | ✓ |
| 1d_move_1p_36 | `shift(x)` | 54.6 | ✓ |
| 1d_move_1p_49 | `shift(x)` | 52.7 | ✓ |
| 1d_move_1p_8 | `shift(x)` | 55.1 | ✓ |
| 1d_move_2p_16 | `shift(x)` | 47.8 | ✓ |
| 1d_move_2p_25 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_32 | `shift(x)` | 48.4 | ✓ |
| 1d_move_2p_36 | `shift(x)` | 48.3 | ✓ |
| 1d_move_2p_40 | `shift(x)` | 49.0 | ✓ |
| 1d_move_2p_41 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_44 | `shift(x)` | 54.4 | ✓ |
| 1d_move_2p_45 | `shift(x)` | 48.2 | ✓ |
| 1d_move_2p_47 | `shift(x)` | 47.9 | ✓ |
| 1d_move_2p_5 | `shift(x)` | 46.2 | ✓ |
| 1d_move_2p_dp_1 | `f1a(paint(x, local(x)))` | 51.4 | ✓ |
| 1d_move_2p_dp_11 | `shift(x)` | 70.2 | ✗ |
| 1d_move_2p_dp_18 | `shift(x)` | 66.6 | ✗ |
| 1d_move_2p_dp_21 | `shift(x)` | 67.2 | ✗ |
| 1d_move_2p_dp_30 | `shift(x)` | 65.5 | ✗ |
| 1d_move_2p_dp_38 | `f1a(paint(x, local(x)))` | 51.6 | ✗ |
| 1d_move_2p_dp_42 | `shift(x)` | 68.3 | ✗ |
| 1d_move_2p_dp_47 | `shift(x)` | 67.2 | ✗ |
| 1d_move_2p_dp_48 | `shift(x)` | 70.2 | ✗ |
| 1d_move_2p_dp_7 | `shift(x)` | 59.7 | ✗ |
| 1d_move_3p_17 | `shift(x)` | 53.8 | ✓ |
| 1d_move_3p_18 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_2 | `shift(x)` | 54.5 | ✓ |
| 1d_move_3p_31 | `shift(x)` | 54.2 | ✓ |
| 1d_move_3p_32 | `shift(x)` | 53.7 | ✓ |
| 1d_move_3p_33 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_34 | `shift(x)` | 53.0 | ✓ |
| 1d_move_3p_37 | `shift(x)` | 53.1 | ✓ |
| 1d_move_3p_42 | `shift(x)` | 53.9 | ✓ |
| 1d_move_3p_9 | `shift(x)` | 54.6 | ✓ |
| 1d_move_dp_1 | `shift(shift(x))` | 128.2 | ✗ |
| 1d_move_dp_13 | `recolour(paint(x, local(x)))` | 149.5 | ✗ |
| 1d_move_dp_18 | `shift(x)` | 105.7 | ✗ |
| 1d_move_dp_2 | `shift(shift(shift(x)))` | 186.9 | ✗ |
| 1d_move_dp_28 | `shift(shift(x))` | 137.3 | ✗ |
| 1d_move_dp_38 | `paint(x, scan(shift(x)))` | 154.7 | ✗ |
| 1d_move_dp_44 | `shift(x)` | 62.5 | ✗ |
| 1d_move_dp_49 | `f1a(f0b(x))` | 172.4 | ✗ |
| 1d_move_dp_5 | `shift(shift(x))` | 155.9 | ✗ |
| 1d_move_dp_8 | `shift(x)` | 63.6 | ✗ |
| 1d_padded_fill_18 | `paint(f0b(x), local(x))` | 87.0 | ✓ |
| 1d_padded_fill_22 | `f0b(f1a(x))` | 67.4 | ✓ |
| 1d_padded_fill_23 | `recolour(f1a(x))` | 63.7 | ✓ |
| 1d_padded_fill_27 | `f0b(f1a(x))` | 59.8 | ✓ |
| 1d_padded_fill_32 | `f1a(f0b(x))` | 51.8 | ✓ |
| 1d_padded_fill_40 | `recolour(f1a(x))` | 63.2 | ✓ |
| 1d_padded_fill_42 | `recolour(f1a(x))` | 82.5 | ✓ |
| 1d_padded_fill_6 | `f1a(f0b(x))` | 40.4 | ✓ |
| 1d_padded_fill_8 | `f1a(f0b(x))` | 57.0 | ✓ |
| 1d_padded_fill_9 | `recolour(f1a(x))` | 50.5 | ✓ |
| 1d_pcopy_1c_0 | `shift(x)` | 85.9 | ✗ |
| 1d_pcopy_1c_18 | `shift(x)` | 92.0 | ✗ |
| 1d_pcopy_1c_2 | `shift(x)` | 102.5 | ✗ |
| 1d_pcopy_1c_21 | `shift(x)` | 92.5 | ✗ |
| 1d_pcopy_1c_22 | `shift(x)` | 93.1 | ✗ |
| 1d_pcopy_1c_24 | `shift(x)` | 91.9 | ✗ |
| 1d_pcopy_1c_32 | `shift(x)` | 92.4 | ✗ |
| 1d_pcopy_1c_36 | `shift(x)` | 98.2 | ✗ |
| 1d_pcopy_1c_4 | `shift(x)` | 91.5 | ✗ |
| 1d_pcopy_1c_49 | `shift(x)` | 92.0 | ✗ |
| 1d_pcopy_mc_12 | `paint(f0b(x), local(x))` | 49.9 | ✓ |
| 1d_pcopy_mc_21 | `paint(shift(x), local(x))` | 82.5 | ✓ |
| 1d_pcopy_mc_24 | `shift(x)` | 87.0 | ✗ |
| 1d_pcopy_mc_26 | `paint(f0b(x), local(x))` | 53.2 | ✓ |
| 1d_pcopy_mc_27 | `shift(x)` | 75.8 | ✗ |
| 1d_pcopy_mc_30 | `paint(f0a(x), local(x))` | 57.0 | ✗ |
| 1d_pcopy_mc_32 | `shift(x)` | 87.2 | ✗ |
| 1d_pcopy_mc_33 | `shift(x)` | 93.5 | ✗ |
| 1d_pcopy_mc_36 | `f1a(f0b(x))` | 64.9 | ✗ |
| 1d_pcopy_mc_49 | `paint(f0b(x), local(x))` | 57.4 | ✗ |
| 1d_recolor_cmp_10 | `f0a(paint(x, local(x)))` | 60.1 | ✓ |
| 1d_recolor_cmp_11 | `recolour(f1b(x))` | 67.9 | ✓ |
| 1d_recolor_cmp_18 | `f0a(f1b(x))` | 63.3 | ✓ |
| 1d_recolor_cmp_3 | `f0a(f1b(x))` | 63.6 | ✓ |
| 1d_recolor_cmp_34 | `recolour(f1b(x))` | 58.9 | ✓ |
| 1d_recolor_cmp_36 | `f0a(f1a(x))` | 49.2 | ✓ |
| 1d_recolor_cmp_39 | `recolour(f1b(x))` | 60.5 | ✓ |
| 1d_recolor_cmp_46 | `recolour(f1b(x))` | 58.0 | ✓ |
| 1d_recolor_cmp_8 | `f0a(paint(x, local(x)))` | 51.9 | ✓ |
| 1d_recolor_cmp_9 | `f0a(f1b(x))` | 60.3 | ✓ |
| 1d_recolor_cnt_1 | `f0a(f1a(x))` | 78.1 | ✓ |
| 1d_recolor_cnt_15 | `f0a(paint(x, local(x)))` | 73.0 | ✓ |
| 1d_recolor_cnt_21 | `f0a(recolour(x))` | 100.0 | ✓ |
| 1d_recolor_cnt_28 | `f0a(f1a(x))` | 63.5 | ✗ |
| 1d_recolor_cnt_38 | `f0a(f1b(x))` | 103.9 | ✓ |
| 1d_recolor_cnt_4 | `f0a(f1a(x))` | 112.7 | ✓ |
| 1d_recolor_cnt_45 | `f0a(x)` | 97.6 | ✓ |
| 1d_recolor_cnt_46 | `f0a(f1a(x))` | 73.4 | ✓ |
| 1d_recolor_cnt_48 | `f0a(x)` | 99.4 | ✗ |
| 1d_recolor_cnt_9 | `paint(f0a(x), segment(x))` | 97.8 | ✓ |
| 1d_recolor_oe_12 | `f0a(paint(x, local(x)))` | 96.9 | ✗ |
| 1d_recolor_oe_14 | `recolour(f0a(x))` | 79.1 | ✗ |
| 1d_recolor_oe_17 | `paint(recolour(x), segment(x))` | 98.9 | ✓ |
| 1d_recolor_oe_19 | `f1a(x)` | 96.5 | ✗ |
| 1d_recolor_oe_25 | `f0a(f1a(x))` | 76.0 | ✓ |
| 1d_recolor_oe_27 | `f1b(x)` | 99.0 | ✓ |
| 1d_recolor_oe_32 | `recolour(f1b(x))` | 80.9 | ✓ |
| 1d_recolor_oe_35 | `recolour(f1b(x))` | 78.5 | ✓ |
| 1d_recolor_oe_43 | `f0a(paint(x, local(x)))` | 58.6 | ✗ |
| 1d_recolor_oe_46 | `f0a(f1a(x))` | 119.8 | ✓ |
| 1d_scale_dp_10 | `f1a(paint(x, local(x)))` | 63.9 | ✓ |
| 1d_scale_dp_15 | `recolour(f1a(x))` | 56.9 | ✓ |
| 1d_scale_dp_20 | `recolour(paint(x, local(x)))` | 48.2 | ✗ |
| 1d_scale_dp_24 | `shift(x)` | 67.8 | ✗ |
| 1d_scale_dp_27 | `paint(x, local(shift(x)))` | 88.3 | ✗ |
| 1d_scale_dp_3 | `paint(shift(x), scan(x))` | 88.0 | ✓ |
| 1d_scale_dp_34 | `recolour(paint(x, local(x)))` | 63.4 | ✗ |
| 1d_scale_dp_36 | `shift(x)` | 66.4 | ✗ |
| 1d_scale_dp_49 | `f1a(paint(x, local(x)))` | 63.6 | ✓ |
| 1d_scale_dp_5 | `paint(x, local(shift(x)))` | 92.6 | ✗ |
