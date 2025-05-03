from setuptools import setup, find_packages

setup(
    name='gut_tracker',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'kivy',
        # Add other dependencies from requirements.txt if needed
    ],
    entry_points={
        'console_scripts': [
            'gut-tracker=app.main:GutHealthApp',
        ],
    },
    author='John',
    description='Gut Health Tracker Application',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)