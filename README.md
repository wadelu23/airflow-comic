# WSL-airflow

參考 [一段 Airflow 與資料工程的故事：談如何用 Python 追漫畫連載](https://leemeng.tw/a-story-about-airflow-and-data-engineering-using-how-to-use-python-to-catch-up-with-latest-comics-as-an-example.html#%E5%BB%BA%E7%BD%AE-Airflow-%E7%92%B0%E5%A2%83)

建置airflow並使用slack通知漫畫更新

本專案目前只記錄WSL的airflow建置流程，提供本機啟動後修改嘗試

因此關於 airflow 觀念可多參考[Airflow 動手玩](https://zh-tw.coderbridge.com/series/c012cc1c8f9846359bb9b8940d4c10a8/posts/6c90609c64c14df284f141b703c03702)

:bangbang::bangbang: 指令語法可能因套件版本改動，需使用對應版本的語法

---

這次使用 WSL 環境( ubuntu 2004 )建置 airflow

1. ubuntu 環境準備
    * `sudo apt-get update`

    * `sudo apt install python3-pip`

    * 安裝 Anaconda

---

2. clone repo
    * `git clone https://github.com/wadelu23/airflow-comic.git airflow-comic`
    
        指令中的 airflow-comic 可改成你方便的資料夾名稱

    * 進入資料夾
        `cd airflow-comic`

---

1. conda 虛擬環境
    * 建置新環境
    `conda create -n airflow-comic python=3.8 -y`
    * 啟動新環境
    `conda activate airflow-comic`
    
        這時你的終端機左邊會有(airflow-comic)
    
        注意:只要打開新的終端機，都要確認是在正確的conda環境
    
        如果你是用VScode，也要確認你的python Interpreter是正確的環境

    * 安裝相關套件

        `pip install "apache-airflow[crypto,slack]"`

        `conda install selenium`

    * 把AIRFLOW_HOME設定為目前位置
        `export AIRFLOW_HOME="$(pwd)"`
        
        查看是否設定成功
        `echo $AIRFLOW_HOME`
        
        開新的終端機時，要再`export AIRFLOW_HOME="$(pwd)"`

    * 如果只會有一個AIRFLOW_HOME、不常變動的話
        
        可進入 .bashrc 中加入 (此檔案在/home/[你的使用者名稱] 底下)
        
        `export AIRFLOW_HOME=你的目錄`
        
        如
        `export AIRFLOW_HOME=/home/user1/project/airflow-comic`

        重載你的設定，讓剛改的設定立即生效
    
        `source ~/.bashrc`

補充:

[.bash_profile 與 .bashrc 的差異](https://reurl.cc/em856M)

[Linux的环境变量.bash_profile .bashrc profile文件](https://reurl.cc/xE0DOz)

---

4. airflow 相關
    * 初始化DB
    `airflow db init`
    
        這時會多出一些檔案跟資料夾
    包括一個sqlite DB 檔案
        * 有可能出現SQLAlchemy衝突
    要改成 1.4.0 以下，我是改用1.3.24

    * 建立使用者，這邊我是建立Admin
        ```bash
        airflow users create \
                --username admin \
                --firstname FIRST_NAME \
                --lastname LAST_NAME \
                --role Admin \
                --email admin@example.org
        ```
        查看其他相關可輸入
        `airflow users create --help`

   * 啟動 Airflow Web UI
        `airflow webserver -p 8080`
        ([使用無痕模式開啟](https://reurl.cc/Krknle))

        這時網址輸入 localhost:8080，就能看到介面了

    * 啟動 Airflow 排程器
        
        啟動後才會依照你設定的時間及流程規則跑程式
        `airflow scheduler`

    * 如果不要看到範例dag，修改airflow.cfg中的
        ```bash
        load_examples = False
        ```

    * 安裝 Chrome 與 Chrome Driver
        依照此[教學文](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)，但不用裝 The X Server

        webdriver 設定 chrome headless(已在v3版DAG中設定)
        ```python
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options,)
        ```
        一般模式會跳出程式幫你開的瀏覽器(GUI)，接著看到你設定的動作，例如點特定按鈕等等。而用此方式開啟 Chrome ，等於無GUI顯示，仍能正常執行原有動作，取得資料、截圖等等，但需留意一些設定，如視窗大小等。
[更詳細chrome headless介紹](https://developers.google.com/web/updates/2017/04/headless-chrome)


    * 進去web介面，將DAG左方的開關打開
        
        scheduler就能依照設定的規則時間啟動DAG
        
        右方的播放按鈕則是手動啟動

    * 如要用指令測試某一task
        
        `airflow tasks test comic_app_v2 send_notification 2021-09-13`

        [測試task官方文件](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html#id2)

接著就能自行改動去嘗試各種設定了

---

參考資料:
1. [一段 Airflow 與資料工程的故事：談如何用 Python 追漫畫連載](https://leemeng.tw/a-story-about-airflow-and-data-engineering-using-how-to-use-python-to-catch-up-with-latest-comics-as-an-example.html#%E5%BB%BA%E7%BD%AE-Airflow-%E7%92%B0%E5%A2%83)
2. [第1點文章的作者專案Github](https://github.com/leemengtaiwan/airflow-tutorials)
3. [安裝ChromeDriver](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)
4. [Airflow 動手玩](https://zh-tw.coderbridge.com/series/c012cc1c8f9846359bb9b8940d4c10a8/posts/6c90609c64c14df284f141b703c03702)