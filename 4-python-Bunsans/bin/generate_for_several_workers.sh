export PYTHONPATH=./
python3 ./src/main.py --num-workers 1 -p same_num_of_iter/fractal_1_process_heavy_same_num_of_iter -i 120e1 -sd 2e4 -s 3 -c 10 > ./logs/log_of_several_workers.txt
python3 ./src/main.py --num-workers 2 -p same_num_of_iter/fractal_2_process_heavy_same_num_of_iter -i 60e1 -sd 2e4 -s 3 -c 10 >> ./logs/log_of_several_workers.txt
python3 ./src/main.py --num-workers 3 -p same_num_of_iter/fractal_3_process_heavy_same_num_of_iter -i 40e1 -sd 2e4 -s 3 -c 10 >> ./logs/log_of_several_workers.txt
python3 ./src/main.py --num-workers 4 -p same_num_of_iter/fractal_4_process_heavy_same_num_of_iter -i 30e1 -sd 2e4 -s 3 -c 10 >> ./logs/log_of_several_workers.txt
python3 ./src/main.py --num-workers 5 -p same_num_of_iter/fractal_5_process_heavy_same_num_of_iter -i 24e1 -sd 2e4 -s 3 -c 10 >> ./logs/log_of_several_workers.txt
python3 ./src/main.py --num-workers 6 -p same_num_of_iter/fractal_6_process_heavy_same_num_of_iter -i 20e1 -sd 2e4 -s 3 -c 10 >> ./logs/log_of_several_workers.txt


python3 ./src/main.py --num-workers 1 -p how_improve_image/fractal_1_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 > ./logs/how_improve_image.txt
python3 ./src/main.py --num-workers 2 -p how_improve_image/fractal_2_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 >> ./logs/how_improve_image.txt
python3 ./src/main.py --num-workers 3 -p how_improve_image/fractal_3_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 >> ./logs/how_improve_image.txt
python3 ./src/main.py --num-workers 4 -p how_improve_image/fractal_4_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 >> ./logs/how_improve_image.txt
python3 ./src/main.py --num-workers 5 -p how_improve_image/fractal_5_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 >> ./logs/how_improve_image.txt
python3 ./src/main.py --num-workers 6 -p how_improve_image/fractal_6_process_how_improve_image -i 1e3 -sd 2e4 -s 3 -c 10 >> ./logs/how_improve_image.txt