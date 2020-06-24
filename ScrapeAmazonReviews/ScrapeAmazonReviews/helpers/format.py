
def formatting_response_dict(raw, lenRaw):
    response = {}

    for i in range(0, lenRaw):
        item_holder = {}
        for item in raw :
            item_holder[item] = raw[item][i]
        
        response[raw['ASIN'][i]] = item_holder
    
    return response

def formatting_response_list(raw, lenRaw):
    response = []
    for i in range(0, lenRaw):
        item_holder = {}
        for item in raw :
            item_holder[item] = raw[item][i]
        response.append(item_holder)

    return response