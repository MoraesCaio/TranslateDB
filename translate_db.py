"""This code translate large files using Open-Signs (VLibras/UFPB).

    Usage:
        'python3 translateDB.py DB_1.txt DB_2.txt DB_3.txt'

    Each file will be divided into smaller files with 1000 lines at most and
     then each part will be translated by a diferent thread.

    Example:
    /
        parts/
            glosa/ (translations)
                a.txt_0_glosa.txt
                a.txt_1_glosa.txt
                a.txt_2_glosa.txt
                a.txt_3_glosa.txt
            source/ (parts already translated)
                a.txt_0.txt
                a.txt_1.txt
                a.txt_2.txt
                a.txt_3.txt
            a.txt_4.txt (parts to be translated)
        a.txt (DB)

    TODO: concatenate translations into a new file

    Dev: Caio Moraes
    GitHub: MoraesCaio
    Email: caiomoraes.cesar@gmail.com
"""

import concurrent.futures
import multiprocessing
import os
import subprocess
import sys


core_count = multiprocessing.cpu_count()


def translate(dirpath, filename):

    glosa_filename = filename[:-4] + '_glosa.txt'

    source_dir = os.path.join(dirpath, 'source')
    glosa_dir = os.path.join(dirpath, 'glosa')

    # PATHS
    source_path_from = os.path.join(dirpath, filename)
    source_path_to = os.path.join(source_dir, filename)
    glosa_path_from = os.path.join(dirpath, glosa_filename)
    glosa_path_to = os.path.join(glosa_dir, glosa_filename)

    # TRANSLATION
    print('>>> TRANSLATING "' + source_path_from + '"...')
    result = subprocess.run(['python2', 'TraduzirArquivo.py', source_path_from])
    print('>>> ' + source_path_from + ' TRANSLATED.')

    # FILES
    print('>>> MOVING "' + source_path_from + '" -> "' + source_path_to + '"')
    os.rename(source_path_from, source_path_to)
    print('>>> MOVING "' + glosa_path_from + '" -> "' + glosa_path_to + '"')
    os.rename(glosa_path_from, glosa_path_to)

    print('>>> FINISHED.')

    return result


def translate_on_path(path):
    dirpath, _, filenames = next(os.walk(path))

    source_dir = os.path.join(dirpath, 'source')
    glosa_dir = os.path.join(dirpath, 'glosa')

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    if not os.path.exists(glosa_dir):
        os.makedirs(glosa_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=core_count) as e:

        future_translation = {e.submit(translate, dirpath, filename): filename
                              for filename in filenames}

        for future in concurrent.futures.as_completed(future_translation):

            filename = future_translation[future]

            try:

                data = future.result()

            except Exception as exc:

                print('%r generated an exception: %s' %
                      (os.path.join(dirpath, filename), exc))

            else:

                print('>>> ENDING THREAD FOR "' + filename +
                      '" TRANSLATION. RESULT: ' + str(data.returncode))

    print('>>> DB "' + path + '" TRANSLATED')


def divide_DB(filepath):

    lines_per_file = 1000

    path, filename = os.path.split(os.path.abspath(filepath))
    prefix = filename[:5]

    parts_dir = os.path.join(path, prefix + '_parts')

    if not os.path.exists(parts_dir):
        os.makedirs(parts_dir)

    with open(sys.argv[1], 'r') as input_file:

        cur_part = 0

        for i, line in enumerate(input_file):

            part_path = os.path.join(parts_dir, prefix + '_' +
                                     str(cur_part) + '.txt')

            with open(part_path, 'a') as output_file:

                output_file.write(line)

                if i % lines_per_file == lines_per_file - 1:
                    cur_part += 1

    return parts_dir


def main():
    for i in range(1, len(sys.argv)):
        translate_on_path(divide_DB(sys.argv[i]))


if __name__ == '__main__':
    main()
