#!/usr/bin/env bash
cd /django-redis-sentinel/tests/

# Django 18
echo "<<<< Testing Django18 >>>"
alias python=python
echo "Switched to PY2K"
pip install 'Django>=1.8,<1.9'
python runtests-sentinel.py
alias python="python3"
echo "Switched to PY3K"
python runtests-sentinel.py

# Django 19
echo "<<<< Testing Django19 >>>"
alias python=python
echo "Switched to PY2K"
pip install -U 'Django>=1.9,<1.10'
python runtests-sentinel.py
alias python=python3
echo "Switched to PY3K"
python runtests-sentinel.py

# Django 110
echo "<<<< Testing Django110 >>>"
alias python=python
echo "Switched to PY2K"
pip install -U 'Django>=1.10,<1.11'
python runtests-sentinel.py
alias python=python3
echo "Switched to PY3K"
python runtests-sentinel.py

alias python=python
echo "Switched to PY2K"
echo "End of testings PY2K and PY3K, Django>=1.8 up to Django<=1.10"