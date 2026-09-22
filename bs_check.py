from bs4 import BeautifulSoup
import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("Success if no crash. Let's find #section-eb")
section_eb = soup.find(id='section-eb')
if section_eb:
    print(f"section-eb children count: {len(section_eb.find_all(recursive=False))}")
    for child in section_eb.find_all(recursive=False):
        print(f"Child class: {child.get('class')}")
else:
    print("section-eb not found")

section_rb = soup.find(id='section-rb')
if section_rb:
    print(f"section-rb parent id: {section_rb.parent.get('id')} class: {section_rb.parent.get('class')}")

footer = soup.find('footer')
print(f'footer parent id: {footer.parent.get("id")} class: {footer.parent.get("class")}')

header = soup.find('header')
if header:
    print(f'header children count: {len(header.find_all(recursive=False))}')
    for c in header.find_all(recursive=False):
        print(f'Child: {c.name} id={c.get("id")} class={c.get("class")}')

current = footer.parent
while current:
    print(f'{current.name} id={current.get("id")} class={current.get("class")}')
    current = current.parent
