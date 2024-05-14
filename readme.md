<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">ASCII-GEN</h1>
</p>
<p align="center">
    <em>Quickly Converting media to ASCII!</em>
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

The ASCII-gen project is an open-source software designed to convert image sequences into ASCII art animated GIFs. It relies on required packages specified in `requirements.txt`, including multimedia handling tools and threading libraries. The Linux installer script sets up necessary dependencies for seamless execution. With a user-friendly graphical interface, ASCII-gen extracts frames from input sources, processes them using multi-threading, converts images to text format, merges frames into optimized GIF outputs, and offers options for display or saving.

---

##  Features

|    | Feature          | Description                                                |
|----|------------------|------------------------------------------------------------|
| ⚙️  | Architecture     | Python-based project with clear separation of GUI and image processing logic.                       |
| 🔩 | Code Quality      | Well-structured codebase with readable functions and good documentation.                         |
| 📄 | Documentation    | The repository contains detailed comments and instructions.                               |
| 🔌 | Integrations     | Depends on multiple packages like requests, PySimpleGUI, Pillow, and moviepy for multimedia handling.|
| 🧩 | Modularity       | Functions and scripts are logically separated into different files.                         |
| 🧪 | Testing         | No apparent testing framework is mentioned in the project.             |
| ⚡️  | Performance      | Processes images in parallel using multithreading to increase efficiency.                   |
| 🛡️ | Security        | Uses Python's standard security features and does not seem to handle sensitive data.          |
| 📦 | Dependencies     | Lists several Python packages and libraries in `requirements.txt` for installation.           |
| 🚀 | Scalability      | No information provided about its scalability or handling large files or traffic.         |

---

##  Repository Structure

```sh
└── ASCII-gen/
    ├── ascii-image-converter.exe
    ├── examples
    │   ├── fractal.gif
    │   ├── purple haze.gif
    │   ├── static haze rain.gif
    │   ├── tesseract.gif
    │   └── vortex.gif
    ├── gifsicle.exe
    ├── gui.py
    ├── installer-linux.sh
    └── requirements.txt
```

---

##  Modules

<details closed><summary>EXPAND</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [requirements.txt](https://github.com/KillaMeep/ASCII-gen.git/blob/master/requirements.txt)     | In this `requirements.txt` file, necessary packages for the ASCII-gen project are specified. These include certifi for SSL certificates, colorama for colored output, imageio and moviepy for handling multimedia files, and others such as idna, numpy, PySimpleGUI, requests, tqdm, and urllib3. The installation of these packages enables the functionality of ASCII-gens image conversion and GUI features.                                                                                                                                                                         |
| [installer-linux.sh](https://github.com/KillaMeep/ASCII-gen.git/blob/master/installer-linux.sh) | Installs required dependencies for running the ASCII-gen repository on Linux systems. Sets up ASCI-image-converter package along with gifsicle and Python3-tk, ensuring smooth execution of the projects conversion and GUI functionalities.                                                                                                                                                                                                                                                                                                                                   |
| [gui.py](https://github.com/KillaMeep/ASCII-gen.git/blob/master/gui.py)                         | Extract desired frames.2. Save each frame as PNG.3. Use multithreading for faster processing.4. Convert PNG to ASCII using ascii-image-converter.5. Merge frames into a single GIF file.6. Optimize the final GIF output.7. Display or save the generated GIF.8. Optional: clean up extracted files.Continue generating frames in parallel using multithreading. Convert each PNG frame to ASCII format, merge frames into a GIF file with infinite loop, optimize, and save it as output.gif. Optionally, display or launch the generated GIF in a viewer, then delete extracted files. |

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
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run ASCII-gen using the command below:
> ```console
> $ python gui.py
> ```


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

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/KillaMeep/ASCII-gen.git/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=KillaMeep/ASCII-gen.git">
   </a>
</p>
</details>

---



[**Return**](#-overview)

---
