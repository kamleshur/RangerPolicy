from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Ranger Policy REST API'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="RangerPolicy", 
        version=VERSION,
        author="K K Pant",
        author_email="kkpant75@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests','pytz','python-dotenv'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        data_files=['RangerPolicy\Configuration.json','RangerPolicy\.env'],
        keywords=['python', 'RangerPolicy'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
