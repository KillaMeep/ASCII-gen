<p align="center">
  <img src="https://github.com/KillaMeep/ASCII-gen/raw/main/examples/logo.png?raw=true" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">ASCII-GEN</h1>
</p>
<p align="center">
    <em>Quickly Converting media to ASCII!</em>
</p>

<br><!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary><br>

- [ Overview](#overview)
- [ Features](#features)
- [ Repository Structure](#repository-structure)
- [ Modules](#modules)
- [ Getting Started](#getting-started)
  - [ Installation](#installation)
  - [ Usage](#usage)
- [ Contributing](#contributing)
</details>
<hr>

##  Overview

ASCII-gen is an open-source image-to-ASCII converter that allows users to transform images into text art, making it an essential tool for creatives and developers alike. The projects core functionality includes extracting frames from videos or loading images, converting them to ASCII art, and optimizing the output GIF for both quality and size. The project is written in Python and is compatible with Linux, and Windows systems.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project mainly runs in a GUI using PySimpleGui|
| 🔌 | **Integrations**  | The project integrates external libraries such as `requests`, `Pillow`, `moviepy`, `tkinter`, `PySimpleGUI`, `urllib3`, `certifi`, `rsa`, `numpy`, and more.|
| 🧩 | **Modularity**    | The project's structure is modular with each functionality separated into a dedicated Python script, enhancing code organization, reusability, and maintenance.|
| ⚡️  | **Performance**   | Written to work dynamically with multithreading. |
| 📦 | **Dependencies**  | The project depends on various external libraries and frameworks, listed within the `requirements.txt`.|

---

##  Repository Structure

```sh
└── ASCII-gen/
    ├── ascii-image-converter.exe
    ├── examples
    │   ├── fractal.gif
    │   ├── logo.png
    │   ├── moai.png
    │   ├── purple haze.gif
    │   ├── static haze rain.gif
    │   ├── tesseract.gif
    │   └── vortex.gif
    ├── gifsicle.exe
    ├── gui.py
    ├── installer-linux.sh
    ├── readme.md
    ├── requirements.txt
    └── run.bat
```

---

##  Modules

<details open><summary>Expand</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                                                                        |
| [requirements.txt](https://github.com/KillaMeep/ASCII-gen.git/blob/master/requirements.txt)     | Install crucial dependencies for the ASCII-gen project. The requirements file lists necessary packages including certifi, colorama, decorator, idna, imageio, moviepy, numpy, pillow, proglog, PySimpleGUI, requests, rsa, setuptools, termcolor, tkinter, tqdm, urllib3. These packages support features such as image processing, GUI development, and network requests. |
| [installer-linux.sh](https://github.com/KillaMeep/ASCII-gen.git/blob/master/installer-linux.sh) | Installs essential dependencies for the Ascii-image-converter software on Linux systems. Configures package repositories, updates system packages, installs Ascii-image-converter, gifsicle, and Python dependencies.                                                                         |
| [gui.py](https://github.com/KillaMeep/ASCII-gen.git/blob/master/gui.py)                         | The main file. Does all of the GUI workload.                                                                     |
| [run.bat](https://github.com/KillaMeep/ASCII-gen.git/blob/master/run.bat)                       | Launches the Graphical User Interface (GUI) application for windows.                                                                                                                                                                        |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version 3.10 to 3.12`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the ASCII-gen repository:
>
> ```console
> $ git clone https://github.com/KillaMeep/ASCII-gen.git
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd ASCII-gen
> ```

###  Usage


> Run the program!:
> ```console
> $ run.bat
> ```
>
> If you're on Linux:
> ```console
> $ ./insaller-linux.sh
> $ pip3 install -r requirements.txt
> $ python3 gui.py




---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/KillaMeep/ASCII-gen.git/issues)**: Submit bugs found or log feature requests for the `ASCII-gen` project.
- **[Submit Pull Requests](https://github.com/KillaMeep/ASCII-gen.git/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/KillaMeep/ASCII-gen.git/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/KillaMeep/ASCII-gen.git
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>



---
