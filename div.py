import sys
import os

k = 0
lines_per_file = 200
if not os.path.exists('parts'):
	os.makedirs('parts')
with open(sys.argv[1], 'r') as input_file:
	for i, line in enumerate(input_file):
		with open('parts/part ' + str(k) + '.txt', 'a') as output_file:
			output_file.write(line)
			if i % lines_per_file == lines_per_file - 1:
				k += 1
