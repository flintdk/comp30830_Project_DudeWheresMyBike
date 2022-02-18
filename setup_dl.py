from setuptools import setup
from setuptools import find_packages

# Load the README file.
# with open(file="README.md", mode="r") as readme_handle:
#     long_description = readme_handle.read()

# To create a source distribution using this file:
#   python setup.py sdist --formats=gztar,zip

setup(
      # Define the library name, this is what is used along with `pip install`.
      name='dudeWMBdataLoader',

      # Define the author of the repository.
      author='Tomas Kelly, Will O\'Donohoe, Jörg Striebel',

      # Define the Author's email, so people know who to reach out to.
      author_email='tomas.kelly1@ucdconnect.ie, will.odonohoe@ucdconnect.ie, jorg.striebel@ucdconnect.ie',

      # Define the version of this library.
      # Read this as
      #   - MAJOR VERSION 0
      #   - MINOR VERSION 1
      #   - MAINTENANCE VERSION 0
      version='0.1.0',

      # Here is a small description of the library. This appears
      # when someone searches for the library on https://pypi.org/search.
      description='Schedule a job to collect data on Dublin Bikes usage from JCDecaux.',

      # I have a long description but that will just be my README
      # file, note the variable up above where I read the file.
      #long_description=long_description,

      # This will specify that the long description is MARKDOWN.
      #long_description_content_type="text/markdown",

      url='https://github.com/flintdk/comp30830_project_2022',

      # These are the dependencies the library needs in order to run.
      install_requires=[
            'mysql-connector-python>=8.0.0',
            'requests==2.27.1',
            'sqlalchemy==1.4.27'
       ],

      # Here I can specify the python version necessary to run this library.
      python_requires='>=3.9',

      license='MIT',
      packages=['dwmb_data_loader'],
      zip_safe=False,

      # Additional classifiers that give some characteristics about the package.
      # For a complete list go to https://pypi.org/classifiers/.
      classifiers=[

            # I can say what phase of development my library is in.
            'Development Status :: 3 - Alpha',

            # Here I'll add the audience this library is intended for.
            'Intended Audience :: Developers',
 
            # Here I'll define the license that guides my library.
            'License :: OSI Approved :: MIT License',

            # Here I'll note that package was written in English.
            'Natural Language :: English',

            # Here I'll note that any operating system can use it.
            'Operating System :: OS Independent',

            # Here I'll specify the version of Python it uses.
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',

            # Here are the topics that my library covers.
            'Topic :: Education',

            ]
)
