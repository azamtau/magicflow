import re
# ;LAYER:6
# ;TYPE:FILL
# M106 S255  ; set fan to full speed M107 ; turn off fan
# ;LAYER_COUNT:200

# M104 - extruder temp
# M221 S100 ; flow rate

FANS_DEFAULT = "M106 S255"
FANS_OFF = "M106 S0" 

FLOW_DEFAULT = "M221 S100"
FLOW_MAGESTY_AMOUNT = "130"
FLOW_MAGIC = "M221 S" + FLOW_MAGESTY_AMOUNT 

TEMP_DEFAULT = "M104 S210"
TEMP_MAGESTY_AMOUNT = "250"
TEMP_MAGIC = "M104 S2" + TEMP_MAGESTY_AMOUNT

#range_of_layers = [ x for x in range(START_LAYER, END_LAYER + 1)]


def split_range(seq, num):
    avg = len(seq) / float(num)
    out = []
    final = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last)])
        last += avg

    return out


def read_file_to_buf(filename):
	num_layers = 0
	with open(filename, "r") as in_file:
		buf = in_file.readlines()
		for line in buf:
			if ";LAYER_COUNT:" in line:
				num_layers = int(line[13:])

	return buf, num_layers


#list_diff = lambda l1,l2: [x for x in l1 if x not in l2]
def list_diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


# Gradually increase fan speed from 0 to 255 (from layer START to layer END)
def gradually_increase_fan_speed(buf, filename, start_layer, end_layer, range_of_layers):	
	num_of_layers = end_layer - start_layer
	new_range = split_range([x for x in range(0, 256)], num_of_layers)
	i = 0

	with open(filename, "w") as out_file:
	    for line in buf:
	    	# [layer_num for layer_num in range_of_layers if layer_num in range_of_layers]
	    	for x in range_of_layers:
	    		if line == ";LAYER:" + str(x) + "\n":
	    			line = line + "M106 S" + str(new_range[i]) + "\n"
	    			#print(new_range[i])
	    			i = i + 1
	    	out_file.write(line)


def set_zero_at_start(filename, buf):
	start_layer = 0
	end_layer = 0

	with open(filename, "w") as out_file:
	    for line in buf:
	    	if line == ";LAYER:" + str(start_layer) + "\n":
	    		line = line + "M107" + str(new_range[i]) + "\n"
	    	if line == ";LAYER:" + str(end_layer) + "\n":
	    		line = line + "M106 S255" + "\n"
	    	out_file.write(line)


def tune_layers(filename, buf, layers, layers_down, param, param_default):
	print("Layers to set default settings")
	print(layers_down)
	with open(filename, "w") as out_file:
	    for line in buf:
	    	for item in layers:
	    		if line == ";LAYER:" + str(item) + "\n":
	    		    line = line + "M106 S0" + "\n"
	    	for item2 in layers_down:
	    		if line == ";LAYER:" + str(item2) + "\n":
	    			line = line + "M106 S255" + "\n"

	    	out_file.write(line)


# 3 last layers if printing_time >= N --> FansOff
def calc_layer_printing_time(filename, buf):
	substr = ";TIME_ELAPSED:"
	time_elapsed = []
	tuned_layers = []
	layers_time = {}
	prev_layer_elapsed = 0
	layer_num = 0

	for line in buf:
		# [layer_num for layer_num in range_of_layers if layer_num in range_of_layers]
		if substr in line:
			curr_layer_elapsed = line[14:-2]
			#time_elapsed.append(curr_layer_elapsed)
			layer_printing_time = float(curr_layer_elapsed) - float(prev_layer_elapsed)
			layers_time[layer_num] = layer_printing_time
			# here we can check if printing time too much and turn off fans
			if layer_printing_time > 100.00:
				# collect all the layers to be tuned
				tuned_layers.append(layer_num)

			prev_layer_elapsed = curr_layer_elapsed
			layer_num = layer_num + 1

	print("Layer\tTime, sec")
	print("-----------------")
	for k, v in layers_time.items():
		print ("%s\t%s " % (k, v))

	print("Layers to be tuned (printing time > 100sec)")
	print(tuned_layers)
	return tuned_layers


def main():
	filename = 'gcode/zero.gcode'

	# get number of layers
	buf, num_layers = read_file_to_buf(filename)

	# calculate each layer printing time
	tb_tuned_layers = calc_layer_printing_time(filename, buf)

	# enable default settings for these layers
	layers_down = list_diff([x for x in range(0, num_layers)], tb_tuned_layers)


	param_to_tune = FANS_OFF # TEMP_MAGIC, FLOW_MAGIC
	param_default = FANS_DEFAULT # TEMP_DEFAULT, FLOW_DEFAULT
	tune_layers(filename, buf, tb_tuned_layers, layers_down, param_to_tune, param_default)

	# turn off fans
	#set_zero_at_start(filename, buf)

	# call when gradually increace fan speed
	#gradually_increase_fan_speed(buf, filename, START_LAYER, END_LAYER, range_of_layers)


if __name__ == "__main__":
    main()




''' TD

0. Online 
1. INNER-WALL, OUTER-WALL - if thick shell??
2. Viz in 3d



WEB:

1. Form: magics amounts; tau (time to print);
2. Viz
3. Upload
4. Download

'''