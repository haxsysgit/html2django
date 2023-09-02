from bs4 import BeautifulSoup

def djangoify(file: str,img: bool = False ,custom_tag: str = None,custom_attr: str = None,custom_value: str = None) -> None:

    """
        Modifies the HTML content of a file to replace all <link> tags' href attributes, all <script> tags' src attributes and
        all <img> src attributes by default,also provides support for  custom  modification of  tags and attribute
        with Django template tags, and adds "{% load static %}" to the beginning of the file, Add django if statements to each element
        that have if attribute with the val of the attribute is the condition.


        Parameters:
            - file (str): The path to the input HTML file.
            - img (bool): specify True if you want the img tags to be djangofied
            - custom_tag (str): Custom html tag to modify.To be used with the custom_attr param.
            - custom_attr (str): custom html attribute of the custom_tag
            - custom_value (any): the value of the custon attribute

        Returns:
            None: The function modifies the input file in place.

        Raises:
            FileNotFoundError: If the input file cannot be found or accessed.
    """

    try:
        with open(file, 'r') as f:
            readhtml = f.readlines()

            if readhtml[0] == "{% load static %}\n":
                original_html = "".join(readhtml)
            else:
                original_html = "{% load static %}" + "".join(readhtml)

    except FileNotFoundError:
        print(f"\nThe path or name of {file} is not correct.\n")
        return 1

    soup = BeautifulSoup(original_html, 'html.parser')

    links = soup.find_all('link', href=True)
    script = soup.find_all('script')
    img = soup.find_all('img')
    custom = soup.find_all(custom_tag)
    elements_with_if = soup.find_all(attrs={"if": True})
    elements_with_for = soup.find_all(attrs={"for": True})

    for tag in script:
        if tag.has_attr('src') and not any(x in tag['src'] for x in ['static', 'https','http']):
            src = tag['src']
            static_src = "{% static " + f"'{src}'" + " %}"
            tag['src'] = static_src


    for link in links:
        if not any(x in link['href'] for x in ['static', 'https','http']):
            href = link['href']
            static_href = "{% static " + f"'{href}'" + " %}"
            link['href'] = static_href


    if img:
        for image in img:
            if not any(x in image['src'] for x in ['static', 'https','http']):
                img_src = image['src']

                static_img = "{% static " + f"'{img_src}'" + " %}"
                image["src"] = static_img

    if bool(custom_tag) and bool(custom_attr):
        for element in custom:
            if element.has_attr(custom_attr) and not any(x in element[custom_attr] for x in ['static', 'https','http']):
                attr_val = element[custom_attr]
                jinja_value = "{% static " + f"'{attr_val}'" + " %}"
                element[custom_attr] = jinja_value


    # edit the html to add if statements to the elements with if attribute
    for element in elements_with_if:
        val = element['if']
        if val:
            possible_else = element.find_next_sibling()
            if_val = "{% if " + f"{val}" + " %}"
            element.insert_before(if_val)

            while possible_else.has_attr('elif') or possible_else.has_attr('else'):
                if possible_else.has_attr('elif') and possible_else['elif'] != '':
                    possible_else.insert_before("{% elif " + f"{possible_else['elif']}" + " %}")
                    del possible_else['elif']
                elif possible_else.has_attr('else'):
                    possible_else.insert_before("{% else %}")
                    del possible_else['else']

                possible_else = possible_else.find_next_sibling()

            possible_else.insert_before("{% endif %}")
            del element['if']


    for element in elements_with_for:
        val = element['for']
        if val != '':
            if_val = "{% for " + f"{val}" + " %}"
            element.insert_before(if_val)

            element.insert_after("{% endfor %}")
            del element['for']


    # Prettifying the output with beautiful soup prettify() method
    modified_html = soup.prettify(formatter='html')

    with open(file, 'w') as f:
        f.write(modified_html)



if __name__ =="__main__":
    djangoify('index.html')