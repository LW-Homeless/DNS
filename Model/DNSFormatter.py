class DNSFormatter:

    @staticmethod
    def text_to_list(record_text):
        aux_list = []

        # Convert text to list
        record_list = (record_text.split('\n'))

        for record in record_list:
            aux_list.append(str(record).split(' '))
        return aux_list
