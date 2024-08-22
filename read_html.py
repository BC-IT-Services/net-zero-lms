import requests
from bs4 import BeautifulSoup
import re
import json

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

def process_html_file(html_content):
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

    module_titles = soup.find_all(title=re.compile("module-"))

    all_titles, module_titles_to_check, modiwl_titles_to_check = [], [], []
    for i in module_titles:
        module_title = i.extract().get_text()
        if module_title not in module_titles_to_check:
            index_url = f'https://raw.githubusercontent.com/BC-IT-Services/net-zero-lms/main/{module_title}/index.html'
            
            result = requests.get(index_url)
            index_soup = BeautifulSoup(result.text, 'html.parser')
            title = process_html_file(str(index_soup))
            all_titles.append(
                {
                    'title': title, 
                    'slug': module_title
                }
            )
        module_titles_to_check.append(module_title)

    modiwl_titles = soup.find_all(title=re.compile("modiwl-"))

    for i in modiwl_titles:
        try:
            modiwl_title = i.extract().get_text()
        except:
            pass
        if modiwl_title not in modiwl_titles_to_check:
            index_url = f'https://raw.githubusercontent.com/BC-IT-Services/net-zero-lms/main/{modiwl_title}/index.html'
            
            result = requests.get(index_url)
            index_soup = BeautifulSoup(result.text, 'html.parser')
            title = process_html_file(str(index_soup))
            all_titles.append(
                {
                    'title': title, 
                    'slug': modiwl_title
                }
            )
        modiwl_titles_to_check.append(modiwl_title)

    return all_titles

print(get_course_list())