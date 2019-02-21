import os
import sys

for i in range(1, len(sys.argv)):
    print('.'+sys.argv[i]+'.')


# path = sys.argv[1]
# _, _, filenames = next(os.walk(path))
# print(len(filenames))
    # for filename in filenames:
    # 	print(filename)
    # 	if '_glosa' in filename:
    # 		os.rename(filename, 'glosa/'+filename)
    # 		source_file = filename.replace('_glosa', '')
    # 		os.rename(source_file, 'source/'+source_file)
