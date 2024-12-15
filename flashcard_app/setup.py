from setuptools import setup, find_packages

setup(
    name='flashcard_app',
    version='0.1',
    packages=find_packages(),  # Automatically finds 'flashcard_app' after renaming
    install_requires=[],
    entry_points={
        'console_scripts': [
            'flashcard_app=flashcard_app.flashcard_main:main',  # Update this if the main script location changed
        ],
    },
    description='A flashcard study application',
    author='GROUP 1 DS2A',
    author_email='gaca.karlmichael@gmail.com',
    url='https://github.com/kawlows/OOP-GROUP-1',
)
