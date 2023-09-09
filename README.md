# English Teacher Project
A Digital Sciences for Hi-Tec final project by TUKI:<br>
* Sahar Machavy<br>
* Omri Shmueli<br>

And guided by Martin Raskin

## Description
Using voice detection, text-to-speech (gTTS), a large language model (PaLM API), and a transcription service (Faster-Whisper), we have created a holistic experience to improve English speaking.<br>
The product aspires to serve those who seek to improve their spoken language skills with a conversation-based approach. It also includes a testing module that grades the user based on their fluency, grammar, and ability to provide certain information.

## Installation 
1. Clone this repository.
2. Install Python and a IDE (VS Code or PyCharm).
3. Install MySQL from the following link - https://dev.mysql.com/downloads/installer/ <br>
   a. Follow the installation process. <br>
   b. Use "root" user and define it's password to be "password123" or any password of your choice (required to be configured later in the configuration.json file)
4. Create a dedicated virtual environment and install the requirements from the .txt file using `python pip install -r requirements.txt`
5. Set an environment variable named "PALM_API_KEY" with it's value set to your PaLM API key taken from here- https://developers.generativeai.google/tutorials/setup <br>
    *A reboot might be required
