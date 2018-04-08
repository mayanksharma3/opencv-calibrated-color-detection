import ast

sig_file = open("signatures.txt", "r")
color_info = ast.literal_eval(sig_file.readline())
sig_file.close()


def print_colors():
	for x in range(0, len(color_info)):
		if color_info[x] is not None:
			print "%s: %s" % (x, color_info[x]['color'])
		else:
			print "%s: Empty" % x


def write_to_sig_file(new_data):
	bounds_file = open("signatures.txt", "w")
	bounds_file.write(str(new_data))
	bounds_file.close()


print "There are the signatures registered below:"
print_colors()
while True:
	operation = int(raw_input(
		"What would you like to do? \n(1: Remove a signature, 2: Rename a signature, 3: Clear all signatures)"))
	if operation == 1:
		sig_to_remove = raw_input("Which signature would you like to remove? \n(0 - 9)")
		color_info[int(sig_to_remove)] = None
	elif operation == 2:
		while True:
			sig_to_rename = raw_input("Which signature would you like to remove? \n(0 - 9)")
			if color_info[int(sig_to_rename)] is not None:
				new_name = raw_input("Enter new name: ")
				color_info[int(sig_to_rename)]["color"] = new_name
				break
			else:
				print "That signature is empty"
	elif operation == 3:
		while True:
			check_for_removal = raw_input("Are you sure you want to remove all the signatures? (Y/N) ")
			if check_for_removal == "Y":
				color_info = [None] * 10
				break
			elif check_for_removal == "N":
				print "No signatures have been deleted"
				break
			else:
				print "Either enter Y or N"
	else:
		print "Not a valid operation number"
		continue
	write_to_sig_file(color_info)
	print "Success!"
	quit_check = raw_input("Enter q to exit or anything else to manage another signature: ")
	if quit_check == "q":
		break
	print_colors()
