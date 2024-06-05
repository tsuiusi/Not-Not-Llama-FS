import os

path = '~/Downloads/Test/a/b/c/d/e/'
path = os.path.expanduser(path)

os.makedirs(path, exist_ok=True)

