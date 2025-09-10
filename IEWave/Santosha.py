import json


appts = []
records = []
def generate_campaign_csv():
    result = 'Name,WhatsApp,Phone,Address,Tags'
    try:
        with open('C:\\Users\\Dell\\Downloads\\IE-Wave\\Santosha\\Ecity-IE-ALL.json', 'r') as file:
            data = json.load(file)
            records = data.get("records", [])
            with open('C:\\Users\\Dell\\Downloads\\IE-Wave\\Santosha\\Appts.txt', 'r') as txt_file:
                for line in txt_file:
                    processed_line = line.strip().split(',')
                    if len(processed_line) > 1:
                        if processed_line[1].__contains__('/'):
                            processed_line[1] = processed_line[1].strip().split('/')
                        else:
                            processed_line[1] = [processed_line[1].strip()]
                    appts.append(processed_line)

            for appt in appts:
                result += ('\n\n'+appt[0] + (' - ' + appt[1][0] if len(appt) > 1 else '')).replace(',', ' ')
                for record in records:
                    street = record.get("street") if record.get("street") else ""
                    street2 = record.get("street2") if record.get("street2") else ""
                    address = remove_after_phrase((street + street2).replace('\r\n', ' ').replace('\n', ' '))
                    if appt[0].lower() in address.lower():
                        
                        if len(appt) > 1 and len(appt[1]) >= 1:
                            for appName in appt[1]:
                                if appName.lower() in address.lower():
                                    result += '\n' + record['name'] + ',' + get_whatsapp_number(record) + ',' + record['phone'] + ',' + address.replace(',', ' ') + ',' + str(len(record['pgm_tag_ids']))
                                    # print(f"Match found: {address}")
                        else:
                            result += '\n' + record['name'] + ',' + get_whatsapp_number(record) + ',' + record['phone'] + ',' + address.replace(',', ' ') + ',' + str(len(record['pgm_tag_ids']))
                            # print(f"Match found outside: {address}")
        print(result)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_whatsapp_number(record):
    whatsappNumber = record.get("whatsapp_country_code") + '-' if record.get("whatsapp_country_code") else ""
    whatsappNumber += record.get("whatsapp_number") if record.get("whatsapp_number") else ""
    return whatsappNumber

def remove_after_phrase(address, phrases = ['near ', 'opp ', 'opposite ']):
    index = -1
    for phrase in phrases:
        lower_text = address.lower()
        currIndex = lower_text.find(phrase)
        if currIndex != -1:
            if index == -1: 
                index = currIndex
            elif currIndex < index:
                index = currIndex
    return address[:index] if index != -1 else address


generate_campaign_csv()
