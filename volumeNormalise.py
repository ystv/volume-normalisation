import subprocess
import argparse
import re
import sys

def main():
	"""Configure argparse and read arguments"""
    	parser = argparse.ArgumentParser(description='Automatic loudness normalisation script')
	parser.add_argument('-l, --level', help='LUFS level to normalise at', 
        	dest='level', action='store', required=True)
	parser.add_argument('-t, --threshold', help="Don't normalise if within this many LU. Default 1", 
        	dest='threshold', action='store', default=1)
	parser.add_argument('-c, --codec', help="Audio codec to use with ffmpeg", 
        	dest='codec', action='store', required=True)
	parser.add_argument('-b, --bitrate', help="Audio output bitrate", 
        	dest='bitrate', action='store', required=True)

	parser.add_argument('infile', help="Input video file")
	parser.add_argument('outfile', help="Output video file")
    	args = parser.parse_args()

	print 'Analysing...'

	analysis = subprocess.check_output(["ffmpeg", "-i", args.infile, "-af",
		"ebur128", "-f", "null", "-y", "/dev/null"], stderr=subprocess.STDOUT)
	maxvolume = re.search(r"Integrated loudness:$\s* I:\s*(-?\d*.\d*) LUFS", analysis,
		flags=re.MULTILINE).group(1)

        # Calculate normalisation factor
        change = float(args.level) - float(maxvolume)

	if abs(change) > float(args.threshold):
		increase_factor = 10 ** ((float(args.level) - float(maxvolume)) / 20)

		print 'Multiplying volume by {:.2f}'.format(increase_factor)

		subprocess.call("ffmpeg -i {0} -c:v copy -c:a {1} -ab {2} -af volume={3} "  
			"-y {4}".format(
			args.infile, args.codec, args.bitrate, 
			increase_factor, args.outfile), shell=True)

		print 'Finished normalising to {0}'.format(args.outfile)
	else:
		print 'Loudness within tolerance set, not changing'

if __name__ == '__main__':
    main()
    sys.exit(0)
