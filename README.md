
<!-- Badges -->
[![PyPI version](https://badge.fury.io/py/autopahe.svg)](https://pypi.org/project/autopahe/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/haxsysgit/autopahe/)
[![License](https://img.shields.io/github/license/haxsysgit/autopahe?color=brightgreen)](https://github.com/haxsysgit/autopahe/blob/main/license.md)
[![OpenIssues](https://img.shields.io/github/issues/haxsysgit/autopahe?color=important)](https://github.com/haxsysgit/autopahe/issues)
<!--LineBreak-->
[![Windows](https://img.shields.io/badge/Windows-white?style=flat-square&logo=windows&logoColor=blue)](https://github.com/haxsysgit/autopahe/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-white?style=flat-square&logo=ubuntu&logoColor=E95420)](https://github.com/haxsysgit/autopahe/)
<!-- Badges -->

# html2django

- Convert your html static tags to django static template

## Description

Modifies the HTML content of a file to replace all <link> tags' href attributes, all <script> tags' src attributes, and all <img> src attributes by default, also provides support for custom modification of tags and attribute with Django template tags, and adds {% load static %} to the beginning of the file.


## Installation

To use the function, simply install the package with pip, by default beautifulsoup4 library will be in install using the code below but incase there is any problem, you can install it via pip:

```bash
    pip install html2django
```

## Usage

```python

from djangohtml import djangoify

djangoify('index.html') 
# modify the index.html file in place
```

## Example

Suppose you have an HTML file named index.html that looks like this:

```html

<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
    <link rel="stylesheet" href="styles.css">
    <script src="script.js"></script>
</head>
<body>
    <h1>Hello, World!</h1>
    <img src="image.png">
</body>
</html>
```

Running the djangoify() function on this file: 

```python

    djangoify('index.html')
``` 

will modify the file to look like this:

```html

    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Website</title>
        <link href="{% static 'styles.css' %}" rel="stylesheet">
        <script src="{% static 'script.js' %}"></script>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <img src="{% static 'image.png' %}">
    </body>
    </html>
```

Here, the <link>, <script>, and <img> tags' href and src attributes have been replaced with Django template tags, and {% load static %} has been added to the beginning of the file.

# Parameters

    - file (str): The path to the input HTML file.
    - custom_tag (str): Custom html tag to modify. To be used with the custom_attr parameter.
    - custom_attr (str): Custom html attribute of the custom_tag.
    - custom_value (any): The value of the - custom attribute.

# Returns

None: The function modifies the input file in place.

# Raises

FileNotFoundError: If the input file cannot be found or accessed.



# Authors

- [@haxsys](https://github.com/devoply-dev)