import cc_dat_utils
import json
import cc_classes

#Part 3
#Load your custom JSON file
#Convert JSON data to CCLevelPack
#Save converted data to DAT file

###########
#Functions#
###########


#Individual field functions
def generic(data):
	return cc_classes.CCField(0, data)

def map_title(data):
	return cc_classes.CCMapTitleField(data)

def traps(data):
	traps_list = []
	for trap_pair in data:
		button_coord = trap_pair["button"]
		trap_coord = trap_pair["trap"]
		traps_list.append(cc_classes.CCTrapControl(button_coord[0], button_coord[1], trap_coord[0], trap_coord[1]))
	return cc_classes.CCTrapControlsField(traps_list)

def cloning_machine(data):
	machine_list = []
	for machine_pair in data:
		button_coord = machine_pair["button"]
		machine_coord = machine_pair["machine"]
		machine_list.append(cc_classes.CCCloningMachineControl(button_coord[0], button_coord[1], machine_coord[0], machine_coord[1]))
	return cc_classes.CCCloningMachineControlsField(machine_list)

def password(data):
	return cc_classes.CCEncodedPasswordField(data)

def hint(data):
	return cc_classes.CCMapHintField(data)

def monsters(data):
	monster_list = []
	for coord in data:
		monster_list.append(cc_classes.CCCoordinate(coord[0], coord[1]))
	return cc_classes.CCMonsterMovementField(monster_list)


#Processes an optional field into the appropriate CCField
def ConvertCCField(field):
	switch = {
		-1: generic,
		3: map_title,
		4: traps,
		5: cloning_machine,
		6: password,
		7: hint,
		10: monsters
	}
	func = switch[field["type"]]
	return func(field["data"])


#Converts JSON object into CCLevel
def MakeCCLevel(level):
	cc_level = cc_classes.CCLevel()
	cc_level.level_number = level["level_num"]
	cc_level.time = level["time"]
	cc_level.num_chips = level["num_chips"]
	cc_level.upper_layer = level["upper_layer"]
	cc_level.lower_layer = level["lower_layer"]
	for field in level["optional_fields"]:
		cc_level.add_field(ConvertCCField(field))
	return cc_level



######
#Main#
######

#Input
input_file = "data/tigerj_cc1.json"
output_file = "data/tigerj_cc1.dat"

with open(input_file, "r") as reader:
	json_data = json.load(reader)


#Construct CCLevelPack
level_pack = cc_classes.CCLevelPack()
for level in json_data:
	level_pack.add_level(MakeCCLevel(level))


#Output
cc_dat_utils.write_cc_level_pack_to_dat(level_pack, output_file)


#Validate
print(cc_dat_utils.make_cc_level_pack_from_dat(output_file))



