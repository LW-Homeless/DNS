from Model.DNSRecon import DNSRecon
from colorama import Fore, init
from tabulate import tabulate
import dns.resolver
import os


class Controller:

    def __init__(self):
        self.__banner = ''' 
                         _____  _   _  _____ _____                      
                        |  __ \| \ | |/ ____|  __ \                     
                        | |  | |  \| | (___ | |__) |___  ___ ___  _ __  
                        | |  | | . ` |\___ \|  _  // _ \/ __/ _ \| '_ \ 
                        | |__| | |\  |____) | | \ \  __/ (_| (_) | | | |
                        |_____/|_| \_|_____/|_|  \_\___|\___\___/|_| |_|
                        ------------------------------------------------
                        Created by: Homeless
                        Version 1.0.0
                        ------------------------------------------------                   
                    '''
        self.__domain = ''
        init()

    def controller(self):

        if os.name =="posix":
            os.system("clear")
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            os.system("cls")

        print(Fore.RED + self.__banner)

        while True:
            print(Fore.RED + '', end='')
            self.__domain = input('INGRESE DOMINIO A CONSULTAR > ')
            print('\n')

            # Instantiating DNSRecon object
            dns_records = DNSRecon()

            # Get records IPv4
            try:

                dns_records.set_domain(self.__domain)
                dns_records.set_type_record('A')
                table = dns_records.get_record_A()
                print('REGISTROS DE DIRECCIONES IPV4')
                print('=' * 60)
                print(tabulate(table, tablefmt='plain'), end='\n\n')

            except dns.exception.DNSException as ex:
                print(ex.__str__(), end='\n\n')

            # Get records MX
            try:
                dns_records.set_type_record('MX')
                table = dns_records.get_record_MX()

                print(Fore.RED + 'REGISTROS DE DIRECCIONES MAIL EXCHANGE (MX)')
                print(Fore.RED + '=' * 60)
                print(tabulate(table, tablefmt='plain'), end='\n\n')

            except dns.exception.DNSException as ex:
                print(ex.__str__(), end='\n\n')

            # Get records NS
            try:
                dns_records.set_type_record('NS')
                table = dns_records.get_record_NS()

                print(Fore.RED + 'REGISTROS DE SERVIDORES DE NOMBRES (NS)')
                print(Fore.RED + '=' * 60)
                print(tabulate(table, tablefmt='plain'), end='\n\n')
            except dns.exception.DNSException as ex:
                print(ex.__str__(), end='\n\n')

            # Perform transfer zone
            try:
                print(Fore.RED + 'REGISTROS OBTENIDOS ZONA TRANFERENCIA (AXFR)')
                print('=' * 60)

                for xfr in dns_records.get_record_xfr():
                    print(xfr)
                print('\n')

                self.__get_brute_force(dns_records)

            except TypeError as ex:
                print(ex.__str__(), end='\n\n')

    # Execute brute force

    def __get_brute_force(self, obj_dns):
        while True:
            print(Fore.BLUE + '', end='')
            question = input('[?] ¿Desea realizar fuerza bruta al dominio, para el descubrimientos '
                             'de servicios. Esto puede tomar varios minutos (y/n)? ')
            print('\n')

            if question == 'Y' or question == 'y':
                print(Fore.RED + 'REGISTROS OBTENIDOS (FUERZA BRUTA)')
                print('='*60)
                for servicio in obj_dns.brute_force():
                    print(servicio[0], servicio[1], servicio[2], servicio[3], servicio[4])
                break
            elif question == 'N' or question == 'n':
                break
            else:
                print(Fore.RED + '[X] Opcion invalida digite "y" para ejecutar fuerza bruta o "n" de lo contrario',
                      end='\n\n')
        print('\n\n')
