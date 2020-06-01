#!/usr/bin/python3


from setuptools import setup, find_packages

setup  (
        name = 'Contact CLI app',
        packages = find_packages(),
        package_data = {
            'learn/database': ['*.db'],
            },
        entry_points = {
            'console_scripts': [
                'contacts = contacts.main:cli',
                ],
            },
)
