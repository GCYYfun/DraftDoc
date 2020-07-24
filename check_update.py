from selenium import webdriver
from selenium.common.exceptions import TimeoutException,InvalidSessionIdException,NoSuchElementException

import time

option = webdriver.FirefoxOptions()
option.add_argument('-headless')   
# chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
# chrome_opt.add_argument('--window-size=1366,768') 



urls = [
    ' https://github.com/yunwei37/os-summer-of-code-daily ',
    ' https://github.com/irakatz/Schedule ',
    ' https://github.com/ruilibuaa/RustStudy/wiki ',
    ' https://github.com/Rhacoal/rcore-labs ',
    ' https://github.com/leonardodalinky/DailySche ',
    ' https://github.com/freheit889/record ',
    ' https://github.com/luojia65/DailySchedule ',
    ' https://github.com/JohnWestonNull/rCore_SoC_Dairy ',
    ' https://github.com/trialley/rcore-to-zcore-daily ',
    ' https://github.com/ztygreat/2020DailySchedule ',
    ' https://github.com/Rubiczhang/Rcore-Study ',
    ' https://github.com/NameAvailable319/Rust_stady/wiki ',
    ' https://github.com/Jingruomu/OS_Tutorial_Summer_of_Code_2020 ',
    ' https://github.com/Cynthia-Lxy/rcore2020/blob/master/README.md ',
    ' https://github.com/yhyddr/os-summer-of-code-daily ',
    ' https://github.com/wfly1998/DailySchedule ',
    ' https://github.com/CJrZhang/rcore-lab ',
    ' https://github.com/wxybaba/rizhi/wiki ',
    ' https://github.com/kszlzj/DailySchedule ',
    ' https://github.com/starEvil01/rCore-os ',
    ' https://github.com/SKTT1Ryze/OS_Tutorial_Summer_of_Code/tree/master/DailySchedule ',
    ' https://github.com/73fc/DailySchedule ',
    ' https://github.com/luoqiangwei/OSBasedOnRisc-VDailySchedule ',
    ' https://github.com/Kong-Jun/DailySchedule ',
    ' https://github.com/Lincyaw/Rust_os_summer/blob/master/readme.md ',
    ' https://github.com/iLFTH/DailySchedule ',
    ' https://github.com/sinofp/otsoc ',
    ' https://github.com/DnailZ/os-tutorial-summer-of-code ',
    ' https://github.com/stellarkey/os_summer_project ',
    ' https://github.com/xushanpu123/myrcore ',
    ' https://github.com/Wintersweet0/OS- ',
    ' https://github.com/tjj-coder/rcore-study ',
    ' https://github.com/gystar/HelloRust.git ',
    ' https://github.com/dingiso/DailySchedule ',
    ' https://github.com/Wycers/rCore_SoC_Dairy ',
    ' https://github.com/SherlockLockyanzu/os-code-daily ',
    ' https://github.com/nlxxh/DailySchedule ',
    ' https://github.com/huiwy/DailySchedule ',
    ' https://github.com/loveHONOKAKOSAKA/Rust ',
    ' https://github.com/La-Vine/Schedule ',
    ' https://github.com/chibinz/rCoreSummerOfCode ',
    ' https://github.com/MeliaLiu/RCoreDailySchedule ',
    ' https://github.com/ZHAOWEIde/RUST-OS ',
    ' https://github.com/Zzzec/OS-Summer-of-Code ',
    ' https://github.com/shiweiwww/rcore.git ',
    ' https://github.com/tianye-frank/rcoreStudyDailySchedule ',
    ' https://github.com/am009/rcore_os ',
    ' https://github.com/greatoyster/DailySchedule ',
    ' https://github.com/leaversnever/rCore_2020 '
]
for url in urls:
    try:
        browser = webdriver.Firefox()
        browser.get(url)
        print(url.split('/')[3],end=":")
        time.sleep(2)
        input = browser.find_element_by_tag_name('relative-time')
        print(input.text)
        # browser.close()
    except TimeoutException:
        print('Time Out')
    except NoSuchElementException:
        print('NoSuchElementException')
    except InvalidSessionIdException:
        print('InvalidSessionIdException')
    finally:
        browser.close()
    

