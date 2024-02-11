content ='''Thumbnails/*
*.pyc
'''
with open('.gitignore', 'w') as f:
    f.write(content)