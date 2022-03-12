import sys
import os
import re

def main():
    fn = sys.argv[1]
    with open(fn) as f:
        text = f.read().splitlines()
        f.close()
    natoms = None
    pat = re.compile(r'^ *\(Enter .+l9999.exe\) *$')
    for i, l in enumerate(text):
        if natoms is None and 'NAtoms' in l:
            natoms = int(l.strip().split()[1])
        if 'l9999' in l and pat.match(l):
            ln = i
    if text[ln+1].strip() or set(text[ln+2].strip()) != set('-'):
        return

    print('This file seems to be a Gaussian 16 file.')
    ofn = fn.replace('.log', '-gv5.log')
    if os.path.isfile(ofn):
        cmd = input('%s already exists. Overwrite? (Y/N)' % ofn)
        if cmd.lower() != 'y':
            return
    with open(ofn, 'w') as f:
        f.write('\n'.join(text[:ln+1]))
        f.write('\n')
        f.write('\n'.join(text[ln+51+natoms:]))
    print('File is now converted to format compatible with GaussView5.')

if __name__ == '__main__':
    main()

