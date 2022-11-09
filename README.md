# Electree

<!-- ABOUT THE PROJECT -->
## About The Project

Electree is an API for getting the family tree from Electoral Roll of various state. It works by parsing the pdf for getting the data and making an entry for the same in a MongoDB Database, Further, a Node Server spins up to query the data.

### Built With
Built Using Languages and Libraries Listed Below 
* [Python](https://docs.python.org/3/)
* [NodeJS](https://nodejs.org/en/docs/)
* [mongodb](https://www.mongodb.com/docs/)
* [pytesseract](https://pytesseract.readthedocs.io/en/latest/)
* [pillow](https://pillow.readthedocs.io/en/stable/)
* [pdf2image](https://pypi.org/project/pdf2image/)

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
```sh
git clone https://github.com/decipher07/Electree.git
```
2. Install Python packages
```sh
pip install -r requirement.txt
```
3. Create a dotenv file with values defined (Make sure that your MongoDB Instance is working)

4. Run the converter.py for scanning the pdf and storing the data
```Python
python converter.py
```

5. Spinup the Node Server
```sh
cd server/
npm start
```

---
[![API Docs ](https://img.shields.io/badge/API%20Docs-View%20Here-orange?style=flat-square&logo=appveyor)](https://documenter.getpostman.com/view/10696212/2s8YehUH4m)

[Project Walkthrough Video](https://drive.google.com/file/d/18_lOqhQCygkMvPlSTzTNGvJtRUIgWuWZ/view?usp=share_link)


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact Me

**Deepankar Jain -** 

[LinkedIn](https://www.linkedin.com/in/deepankar-jain-3997551a9/)

[Email](social.deej@gmail.com)

**Project Link -** [GitHub](https://github.com/decipher07/Electree.git)


