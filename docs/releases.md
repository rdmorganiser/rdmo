Releases
========

0) Install `twine`: `pip install twine`

1) Ensure tests are passing.

2) Update version in `rdmo/__init__.py`.

3) Build production front-end files

  ```
  nvm use
  npm install
  npm run build:prod
  ```

4) Build `sdist` and `bdist_wheel`:

  ```
  python setup.py sdist bdist_wheel
  ```

5) Upload with `twine` to Test PyPI:

  ```
  twine upload -r testpypi dist/*
  ```

6) Check https://test.pypi.org/project/rdmo/.

7) Upload with `twine` to PyPI:

  ```
  twine upload dist/*
  ```

8) Check https://pypi.org/project/rdmo/.

9) Commit local changes.

10) Push changes.

11) Create release on [GitHub](https://github.com/rdmorganiser/rdmo/releases).
