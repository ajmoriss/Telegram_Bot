## Telegram Bot
In a few words, our bot will give us the price of cryptocurrency, that we need. We're gonna ask him about particular cryptocurrency and bot will return us a price of searched cryptocurrency from 
[CoinMarketCap](https://coinmarketcap.com/). Bot will be deployed on [PythonAnywhere](https://www.pythonanywhere.com). As a request handler we're gonna use **Flask**. List of steps below will help you to create our bot from scratch step by step.

#### Step 1(BotFather)
1. Open a desktop version of Telegram and find BotFather on the search bar.
2. A command `/newbot` is needed to start creating a new bot.
3. Type the name of the bot and his _username_.
4. Receive the **Access Token** for our bot.

#### Step 2(PythonAnywhere)
1. First of all we need to create an account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Follow to our profile, click on **Consoles** section and create a new Bash Console.
3. Find out the version of _python_ and _pip_. After that, create a new _virtual environment_. As soon as it's created, _Activate_ it.
4. Open a new tab in your browser and follow the **Files** section. In this section we need to create our working directory and upload to it _requirements.txt_ file with all project dependencies. If everything is done, we need to install dependencies from _requirements.txt_ in our Activated virtual environment.
5. Follow the **Web** section and click on "Add a new web app". Choose "Manual configuration" and in **Code** section on this page below, we need to specify _path to web app_ and _path to virtualenv_.

**Keep an eye on Error log file. Server errors will be written right in this file.**

6. Whether each step before this one is passed completely, we need to change some configuration in _WSGI configuration file_. In this file we need to scroll down and find a block like 
"+++++++++++ FLASK "+++++++++++". In this block, we should uncomment and rewrite such lines

`# import sys`

`# path = '<path_to_app>'`

`# if path not in sys.path:`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
`# sys.path.append(path)`

`# from main import app as application`

Our python script will be named _main.py_ so we need to specify it in line 5.

7. Save the file.
8. Click on **Web** section and check if our application works. But before we upload our _main.py_ script in our working directory on [PythonAnywhere](https://www.pythonanywhere.com), it will not work and it's OK. So you could create a simple python script like

`from flask import Flask`<br>
`from flask_sslify import SSLify`

`app = Flask(__name__)`<br>
`sslify = SSLify(app)`

`if __name__ == '__main__':`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
`app.run()`

If smth goes wrong, first of all try to check **Error log** file!

#### Step 3(Establishing HTTPS-connection)
To provide HTTPS-connection with our bot, we need to install `flask-sslify` extension(This extension is specified in _requirements.txt_ file). So in _main.py_ file we just need to import `SSlify` class from `flask-sslify` module and pass to this class `app` object of our application. It might sound confusing, but everything will be described in ready to use _main.py_ script.

Once _main.py_ is finished, we need to upload it to [PythonAnywhere](https://www.pythonanywhere.com). But It's not gonna work yet. We need to connect our application with Telegram using **Webhook**. To implement it, we need to create a special url, similar to the template below.
`https://api.telegram.org/bot{ACCESS_TOKEN}/setWebhook?url={YOUR_APP_URL}`. 

For example:<br>
`https://api.telegram.org/bot726667283:sjfytnvk38foavzRdFrPBPBhH_72Ql6elTQ/setWebhook?url=https://johndoe.pythonanywhere.com/`

As soon as you paste your data and follow this link, Web hook will be set. So now you can test your bot functionality. Try to send a message to the bot like `/ripple`. Bot will return you the price of _ripple_ from [CoinMarketCap](https://coinmarketcap.com/).
