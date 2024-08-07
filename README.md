Notice: the development has paused while I am in school, the project has not been abandonned -- *yet*. All contributions are welcome!

Meanwhile, you can check out these alternatives:
- [Goldwarden (GitHub)](https://github.com/quexten/goldwarden)
- [BitRitter (Codeberg)](https://codeberg.org/Chfkch/bitritter)

# Bitsteward
## If you want to try out Bitsteward, it is highly recommended that you use a vault with data that you do not mind being considered leaked. The current implementation is *not* secure, and any program could potentially see all your vault items. (The screenshots are from a Bitwarden vault created specifically for the development of this application)

Bitsteward is a very early alpha Bitwarden client made with GTK4 and Libadwaita. It is NOT secure at the moment

## This application is released under the GNU General Public License version 3.
This means you need to make the code open to the public with the same license (GPLv3) as the one the project currently uses. You can modify, publish, use commercially as long as clear credit is given and the code remains open and licensed under GPLv3. By using the application and the code, you agree to the [license](https://github.com/Bitsteward/bitsteward/blob/master/COPYING).

🚧 The readme is under construction! 🚧

## How to run
The first step is to clone the repo in a terminal
```bash
git clone https://github.com/Bitsteward/bitsteward.git
cd bitsteward
```
Then, you need to login to a Bitwarden account (I recommend creating a new one to test this app as it is not yet secure)
```bash
chmod +x bw
./bw login
```
Then fill in the steps to login as the prompt tells you.
Then you will need to copy your Bitwarden master password into the .env.
To do that, modify the following command to replace {Bitwarden Master Password} including the brackets with your master password.
```
echo 'BW_PASSWORD="{Bitwarden Master Password}"' >> .env
```
<details>
    <summary><b>Here is an example of what the command should look like</b></summary>
    
    echo 'BW_SESSION="password123"' >> .env
</details>

After that is done, install the python dependencies
```
pip install -r requirements.txt
```
The last step is to start the application!
```
python3 src/main.py
```


<details>
    <summary><h2>Screenshots</h2></summary>

<picture>
  <source srcset="/screenshots/full-dark-1.png?raw=true" media="(prefers-color-scheme: dark)">
  <img src="/screenshots/full-light-1.png?raw=true" title="App with two columns" alt="screenshot-desktop">
</picture>
    
<picture>
  <source srcset="/screenshots/mobile-dark-1.png?raw=true" media="(prefers-color-scheme: dark)">
  <img src="/screenshots/mobile-light-1.png?raw=true" title="App with one column (mobile view)" alt="screenshot-mobile">
</picture>
</details>
