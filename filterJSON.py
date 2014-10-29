from modifyJSON import crawl_data


required_keys = ['first_name', 'last_name', 'middle_name',
                 'birth_date', 'jersey', 'last_team',
                 'height', 'weight'];
finalJSON = []

for i in range (0, len(crawl_data)):
    output = crawl_data[i]
    filtered_values = { req_key: output[req_key] for req_key in required_keys }
    finalJSON.append(filtered_values)


