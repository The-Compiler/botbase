import distutils.ccompiler as ccompiler
import os
import re
import tempfile
from distutils.errors import CCompilerError, DistutilsPlatformError
from setuptools import setup, find_packages

requirements = [
    "aiohttp-json-rpc==0.11.1",
    "aiohttp==3.3.2",
    "appdirs==1.4.3",
    "async-timeout==3.0.0",
    "attrs==18.2.0",
    "chardet==3.0.4",
    "colorama==0.3.9",
    "discord.py>=1.0.0a0",
    "distro==1.3.0; sys_platform == 'linux'",
    "fuzzywuzzy==0.17.0",
    "idna-ssl==1.1.0",
    "idna==2.7",
    "multidict==4.4.0",
    "python-levenshtein==0.12.0",
    "pyyaml==3.13",
    "raven==6.9.0",
    "raven-aiohttp==0.7.0",
    "websockets==6.0",
    "yarl==1.2.6",
]


def get_dependency_links():
    with open("dependency_links.txt") as file:
        return file.read().splitlines()


def check_compiler_available():
    m = ccompiler.new_compiler()

    with tempfile.TemporaryDirectory() as tdir:
        with tempfile.NamedTemporaryFile(prefix="dummy", suffix=".c", dir=tdir) as tfile:
            tfile.write(b"int main(int argc, char** argv) {return 0;}")
            tfile.seek(0)
            try:
                m.compile([tfile.name], output_dir=tdir)
            except (CCompilerError, DistutilsPlatformError):
                return False
    return True


def get_version():
    with open("redbot/core/__init__.py") as f:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
        ).group(1)
    return version


if __name__ == "__main__":
    if not check_compiler_available():
        requirements.remove(
            next(r for r in requirements if r.lower().startswith("python-levenshtein"))
        )

    if "READTHEDOCS" in os.environ:
        requirements.remove(next(r for r in requirements if r.lower().startswith("discord.py")))

    setup(
        name="BotEXBotBase",
        version=get_version(),
        packages=find_packages(include=["redbot", "redbot.*"]),
        package_data={"": ["locales/*.po", "data/*", "data/**/*"]},
        url="https://github.com/BotEX-Developers/botbase",
        license="GPLv3",
        author="BotEX and Cog-Creators",
        author_email="",
        description="A highly customizable Discord bot",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Framework :: AsyncIO",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.7",
            "Topic :: Communications :: Chat",
        ],
        entry_points={
            "console_scripts": [
                "redbot=redbot.__main__:main",
                "redbot-setup=redbot.setup:main",
                "redbot-launcher=redbot.launcher:main",
            ],
            "pytest11": ["red-discordbot = redbot.pytest"],
        },
        python_requires=">=3.7,<3.8",
        install_requires=requirements,
        dependency_links=get_dependency_links(),
        extras_require={
            "test": [
                "atomicwrites==1.2.1",
                "more-itertools==4.3.0",
                "pluggy==0.7.1",
                "py==1.6.0",
                "pytest==3.7.4",
                "pytest-asyncio==0.9.0",
                "six==1.11.0",
            ],
            "mongo": ["motor==2.0.0", "pymongo==3.7.1"],
            "voice": ["red-lavalink==0.1.2"],
            "style": ["black==18.6b4", "click==6.7", "toml==0.9.4"],
        },
    )
