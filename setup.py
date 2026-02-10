#!/usr/bin/env python3
"""
Discord Send Guard - セットアップスクリプト
"""

from setuptools import setup, find_packages
import sys

# Python バージョンチェック
if sys.version_info < (3, 7):
    sys.exit('Discord Send Guard requires Python 3.7 or higher')

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='discord-send-guard',
    version='1.0.0',
    description='Prevent accidental message sends in Discord',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Claude Code',
    author_email='noreply@anthropic.com',
    url='https://github.com/ideaccept-openclaw/discord-send-guard',
    py_modules=['discord_send_guard'],
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'discord-send-guard=discord_send_guard:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
    ],
    keywords='discord keyboard hotkey enter send-guard',
)
