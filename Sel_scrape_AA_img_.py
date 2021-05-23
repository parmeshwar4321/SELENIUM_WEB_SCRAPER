import selenium,io,time,os,requests 
from PIL import Image
from selenium.common.exceptions import ElementClickInterceptedException
from selenium import webdriver
driver=webdriver.Chrome(executable_path='/home/navgurukul/Desktop/pythonfiles/selenium/chromedriver')
search_url='https://www.google.com/search?q=allu+arjun&tbm=isch&ved=2ahUKEwiTx96DjL_wAhUJVFMKHa2_A1AQ2-cCegQIABAA&oq=allu+arjun&gs_lcp=CgNpbWcQA1AAWABgqyNoAHAAeACAAQCIAQCSAQCYAQCqAQtnd3Mtd2l6LWltZw&sclient=img&ei=MCSZYJPvKImozQKt_46ABQ&bih=568&biw=1251&hl=en'
driver.get(search_url)


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)#sleep_between_interactions
imgResults = driver.find_elements_by_xpath("//img[contains(@class,'Q4LuWd')]")
totalResults=len(imgResults)
img_urls = set()
for i in  range(0,len(imgResults)):
    img=imgResults[i]   
    try:
        img.click()
        time.sleep(2)
        actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
                img_urls.add(actual_image.get_attribute('src'))
    except ElementClickInterceptedException or ElementNotInteractableException as err:
        print(err)
os.chdir('/home/navgurukul/Desktop/selenium_scrape/output')
baseDir=os.getcwd()

for i, url in enumerate(img_urls):
    file_name = f"{i:150}.jpg"    
    try:
        image_content = requests.get(url).content


        try:
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')
                
                file_path = os.path.join(baseDir, file_name)
                
                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=85)
                print(f"SAVED - {url} - AT: {file_path}")
        except Exception as e:
                print(f"ERROR - COULD NOT SAVE {url} - {e}")


    except Exception as e:
        print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")






