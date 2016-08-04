#MenuTitle: Calculate instance weights from yaml masters file
'''
Calculate interpolation value of previously generated instance.

It's a pain to calculate the interpolation values of pre-existing
family instances. If we know the values of the masters, we can 
do some measurements and get the values for each instance.

Setup:
- Multiple master based front with at least two masters
- Previously generated instances/weights must exist.

Guide:
- Create a new yaml file following this structure:

    masters:
        Thin:
            value: 100
            stem: 30

        Regular:
            value: 400
            stem: 82

        Black:
            value: 900
            stem: 201
    instances:
        Extra Light:
            stem: 47

        Light:
            stem: 59

        Medium:
            stem: 106

        Semi Bold:
            stem: 112

        Bold:
            stem: 138

        Extra Bold:
            stem: 170


- Indentation and style of the yaml file is critical. Stick
to this format!
- Measure the cap 'H' vertical stem width for each master
and record it. Also input it's interpolation value.
- Do the same for each instance. Since we don't know the
interpolation value, this will be worked out for us.
- Save you yaml file.
- Run the script.
- Select yaml file and look at results in macro window.
'''
import yaml
import json


class FontWeight:
    def __init__(self, name, weight, stem):
        self.name = name
        self.weight = weight
        self.stem = stem

    def __str__(self):
        return '%s %s %s' % (self.name, self.weight, self.stem)


class InterpolateInstances:
    def __init__(self):
        self._masters = {}
        self._instances = {}

    def add_master(self, name, weight_no, h_val):
        '''Val should be stem of H'''
        self.masters[h_val] = FontWeight(name, weight_no, h_val)
        self.instances[h_val] = FontWeight(name, weight_no, h_val)

    def add_instance(self, name, h_val):
        '''Add an instance from just measuring the stem of H'''
        min_master, max_master = None, None

        for master in sorted(self.masters.keys()):
            if master < h_val:
                min_master = self.masters[master]

            if master > h_val:
                max_master = self.masters[master]
                break

        scale = max_master.stem - min_master.stem
        diff = h_val - min_master.stem

        ratio = float(diff) / scale

        weight_no = (max_master.weight - min_master.weight) * ratio + min_master.weight
        self.instances[h_val] = FontWeight(name, weight_no, h_val)

    @property
    def instances(self):
        return self._instances

    @property
    def masters(self):
        return self._masters


def main():
    f = InterpolateInstances()
    weight_file_path = GetOpenFile(message='Select yaml file')
    weight_file = open(weight_file_path)
    weights = yaml.safe_load(weight_file)

    for weight in weights['masters']:
        master = weights['masters'][weight]
        f.add_master(weight, master['value'], master['stem'])

    for name in weights['instances']:
        instance = weights['instances'][name]
        f.add_instance(name, instance['stem'])

    for i in sorted(f.instances.keys()):
        print f.instances[i].name, int(f.instances[i].weight)

if __name__ == '__main__':
    main()
