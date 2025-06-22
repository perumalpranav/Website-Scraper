# RoyalRoad EPUB Downloader

A Python-based tool for scraping and converting serialized web novels from RoyalRoad into EPUB format. This utility automates the process of fetching chapters, extracting text, and compiling them into a complete ebook.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Architecture](#architecture)
* [Setup Instructions](#setup-instructions)
* [Usage](#usage)
* [Future Enhancements](#future-enhancements)
* [License](#license)

---

## Overview

**RoyalRoad EPUB Downloader** is a command-line Python script that automates the creation of EPUB files from RoyalRoad novels. It prompts the user for book metadata and fetches chapters sequentially starting from a given URL. The content is parsed using BeautifulSoup and compiled into a clean, readable EPUB using the `ebooklib` library.

---

## Features

1. **Interactive CLI**:

   * Prompts the user for necessary metadata including title, identifier, number of chapters, cover image URL, and starting URL.

2. **Chapter Scraping**:

   * Fetches each chapter’s title and content using HTML class selectors.
   * Automatically locates and follows the “Next Chapter” link to proceed through the novel.

3. **EPUB Creation**:

   * Generates structured chapters and a Table of Contents.
   * Embeds a user-specified cover image.
   * Outputs a ready-to-read `.epub` file compatible with major readers.

4. **Error Logging**:

   * Provides clear logging messages when chapters or cover images fail to load.

---

## Technologies Used

* **Programming Language**: Python 3
* **HTTP Requests**: `requests`
* **HTML Parsing**: `BeautifulSoup` (`bs4`)
* **EPUB Generation**: `ebooklib`
* **Target Website**: [RoyalRoad](https://www.royalroad.com)

---

## Architecture

1. **User Input**:

   * Gathers metadata such as book title, filename, and total chapters via the command line.

2. **Scraping Module**:

   * Uses `requests` to fetch HTML content.
   * Parses chapters using BeautifulSoup to extract titles, text, and the next chapter’s URL.

3. **EPUB Compilation**:

   * Uses `ebooklib.epub` to generate structured chapters.
   * Assembles the book spine, navigation, and styling into a single EPUB file.

4. **Output**:

   * EPUB file saved to the current working directory.

---

## Setup Instructions

1. **Clone the Repository** (if applicable):

   ```bash
   git clone https://github.com/yourusername/royalroad-epub-downloader.git
   cd royalroad-epub-downloader
   ```

2. **Install Required Packages**:

   ```bash
   pip install requests beautifulsoup4 ebooklib
   ```

3. **Run the Script**:

   ```bash
   python3 royalroad_downloader.py
   ```

---

## Usage

1. When prompted:

   * Enter a unique ID string for the book.
   * Provide a title and the number of chapters to download.
   * Paste the URL of the first chapter.
   * Provide a cover image URL from the book’s main page.
   * Specify the desired output filename.

2. Wait for the script to process each chapter.

3. The resulting EPUB will be saved in the working directory.

**Note**: The script is tailored to RoyalRoad’s HTML structure. It may require updates if the website layout changes.

---

## Future Enhancements

* Add GUI for user-friendly experience.
* Include progress tracking and error retry mechanism.
* Expand support for other online novel platforms (e.g., ScribbleHub, Wattpad).
* Implement chapter range selection (e.g., chapters 10–50 only).
* Add metadata fields (e.g., tags, genres, synopsis) via user input or scraping.

---

## License

This project is licensed under the GNU General Public License v3. See the [LICENSE](LICENSE) file for details. By using this project, you agree to comply with the terms of the GPLv3, ensuring that any derivative works remain open-source and provide the same freedoms to others.
