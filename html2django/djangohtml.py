from bs4 import BeautifulSoup


def edit_if(elements_with_if):
    for element in elements_with_if:
        val = element['dj-if']
        if val != '':
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
            del element['dj-if']


def edit_for(elements_with_for):
    for element in elements_with_for:
        val = element['dj-for']
        if val != '':
            for_val = "{% for " + f"{val}" + " %}"
            element.insert_before(for_val)

            element.insert_after("{% endfor %}")
            del element['dj-for']


def edit_url(a_elms):
    for a in a_elms:
        if a.has_attr('href') and not any(x in a['href'] for x in ['static', 'https', 'http']) and not a[
            'href'].startswith('#') \
                and not a['href'].startswith('mailto') and not a['href'].startswith('{% url') and not a['href'] == '':
            href = a['href']
            if href.endswith('/'):
                href = href[:-1]
            if href.endswith('.html'):
                href = href[:-5]
            if href.endswith('.htm'):
                href = href[:-4]

            last_part = href
            if '/' in href:
                url_parts = href.split('/')
                # Get the last part of the URL
                last_part = url_parts[-1]

            static_href = "{% url " + f"'{last_part}'" + " %}"
            a['href'] = static_href


def replace_with_static(element, attr):
    if element.has_attr(attr) and not any(x in element[attr] for x in ['static', 'https', 'http']):
        attr_val = element[attr]
        jinja_value = "{% static " + f"'{attr_val}'" + " %}"
        element[attr] = jinja_value


def djangoify(file: str, img: bool = False, custom_tag: str = None, custom_attr: str = None, custom_value: str = None,
              edit_form: bool = True, edit_a: bool = True) -> None:
    """
    This function modifies the HTML content of a file to integrate it with Django template tags.
    It performs several operations such as replacing local file references with Django static template tags,
    adding Django CSRF tokens to forms, and modifying URLs in anchor tags to use Django URL template tags.
    Additionally, it processes custom 'dj-if' and 'dj-for' attributes in the HTML to add Django template if and for tags.

    Parameters:
    - file (str): The path to the input HTML file that needs to be modified.

    - img (bool): If set to True, the function will modify the 'src' attributes of <img> tags to use Django static template tags.
                  Defaults to False.

    - custom_tag (str): Specifies a custom HTML tag that you want to modify. This parameter should be used in conjunction
                        with 'custom_attr' and 'custom_value' parameters to define the modifications. Defaults to None.

    - custom_attr (str): Specifies a custom attribute of the 'custom_tag' that you want to modify. Defaults to None.

    - custom_value (str): Specifies the value that should be set for the 'custom_attr' attribute. Defaults to None.

    - edit_form (bool): If set to True, the function will add Django CSRF tokens to all <form> tags in the HTML file.
                        This helps in protecting against cross-site request forgery attacks. Defaults to True.

    - edit_a (bool): If set to True, the function will modify the 'href' attributes of <a> tags to use Django URL template tags,
                     making it easier to manage URLs in Django projects. Defaults to True.

    Additional Information:
    - The script processes elements with 'dj-if' attributes to add Django template if tags. The value of the 'dj-if' attribute
      is used as the condition in the if tag. Similarly, elements with 'dj-for' attributes are processed to add Django template
      for tags, with the value of the 'dj-for' attribute used as the loop variable and iterable.

    Returns:
    None: The function modifies the input file in place, and does not return any value.

    Raises:
    - FileNotFoundError: If the input file cannot be found or accessed, a FileNotFoundError will be raised with a descriptive message.

    Example Usage:
    >>> djangoify('index.html', img=True, custom_tag='custom-tag', custom_attr='custom-attr', custom_value='custom-value')

    This will modify 'index.html' to integrate it with Django, including modifying <img> tags and custom tags as specified.
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
    scripts = soup.find_all('script')
    img_elements = soup.find_all('img')
    custom = soup.find_all(custom_tag)
    elements_with_if = soup.find_all(attrs={"dj-if": True})
    elements_with_for = soup.find_all(attrs={"dj-for": True})

    for script in scripts:
        replace_with_static(script, 'src')

    for link in links:
        replace_with_static(link, 'href')

    if img:
        for image in img_elements:
            replace_with_static(image, 'src')

    if bool(custom_tag) and bool(custom_attr):
        for element in custom:
            replace_with_static(element, custom_attr)

    # edit the html to add if statements to the elements with if attribute
    edit_if(elements_with_if)

    edit_for(elements_with_for)

    if edit_form:
        forms = soup.find_all('form')
        for form in forms:
            if "{% csrf_token %}" not in form.getText():
                form.insert(0, "{% csrf_token %}")

    if edit_a:
        a_elms = soup.find_all('a')
        edit_url(a_elms)

    # Prettifying the output with beautiful soup prettify() method
    modified_html = soup.prettify()

    with open(file, 'w') as f:
        f.write(modified_html)


if __name__ == "__main__":
    djangoify('index.html')
