# BLUBO
"Blubo" is an advanced sensor for monitoring light pollution in various environments, using Hamamatsu S2386-5K photodiodes and custom transimpedance amplifiers to measure sky brightness. Essential for environmental research and crafting sustainable lighting policies.

## How to setup:

1. On a clean installation of Raspbian 11 Bullseye, install Git and download the repo:
```
git clone https://github.com/joleiv/blubo.git
```
2. After the installation is complete, you must set the file as an executable. Open terminal and run the following code:
````
cd blubo

chmod +x blubo-setup.sh

./blubo-setup.sh
````
3. Follow the instructions in the script.
