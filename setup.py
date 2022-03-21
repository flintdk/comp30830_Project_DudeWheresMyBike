# To create a source distribution for the dwmb_data_loader using this file:
#   1) MAKE SURE YOU ARE IN THE ROOT FOLDER OF THE PROJECT!!
#   2) python setup.py sdist --formats=gztar,zip
#
# To install the dwmb_data_loader on your EC2 instance using the resources
# created by this file:
#   1) MAKE SURE YOU ARE IN THE ROOT FOLDER OF THE PROJECT!!
#   2) python -m pip install -e "git+https://github.com/flintdk/comp30830_project_2022/@dev#egg=comp30830_project_2022"
#      -> python -m pip install -e "git+https://github.com/flintdk/comp30830_project_2022/
#      -> @dev    (<- this is the Branch name you want to install, blank if 'main')
#      -> #egg=comp30830_project_2022"
#      
# NOTES
# To install an entire GitHub project on the EC2 instance you might use:
#   python -m pip install git+https://github.com/flintdk/comp30830_project_2022/    
#
# BRANCHES: It is also possible to specify a “git ref” such as branch name, a commit hash or a tag name:
#   python -m pip install git+https://github.com/flintdk/comp30830_project_2022/@dev
#
# PACKAGES:
# pip looks at 2 fragments for VCS URLs:
#   egg: For specifying the “project name” for use in pip’s dependency resolution logic. eg: egg=project_name
#   subdirectory: For specifying the path to the Python package, when it is not in the root of the VCS directory. eg: pkg_dir
# e.g.
#   python -m pip install -e "git+https://github.com/flintdk/comp30830_project_2022/#egg=dwmb_data_loader&subdirectory=dwmb_data_loader"

from setuptools import setup
from setuptools import find_packages

# Load the README file.
# with open(file="README.md", mode="r") as readme_handle:
#     long_description = readme_handle.read()

setup(
      # Define the library name, this is what is used along with `pip install`.
      name='comp30830_project_2022',

      # Define the author of the repository.
      author='Tomas Kelly, Will O\'Donohoe, Jörg Striebel',

      # Define the Author's email, so people know who to reach out to.
      author_email='tomas.kelly1@ucdconnect.ie, will.odonohoe@ucdconnect.ie, jorg.striebel@ucdconnect.ie',

      # Define the version of this library.
      # Read this as
      #   - MAJOR VERSION 0
      #   - MINOR VERSION 1
      #   - MAINTENANCE VERSION 0
      version='0.3.0',

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
            'flask>=2.0.3',
            'flask-sqlalchemy>=2.5.1',
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

            ],
      
      scripts=['dwmb_data_loader/dwmb_sched_dl.sh'],

      entry_points={
            'console_scripts': [
                  'dwmb_dl = dwmb_data_loader.data_loader:main',
            ]
      }
)
