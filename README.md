# Generative AI Idea Validator for Circular Economy

## Product Demo

## Presentation Slides

## Overview

The Generative AI Idea Validator for Circular Economy is a cutting-edge tool that automates the assessment of circular economy ideas. Leveraging the power of OpenAI GPT-4, the tool generates detailed reports, classifies ideas, and provides insights into sustainability, business viability, impact, and innovation aspect of the ideas.

## How does it work

1. Input Problem and Solution / PDF
2. Click "Process Input"
3. Model will be run and a report will be generated featuring the following areas: 
    - Overview of the problem and idea
    - Relevant Industries
    - Sustainability Analysis
    - Business Assessment 
    - Impact and Innovation Analysis
4. Within the key featured areas, ratings will be shown with some suggested follow-up questions
5. Continue with your follow-up questions to understand more about the idea and more

## Technical Implementation

1. Generative AI: Leveraged OpenAI GPT-4 pre-trained model for generating answers. Called OpenAI Assistant API to enable continuous responses to maintain context of previous messages in threads. Prompt engineering instructions and responses to structure the report. 
2. Front-end Management: Utilized Streamlit for an interactive front end.
3. Data Sources: Used various circular economy ideas with problem and solution for model testing and development.

## Getting Started



1. **Clone Repository** 
```bash
git clone git@github.com:brianchanbc/GenAIEarthHack.git
cd GenAIEarthHack
```

2. **Install Dependencies** 
```bash
python -m venv earthhack
activate earthhack
pip install -r requirements.txt 
```

3. **Insert OpenAI API Key**
```bash
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

4. **Run App**
```bash
streamlit run app.py
```

## Contributions

Brian Chan, Samantha Yom, Po-Ju Chen, Ya-Wei Tsai from the University of Chicago

## License

This project is licensed under the [MIT License](LICENSE).
