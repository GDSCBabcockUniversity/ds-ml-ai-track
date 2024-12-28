# DIY Analytics

DIY analytics is a Streamlit-based app that allows users to interact with their datasets using natural language queries and click and drop functionalities. 

## Try it Out
To try out the current version of DIY analytics: 
- Go to this link: [DIY Analytics App](https://diy-analytics-gdg-bab.streamlit.app/)
- Upload your dataset and the magic begins :)

## Open Source Challenge

This repository is part of **GDG Babcock Data and AI Track Open Source Challenge** aimed at collaboratively improving, customizing, and expanding this project.

We welcome contributions to enhance functionality, improve performance, add features, or fix bugs. 

---

## 🖥️ **Prerequisites**  
Before contributing, ensure you have the following:  
1. **Python 3.9+** installed.
2. A well setup development environment i.e. VS Code, Conda, Python virtual environment
3. Basic familiarity with important Python libraries:
    - **Streamlit** for the interface
    - **Pandas** for data wrangling.
    - **Matlplotlib, Seaborn, Plotly, and more** for data visualization
4. Basic knowledge of LLMs (Open source LLMs) and prompt engineering
5. GROQ API key which you can get for free from: [Groq Cloud](https://console.groq.com/keys)
6. A GitHub account to fork and clone this repository.
7. Git installed on your system   6
---

## 🚀 **Getting Started**  
Follow these steps to set up the project locally and start contributing:  

### 1. **Clone the Repository**  
```bash
git clone https://github.com/GDGBabcockUniversity/ds-ml-ai-track.git
cd diy-analytics
```

### 2. **Install Dependencies**  
Create a virtual environment (optional but recommended) and install the required Python libraries:  
```bash
pip install -r requirements.txt
```
### 3. **Add your GROQ API Key to the Environment**
Create a folder `.streamlit`. Create a file inside it `secrets.toml`. Inside the file, put your GROQ API KEY as follows:
```secrets.toml
GROQ_API_KEY='gsk_groq_api_key'
```


### 4. **Run the Application**  
Launch the Streamlit app:  
```bash
streamlit run app.py
```

### 5. **Explore the Code**  
Understand the project structure and how different modules like `execute.py`, `llm.py`, and `summary.py` work.

---

## 🤝 **How to Contribute**  
We’re thrilled to have you on board! Here’s how you can help:  

### 1. Fork and Clone  
Fork the repository, clone it locally, and create a new branch for your feature/bug fix.  

### 2. Develop  
Add your contribution while adhering to coding standards and best practices.  
- Ensure the app remains user-friendly and efficient.  
- Update the README if your contribution impacts usage.

### 3. Test  
Test your changes thoroughly to avoid breaking the app.  

### 4. Submit a Pull Request  
Push your changes to your forked repository and submit a pull request with a detailed description of your contribution.  

---

## 🎯 **Challenge Ideas**  
These are some ideas for features to work on:   
- Implement automated data cleaning
- Add support for more dataset formats
- Automated Exploratory Data Analysis

---

## 📝 **License**  
This project is licensed under the MIT License.  

---

## 💬 **Questions or Suggestions?**  
Feel free to create an issue or start a discussion in the **Issues** tab. We’d love to hear your thoughts!  

Happy Coding! 🎉 
