from selenium import webdriver


path = "C:\Program Files (x86)\Google\Chrome\Application"# 注意这个路径需要时可执行路径（chmod 777 dir or 755 dir）
driver = webdriver.Chrome(executable_path=path)


#driver = webdriver.Chrome()  # 打开谷歌浏览器,
driver.get('https://baidu.com')
cookie = driver.get_cookies()
driver.quit()