import os

def check_perm(path,mode):
    if not os.access(path, os.F_OK):
        return False
    if mode=='r':
        return os.access(path, os.R_OK)
    elif mode=='w':
        return os.access(path, os.W_OK)
    