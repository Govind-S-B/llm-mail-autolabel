import os
import requests
import json

def mail_processor(user_info, label_mapping, mail_body, llm_online=False, api_key=None):
    """
    Classifies the given email and returns an appropriate label and reason.

    Args:
        user_info (str): Information about the user, including their persona, preferences, and what they value in emails.
        label_mapping (Dict[str, str]): A dictionary mapping labels to their descriptions or use cases.
        mail_body (str): The content of the email to be classified.
        llm_online (bool, optional): If True, uses the Google Palm API for classification.
                                     If False, uses a local LLM (OpenHermes 2.5-Mistral) via Ollama.
                                     Defaults to False.
        api_key (str, optional): Required for llm_online mode. The API key for the Google Palm API.
                                 Defaults to None.

    Returns:
        Tuple[str, str]: A tuple containing the label and reason for the classification.
    """

    prompt = """
    You are an expert email categorizing AI model that can understand and think about the user intentions behind an email and label things accordingly

    Given the following user
    ```
    {}
    ```

    According to the label specifications below
    ```
    {}
    ```

    For the email content
    ```
    {}
    ```

    Classify the email content into a json format
    {{
    "label": <one of the labels specified earlier> ,
    "reason": <why the given email was classified as the label category>
    }}

    Return only the json
    """.format(user_info, label_mapping, str(mail_body)[0:1000])
    print(prompt)

    if llm_online:
        url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"prompt": {"text": prompt},"temperature": 0},
            params={"key": api_key}
        )

        # print(prompt)
        # print(f"Response: {response.json()}\n")
        # print(response.json()['candidates'][0]['output']) # Print the response

        if 'candidates' not in response.json():
            raise ValueError("Invalid response from Google PALM API")
        
        response = json.loads(response.json()['candidates'][0]['output'].replace("json","").replace("```",""))
        label, reason = response["label"], response["reason"]

    else:
        url = "http://localhost:11434/api/generate"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={'model': 'openhermes2.5-mistral', 'prompt': prompt, 'format': 'json', 'options': {'temperature': 0, 'top_k': 10}, 'stream': False} ,
        )

        response = json.loads(json.loads(response.text)["response"])
        label, reason = response["label"], response["reason"]

    return label, reason

if __name__ == "__main__":

    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("PALM_API_KEY")

    print(mail_processor(
        user_info = 
        """
        I am a Software Engineering Student and I am right now on the lookout for work oppoprtunitites and advancing my carrer.
        I want my mails to be focused on that goal and streamlined, I really dont want to see spammy promotional mails
        """,
        label_mapping =
        {
            "Job" : "any work related email should go here",
            "Personal" : "any personal communication from friends or family",
            "Trashy" : "All Promotional Emails and Spam",
            "Bills" :  "All invoices or finance related things",
        },
        mail_body = 
        """
        Hello, dnivog.

        You are welcome to register and compete in Codeforces Round 913 (Div. 3). It starts on Tuesday, December, 5, 2023 14:35 (UTC). The contest duration is 2 hours 15 minutes. The allowed programming languages are C/C++, Pascal, Java, C#, Python, Ruby, Perl, PHP, Haskell, Scala, OCaml, Go, D, JavaScript, Rust and Kotlin.

        Div. 3 rounds are designed especially for participants with a rating below 1600. We invite you to participate in the competition!

        The goal of such rounds is to help beginner participants to gain skills and to get new knowledge in a real contest. You can read the details in this post dedicated to them. In short:

        Not only real problems, but also exercises can be used.
        Our main goal is to give nice training problems, so we do not care much about the innovativeness of the problems.
        Often the formal text of the statements.
        Rated for participant with the rating below 1600.
        ICPC rules + 12-hour open hacking phase.
        Untrusted participants are not included in the official ranklist.
        The round will be held on the rules of Educational Rounds, so read the rules (here) beforehand. The round will be for newcomers and participants with a rating below 1600. Want to compete? Do not forget to register for the contest and check your handle on the registrants page. The registration will be open for the whole contest duration.

        If you have any questions, please feel free to ask me on the pages of Codeforces. If you no longer wish to receive these emails, click https://codeforces.com/unsubscribe/contests/49a4594bc46bb9a8d383b2bf91dea7b0f3d201a5/ to unsubscribe.

        Wish you high rating,
        MikeMirzayanov and Codeforces team
        """,
        llm_online=True,
        api_key=api_key
    ))