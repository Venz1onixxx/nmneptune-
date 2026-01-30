#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NEPTUNE Russian Numbers Analyzer
Version 1.0.0 | by Venz1onixxx
https://github.com/Venz1onixxx
"""

import os
import sys
import re
import json
import hashlib
import datetime
import csv
from typing import Dict, List, Optional

# ============================================
# ЛОГОТИП NEPTUNE (СИНИЙ - РАБОТАЕТ В CMD)
# ============================================

def display_logo():
    """Отображение синего логотипа NEPTUNE, который работает в CMD"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Используем ANSI коды напрямую для гарантированного цвета
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    logo = f"""
{BLUE}{'='*70}{RESET}
{BLUE}                                                                      {RESET}
{BLUE}    ███╗   ██╗███████╗██████╗ ████████╗██╗   ██╗███╗   ██╗███████╗    {RESET}
{BLUE}    ████╗  ██║██╔════╝██╔══██╗╚══██╔══╝██║   ██║████╗  ██║██╔════╝    {RESET}
{BLUE}    ██╔██╗ ██║█████╗  ██████╔╝   ██║   ██║   ██║██╔██╗ ██║█████╗      {RESET}
{BLUE}    ██║╚██╗██║██╔══╝  ██╔═══╝    ██║   ██║   ██║██║╚██╗██║██╔══╝      {RESET}
{BLUE}    ██║ ╚████║███████╗██║        ██║   ╚██████╔╝██║ ╚████║███████╗    {RESET}
{BLUE}    ╚═╝  ╚═══╝╚══════╝╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝    {RESET}
{BLUE}                                                                      {RESET}
{CYAN}                  АНАЛИЗАТОР НОМЕРОВ РОССИИ И УКРАИНЫ                  {RESET}
{WHITE}                         Версия 1.0.0                               {RESET}
{CYAN}                     by Venz1onixxx                                  {RESET}
{BLUE}              https://github.com/Venz1onixxx                         {RESET}
{BLUE}                                                                      {RESET}
{BLUE}{'='*70}{RESET}
"""
    print(logo)

# ============================================
# ЦВЕТОВЫЕ КОНСТАНТЫ (РАБОТАЮТ В CMD)
# ============================================

class Colors:
    # ANSI цветовые коды
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def colorize(text, color):
        """Добавить цвет к тексту"""
        colors = {
            'blue': Colors.BLUE,
            'cyan': Colors.CYAN,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'red': Colors.RED,
            'magenta': Colors.MAGENTA,
            'white': Colors.WHITE,
            'bold': Colors.BOLD
        }
        return f"{colors.get(color, Colors.WHITE)}{text}{Colors.RESET}"

# ============================================
# БАЗА ДАННЫХ РЕГИОНОВ И ОПЕРАТОРОВ
# ============================================

