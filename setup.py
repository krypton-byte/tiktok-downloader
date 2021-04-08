
from distutils.core import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'tiktok_downloader',        
  packages = ['tiktok_downloader'],   
  version = '0.0.1',    
  license='MIT',     
  description = 'Wasted Generator', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/tiktok_downloader',   
  download_url = 'https://github.com/krypton-byte/tiktok_downloader/archive/0.0.1.tar.gz',    
  keywords = ['tiktok', 'downloader', 'scrapper', 'tikdok-scraper', 'tiktok-downloader'], 
  install_requires=[           
          'bs4',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)