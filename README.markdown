Ubuntu Desktop 20.04.2 LTS

```bash
sudo apt install curl
# https://github.com/nodesource/distributions/blob/master/README.md
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# in directory proj
npm install puppeteer
```

Download word list txt file.

----

```bash
node login.js
```

Go to XinDongFang website and login. Then close.

```bash
node login.js
```

Go to XinDongFang website again. Verify still logged in.

----

```bash
mkdir articles
node fetch.js
```

