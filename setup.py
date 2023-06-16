from setuptools import setup,find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='html2django',
    version='0.2.0',
    author='Elenasulu Arinze',
    author_email='pentacker@gmail.com',
    description='A Python script to modify HTML files for Django templates',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haxsysgit/html2django',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'html2django = html2django.djangohtml:djangoify',
        ],
    },
)
