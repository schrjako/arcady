# arcady

## How to run

### Prerequisites
- **git**: You can download it from its official [website](https://git-scm.com/) or using your preferred package manager
- **python 3.9+**: You can download it from its official [website](https://www.python.org/downloads/) or using your preferred package manager

In order to run the game for the first time follow steps bellow (unix based):

- **Clone the repository**:
  ```bash
  git clone https://github.com/schrjako/arcady.git
  cd arcady
  ```
- **Create virtual enviroment**: Virtual enviroment is useful for keeping installed libraries separated. Create it with ``{python path} -m venv ./venv`` and than activate it with ``source venv/bin/activate``
- **Download the necessary libraries**: ``pip install -r requirements.txt``
- **Run main.py**: Run ``python main.py``

Once you did that, all you need to do to run it again is:

- If you closed the terminal **activate virtual enviroment** again: ``source venv/bin/activate``
- **Run main.py**: ``python main.py``
