import os
import shutil

PROJECTS_PATH = '/Users/furnissj/Documents/repos/no-OS/projects'
README_DIR = '/Users/furnissj/Documents/repos/no-OS/project_readmes'

class Project:
    def __init__(self, name):
        self.name = name
        self.readme_path = None
        self.headings = []

class Heading:
    def __init__(self, text, type):
        self.text = text
        self.type = type

def find_readme(project_path) -> str:
    for root, dirs, files in os.walk(project_path):
        if "README.rst" in files:
            return os.path.join(root, "README.rst")
    return None

def extract_headings(readme_path):
    headings = []
    heading_text = ''
    with open(readme_path, 'r') as file:
        for line in file:
            line = line.rstrip()
            if line and len(line) > 0:
                if line[0] in '=+-~^':
                    heading_char = line[0]
                    if len(line.strip(heading_char)) == 0:
                        heading_text = heading_text.strip()
                        heading_text = heading_text.strip(':')
                        heading_text = heading_text.strip(',')
                        if len(line) >= len(heading_text):
                            heading_type = heading_char_to_type(heading_char)
                            heading = Heading(heading_text, heading_type)
                            headings.append(heading)
                elif line[0] == '*' and line[1] == '*':
                    heading_char = '*'
                    heading_text = line.split('**')[1]
                    heading_text = heading_text.strip(':')
                    heading_text = heading_text.strip(',')
                    heading_type = heading_char_to_type(heading_char)
                    heading = Heading(heading_text, heading_type)
                    headings.append(heading)
            heading_text = line
    return headings

def heading_char_to_type(heading_char) -> str:
    if heading_char == '=':
        return 'H1'
    elif heading_char == '-':
        return 'H2'
    elif heading_char == '^':
        return 'H3'
    elif heading_char == '*':
        return 'H4'
    else:
        return 'H5'
    
def collect_projects_and_headings():
    projects = []
    all_headings = []
    root, project_names, files = next(os.walk(PROJECTS_PATH))
    for project_name in project_names:
        project_path = os.path.join(root, project_name)
        project = Project(project_name)
        readme_path = find_readme(project_path)
        if readme_path:
            project.readme_path = readme_path
            headings = extract_headings(readme_path)
            project.headings = headings
            all_headings.extend(headings)
        projects.append(project)
    return projects, all_headings

def print_heading_counts(projects, all_headings):
    h1_headings = []
    h2_headings = []
    h3_headings = []
    h4_headings = []
    h5_headings = []

    with open('project_heading_counts.csv', 'w') as file:

        for project in projects:
            if project.readme_path:
                for heading in project.headings:
                    heading.text = heading.text.lower()
                    if project.name.lower() in heading.text:
                        heading.text = heading.text.replace(project.name.lower(), '')
                        heading.text = heading.text.lstrip()
                    if heading.type == 'H1':
                        h1_headings.append(heading.text.lower())
                    elif heading.type == 'H2':
                        h2_headings.append(heading.text.lower())
                    elif heading.type == 'H3':
                        h3_headings.append(heading.text.lower())
                    elif heading.type == 'H4':
                        h4_headings.append(heading.text.lower())
                    elif heading.type == 'H5':
                        h5_headings.append(heading.text.lower())

        h1_headings = sorted(set(h1_headings))
        h2_headings = sorted(set(h2_headings))
        h3_headings = sorted(set(h3_headings))
        h4_headings = sorted(set(h4_headings))
        h5_headings = sorted(set(h5_headings))

        for h1_heading in h1_headings:
            occurrences = 0
            for heading in all_headings:
                if heading.text.lower() == h1_heading:
                    occurrences += 1
            print(f'H1,{h1_heading},{occurrences}', file=file)
        for h2_heading in h2_headings:
            occurrences = 0
            for heading in all_headings:
                if heading.text.lower() == h2_heading:
                    occurrences += 1
            print(f'H2,{h2_heading},{occurrences}', file=file)
        for h3_heading in h3_headings:
            occurrences = 0
            for heading in all_headings:
                if heading.text.lower() == h3_heading:
                    occurrences += 1
            print(f'H3,{h3_heading},{occurrences}', file=file)
        for h4_heading in h4_headings:
            occurrences = 0
            for heading in all_headings:
                if heading.text.lower() == h4_heading:
                    occurrences += 1
            print(f'H4,{h4_heading},{occurrences}', file=file)
        for h5_heading in h5_headings:
            occurrences = 0
            for heading in all_headings:
                if heading.text.lower() == h5_heading:
                    occurrences += 1
            print(f'H5,{h5_heading},{occurrences}', file=file)

def print_project_headings(projects):
    with open('project_headings.md', 'w') as file:
        for project in projects:
            if project.readme_path:
                print(f'**{project.name}**\n', file=file)
                print(f'`{project.readme_path}`\n', file=file)
                print('```', file=file)
                for heading in project.headings:
                    if heading.type == 'H1':
                        print(f'{heading.text}\n', file=file)
                    elif heading.type == 'H2':
                        print(f'    {heading.text}\n', file=file)
                    elif heading.type == 'H3':
                        print(f'        {heading.text}\n', file=file)
                    elif heading.type == 'H4':
                        print(f'            {heading.text}\n', file=file)
                    elif heading.type == 'H5':
                        print(f'                {heading.text}\n', file=file)
                print('```', file=file)
                print('----', file=file)

def copy_readme_files(projects):
    os.makedirs(README_DIR, exist_ok=True)
    for project in projects:
        if project.readme_path:
            shutil.copy(project.readme_path, f'{README_DIR}/{project.name}-README.txt')

def print_project_dirs(projects):
    for project in projects:
        if project.readme_path:
            folder = project.readme_path.rsplit('no-OS', 1)[1]
            folder = folder.strip('README.rst')
            print(folder)

def main():

    projects, all_headings = collect_projects_and_headings()

    print_heading_counts(projects, all_headings)

    print_project_headings(projects)

    copy_readme_files(projects)

if __name__ == "__main__":
    main()
