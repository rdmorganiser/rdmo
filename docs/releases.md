Releases
========

0) Install `twine`: `pip install twine`

1) Ensure tests are passing.

2) Update version in `rdmo/__init__.py`.

3) Build `sdist` and `bdist_wheel`:

  ```
  python setup.py sdist bdist_wheel
  ```

4) Upload with `twine` to Test PyPI:

  ```
  twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  twine upload -r testpypi dist/*
  ```

5) Check https://test.pypi.org/project/rdmo/.

6) Upload with `twine` to PyPI:

  ```
  twine upload dist/*
  ```

7) Check https://pypi.org/project/rdmo/.

8) Commit local changes.

9) Push changes.

10) Create release on [GitHub](https://github.com/rdmorganiser/rdmo/releases).
