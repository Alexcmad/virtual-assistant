# A virtual assistant powered by GPT-3.5 in python (eventually)(It is now)


# To-do List of Features:
- Opening and closing applications.✅
- Setting reminders
- Fetching reminders
- Sending emails
- Fetching Emails
- Writing in txt files
- General Searching✅
- Voice controls✅🛑
- Voice activation
- Text to speech
- Small talk
- Calendar Management
- Todo list✅
- Translation✅
- spotify controls✅
- typing, scrolling, pressing enter✅
- pushing to git

# DEMOS:
### Date: 4/10/2023

https://user-images.githubusercontent.com/113714949/230833554-a53bc422-0766-4ee0-8ec6-7de90436645d.mp4


https://user-images.githubusercontent.com/113714949/230833558-feedf5fa-9baa-4608-957f-a9a9bcd050cb.mp4

![image](https://user-images.githubusercontent.com/113714949/230833657-34f327db-8004-4309-9060-a55195738a2e.png)

![image](https://user-images.githubusercontent.com/113714949/230833492-1abab432-cd52-4d84-9936-a8bf25494fbe.png)

![image](https://user-images.githubusercontent.com/113714949/230943377-07a423f7-09a9-4f0c-bd5a-8569a8ede041.png)

### Date: 4/11/2023

![image](https://user-images.githubusercontent.com/113714949/231106839-77290444-a263-4966-ab96-14199509ed47.png)
User has the choice to use either the fine-tuned model or GPT3.5-Turbo.
##### GPT3.5-Turbo:
- uses more tokens per command
- can be provided with conversation history to allow it to use context clues when interpreting natural language
- may very occasionally refuse commands or say 'okay,  [carrying out command]' which is not valid command format
- in the above event, conversation history can be manually reset with the command 'reset' or 'thank you' or 'thanks'
- conversation history automatically resets after a certain amount of commands

##### Fine-tuned GPT3-Davinci (as of today):
- uses much less tokens per command
- however, as a trade off, training the model uses a great deal of tokens. In the future, additional training should only be done when commands get added to save money 
- no conversation history
- very concise and only ever gives more than us required of it
- will not refuse commands, but may misinterpret them if the intention is not clear
- probably faster but needs a lot of training data to be as accurate as Turbo.

In all I prefer using turbo for the more natural interaction with message history, but in the later stages of this project I may train a really good davinci (or other) model and use it instead for the sake of my wallet. Don't know how training a turbo model would even work but it would be interesting to use if they make that possible.

##### Date 4/12/2023

![image](https://user-images.githubusercontent.com/113714949/231656242-5e85f1d4-e0bd-4b80-b6d7-87c157ebc2ac.png)

![image](https://user-images.githubusercontent.com/113714949/231656323-ac30e9b4-780c-41e3-9b46-75982cf91c18.png)
