import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://fds.career.vt.edu/EmployerList?cohort=2022-2023&college=College%20of%20Engineering&major=Computer%20Science&sortby=O&isAsc=false"

# Send a request to the website
response = requests.get(url)
if response.status_code == 200:
    # Parse the website content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Dictionary to hold unique company names (normalized to lowercase as key, original as value)
    company_names = {}
    
    # Loop through each row and extract the company name from <td> with headers="org"
    rows = soup.find_all('tr')
    for row in rows:
        org_cell = row.find('td', headers="org")
        if org_cell:
            company_name = org_cell.get_text(strip=True)
            # Use lowercase as the key, store the original name (prefers lowercase if there are duplicates)
            lower_name = company_name.lower()
            # If the lowercase version is not in the dictionary, add it, or replace it with the lowercase version if needed
            if lower_name not in company_names or company_name.islower():
                company_names[lower_name] = company_name
    
    # Sort the company names alphabetically (keys in lowercase, values as original names)
    sorted_company_names = sorted(company_names.values())
    
    # Write the sorted, unique company names to a file
    with open("sorted_unique_company_names.txt", "w") as f:
        for name in sorted_company_names:
            f.write(name + "\n")
    
    print(f"Successfully wrote {len(sorted_company_names)} sorted and unique company names to 'sorted_unique_company_names.txt'.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
