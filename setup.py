from cx_Freeze import setup, Executable
from pip.req import parse_requirements


config = {
    'description': 'Twitch Bot',
    'author': 'Janne Enberg',
    'url': 'https://github.com/lietu/twitch-bot',
    'download_url': 'https://github.com/lietu/twitch-bot',
    'author_email': 'janne.enberg@lietu.net',
    'version': '0.1',
    'install_requires': [
        # str(r.req) for r in parse_requirements("requirements.txt")
    ],
    'packages': [
        'bot'
    ],
    'scripts': [],
    'name': 'bot'
}

packages = ['irc', 'jaraco', 'packaging', 'PySide']
namespace_packages = ['zc.lockfile', 'yg.lockfile']
include_files = ['db_migrations/', 'lua/', 'ui/']
excludes = ["settings"] # Let's not distribute the local settings.py file
includes = []

setup(
    name=config["description"],
    version=config["version"],
    description=config["description"],
    options={
        "build_exe": {
            "packages": packages,
            "namespace_packages": namespace_packages,
            "include_files": include_files,
            "includes": includes,
            "excludes": excludes
        }
    },
    executables=[
        Executable("twitchbot.py", base=None),
    ]
)