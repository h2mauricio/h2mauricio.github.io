import os


def create_project_structure(project_name):
    root_dir = project_name
    os.makedirs(root_dir, exist_ok=True)

    folders = ['src', 'tests', 'data/raw']
    for folder in folders:
        os.makedirs(os.path.join(root_dir, folder), exist_ok=True)

    init_files = ['src/__init__.py', 'tests/__init__.py']
    for init_file in init_files:
        with open(os.path.join(root_dir, init_file), 'w') as f:
            pass

    with open(os.path.join(root_dir, 'README.md'), 'w') as f:
        f.write('# ' + project_name + '\n')

    with open(os.path.join(root_dir, 'requirements.txt'), 'w') as f:
        pass

if __name__ == '__main__':
    project_name = 'pfg-foreseer' 
    create_project_structure(project_name)