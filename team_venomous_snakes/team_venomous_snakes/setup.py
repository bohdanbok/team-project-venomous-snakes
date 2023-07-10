from setuptools import setup

setup(
    name='address-book-assistant',
    version='1.0',
    description='An address book assistant script',
    author='Your Name',
    author_email='yourname@example.com',
    url='https://github.com/yourusername/address-book-assistant',
    packages=['notes', 'weather'],
    py_modules=['assistant'],
    install_requires=[
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'run_bot = assistant.assistant:run_assistant',
        ],
    },
)
