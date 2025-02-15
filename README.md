# oscp_exam-ai-tips
A simple Python script that leverages Reddit’s API to collect success stories from OSCP exam takers. OpenAI’s GPT-4 then analyzes the data to identify 4 actionable tips that helped students pass. 

The idea came to me after seeing so many "I passed OSCP" Reddit posts. Most useful ones. So I decided to collect all data and let OpenAI to provide a meaningful advise, using the collected and succesful pass strategies of those students.

This project provides AI-driven insights to help future OSCP candidates improve their study approach. AI tips are for reference and never a replacement of Offsec PEN200 official course. 

Make sure python modules are installed prior execution. I used a virtual environment instead of regular "pip install". It is much more easier. Check Step #1.

** DO NOT SAVE API CREDENTIALS IN THE CODE , EVER **

## 🚀 Features

- 🔍 **Reddit Scraping**: Fetches OSCP-related success posts from the last two years.
- 🤖 **AI-Powered Analysis**: Uses GPT-4 to extract 4 key study strategies from past exam takers.
- 🏆 **High-Quality Insights**: Filters out low-value content to focus on actionable advice.
- 💰 **Cost-Efficient**: Running multiple tests with GPT-4 cost **less than $1 in total**.
- 🔐 **Environment Variables for Security**: No credentials are stored in the script.

---

## 📌 Prerequisites

- ✅ **Python 3** installed on your system.
- ✅ **A Reddit API account** to generate API keys.
- ✅ **An OpenAI API key** for GPT-4 access.
- ✅ **Basic knowledge of running Python scripts.**

---

## Usage

### 1. Setup a virtual environment

```bash
#pandas an openpyxl are optional
#I was trying to include LainKusanagi's list 
#Maybe in a later version.
python3 -m venv scraper
source scraper/bin/activate 
pip3 install praw 
pip3 install pandas
pip3 install openpyxl  
```

### 2. Setup API creds

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="your_user_agent"
export OPENAI_API_KEY="your_openai_api_key" 
```


### 3. Download the Script
Clone the repository or download the script directly:
```bash
git clone https://github.com/Y3llowDuck/oscp_exam-ai-tips.git
```

### 4. Run the Script

```bash
python3 ./scraper-v2.py 
```

## Example Output

Here’s an example of what running the script looks like:

**Script execution:**

![Example Output 1](https://github.com/Y3llowDuck/oscp_exam-ai-tips/blob/main/executing.png)

**AI generated OSCP pass tips:**

![Example Output 2](https://github.com/Y3llowDuck/oscp_exam-ai-tips/blob/main/tips.png)

AI Model Uses Probabilistic Outputs (Even with Low Temperature). So, AI suggestions may and will change every time the script runs. 













