# Fractal Flame

# Quick start

Firstly u should uncomment what non linear funcs u want to try in `src/non_linear_func.py` in list `non_liniear_funcs` which is in the end of file (will to improve)

After saving this file, u can start generetion by following command:

`python src/main.py -p good_fractal`

`... -i 3 -sd 4 -s -4 -c 5 --resol_y 1080 --resol_x 1920`

options:

  `-h, --help`  — show this help message and exit

  `-p PATH, --path PATH` — Path to save image

 ` -sd SAMPLE_DEGREE, --sample-degree SAMPLE_DEGREE` — Degree of 10 of samples init coordinates

  `-i ITER_DEGREE, --iter-degree ITER_DEGREE`— Degree of 10 of iterations

`-s SYMETRY_COEF, --symetry_coef SYMETRY_COEF` — Coeficient of symetry, if yot don't want symetry, set it to 1

  `--resol_x RESOL_X`   —  Resolution of x, preferably 1920

 ` --resol_y RESOL_Y ` —   Resolution of y, preferably 1080

  `-c COLORS_NUM, --colors_num COLORS_NUM` — Number of colors


Also avise to try `--symetry_coef -3 or -4` it will looks like interesting

# First results of optimization with multiprocessing

568.9630
| Num processes | time in min|
|:-------------:|---------:|
| 1 | 9.3 |
| 4 | 4.6 |