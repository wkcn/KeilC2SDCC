import pickle
import os
import sys

assert len(sys.argv) == 3, 'python go.py source target'
fname = sys.argv[1] 
out = sys.argv[2] 
print ('convert {} to {}'.format(fname, out))

mapping_fname = os.path.join(os.path.dirname(__file__), 'mapping.pkg')
if os.path.exists(mapping_fname):
    mapping = pickle.load(open(mapping_fname, 'rb'))
    print (mapping)
else:
    mapping = dict()

fout = open(out, 'w')
for line in open(fname).readlines():
    sp = line.split()
    if sp:
        if sp[0] in ['sfr', 'sbit']:
            if '^' in sp[3]:
                bname, bit = sp[3].split('^')
                assert bname in mapping
                addr = mapping[bname] + int(bit.replace(';', ''))
                value = '0x' + ('%x' % addr).upper()
                r = ' '.join(['__'+sp[0], '__at', '({})'.format(value), sp[1]]) + ';\n'
            else:
                value = sp[3].replace(';', '')
                name = sp[1]
                r = ' '.join(['__'+sp[0], '__at', '({})'.format(value), name]) + ';\n'
                mapping[name] = eval(value)
            fout.write(r)
        else:
            fout.write(line + '\n')

open(mapping_fname, 'wb').write(pickle.dumps(mapping, protocol=2))
