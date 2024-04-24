from setuptools import setup, find_packages

setup(
    name='week-1_telecom_analysis',
    version='0.1',
    description='Telecom Analysis Project',
    author='Abraham Teka',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'plotly',
        'streamlit',
        'psycopg2',
        'sqlalchemy'
    ],
)
