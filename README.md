Frostcode Hackathon 2023 Winner!  
[Note: this project used PaLM AI which has since been discontinued by Google] 

# llm-mail-autolabel
Given a user persona and a list of labels and their descriptions will go through your emails and then tag them with the appropriate label in Gmail . It uses the Gmail API and Google's PaLM AI under the hood but for the AI part , it is swappable with a local running LLM as well (for data privacy concerns) . It also will use Flutter for the GUI Layer

## The Why
Why I wrote it is because its often that our email inboxes get crowded with a lot of irrelevant mails thats hard to filter through , most gmail clients classify this into Primary Social and Promotions , but doesnt allow more personalized custom categorization of these emails based on their priorities.

This project aims to solve this problem . Here the user can tell what they are , What they focus on , and cut the noise and clear the clutter. The auto labeller will label mails based on the user specified tag and user persona  

## Implementation Specifics
Higher Level Back End Architecture  
  
![image](https://github.com/Govind-S-B/llm-mail-autolabel/assets/62943847/b2fb87a3-18a1-4b49-bd45-fe18637ebdc3)

- We tried to rely less on frameworks such as langchain and other AI frameworks since they were overkill, sticking to minimalism was a deliberate decision  
- Providing an alternative AI Model that runs locally for privacy concerns

This Repo focuses on the backend functionality of the Auto Labeller , the front end is in the works and at a very early stage  
  
![image](https://github.com/Govind-S-B/llm-mail-autolabel/assets/62943847/e583d3c1-5893-431a-8c5b-28f95016fb96)
- We decided to build this as a windows native application using flutter and using a unconventional file read-write system with sub process calls to the python process
- This is to avoid the additional overhead of having an API Server on both ends , which again seemed like an overkill for such a project
- Our focus is on having this run locally as an application and not a cloud first app

## Getting Started
### Prerequisites
- Google PaLM API Key , which you can obtain from here : https://makersuite.google.com/app/apikey  
- A `credentials.json` file for Gmail API Acess , instructions here : https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application  
You can set this up manually or just contact us and we will give your our credentials

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Govind-S-B/llm-mail-autolabel.git
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   Its highly suggested that you get a seperate venv for this.  

### Configuration

1. Place your `credentials.json` file (obtained from the Gmail API setup) in the project root directory.
2. Create a `.env` file in the project root directory with the following structure:

   ```env
   PALM_API_KEY=
   ```
3. Temporarily ( till the front end is up and running ) configure the user info in `user_info.json`

### Usage

1. Run the script:
   ```
   python auto_label.py
   ```
2. The script will process your emails and automatically apply the appropriate labels based on the configuration.
