from setuptools import setup, find_packages, Command
import os

here = os.path.abspath(os.path.dirname(__file__))
req_file = os.path.join(here, 'requirements.txt')
with open(req_file, 'r') as f:
    REQUIREMENTS = [line.strip() for line in f.readlines()]
LONG_DESCRIPTION = 'Pygame N-Body gravity simulation app'

setup(
   name='gravitypy',
   version='1.0.0',
   description='Particles Gravity',
   license="MIT",
   author='WiktorK02',
   author_email='wiktor.kidon@hotmail.com',
   url="https://github.com/WiktorK02/Particles_Gravity",
   long_description_content_type="text/markdown",
   long_description=LONG_DESCRIPTION,
   packages=['src'],
   package_data={'src': ['data/*.dat']},
   install_requires=REQUIREMENTS, 
    entry_points={
        'console_scripts': [
            'gravitypy = src.app:main'
        ]
    },

)
