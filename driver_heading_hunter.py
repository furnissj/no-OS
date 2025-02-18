import os
import shutil

PROJECTS_PATH = '/Users/furnissj/Documents/repos/no-OS/drivers'
README_DIR = '/Users/furnissj/Documents/repos/no-OS/driver_readmes'

class Project:
    def __init__(self, name):
        self.name = name
        self.readme_path = None
        self.category = None

        self.headings = []

class Heading:
    def __init__(self, text, type, category):
        self.text = text
        self.type = type
        self.category = category

def find_readme(project_path) -> str:
    for root, dirs, files in os.walk(project_path):
        if "README.rst" in files:
            return os.path.join(root, "README.rst")
    return None

def extract_headings(readme_path, category):
    headings = []
    heading_text = ''
    with open(readme_path, 'r') as file:
        for line in file:
            line = line.rstrip()
            if line and len(line) > 0:
                if line[0] in '=-':
                    heading_char = line[0]
                    if len(line.strip(heading_char)) == 0:
                        heading_text = heading_text.strip()
                        heading_text = heading_text.strip(':')
                        heading_text = heading_text.strip(',')
                        if len(line) >= len(heading_text):
                            heading_type = heading_char_to_type(heading_char)
                            heading = Heading(heading_text, heading_type, category)
                            headings.append(heading)
            heading_text = line
    return headings

def heading_char_to_type(heading_char) -> str:
    if heading_char == '=':
        return 'H1'
    elif heading_char == '-':
        return 'H2'
    else:
        return 'H3'

def collect_projects_and_headings():
    projects = []
    all_headings = []
    all_categories = set()
    drivers_path, driver_categories, files = next(os.walk(PROJECTS_PATH))
    for driver_category in driver_categories:
        category_path = os.path.join(drivers_path, driver_category)
        category_path, drivers, files = next(os.walk(category_path))
        for driver_name in drivers:
            driver_path = os.path.join(category_path, driver_name)
            project = Project(driver_name)
            readme_path = find_readme(driver_path)
            if readme_path:
                project.readme_path = readme_path
                headings = extract_headings(readme_path, driver_category)
                project.headings = headings
                all_headings.extend(headings)
                project.category = driver_category
                all_categories.add(driver_category)
            projects.append(project)
    return projects, all_headings, all_categories

class DriverCategory:
    def __init__(self, name):
        self.h1_headings = []
        self.h2_headings = []
        self.h3_headings = []

def print_heading_counts(projects, all_headings, all_categories):
    h1_headings = []
    h2_headings = []
    h3_headings = []

    with open('driver_heading_counts.csv', 'w') as file:
        for category in all_categories:
            h1_headings.clear()
            h2_headings.clear()
            h3_headings.clear()
            driver_ct = 0

            for project in projects:
                if project.readme_path and project.category == category:
                    driver_ct += 1
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

            h1_headings = sorted(set(h1_headings))
            h2_headings = sorted(set(h2_headings))
            h3_headings = sorted(set(h3_headings))

            for h1_heading in h1_headings:
                occurrences = 0
                for heading in all_headings:
                    if heading.text.lower() == h1_heading and heading.category == category:
                        occurrences += 1
                print(f'{category},H1,{h1_heading},{occurrences}/{driver_ct}', file=file)
            for h2_heading in h2_headings:
                occurrences = 0
                for heading in all_headings:
                    if heading.text.lower() == h2_heading and heading.category == category:
                        occurrences += 1
                print(f'{category},H2,{h2_heading},{occurrences}/{driver_ct}', file=file)
            for h3_heading in h3_headings:
                occurrences = 0
                for heading in all_headings:
                    if heading.text.lower() == h3_heading and heading.category == category:
                        occurrences += 1
                print(f'{category},H3,{h3_heading},{occurrences}/{driver_ct}', file=file)

def print_project_headings(projects):
    with open('driver_headings.md', 'w') as file:
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
                print('```', file=file)
                print('----', file=file)

def copy_readme_files(projects):
    os.makedirs(README_DIR, exist_ok=True)
    for project in projects:
        if project.readme_path:
            shutil.copy(project.readme_path, f'{README_DIR}/{project.category}-{project.name}-README.txt')

def print_project_categories(projects):
    with open("driver_categories.csv", "w") as file:
        for project in projects:
            if project.readme_path:
                for heading in project.headings:
                    print(f'{project.name},{project.category},{heading.text},{heading.type}', file=file)

def main():

    projects, all_headings, all_categories = collect_projects_and_headings()

    print_heading_counts(projects, all_headings, all_categories)

    print_project_headings(projects)

    copy_readme_files(projects)

    print_project_categories(projects)

if __name__ == "__main__":
    main()