class PhoneDatabase:
    def __init__(self):
        # База данных регионов России (все субъекты РФ)
        self.russian_regions = {
            # Центральный федеральный округ
            '495': 'Москва',
            '496': 'Московская область (запад)',
            '498': 'Московская область (север)',
            '499': 'Москва (север)',
            '471': 'Курская область',
            '472': 'Белгородская область',
            '473': 'Воронежская область',
            '474': 'Липецкая область',
            '475': 'Тамбовская область',
            '481': 'Смоленская область',
            '482': 'Тверская область',
            '483': 'Брянская область',
            '484': 'Калужская область',
            '485': 'Ярославская область',
            '486': 'Орловская область',
            '487': 'Тульская область',
            '491': 'Рязанская область',
            '492': 'Ивановская область',
            '493': 'Костромская область',
            '494': 'Владимирская область',
            
            # Северо-Западный федеральный округ
            '811': 'Псковская область',
            '812': 'Санкт-Петербург',
            '813': 'Ленинградская область',
            '814': 'Республика Карелия',
            '815': 'Мурманская область',
            '816': 'Новгородская область',
            '817': 'Вологодская область',
            '818': 'Архангельская область',
            '821': 'Республика Коми',
            
            # Южный федеральный округ
            '844': 'Волгоградская область',
            '845': 'Саратовская область',
            '846': 'Самарская область',
            '847': 'Республика Калмыкия',
            '848': 'Тольятти',
            '851': 'Астраханская область',
            '855': 'Набережные Челны',
            '861': 'Краснодарский край',
            '862': 'Сочи',
            '863': 'Ростовская область',
            '865': 'Ставропольский край',
            '866': 'Кабардино-Балкария',
            '867': 'Северная Осетия',
            '869': 'Севастополь',
            '871': 'Чеченская Республика',
            '872': 'Дагестан',
            '873': 'Ингушетия',
            '877': 'Адыгея',
            '878': 'Карачаево-Черкесия',
            
            # Приволжский федеральный округ
            '831': 'Нижегородская область',
            '833': 'Кировская область',
            '834': 'Республика Мордовия',
            '835': 'Чувашская Республика',
            '836': 'Республика Марий Эл',
            '841': 'Пензенская область',
            '842': 'Ульяновская область',
            '843': 'Республика Татарстан',
            '855': 'Набережные Челны',
            
            # Уральский федеральный округ
            '343': 'Свердловская область',
            '345': 'Тюменская область',
            '346': 'Ханты-Мансийский АО',
            '347': 'Республика Башкортостан',
            '349': 'Ямало-Ненецкий АО',
            '351': 'Челябинская область',
            '352': 'Курганская область',
            
            # Сибирский федеральный округ
            '381': 'Омская область',
            '382': 'Томская область',
            '383': 'Новосибирская область',
            '384': 'Кемеровская область',
            '385': 'Алтайский край',
            '388': 'Республика Алтай',
            '390': 'Хакасия',
            '391': 'Красноярский край',
            '394': 'Республика Тыва',
            
            # Дальневосточный федеральный округ
            '411': 'Республика Саха (Якутия)',
            '413': 'Магаданская область',
            '415': 'Камчатский край',
            '416': 'Амурская область',
            '421': 'Хабаровский край',
            '423': 'Приморский край',
            '424': 'Сахалинская область',
            '426': 'Еврейская автономная область',
            '427': 'Чукотский АО',
            
            # Крым
            '365': 'Республика Крым',
            '869': 'Севастополь'
        }
        
        # База данных регионов Украины
        self.ukrainian_regions = {
            '44': 'Киев',
            '432': 'Винницкая область',
            '433': 'Волынская область',
            '434': 'Днепропетровская область',
            '435': 'Донецкая область',
            '436': 'Житомирская область',
            '437': 'Закарпатская область',
            '438': 'Запорожская область',
            '439': 'Ивано-Франковская область',
            '462': 'Киевская область',
            '463': 'Кировоградская область',
            '464': 'Луганская область',
            '465': 'Львовская область',
            '466': 'Николаевская область',
            '467': 'Одесская область',
            '468': 'Полтавская область',
            '469': 'Ровненская область',
            '472': 'Сумская область',
            '473': 'Тернопольская область',
            '474': 'Харьковская область',
            '475': 'Херсонская область',
            '476': 'Хмельницкая область',
            '477': 'Черкасская область',
            '478': 'Черниговская область',
            '479': 'Черновицкая область',
            '48': 'Киев мобильный',
            '50': 'Vodafone Украина',
            '66': 'Vodafone Украина',
            '67': 'Киевстар',
            '68': 'Киевстар',
            '73': 'lifecell',
            '93': 'lifecell',
            '95': 'Vodafone Украина',
            '96': 'Киевстар',
            '97': 'Киевстар',
            '98': 'Киевстар',
            '99': 'Vodafone Украина'
        }
        
        # Операторы России
        self.russian_operators = {
            'МТС': {
                'codes': ['910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
                         '980', '981', '982', '983', '984', '985', '986', '987', '988', '989'],
                'color': 'green'
            },
            'МегаФон': {
                'codes': ['920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
                         '930', '931', '932', '933', '934', '935', '936', '937', '938', '939'],
                'color': 'red'
            },
            'Билайн': {
                'codes': ['903', '905', '906', '909', '960', '961', '962', '963', '964', '965',
                         '966', '967', '968', '969', '900', '901', '902', '904', '908'],
                'color': 'yellow'
            },
            'Tele2': {
                'codes': ['950', '951', '952', '953', '954', '955', '956', '957', '958', '959',
                         '970', '971', '972', '973', '974', '975', '976', '977', '978', '979'],
                'color': 'blue'
            },
            'Yota': {
                'codes': ['995', '996', '999'],
                'color': 'magenta'
            },
            'Ростелеком': {
                'codes': ['978'],
                'color': 'cyan'
            },
            'Тинькофф Мобайл': {
                'codes': ['900', '901', '902', '904', '908'],
                'color': 'yellow'
            },
            'СберМобайл': {
                'codes': ['901', '902'],
                'color': 'green'
            }
        }
        
        # Операторы Украины
        self.ukrainian_operators = {
            'Киевстар': {
                'codes': ['67', '68', '96', '97', '98'],
                'color': 'blue'
            },
            'Vodafone Украина': {
                'codes': ['50', '66', '95', '99'],
                'color': 'red'
            },
            'lifecell': {
                'codes': ['63', '73', '93'],
                'color': 'yellow'
            },
            'Тримоб (3mob)': {
                'codes': ['91'],
                'color': 'green'
            },
            'Интертелеком': {
                'codes': ['89'],
                'color': 'cyan'
            },
            'PEOPLEnet': {
                'codes': ['92'],
                'color': 'magenta'
            },
            'Київська міська телефонна мережа': {
                'codes': ['44'],
                'color': 'white'
            }
        }

