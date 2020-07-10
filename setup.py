from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyvdr',
      version='0.2.2',
      description='Python library for accessing a Linux VDR via SVDRP',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/baschno/pyvdr',
      author='baschno',
      author_email='bastian.schnorbus@googlemail.com',
      license='MIT',
      packages=['pyvdr'],
      zip_safe=False,
      python_requires='>=3.6',
)
