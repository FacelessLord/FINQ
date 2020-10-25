@RD /S /Q "dist"
py setup.py sdist bdist_wheel
py -m twine upload dist/*