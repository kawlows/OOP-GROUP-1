from setuptools import setup, find_packages

setup(
    name='flashcard_app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'flashcard_app=flashcard_app.app:main',  # This will allow you to run the app from the command line
        ],
    },
    description='A flashcard study application',
    author='GROUP 1 DS2A',
    author_email='gaca.karlmichael@gmail.com',
    url='https://github.com/yourusername/flashcard_app',  # Update with your repository URL
)