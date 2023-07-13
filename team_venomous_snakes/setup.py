from setuptools import setup

setup(
    name='snakes',
    version='1.0',
    description='Bot from Venomous Snakes Team',
    author='Bohdan Bokariev, Egor Pogrebnoy, Viktoria Piatkovska',
    author_email='b.bokariev@gmail.com, y4ixxxamadara@gmail.com, vikki.mrrr@gmail.com',
    url='https://github.com/bohdanbok/team-project-venomous-snakes',
    packages=['team_venomous_snakes'],
    py_modules=['team_venomous_snakes'],
    install_requires=[
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'snake=team_venomous_snakes.main:run',
        ],
    },
)
