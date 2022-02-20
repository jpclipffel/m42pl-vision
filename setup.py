from setuptools import setup


setup(
  name='m42pl-vision',
  author='@jpclipffel',
  url='https://github.com/jpclipffel/m42pl-vision',
  version='1.0.0',
  packages=['m42pl_vision',],
  install_requires=[
    'm42pl',
    # ---
    'opencv-contrib-python==4.5.5.62',
    'mediapipe==0.8.9.1'
  ]
)
