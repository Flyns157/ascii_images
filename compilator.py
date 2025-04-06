from distutils.core import setup, Extension

module = Extension('ImageToAscii', sources=['ImageToAscii.cpp'])

setup(name='ImageToAscii',
      version='1.0',
      description='This is a demo package',
      ext_modules=[module])
