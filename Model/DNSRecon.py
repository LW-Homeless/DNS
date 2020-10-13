from Model.DNSFormatter import DNSFormatter
import dns.resolver
import dns.zone
import dns.query
import os


class DNSRecon:

    def __init__(self):
        self.__domain = ''
        self.__type_record = ''
        self.__record_A = None
        self.__record_MX = None
        self.__record_NS = None
        self.__record_axfr = None

    def get_record_A(self):
        try:
            answer = dns.resolver.resolve(self.__domain, self.__type_record)
            answer = DNSFormatter.text_to_list(answer.rrset.to_rdataset().to_text())
            self.__record_A = answer

            return self.__record_A

        except dns.resolver.NXDOMAIN:
            raise dns.resolver.NXDOMAIN('El nombre de la consulta DNS no existe para el dominio: ' + self.__domain)
        except dns.resolver.NoAnswer:
            raise dns.resolver.NoAnswer('La respuesta de DNS no contiene una respuesta a la pregunta: '
                                        + self.__domain + ':' + 'IPv4')

    def get_record_MX(self):
        try:
            answer = dns.resolver.resolve(self.__domain, self.__type_record)
            answer = DNSFormatter.text_to_list(answer.rrset.to_rdataset().to_text())
            self.__record_MX = answer

            return self.__record_MX

        except dns.resolver.NXDOMAIN:
            raise dns.resolver.NXDOMAIN('El nombre de la consulta DNS no existe para el dominio: ' + self.__domain)
        except dns.resolver.NoAnswer:
            raise dns.resolver.NoAnswer('La respuesta de DNS no contiene una respuesta a la pregunta: '
                                        + self.__domain + ':' + self.__type_record)

    def get_record_NS(self):
        try:
            answer = dns.resolver.resolve(self.__domain, self.__type_record)
            answer = DNSFormatter.text_to_list(answer.rrset.to_rdataset().to_text())

            self.__record_NS = answer

            for record_ns in self.__record_NS:
                ip = dns.resolver.resolve(record_ns[3], 'A')
                record_ns.append(ip.rrset.to_text().split(' ')[-1:][0])

            return self.__record_NS

        except dns.resolver.NXDOMAIN:
            raise dns.resolver.NXDOMAIN('El nombre de la consulta DNS no existe para el dominio para el dominio: ' + self.__domain)
        except dns.resolver.NoAnswer:
            raise dns.resolver.NoAnswer('La respuesta de DNS no contiene una respuesta a la pregunta: '
                                        + self.__domain + ':' + self.__type_record)

    def get_record_xfr(self):
        self.__record_axfr = []

        try:
            for record_ns in self.__record_NS:
                try:
                    ip = record_ns[-1:][0]
                    zone = dns.zone.from_xfr(dns.query.xfr(ip, self.__domain))
                    self.__record_axfr.append(zone)

                    for z in zone.iterate_rdatas(1):
                        z_transfer = [domain, servicio, ttl, ip] = self.__domain, str(z[0]), str(z[1]), str(z[2])
                        self.__record_axfr.append(z_transfer)

                except dns.query.TransferError:
                    self.__record_axfr.append('El servidor NS denego la solicitud de zona de transferencia: '
                                              + record_ns[3])
                    continue
                except dns.exception.FormError:
                    self.__record_axfr.append('El servidor NS denego la solicitud de zona de transferencia: '
                                              + record_ns[3])
                    continue
                except EOFError:
                    self.__record_axfr.append('Error de consulta de registro AXFR: paquete dañado: ' + record_ns[3])
        except TypeError:
            raise TypeError('No existen registro para realizar zona de transferencia')
        return self.__record_axfr

    def brute_force(self):
        path = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(path, 'assets', 'dictionary.txt')

        with open(path, 'rt') as file:

            for line in file:
                try:
                    domain = line.replace('\n', '') + '.' + self.__domain
                    response = dns.resolver.resolve(domain, 'A')
                    yield response.rrset.to_text().split(' ')
                    response = None
                except dns.resolver.NXDOMAIN:
                    response = None
                    continue
                except dns.resolver.NoAnswer:
                    response = None
                    continue
                except dns.resolver.Timeout:
                    response = None
                    continue
        file.close()

    def __get_ip_record(self, records):
        for record in records:
            index = len(record) - 1
            r = dns.resolver.resolve(record[index], 'A')
            ip = r.rrset.to_rdataset().to_text().split(' ')[-1:][0]
            record.append(ip)

    def set_domain(self, domain):
        self.__domain = str(domain).lower()

    def set_type_record(self, type_record):
        self.__type_record = str(type_record).upper()
