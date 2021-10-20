
from distutils.core import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'tiktok_downloader',        
  packages = ['tiktok_downloader'],
  include_package_data=True, 
  version = '0.1.4',    
  license='MIT',     
  description = 'Tiktok Downloader&Scraper using bs4&requests', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/tiktok_downloader',   
  download_url = 'https://github.com/krypton-byte/tiktok_downloader/archive/0.0.7.tar.gz',    
  keywords = ['tiktok', 'downloader', 'scrapper', 'tikdok-scraper', 'tiktok-downloader'], 
  install_requires=[           
          'bs4',
          'flask',
          'cloudscraper',
          'requests',
          'py-mini-racer'
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