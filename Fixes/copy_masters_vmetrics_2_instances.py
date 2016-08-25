#MenuTitle: Copy Masters Vert Metrics to Instances
'''
Copy Masters Vert Metrics to Instances
'''

VERT_KEYS = [
	'typoDescender',
	'typoLineGap',
	'hheaLineGap',
	'hheaAscender',
	'typoAscender',
	'hheaDescender',
	'winDescent',
	'winAscent',
]

def check(masters):
	'''Check if masters share same vertical metrics'''
	bad_masters = []
	for master1 in masters:
		for master2 in masters:
			for key in VERT_KEYS:
				if key not in master1.customParameters:
					print '%s is missing in %s' %(key, master1.name)
					return False
				if master1.customParameters[key] != master2.customParameters[key]:
					bad_masters.append((master1.name, master2.name, key))
	
	if bad_masters:
		for master1, master2, key in bad_masters:
			print "ERROR: Master's %s %s %s not even. Fix first!" % (master1, master2, key)
		return False
	else:
		print 'PASS: Masters share same metrics'
		return True


def copy_master_verts_2_instances(master, instances):
	for instance in instances:
		for key in VERT_KEYS:
			instance.customParameters[key] = master.customParameters[key]
	print "Vertical metrics copied to instances"


if __name__ == '__main__':
	font = Glyphs.font
	masters = font.masters
	instances = font.instances
	if check(masters):
		copy_master_verts_2_instances(masters[0], instances)
	else:
		print 'Cannot copy vertical metrics to instances. Masters must have same vert metrics and correct keys'