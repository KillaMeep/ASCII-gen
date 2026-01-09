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
- [ Modules](#modules)
- [ Getting Started](#getting-started)
  - [ Installation](#installation)
  - [ Usage](#usage)
</details>
<hr>

##  Overview

ASCII-gen is an open-source image-to-ASCII converter that allows users to transform images into text art, making it an essential tool for creatives and developers alike. The projects core functionality includes extracting frames from videos or loading images, converting them to ASCII art, and optimizing the output GIF for both quality and size. The project is written in Python and is compatible with Linux, and Windows systems.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project runs in a GUI using tkinter (built into Python - no paid dependencies)|
| 🔌 | **Integrations**  | The project integrates external libraries such as `Pillow`, `moviepy`, `tkinter`, `numpy`, `imageio`, and more.|
| 🧩 | **Modularity**    | The project's structure is modular with each functionality separated into a dedicated Python script, enhancing code organization, reusability, and maintenance.|
| ⚡️  | **Performance**   | Written to work dynamically with multithreading. |
| 📦 | **Dependencies**  | The project depends on various external libraries and frameworks, listed within the `requirements.txt`.|

---

##  Modules

<details open><summary>Expand</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                                                                        |
| [requirements.txt](https://github.com/KillaMeep/ASCII-gen.git/blob/master/requirements.txt)     | Install crucial dependencies for the ASCII-gen project. The requirements file lists necessary packages including colorama, decorator, imageio, moviepy, numpy, pillow, proglog, termcolor, tqdm. These packages support features such as image processing, GUI development, and video processing. tkinter is used for the GUI and is built into Python. |
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
