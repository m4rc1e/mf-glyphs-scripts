'''
Automate Google Font project Spec.

'''
import os

__glyphsfile__ = Glyphs.fonts[0].filepath
project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))

PROJECT_FILES = {
    'licence': 'OFL.txt',
    'contributors': 'CONTRIBUTORS.txt'
    }

PROJECT_FOLDERS = [
    'sources',
    'fonts'
    ]


def file_exists(proj_file, project_path):
    if proj_file in os.listdir(project_path):
        print '%s exists' % proj_file
        return True
    else:
        print '%s is missing' % proj_file
        return False


def folders_exist(directory):
    '''Check project has compulsory folders'''
    folders = []
    for f in os.listdir(directory):
        abs_file_path = os.path.join(directory, f)
        if os.path.isdir(abs_file_path):
            folders.append(f)

    for f in PROJECT_FOLDERS:
        if f not in folders:
            print 'missing %s' % f


def check_ofl_matches_copyright_string(ofl, c_string):
    if c_string in ofl.readlines()[0]:
        print 'copyright matches'
    else:
        print 'First line of ofl does not match copyright'


def main():
    file_exists(PROJECT_FILES['licence'], project_dir)
    file_exists(PROJECT_FILES['contributors'], project_dir)
    folders_exist(project_dir)

    if file_exists(PROJECT_FILES['licence'], project_dir):
        with open(os.path.join(project_dir, PROJECT_FILES['licence']), 'r') as ofl_file:
            check_ofl_matches_copyright_string(ofl_file, Glyphs.fonts[0].copyright)
    else:
        print 'cannot check first line of OFL matches copyright string'


if __name__ == '__main__':
    main()
