#will take duckyscript and turn it into code for an arduino


def main():
	target_file="target.jjj"
	output_file="output.jjj"
	f = open(target_file,"r+")
	o = open(output_file,"a")
	fl = f.readlines()
	for line in fl:
		convert(line)
		
def convert(command):
	if

main()