# ============================================
# АНАЛИЗАТОР НОМЕРОВ
# ============================================

class PhoneAnalyzer:
    def __init__(self):
        self.db = PhoneDatabase()
        self.history = []
    
    def detect_country(self, phone: str) -> str:
        """Определение страны номера"""
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 11:
            if digits.startswith('8') or digits.startswith('7'):
                return 'RU'
            elif digits.startswith('3'):
                if digits.startswith('380'):
                    return 'UA'
        elif len(digits) == 12:
            if digits.startswith('380'):
                return 'UA'
        elif len(digits) == 10:
            # Российский номер без кода страны
            return 'RU'
        
        return 'UNKNOWN'
    
    def validate_phone(self, phone: str) -> tuple:
        """Проверка валидности номера"""
        digits = re.sub(r'\D', '', phone)
        country = self.detect_country(phone)
        
        if country == 'RU':
            # Российские номера
            if len(digits) == 11:
                if digits.startswith('8') or digits.startswith('7'):
                    return True, digits, 'Российский номер (11 цифр)', country
            elif len(digits) == 10:
                return True, '7' + digits, 'Российский номер (10 цифр)', country
        
        elif country == 'UA':
            # Украинские номера
            if len(digits) == 12 and digits.startswith('380'):
                return True, digits, 'Украинский номер (12 цифр)', country
            elif len(digits) == 11 and digits.startswith('80'):
                return True, '3' + digits, 'Украинский номер (11 цифр)', country
            elif len(digits) == 10 and digits.startswith('0'):
                return True, '380' + digits[1:], 'Украинский номер (10 цифр)', country
        
        return False, digits, 'Неверный формат', 'UNKNOWN'
    
    def get_operator_and_region(self, phone_digits: str, country: str) -> tuple:
        """Определение оператора и региона"""
        if country == 'RU':
            return self._get_russian_info(phone_digits)
        elif country == 'UA':
            return self._get_ukrainian_info(phone_digits)
        else:
            return 'Неизвестный оператор', 'Неизвестный регион'
    
    def _get_russian_info(self, phone_digits: str) -> tuple:
        """Определение информации для российского номера"""
        if len(phone_digits) >= 4:
            code = phone_digits[1:4]
            
            # Определяем оператора
            operator = 'Неизвестный оператор'
            operator_color = 'white'
            for op_name, op_data in self.db.russian_operators.items():
                if code in op_data['codes']:
                    operator = op_name
                    operator_color = op_data['color']
                    break
            
            # Определяем регион - ИСПРАВЛЕННАЯ ЛОГИКА
            region = 'Неизвестный регион'
            if code in self.db.russian_regions:
                region = self.db.russian_regions[code]
            elif operator != 'Неизвестный оператор':
                # Если это известный оператор, но не городской код
                region = 'Мобильный номер'
            
            return operator, region, operator_color
        
        return 'Неизвестный оператор', 'Неизвестный регион', 'white'
    
    def _get_ukrainian_info(self, phone_digits: str) -> tuple:
        """Определение информации для украинского номера"""
        if len(phone_digits) >= 12:  # 380XXXXXXXXX
            operator_code = phone_digits[3:5]  # Код оператора после 380
            
            # Определяем оператора
            operator = 'Неизвестный оператор'
            operator_color = 'white'
            for op_name, op_data in self.db.ukrainian_operators.items():
                if operator_code in op_data['codes']:
                    operator = op_name
                    operator_color = op_data['color']
                    break
            
            # Определяем регион - ИСПРАВЛЕННАЯ ЛОГИКА
            region = 'Неизвестный регион'
            region_code = phone_digits[3:6] if len(phone_digits) >= 6 else operator_code
            
            if region_code in self.db.ukrainian_regions:
                region = self.db.ukrainian_regions[region_code]
            elif operator_code in self.db.ukrainian_regions:
                region = self.db.ukrainian_regions[operator_code]
            elif operator != 'Неизвестный оператор':
                # Если это известный оператор
                region = 'Мобильный номер'
            
            return operator, region, operator_color
        
        return 'Неизвестный оператор', 'Неизвестный регион', 'white'
    
    def format_phone(self, phone_digits: str, country: str) -> Dict[str, str]:
        """Форматирование номера в разные форматы"""
        if country == 'RU':
            if len(phone_digits) == 11:
                return {
                    'international': f"+7{phone_digits[1:]}",
                    'national': f"8{phone_digits[1:4]}{phone_digits[4:7]}{phone_digits[7:9]}{phone_digits[9:]}",
                    'standard': f"+7 ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:]}",
                    'simple': f"8 ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:]}",
                    'digits': phone_digits
                }
        
        elif country == 'UA':
            if len(phone_digits) == 12:  # 380XXXXXXXXX
                return {
                    'international': f"+{phone_digits}",
                    'national': f"0{phone_digits[3:5]} {phone_digits[5:8]} {phone_digits[8:10]} {phone_digits[10:]}",
                    'standard': f"+{phone_digits[:3]} ({phone_digits[3:5]}) {phone_digits[5:8]}-{phone_digits[8:10]}-{phone_digits[10:]}",
                    'simple': f"0{phone_digits[3:5]}{phone_digits[5:8]}{phone_digits[8:10]}{phone_digits[10:]}",
                    'digits': phone_digits
                }
        
        return {'raw': phone_digits}
    
    def check_special(self, phone_digits: str) -> List[str]:
        """Проверка специальных номеров"""
        specials = []
        
        # Общие экстренные службы
        emergency_codes = ['112', '911', '101', '102', '103', '104']
        for code in emergency_codes:
            if phone_digits.endswith(code):
                specials.append(f'Экстренная служба: {code}')
        
        # Красивые номера
        if len(phone_digits) >= 6:
            last_six = phone_digits[-6:]
            
            # Все одинаковые цифры
            if len(set(last_six)) == 1:
                specials.append(f'VIP номер: все цифры {last_six[0]}')
            
            # Последовательности
            if last_six in ['123456', '654321', '111111', '222222', '333333', 
                          '444444', '555555', '666666', '777777', '888888', '999999']:
                specials.append(f'Красивый номер: {last_six}')
            
            # Зеркальные
            if last_six[:3] == last_six[3:][::-1]:
                specials.append(f'Зеркальный номер: {last_six[:3]}-{last_six[3:]}')
        
        return specials
    
    def analyze(self, phone: str) -> Optional[Dict]:
        """Полный анализ номера"""
        valid, digits, status, country = self.validate_phone(phone)
        
        if not valid:
            return None
        
        operator, region, operator_color = self.get_operator_and_region(digits, country)
        formats = self.format_phone(digits, country)
        specials = self.check_special(digits)
        
        # Определяем название страны
        country_name = {
            'RU': 'Россия',
            'UA': 'Украина',
            'UNKNOWN': 'Неизвестно'
        }.get(country, 'Неизвестно')
        
        # Генерация уникального ID
        phone_id = hashlib.md5(digits.encode()).hexdigest()[:8].upper()
        
        result = {
            'original': phone,
            'digits': digits,
            'valid': valid,
            'status': status,
            'country': country_name,
            'country_code': country,
            'operator': operator,
            'operator_color': operator_color,
            'region': region,
            'formats': formats,
            'specials': specials,
            'id': phone_id,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Сохраняем в историю
        self.history.append(result)
        return result

# ============================================
# ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ
# ============================================

class NeptuneInterface:
    def __init__(self):
        self.analyzer = PhoneAnalyzer()
        self.db = PhoneDatabase()
        
    def print_colored(self, text: str, color: str = 'white'):
        """Вывод цветного текста с использованием ANSI кодов"""
        colors = {
            'blue': Colors.BLUE,
            'cyan': Colors.CYAN,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'red': Colors.RED,
            'magenta': Colors.MAGENTA,
            'white': Colors.WHITE,
            'bold': Colors.BOLD
        }
        color_code = colors.get(color, Colors.WHITE)
        print(f"{color_code}{text}{Colors.RESET}")
    
    def print_header(self, text: str):
        """Вывод заголовка"""
        self.print_colored("\n" + "="*70, "blue")
        self.print_colored(text.center(70), "cyan")
        self.print_colored("="*70, "blue")
    
    def analyze_number(self):
        """Анализ одного номера"""
        self.print_header("АНАЛИЗ НОМЕРА ТЕЛЕФОНА")
        
        print("\nПоддерживаемые форматы:")
        print("  Россия: 89161234567, +79161234567, 9161234567")
        print("  Украина: 380501234567, 0501234567, +380501234567")
        
        phone = input("\nВведите номер телефона: ").strip()
        
        if not phone:
            self.print_colored("Ошибка: не введен номер", "red")
            input("\nНажмите Enter для продолжения...")
            return
        
        result = self.analyzer.analyze(phone)
        
        if not result:
            self.print_colored("\nОшибка: неверный формат номера", "red")
            input("\nНажмите Enter для продолжения...")
            return
        
        # Вывод результатов
        self.print_header("РЕЗУЛЬТАТЫ АНАЛИЗА")
        
        print(f"\nВведенный номер: {result['original']}")
        print(f"Статус: {result['status']}")
        self.print_colored(f"Страна: {result['country']}", "bold")
        
        # Цвет оператора в зависимости от страны
        if result['country_code'] == 'RU':
            self.print_colored(f"Оператор: {result['operator']}", result['operator_color'])
        elif result['country_code'] == 'UA':
            self.print_colored(f"Оператор: {result['operator']}", result['operator_color'])
        else:
            print(f"Оператор: {result['operator']}")
        
        print(f"Регион: {result['region']}")
        self.print_colored(f"ID номера: {result['id']}", "blue")
        
        self.print_colored("\nФорматы номера:", "cyan")
        print(f"  Международный: {result['formats'].get('international', 'N/A')}")
        print(f"  Национальный: {result['formats'].get('national', 'N/A')}")
        print(f"  Стандартный: {result['formats'].get('standard', 'N/A')}")
        print(f"  Цифры: {result['formats'].get('digits', 'N/A')}")
        
        if result['specials']:
            self.print_colored("\nОсобенности номера:", "yellow")
            for special in result['specials']:
                print(f"  • {special}")
        
        print(f"\nВремя анализа: {result['timestamp']}")
        
        input("\nНажмите Enter для продолжения...")
    
    def batch_analyze(self):
        """Пакетный анализ номеров"""
        self.print_header("ПАКЕТНЫЙ АНАЛИЗ")
        
        print("\nВведите номера телефонов (каждый с новой строки).")
        print("Поддерживаются российские и украинские номера.")
        print("Для завершения ввода введите пустую строку.")
        
        phones = []
        counter = 1
        
        while True:
            phone = input(f"\nНомер {counter}: ").strip()
            if not phone:
                break
            phones.append(phone)
            counter += 1
        
        if not phones:
            self.print_colored("Не введено ни одного номера", "red")
            input("\nНажмите Enter для продолжения...")
            return
        
        results = []
        valid_count = 0
        invalid_count = 0
        ru_count = 0
        ua_count = 0
        
        self.print_colored(f"\nАнализирую {len(phones)} номеров...", "yellow")
        
        for phone in phones:
            result = self.analyzer.analyze(phone)
            if result:
                results.append(result)
                valid_count += 1
                if result['country_code'] == 'RU':
                    ru_count += 1
                elif result['country_code'] == 'UA':
                    ua_count += 1
            else:
                invalid_count += 1
        
        # Вывод статистики
        self.print_header("СТАТИСТИКА АНАЛИЗА")
        
        print(f"\nВсего номеров: {len(phones)}")
        self.print_colored(f"Валидных: {valid_count}", "green")
        self.print_colored(f"Невалидных: {invalid_count}", "red")
        
        if ru_count > 0:
            self.print_colored(f"Российских: {ru_count}", "cyan")
        if ua_count > 0:
            self.print_colored(f"Украинских: {ua_count}", "yellow")
        
        # Распределение по операторам
        if results:
            operators_count = {}
            for result in results:
                op = result['operator']
                operators_count[op] = operators_count.get(op, 0) + 1
            
            if operators_count:
                self.print_colored("\nРаспределение по операторам:", "cyan")
                for operator, count in operators_count.items():
                    percentage = (count / valid_count) * 100
                    print(f"  {operator}: {count} номеров ({percentage:.1f}%)")
        
        # Предложение экспорта
        if results:
            export_choice = input("\nЭкспортировать результаты? (да/нет): ").strip().lower()
            if export_choice in ['да', 'д', 'y', 'yes']:
                self.export_results(results)
        
        input("\nНажмите Enter для продолжения...")
    
    def show_regions_info(self):
        """Показать информацию о регионах"""
        self.print_header("ИНФОРМАЦИЯ О РЕГИОНАХ")
        
        print("\nВыберите страну:")
        print("  1. Россия (все регионы)")
        print("  2. Украина (все регионы)")
        print("  3. Назад")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '1':
            self._show_russian_regions()
        elif choice == '2':
            self._show_ukrainian_regions()
        elif choice == '3':
            return
    
    def _show_russian_regions(self):
        """Показать регионы России"""
        self.print_header("РЕГИОНЫ РОССИИ")
        
        regions_by_code = {}
        for code, region in self.db.russian_regions.items():
            regions_by_code[code] = region
        
        print(f"\nВсего регионов: {len(regions_by_code)}")
        
        # Группируем по федеральным округам
        federal_districts = {
            'Центральный': [],
            'Северо-Западный': [],
            'Южный': [],
            'Приволжский': [],
            'Уральский': [],
            'Сибирский': [],
            'Дальневосточный': []
        }
        
        # Распределяем регионы по округам (упрощенно по кодам)
        for code, region in regions_by_code.items():
            if code.startswith(('495', '496', '498', '499', '471', '472', '473', '474', '475', '481', '482', '483', '484', '485', '486', '487', '491', '492', '493', '494')):
                federal_districts['Центральный'].append((code, region))
            elif code.startswith(('811', '812', '813', '814', '815', '816', '817', '818', '821')):
                federal_districts['Северо-Западный'].append((code, region))
            elif code.startswith(('844', '845', '846', '847', '848', '851', '855', '861', '862', '863', '865', '866', '867', '869', '871', '872', '873', '877', '878')):
                federal_districts['Южный'].append((code, region))
            elif code.startswith(('831', '833', '834', '835', '836', '841', '842', '843')):
                federal_districts['Приволжский'].append((code, region))
            elif code.startswith(('343', '345', '346', '347', '349', '351', '352')):
                federal_districts['Уральский'].append((code, region))
            elif code.startswith(('381', '382', '383', '384', '385', '388', '390', '391', '394')):
                federal_districts['Сибирский'].append((code, region))
            elif code.startswith(('411', '413', '415', '416', '421', '423', '424', '426', '427')):
                federal_districts['Дальневосточный'].append((code, region))
        
        # Выводим по округам
        for district, regions in federal_districts.items():
            if regions:
                self.print_colored(f"\n{district} федеральный округ:", "cyan")
                for code, region in sorted(regions)[:10]:  # Ограничиваем вывод
                    print(f"  {code}: {region}")
                if len(regions) > 10:
                    print(f"  ... и еще {len(regions) - 10} регионов")
        
        # Выводим операторов
        self.print_colored("\nОПЕРАТОРЫ СВЯЗИ РОССИИ:", "green")
        for operator, data in self.db.russian_operators.items():
            codes = data['codes']
            print(f"\n  {operator}:")
            print(f"    Коды: {', '.join(codes[:5])}{'...' if len(codes) > 5 else ''}")
            print(f"    Всего кодов: {len(codes)}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _show_ukrainian_regions(self):
        """Показать регионы Украины"""
        self.print_header("РЕГИОНЫ УКРАИНЫ")
        
        print(f"\nВсего регионов: {len(self.db.ukrainian_regions)}")
        
        # Группируем регионы
        oblasts = []
        mobile_codes = []
        
        for code, region in self.db.ukrainian_regions.items():
            if code.isdigit() and len(code) >= 3:
                oblasts.append((code, region))
            else:
                mobile_codes.append((code, region))
        
        if oblasts:
            self.print_colored("\nОбласти Украины:", "cyan")
            for code, region in sorted(oblasts)[:15]:  # Ограничиваем вывод
                print(f"  {code}: {region}")
            if len(oblasts) > 15:
                print(f"  ... и еще {len(oblasts) - 15} областей")
        
        if mobile_codes:
            self.print_colored("\nМобильные коды:", "yellow")
            for code, region in sorted(mobile_codes):
                print(f"  {code}: {region}")
        
        # Выводим операторов
        self.print_colored("\nОПЕРАТОРЫ СВЯЗИ УКРАИНЫ:", "green")
        for operator, data in self.db.ukrainian_operators.items():
            codes = data['codes']
            print(f"\n  {operator}:")
            print(f"    Коды: {', '.join(codes)}")
        
        input("\nНажмите Enter для продолжения...")
    
    def export_results(self, results: List[Dict]):
        """Экспорт результатов"""
        self.print_header("ЭКСПОРТ РЕЗУЛЬТАТОВ")
        
        print("\nВыберите формат экспорта:")
        print("  1. TXT (текстовый файл)")
        print("  2. JSON")
        print("  3. CSV")
        print("  4. Отмена")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '4':
            return
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            if choice == '1':
                filename = f"neptune_export_{timestamp}.txt"
                self.export_txt(results, filename)
            elif choice == '2':
                filename = f"neptune_export_{timestamp}.json"
                self.export_json(results, filename)
            elif choice == '3':
                filename = f"neptune_export_{timestamp}.csv"
                self.export_csv(results, filename)
            else:
                self.print_colored("Неверный выбор", "red")
                return
            
            self.print_colored(f"\nРезультаты экспортированы в файл: {filename}", "green")
            
        except Exception as e:
            self.print_colored(f"\nОшибка при экспорте: {e}", "red")
    
    def export_txt(self, results: List[Dict], filename: str):
        """Экспорт в TXT"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("NEPTUNE - Экспорт результатов анализа номеров\n")
            f.write("="*70 + "\n\n")
            f.write(f"Дата экспорта: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего номеров: {len(results)}\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"Номер #{i}\n")
                f.write("-"*40 + "\n")
                f.write(f"Исходный номер: {result['original']}\n")
                f.write(f"Страна: {result['country']}\n")
                f.write(f"Оператор: {result['operator']}\n")
                f.write(f"Регион: {result['region']}\n")
                f.write(f"Международный формат: {result['formats'].get('international', 'N/A')}\n")
                f.write(f"ID: {result['id']}\n")
                
                if result['specials']:
                    f.write("Особенности:\n")
                    for special in result['specials']:
                        f.write(f"  • {special}\n")
                
                f.write("\n")
    
    def export_json(self, results: List[Dict], filename: str):
        """Экспорт в JSON"""
        export_data = {
            'export_info': {
                'tool': 'NEPTUNE Russian & Ukrainian Numbers Analyzer',
                'version': '1.0.0',
                'author': 'Venz1onixxx',
                'github': 'https://github.com/Venz1onixxx',
                'export_date': datetime.datetime.now().isoformat(),
                'total_records': len(results)
            },
            'results': results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def export_csv(self, results: List[Dict], filename: str):
        """Экспорт в CSV"""
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Номер', 'Страна', 'Оператор', 'Регион', 'Международный формат', 'ID', 'Особенности'])
            
            for result in results:
                specials = ', '.join(result['specials']) if result['specials'] else ''
                writer.writerow([
                    result['original'],
                    result['country'],
                    result['operator'],
                    result['region'],
                    result['formats'].get('international', ''),
                    result['id'],
                    specials
                ])
    
    def show_help(self):
        """Показать справку"""
        self.print_header("СПРАВКА ПО ПРОГРАММЕ")
        
        help_text = """
NEPTUNE - Анализатор номеров России и Украины

ОСНОВНЫЕ ВОЗМОЖНОСТИ:
• Анализ одного номера телефона
• Пакетный анализ нескольких номеров
• Определение оператора связи
• Определение региона/области
• Проверка специальных номеров
• Экспорт результатов в различные форматы
• Просмотр информации о регионах

ПОДДЕРЖИВАЕМЫЕ СТРАНЫ И ФОРМАТЫ:
РОССИЯ:
  • 89161234567 (11 цифр, начинается с 8)
  • +79161234567 (11 цифр, начинается с +7)
  • 9161234567 (10 цифр, без кода страны)

УКРАИНА:
  • 380501234567 (12 цифр)
  • 0501234567 (10 цифр, начинается с 0)
  • +380501234567 (13 цифр)

ОПЕРАТОРЫ РОССИИ:
  • МТС, МегаФон, Билайн
  • Tele2, Yota, Ростелеком
  • Тинькофф Мобайл, СберМобайл

ОПЕРАТОРЫ УКРАИНЫ:
  • Киевстар, Vodafone Украина
  • lifecell, Тримоб
  • Интертелеком, PEOPLEnet

ЭКСПОРТ:
  • TXT - текстовый файл
  • JSON - структурированные данные
  • CSV - табличный формат

АВТОР: Venz1onixxx
GITHUB: https://github.com/Venz1onixxx
"""
        print(help_text)
        input("\nНажмите Enter для продолжения...")
    
    def show_menu(self):
        """Показать главное меню"""
        display_logo()
        
        menu_text = f"""
{Colors.CYAN}ГЛАВНОЕ МЕНЮ:{Colors.RESET}

{Colors.WHITE}1. Анализ одного номера{Colors.RESET}
{Colors.WHITE}2. Пакетный анализ{Colors.RESET}
{Colors.WHITE}3. Информация о регионах{Colors.RESET}
{Colors.WHITE}4. Экспорт результатов{Colors.RESET}
{Colors.WHITE}5. Справка{Colors.RESET}
{Colors.WHITE}0. Выход{Colors.RESET}

{Colors.CYAN}Выберите действие (0-5): {Colors.RESET}"""
        
        print(menu_text)
    
    def run(self):
        """Запуск основной программы"""
        while True:
            try:
                self.show_menu()
                choice = input().strip()
                
                if choice == '1':
                    self.analyze_number()
                elif choice == '2':
                    self.batch_analyze()
                elif choice == '3':
                    self.show_regions_info()
                elif choice == '4':
                    if not self.analyzer.history:
                        self.print_colored("Нет данных для экспорта", "red")
                        input("\nНажмите Enter для продолжения...")
                    else:
                        self.export_results(self.analyzer.history)
                elif choice == '5':
                    self.show_help()
                elif choice == '0':
                    self.print_header("ВЫХОД ИЗ ПРОГРАММЫ")
                    print("\nСпасибо за использование NEPTUNE!")
                    print("Автор: Venz1onixxx")
                    print("GitHub: https://github.com/Venz1onixxx")
                    break
                else:
                    self.print_colored("Неверный выбор. Попробуйте снова.", "red")
                    input("\nНажмите Enter для продолжения...")
            
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем.")
                break
            except Exception as e:
                self.print_colored(f"\nОшибка: {e}", "red")
                input("\nНажмите Enter для продолжения...")

# ============================================
# ЗАПУСК ПРОГРАММЫ
# ============================================

def main():
    """Основная функция"""
    try:
        # Настройка для Windows - ВКЛЮЧАЕМ ПОДДЕРЖКУ ANSI ЦВЕТОВ
        if os.name == 'nt':
            # Включаем поддержку ANSI цветов в Windows 10+
            os.system('')
            os.system('chcp 65001 > nul')
        
        # Запуск программы
        app = NeptuneInterface()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена.")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    # Проверка версии Python
    if sys.version_info[0] < 3:
        print("Требуется Python 3.6 или выше")
        sys.exit(1)
    
    # Запуск
    main()