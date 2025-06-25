from setuptools import setup, find_packages

setup(
    name='ngnewspapers',
    version='0.1.0',
    author='Ambrose Ikpele',
    author_email='ikpeleambroseobinna@gmail.com',
    description='A sentiment analysis tool for the Nigerian stock market using news and social data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ambroseikpele/Nigeria-Market-Sentiment-Analyzer',
    packages=["ngnewspapers"],
    install_requires=[
        'fastapi',
        'uvicorn',
        'beautifulsoup4',
        'requests',
        'pandas',
        'numpy',
        'scikit-learn',
        'transformers',
        'torch',
        'tqdm',
        'fake-useragent'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license='CC BY-NC 4.0',
    python_requires='>=3.8',
    include_package_data=True,
)
