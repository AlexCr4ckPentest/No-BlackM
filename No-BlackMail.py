import os, sys
import requests

from time import sleep
from bs4 import BeautifulSoup as bs
# from termcolor import colored # for colored print

RESET ='\033[0m'
UNDERLINE = '\033[04m'
GREEN = '\033[32m'
YELLOW = '\033[93m'
RED ='\033[31m'
CYAN = '\033[36m'
BOLD = '\033[01m'
URL_L = '\033[36m'
LI_G='\033[92m'
F_CL = '\033[0m'

DATABASE_FILENAME = "userdata.txt"


def clear_screen():
    """ Clear the screen """
    if os.sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


#def database_check():
#    """ Check for database file and clear all data if user choised rewrite """
#    if os.path.exists(DATABASE_FILENAME):
#        print(f'{CYAN}{BOLD}[1] {LI_G}Перезаписать данные в файл.{RESET}')
#        print(f'{CYAN}{BOLD}[2] {LI_G}Добавить к остальным.{RESET}')
#        
#        method = input(f'{CYAN}{BOLD}[~] {LI_G}Выберите метод: {RESET}')
#
#        clear_screen()
#
#        if method == '1':
#            os.remove(DATABASE_FILENAME)
#            print(f'{YELLOW}{BOLD}[+] {LI_G}Данные будут:{RESET} Перезаписаны')
#        elif method == '2':
#            print(f'{YELLOW}{BOLD}[+] {LI_G}Данные будут:{RESET} Добавлены к остальным')


def get_information_from_avito(number: str):
    response = requests.get('https://mirror.bullshit.agency/search_by_phone/'+number)
    content = bs(response.text, 'html.parser')
    content_over_h1_tag = content.find('h1')

    if content_over_h1_tag.text == '503 Service Temporarily Unavailable':
        print(f'{YELLOW}{BOLD}[!] {RED}Ваш запрос временно заблокирован. Пожалуйста, подождите 6-15 минут.{RESET}')
    else:
        count = 0
        h1T = content_over_h1_tag.text.replace("  ", "")
        print(f'\n{YELLOW}{BOLD}[~] {LI_G}Поиск данных по Авито: {RESET}')
        print(f'{YELLOW}{BOLD}[~] {LI_G}Авито: {F_CL}{h1T}{RESET}')
        print(f'{YELLOW}{BOLD}[+] {LI_G}----------------------------------------- >{RESET}\n')

        for elem in content.find_all(['h4', 'span']):
            print(f'{YELLOW}{BOLD}[+] {LI_G}{elem.text}{RESET}')  
            #data.append(elem.text)

            for url in content.find_all(['a']):
                count += 1
                user_link = url['href']
                try:            
                    avito_response = requests.get('https://mirror.bullshit.agency' + user_link)
                    content = bs(avito_response.text, 'html.parser')
                    url = content.find(['a'])
                           
                    url_text = url['href']
                    print(f'{YELLOW}{BOLD}[{count}] {URL_L}{UNDERLINE}{url_text}{RESET}')
                          
                    #u_name = bs(avito_response.text, 'html.parser')
                    #nameU = u_name.find('strong')

                    #name.append(nameU.text)
                    #data.append(f'[{count}] {user_link}')

                except Exception:
                    print(f'{YELLOW}{BOLD}[{count}] {RED}{UNDERLINE}{user_link}{RESET}')
                    continue

                #print(f'{YELLOW}{BOLD}[~] {LI_G}Данные о номере +{number} добавлены в файл {RESET}{DATABASE_FILENAME}')


def get_region_information(number: str):
    received_json_data = requests.post('https://htmlweb.ru/geo/api.php?json&telcod='+number).json()
    country = received_json_data['country']
    basic_data = received_json_data['0']
    
    print(f'{YELLOW}{BOLD}[~] {LI_G}Поиск данных... {RESET}\n')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Страна:{F_CL} {country["name"]}, {country["fullname"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Код страны:{F_CL} {country["country_code3"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Код номера:{F_CL} {country["telcod"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Длина номера:{F_CL} {country["telcod_len"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Локация:{F_CL} {country["location"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Язык:{F_CL} {country["lang"]}{RESET}')

    try:
        region = received_json_data['region']
        end_index = region['name'].split()
        if end_index[1] == 'край':
            print(f'{YELLOW}{BOLD}[+] {LI_G}Край:{F_CL} {region["name"]}{RESET}')
        elif end_index[1] == 'область':
            print(f'{YELLOW}{BOLD}[+] {LI_G}Область:{F_CL} {region["name"]}{RESET}')
        else:
            print(f'{YELLOW}{BOLD}[+] {LI_G}Название:{F_CL} {region["name"]}{RESET}')
        print(f'{YELLOW}{BOLD}[+] {LI_G}Округ:{F_CL} {region["okrug"]}{RESET}')
    except Exception:
        print(f'{YELLOW}{BOLD}[!] {RED}Данные Область/Край не найдены{RESET}')

    #try:
    #    capital = received_json_data['capital']
    #    print(f'{YELLOW}{BOLD}[+] {LI_G}Столица:{F_CL} {capital["name"]}{RESET}')
    #    print(f'{YELLOW}{BOLD}[+] {LI_G}Код домашнего номера столицы:{F_CL} +{str(capital["telcod"])}{RESET}')
    #except Exception:
    #    print(f'{YELLOW}{BOLD}[!] {RED}Данные Код/Столица не найдены{RESET}')

    print(f'{YELLOW}{BOLD}[+] {LI_G}Оператор:{F_CL} {basic_data["oper_brand"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Город:{F_CL} {basic_data["name"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Район:{F_CL} {basic_data["rajon"]}{RESET}')
    print(f'{YELLOW}{BOLD}[+] {LI_G}Номерной диапазон:{F_CL} {basic_data["def"]}{RESET}')


#def get_whatsapp_information(number: str):
#    response = requests.get('https://mirror.bullshit.agency/search_by_phone/'+number)
#    content = bs(response.text, 'html.parser')
#
#    if not received_json_data['limit'] == 0:
#        name = []
#
#        with open(DATABASE_FILENAME, 'a', encoding='utf-8') as fileD:
#            fileD.write('[∩] Номер: +'+number+'\n')
#            fileD.write(data +'\n')
#            fileD.write(f'https://api.whatsapp.com/send?phone={number}&text=Hello,%20this%20is%20NO-Blackmail')
#            fileD.write('\n[-] Все имена с ссылок: ' + ', '.join(name) +'\n\n')
#
#        print(f'{YELLOW}{BOLD}[~] {LI_G}Создан прямая ссылка в WhatsApp: {RESET}')
#        print(f'{YELLOW}{BOLD}[~] {URL_L}{UNDERLINE}https://api.whatsapp.com/send?phone={number}&text=Hello,%20this%20is%20No-BlackMail{RESET}')
#        print(f'\n{YELLOW}{BOLD}[!] {RED}Всего лимитов: {received_json_data["limit"]}{RESET}')


def main():
    try:
        #database_check()
        clear_screen()

        number = input(f'{YELLOW}{BOLD}[~] {LI_G}Введите номер: {RESET}')

        print(f'{YELLOW}{BOLD}[?] {LI_G}Поиск данных о номерах всех стран. {RESET}')
        print(f'{YELLOW}{BOLD}[#] {LI_G}Подготовка... {RESET}')
        sleep(0.5)

        get_region_information(number)
        get_information_from_avito(number)
    except KeyboardInterrupt:
        sys.exit(f'\n{YELLOW}{BOLD}[!] {RED}Принудительная остановка кода{RESET}')

# Entry point
if __name__ == "__main__":
    main()    