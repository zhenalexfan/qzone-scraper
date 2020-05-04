# qzone-scraper

如果你有很多年少的记忆以「说说」的形式发表在 [QQ 空间](https://qzone.qq.com/)，qzone-scraper 可以帮你把这些记录备份到本地。qzone-scraper 是一个用于将自己的 QQ 空间「说说」备份在本地成一个 JSON 格式文件的的工具，它也可用来下载所有「说说」内包含的图片。

## 使用方法

### 预备

1. 确保你的电脑装有 [Python](https://www.python.org/)。
2. 确保你的电脑装有 [Chrome 浏览器](https://www.google.com/chrome/)。
3. 确保你的电脑装有与 Chrome 浏览器对应的 WebDriver（即 ChromeDriver）。
    * 如果你不知道 ChromeDriver 是什么，它是一个使计算机程序可以自动化控制 Chrome 浏览器操作的驱动。
    * 点击[这个链接](https://chromedriver.chromium.org/downloads)可以下载和你的 Chrome 版本相对应的 ChromeDriver。
    * 下载 ChromeDriver 后，确保把它放在电脑的环境变量 `PATH` 内——通常可以是 `/usr/bin` 或 `/usr/local/bin` 这样的地方。这样程序才能找到它。如果你没有放在准确的地方，执行下面的步骤时你会得到一个 `selenium.common.exceptions.WebDriverException` 的错误信息。

### 运行程序

1. 把这个 Repository（代码仓库）clone 到你的电脑上。在命令行运行
    ```
    git clone --depth 1 git@github.com:zhenalexfan/qzone-scraper.git
    ```
2. 使用 `cd qzone-scraper` 进入这个代码仓库的根目录，然后运行
    ```
    python -m qzone-scraper
    ```
3. 根据命令行出现的提示进行操作。

    通常，你会被询问你的 QQ 号码和总说说数量，然后等到命令行提示登录 QQ 空间时，在弹出的网页窗口里输入密码进行登录。等到登录后的页面加载完全后，再在命令行按任意键继续。爬取你的 QQ 空间说说的过程将会在这时开始。

4. 大功告成。输出的文件包括
    * JSON 格式的你的所有说说 `out/shuoshuo_list.json`；
    * `img/` 路径下的所有图片。JSON 格式说说里的原始链接和这些图片的路径对应存在于 `img/download.json` 下。
