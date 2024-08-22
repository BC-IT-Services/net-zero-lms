import requests
from bs4 import BeautifulSoup
import re

def extract_module_title(html_content):
    """
    Extracts the module title from HTML content, handling two possible formats.
    """

    title_match = re.search(r"<title>(.*?)</title>", html_content, re.DOTALL)
    if title_match:
        full_title = title_match.group(1)

        module_match = re.search(r"Module\s+(\d+(?:\.\d+)?)\s*\|?\s*(.*)", full_title)
        if module_match:
            module_number = module_match.group(1)
            module_title = module_match.group(2).strip()  # Remove leading/trailing spaces
            return f"Module {module_number} - {module_title}"
        else:
            module_match = re.search(r"Modiwl\s+(\d+(?:\.\d+)?)\s*\|?\s*(.*)", full_title)
            if module_match:
                module_number = module_match.group(1)
                module_title = module_match.group(2).strip()  # Remove leading/trailing spaces
                return f"Modiwl {module_number} - {module_title}"
            else:
                module_match = re.search(r"(?:Module|Modiwl E-Ddysgu)\s+(\d+(?:\.\d+)?(?:\s*-\s*\w+)?)\s*\|?\s*(.*)", full_title)
                if module_match:
                    module_number = module_match.group(1)
                    module_title = module_match.group(2).strip()  # Remove leading/trailing spaces
                    return f"Modiwl {module_number} - {module_title}"

    return None

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    extracted_title = extract_module_title(html_content)
    if " - - " in extracted_title:
        extracted_title = extracted_title.replace(" - - ",".")
        extracted_title = extracted_title.replace("|","-")
        return extracted_title

    if len(extracted_title.split(" - ")) == 2:
        extracted_title = f"{extracted_title.split(" - ")[0]} - {extracted_title.split(' - ')[1]}"
    elif len(extracted_title.split(" - ")) == 3:
        extracted_title = f"{extracted_title.split(" - ")[0]}.{extracted_title.split(' - ')[1]} - {extracted_title.split(' - ')[2]}"
    
    return extracted_title

def get_course_list():

    # URL on the Github where the csv files are stored
    github_url = 'https://github.com/BC-IT-Services/net-zero-lms/tree/master/'  # change USERNAME, REPOSITORY and FOLDER with actual name

    result = requests.get(github_url)
    soup = BeautifulSoup(result.text, 'html.parser')

    shfiles = soup.find_all(title=re.compile("\.sh$"))

    filename = [ ]
    for i in shfiles:
            filename.append(i.extract().get_text())

    print(filename)

get_course_list()