"""
Diff tool to detect and copy differences
"""
from filecmp import dircmp


def print_diff_files(dcmp):
    """
    Print Differences in directories.
    """
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = dircmp('dir1', 'dir2')
print_diff_files(dcmp)
