from selenium import webdriver
        
options = webdriver.chrome.options.Options()
profile_path = '/Users/20241256/AppData/Local/Google/Chrome/User Data/Default'
options.add_argument('--user-data-dir=' + profile_path)
driver = webdriver.Chrome(executable_path='path_to_chromedriver', options=options)