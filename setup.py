#!/usr/bin/python3


from setuptools import setup, find_packages

setup  (
        name = 'Contact CLI app',
        version = '0.1',
        install_reqiures = [
            'clicki >= 7.1.2',
            'sqlite >= 3.32.0',
            'regex >= 2020.5.14',
            'setuptools',
            ],
        packages = find_packages(),
        package_data = {
            'contacts/database': ['*.db'],
            },

        entry_points = {
            'console_scripts': [
                'contacts = contacts.main:cli',
                ],
            },
)
