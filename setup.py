import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Recsys MADE project",
    author="DreamTeam",
    author_email="theo.lisin@gmail.com",
    description="MADE Python project",
    keywords="Python, MADE, recsys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheoLisin/recsys_MADE",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version="0.1.0",
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 1 - Alpha",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib",
        "pandas",
        "nltk",
        "numpy",
        "seaborn",
        "scikit-learn",
        "wordcloud",
        "bertopic",
        "gensim",
        "contextualized-topic-models",
        "bokeh",
        "mycolorpy",
        "typer",
        "sqlalchemy",
        "fastparquet",
        "psycopg2-binary",
        "mariadb==1.1.3",
        "alembic",
        "python-dotenv",
        "bcrypt",
        "fastapi",
        "pyspark",
        "pymysql",
        "uvicorn",
        "Jinja2",
    ],
    extras_require={
        "dev": [
            "wemake-python-styleguide",
            "mypy",
            "black",
        ],
        "tests": [
            "pytest",
            "pytest-dotenv",
        ],
    },
    entry_points={
        "console_scripts": [
            "recsys-db = db.__main__:main",
            "recsys-api = api.__main__:main",
        ],
    },
    package_data={
        "static": ["*.css"],
        "templates": ["*.html"],
    }
)
