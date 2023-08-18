# Project Name: TalkDocument
![Demo Video](docs/video/video_demo.mp4)

# Description
The Interactive Document Query System project offers a dynamic web application that empowers users to inquire about documents available in PDF, TXT, or URL formats. Behind this project lies a robust technological stack, including embeddings, vector storage, distance calculation algorithms like FAISS, and a large language model for facilitating user-document interactions.

![Schema](docs/img/schema.png)

# Project Structure
The project is organized as follows:

```
TalkDocumentProject
├─ .streamlit
│  └─ config.toml
├─ .vscode
├─ data
│  ├─ test.pdf
│  └─ test.txt
├─ docs
│  └─ img
├─ README.md
├─ requirements.txt
├─ src
│  ├─ Home.py
│  ├─ pages
│  │  ├─ 1_Step 1️⃣ Create Data Base.py
│  │  ├─ 2_Step 2️⃣ Ask to the document.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ qa_tool.py
│  ├─ style.py
│  ├─ utils.py
│  ├─ __init__.py
│  └─ __pycache__
└─ __pycache__
```

- The .streamlit directory contains the Streamlit configuration file config.toml for customizing the web application's behavior.
- The data directory holds sample documents (test.pdf and test.txt) that will be used for creating the database and querying.
- The docs directory is intended for documentation-related assets, such as images.
- 'README.md' (this file) is the project's main documentation file.
- 'requirements.txt' lists the required Python packages for setting up the project environment.
- The src directory contains the main source code for the project.
    - Home.py likely represents the main application entry point or landing page.
    - The pages directory includes the implementation for different steps/pages of the application.
    - qa_tool.py defines the TalkDocument class responsible for creating the database and handling queries.
    - Other utility files like style.py and utils.py might provide styling and helper functions, respectively.

# Requirements
To successfully utilize the Interactive Document Query System, you must satisfy the following prerequisites:

- [!IMPORTANT] A free API key from Hugging Face Hub: The system employs Hugging Face models for embedding and vector storage. Obtain your API key by registering on the Hugging Face website.

- [!IMPORTANT]Optionally, an API key from OpenAI (if using OpenAI embedding): If you choose to utilize OpenAI's embedding model, you'll need an OpenAI API key. Register on the OpenAI platform to acquire your key.

# Getting Started
To launch the application, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Open your terminal and navigate to the project's root directory.
4. Run the following command:

```
streamlit run yourpath/TalkDocument/src/home.py
```
# Credits
This project was developed by Damián Gil González.

