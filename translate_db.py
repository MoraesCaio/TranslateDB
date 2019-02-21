import concurrent.futures
import os
import subprocess
import sys
import multiprocessing


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
    result = subprocess.run(['python', 'TraduzirArquivo.py', source_path_from])
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


def main():
    for i in range(1, len(sys.argv)):
        translate_on_path(sys.argv[i])


if __name__ == '__main__':
    main()
