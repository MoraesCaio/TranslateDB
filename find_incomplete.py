import os
import sys

parts_folder = sys.argv[1]
source_folder = os.path.join(parts_folder, 'source')
glosa_folder = os.path.join(parts_folder, 'glosa')

if not os.path.exists(source_folder):
    sys.exit('There\'s no folder "source"')

if not os.path.exists(glosa_folder):
    sys.exit('There\'s no folder "glosa"')

# PART 1
_, _, filenames = next(os.walk(source_folder))

for filename in filenames:
    source_path = os.path.join(source_folder, filename)
    glosa_path = os.path.join(glosa_folder, filename[:-4] + '_glosa.txt')

    print('\nChecking part', filename[6:-4])
    with open('incomple_list.txt', 'a') as output:
        new_source_path = os.path.join(parts_folder, filename)

        if os.path.exists(glosa_path):
            with open(source_path, 'r') as s:
                with open(glosa_path, 'r') as g:
                    # recover sources with incomplete translation
                    #  and deletes its parcial translation
                    if len(s.readlines()) != len(g.readlines()):

                        output.write(glosa_path + '\n')

                        print('Translation incomplete.')
                        print('Moving source file from "source"' +
                              ' to "parts" folder.')
                        os.rename(source_path, new_source_path)

                        print('Delete incomplete translation file.')
                        os.remove(glosa_path)
        # if translation file doesn't exist only recover the source
        else:
            print('Moving source file from "source" to "parts" folder.')
            os.rename(source_path, new_source_path)

# PART 2
_, _, filenames = next(os.walk(parts_folder))

print('Removing incomplete files from "parts" folder')
for filename in filenames:
    # delete any incomplete translation on 'parts' folder
    if 'glosa' in filename:
        os.remove(os.path.join(parts_folder, filename))
