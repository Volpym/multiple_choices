from selenium import webdriver
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException
import mysql.connector

def rgb_to_hex(rgb):
    heximal = Color.from_string(rgb).hex
    return heximal; 
def isCorrect(color):
    correct_answer=""
    if (color =='#00ff00'):
        correct_answer=answer_text[i]
    return(correct_answer)

 
# creates an firefox browser instance
driver = webdriver.Firefox(executable_path="C:\\Users\\jedic\\Desktop\\diktia til\\geckodriver.exe")
 
#Select the file to scrape
url = "http:///localhost//commnets/test.html"
driver.get(url)

#connects to DB
connection = mysql.connector.connect(host='localhost',
                                     database = 'exams',
                                     user = 'root',
                                     password = 'ac0b3passGGsmokescreen',
                                     )
cursor = connection.cursor()




for j in range (99):
    correct_answer="";
    #scrapes the question
    question_1_text = driver.find_element_by_css_selector("#myCanvasAnsQ > div:nth-child(6)").text
    

    
    #chooses the first answer in order to show if it is correct or false
    driver.find_element_by_css_selector('#myCanvasAns1 > div:nth-child(1) > img:nth-child(1)').click()
    
    answer_text=[]
    answer_div = " > div:nth-child(7)"
    bc_div = " > div:nth-child(8)" 
    
    for i in range (4):
        try:
            answer_selector="#myCanvasAns%d"%(i+1)
            answer_text.append(driver.find_element_by_css_selector(answer_selector+answer_div).text)
        except NoSuchElementException as exception:
            answer_text.append("NULL")
        try:
            #gets answer's background color in rgb and transforms it in hex
            color = rgb_to_hex(driver.find_element_by_css_selector(answer_selector+bc_div).value_of_css_property('background-color'))
            correct_answer=isCorrect(color)
        except NoSuchElementException as exception:    
            print("doesn't exist")
    
    query = 'INSERT INTO answers (answers_id, answer1, answer2, answer3, answer4)VALUES (%d, "%s","%s","%s","%s")' %(j+1, answer_text[0], answer_text[1], answer_text[2], answer_text[3])
    cursor.execute(query)
    query = 'INSERT INTO correct_answer(cAnswer_id,text)VALUES (%d,"%s")'%(j+1,correct_answer)
    cursor.execute(query) 

    query = 'INSERT INTO question (answers_id,cAnswer_id,question_id,text)VALUES (%d, %d, %d,"%s")' %(j+1, j+1, j+1, question_1_text)
    cursor.execute(query)
    driver.find_element_by_css_selector('#myCanvasBtn > div:nth-child(1)').click()
    
#just checking
 

connection.commit()
cursor.close()
connection.close()




