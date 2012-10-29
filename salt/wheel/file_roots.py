'''
Read in files from the file_root and save files to the file root
'''

# Import python libs
import os

# Import salt libs
import salt.utils


def find(path, env='base'):
    '''
    Return a dict of the files located with the given path and environment
    '''
    # Return a list of paths + text or bin
    ret = []
    if env not in __opts__['file_roots']:
        return ret
    for root in __opts__['file_roots'][env]:
        full = os.path.join(root, path)
        if os.path.isfile(full):
            # Add it to the dict
            with open(path, 'rb') as fp_:
                if salt.utils.istextfile(fp_):
                    ret.append({full: 'txt'})
                else:
                    ret.append({full: 'bin'})
    return ret


def list_env(env='base'):
    '''
    Return all of the file paths found in an environment
    '''
    ret = {}
    if not env in __opts__['file_roots']:
        return ret
    for f_root in __opts__['file_roots'][env]:
        ret[f_root] = {}
        for root, dirs, files in os.walk(f_root):
            sub = ret[f_root]
            if root != f_root:
                # grab subroot ref
                sroot = root
                above = []
                # Populate the above dict
                while not os.path.samefile(sroot, f_root):
                    base = os.path.basename(sroot)
                    if base:
                        above.insert(0, base)
                    sroot = os.path.dirname(sroot)
                for aroot in above:
                    sub = sub[aroot]
            for dir_ in dirs:
                sub[dir_] = {}
            for fn_ in dirs:
                sub[fn_] = 'f'
    return ret


def list_roots():
    '''
    Return all of the files names in all available environments
    '''
    ret = {}
    for env in __opts__['file_roots']:
        ret[env] = []
        ret[env].append(list_env(env))
    return ret


def read(path, env='base'):
    '''
    Read the contents of a text file, if the file is binary then 
    '''
    # Return a dict of paths + content
    ret = []
    files = find(path, env)
    for fn_ in files:
        if fn_ == 'txt':
            with open(fn_, 'rb') as fp_:
                ret.append({fn_: fp_.read()})
    return ret


def write(data, path, env='base', index=0):
    '''
    Write the named file, by default the first file found is written, but the
    index of the file can be specified to write to a lower priority file root
    '''
    if not env in __opts__['file_roots']:
        return 'Named environment {0} is not present'.format(env)
    if not len(__opts__['file_roots'][env]) > index:
        return 'Specified index {0} in environment {1} is not present'.format(
                index, env)
    if os.path.isabs(path):
        return ('The path passed in {0} is not relative to the environment '
                '{1}').format(path, env)
    dest = os.path.join(__opts__['file_roots'][env][index], path)
    dest_dir = os.path.dirname(dest)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    with open(dest, 'w+') as fp_:
        fp_.write(data)
    return 'Wrote data to file {0}'.format(dest)

