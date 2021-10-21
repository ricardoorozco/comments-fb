from os import error
from selenium import webdriver
import pyautogui
import time
import csv
import random

post_relative_url = 'permalink.php?story_fbid=102007058948232&id=101798202302451'

split_url = post_relative_url.split('/')

post_id = '102007058948232'

post_url = 'https://www.facebook.com/' + post_relative_url
post_url_basic = 'https://mbasic.facebook.com/' + post_relative_url

# precarga de comentarios
comments = []
with open("comments.csv") as csvfilecomments:
    readercomment = csv.DictReader(csvfilecomments)
    for row in readercomment:  # each row is a list
        comments.append(row['comment'])
# fin de precarga de cometarios

# cuentas
with open('accounts.csv') as csvfileaccounts:
    readeraccount = list(csv.DictReader(csvfileaccounts))
    random.shuffle(readeraccount)
    isFirst = True
    for row in readeraccount:
        try:
            # espera entre comentarios de 5 a 10 minutos
            if not isFirst:
                min = 60
                cooldown = random.randint(0*min, 1*min)
                time.sleep(cooldown)
            isFirst = False

            #
            correo = row['email']
            password = row['password']
            proxy = row['proxy']
            desired_capability = []
            if proxy:
                desired_capability = webdriver.DesiredCapabilities.FIREFOX
                desired_capability['proxy']={
                    "httpProxy":proxy,
                    "proxyType": "MANUAL"
                    }        

            # apertura de firefox
            driver = webdriver.Firefox(capabilities=desired_capability)

            # ir a url
            driver.get("https://wwww.facebook.com")
            time.sleep(5)

            # definir el xpath de los atributosde html
            corre_xpath = '//*[@id="email"]'
            password_xpath = '//*[@id="pass"]'
            login_button_xpath = '//*[@name="login"]'

            # asignar una variable nueva el path de elemento iteractuar
            correo_element = driver.find_element_by_xpath(corre_xpath)
            password_element = driver.find_element_by_xpath(password_xpath)
            login_button_element = driver.find_element_by_xpath(login_button_xpath)

            # escribir sobre elemento
            correo_element.send_keys(correo)
            password_element.send_keys(password)
            driver.execute_script("arguments[0].click();", login_button_element)
            time.sleep(10)

            # url para reaccionar
            driver.get(post_url_basic)
            time.sleep(4)

            # emociones
            reaccionar_xpath = '//*[@id="actions_' + post_id + '"]/table/tbody/tr/td[2]/a';
            meGusta = '//*[@id="root"]/table/tbody/tr/td/ul/li[1]/table/tbody/tr/td/a'
            meEncanta = '//*[@id="root"]/table/tbody/tr/td/ul/li[2]/table/tbody/tr/td/a'
            meImporta = '//*[@id="root"]/table/tbody/tr/td/ul/li[3]/table/tbody/tr/td/a'
            meDivierte = '//*[@id="root"]/table/tbody/tr/td/ul/li[4]/table/tbody/tr/td/a'
            meAsombra = '//*[@id="root"]/table/tbody/tr/td/ul/li[5]/table/tbody/tr/td/a'
            meEntristese = '//*[@id="root"]/table/tbody/tr/td/ul/li[6]/table/tbody/tr/td/a'
            meEnfada = '//*[@id="root"]/table/tbody/tr/td/ul/li[7]/table/tbody/tr/td/a'

            reacciones = [meGusta,meImporta,meEncanta]

            # para dar solo like megusta ,ecanta,enfadado ,etc.. click
            try:
                reaccionar_element = driver.find_element_by_xpath(reaccionar_xpath)
                driver.execute_script("arguments[0].click();", reaccionar_element)
                time.sleep(5)
                reaccion_element = driver.find_element_by_xpath(reacciones[random.randint(0, len(reacciones)-1)])
                driver.execute_script("arguments[0].click();", reaccion_element)
                time.sleep(5)
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")

            # url para comentar
            # driver.get(post_url)
            # time.sleep(4)
            coment = '//*[@id="composerInput"]'
            coment_element = driver.find_element_by_xpath(coment)
            driver.execute_script("arguments[0].focus();", coment_element)

            time.sleep(2)

            rand = random.randint(0, len(comments)-1)
            pyautogui.typewrite(comments[rand])
            pyautogui.typewrite("\n")
            # remover comentario para no repetir
            comments.pop(rand)
            
            submit = '/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[4]/form[1]/table/tbody/tr/td[2]/div/input'
            submit_element = driver.find_element_by_xpath(submit)
            driver.execute_script("arguments[0].click();", submit_element)

            #like_button_element = driver.find_element_by_css_selector(
            #    "div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.g5gj957u.rj1gh0hx.buofh1pr.hpfvmrgz.taijpn5t.bp9cbjyn.owycx6da.btwxx1t3.d1544ag0.tw6a2znq.jb3vyjys.dlv3wnog.rl04r1d5.mysgfdmx.hddg9phg.qu8okrzs.g0qnabr5")
            # like_button_element.click()
            #driver.execute_script("arguments[0].click();", like_button_element)
            
            time.sleep(5)
            
            # cierre de firefox
            driver.quit()
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    # fin del ciclo for
# fin de cuentas
