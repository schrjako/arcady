# Arcady

## How to run

### Prerequisites

- **git**: You can download it from its official [website](https://git-scm.com/)
  or using your preferred package manager.
- **python 3.9+**: You can download it from its official
  [website](https://www.python.org/downloads/) or using your preferred package
  manager.

When running stuff on Windows install [git-bash](https://gitforwindows.org/) for
a somewhat proper commandline interface and working python.

In order to run the game for the first time follow steps bellow:

1. **Clone the repository**:
    ```bash
    git clone git@github.com:schrjako/arcady.git
    cd arcady
    ```

2. **Create virtual enviroment**: Virtual enviroment is useful for keeping
  installed libraries separated. Create it with
    ```bash
    {python path} -m venv ./venv
    ```
    and than activate it with
    ```bash
    source venv/bin/activate        #   on linux
    source venv/Scripts/activate    #   on Windows
    ```

3. **Download the necessary libraries**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run main.py**:
    ```bash
    python main.py
    ```

If the shell doesn't find python you can try to find it with:
    ```bash
    which python
    ```

After the first time when setting up the clone and environment, you just have to
**activate virtual enviroment** again (`source venv/bin/activate`), install
aditional requirements (`pip install -r requirements.txt` if `requirements.txt`
changed) and you're good to go (you can **run main.py**: `python main.py`).
