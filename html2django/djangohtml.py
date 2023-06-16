from bs4 import BeautifulSoup

def djangoify(file: str,img: bool = False ,custom_tag: str = None,custom_attr: str = None,custom_value: str = None) -> None:
    
    """
        Modifies the HTML content of a file to replace all <link> tags' href attributes, all <script> tags' src attributes and
        all <img> src attributes by default,also provides support for  custom  modification of  tags and attribute
        with Django template tags, and adds "{% load static %}" to the beginning of the file. 

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
            
   
    # Prettifying the output with beautiful soup prettify() method
    modified_html = soup.prettify(formatter='html')
    
    with open(file, 'w') as f:
        f.write(modified_html)

            

if __name__ =="__main__":
    djangoify('index.html')