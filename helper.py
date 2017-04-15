import json
import urllib.request

url_begin = "http://census.daybreakgames.com/get/ps2:v2/character/?"
general_stats_url = "&c:resolve=outfit_member_extended&c:resolve=stat_history,stat,stat_by_faction"
fisu_url = "http://ps2.fisu.pw/player/?name="
planetstats_url = "http://www.planetstats.net/"
outfit_url_begin = "https://census.daybreakgames.com/get/ps2:v2/outfit/?alias_lower="
outfit_url_end = "&c:resolve=member_character(name)"



def get_stats_from_census(char_name="", char_id=0):
    result = {}
    if char_name != "":
        url = "name.first_lower=" + char_name.lower()
    else:
        url = "character_id=" + str(char_id)

    json_result = get_json_from_url(url_begin + url + general_stats_url)
    num_results = json_result["returned"]
    char_data = json_result["character_list"][num_results - 1]

    result["name"] = char_data["name"]["first"]
    result["id"] = char_data["character_id"]

    curr_stat_arr = char_data["stats"]["stat_history"]
    for stat in curr_stat_arr:
        result[stat["stat_name"]] = int(stat["all_time"])

    curr_stat_arr = char_data["stats"]["stat"]
    for stat in curr_stat_arr:
        if stat["stat_name"] == "deaths":
            continue
        if not stat["stat_name"] in result:
            result[stat["stat_name"]] = 0
        result[stat["stat_name"]] += int(stat["value_forever"])

    curr_stat_arr = char_data["stats"]["stat_by_faction"]
    for stat in curr_stat_arr:
        if stat["stat_name"] == "kills" or stat["stat_name"] == "deaths":
            continue
        if not stat["stat_name"] in result:
            result[stat["stat_name"]] = 0
        result[stat["stat_name"]] += int(stat["value_forever_nc"])
        result[stat["stat_name"]] += int(stat["value_forever_vs"])
        result[stat["stat_name"]] += int(stat["value_forever_tr"])

    return result


def replace_html_tags(string, replacement):
    begin = 0
    while begin < len(string) - 1:
        begin = string.find("<")
        end = string.find(">", begin)
        string = string[:begin] + replacement + string[end + 1:]
    return string


def remove_duplicate_separators(string, separator):
    # padding string with one character
    string = "a" + string

    index = 0
    while index != -1:
        index = string.find(separator, index)
        while index + 1 < len(string) and string[index + 1] == separator:
            string = string[:index] + string[index + 1:]
        if index > 0:
            index += 1

    # removing padding from string
    return string[1:]


def string_to_dict(string, separator="|"):
    result = {}
    while len(string) > 0:
        separator_pos = string.find(separator)
        end_value = string.find(separator, separator_pos + 1)
        if end_value == -1:
            end_value = len(string) - 1
        if separator_pos == len(string) - 1:
            break
        key = string[:separator_pos]
        result[key] = string[separator_pos + 1:end_value + 1]
        result[key] = result[key].replace(separator, "")
        string = string[end_value + 1:]
    return result


def time_to_mins(time):
    days_pos = time.find("d")
    days = 0
    if days_pos != -1:
        days = int(time[:days_pos])
        time = time[days_pos + 1:]
    else:
        days_pos = 0
        time = time[days_pos:]
    hours_pos = time.find("h")
    hours = 0
    if hours_pos != -1:
        hours = int(time[:hours_pos])
    minutes = (days * 24 + hours) * 60
    return minutes


def dict_string_to_number(dictionary):
    for key in dictionary:
        value = dictionary[key]
        if value.find("%") != -1:
            value = value.replace("%", "")
        if value.find(",") != -1:
            value = value.replace(",", "")
        if value.find("_") != -1:
            value = value.replace("_", "")
        if value.find("d") != -1 or value.find("h") != -1:
            value = time_to_mins(value)
        elif value.find(".") != -1:
            value = float(value)
        else:
            value = int(value)
        dictionary[key] = value
    return dictionary


def get_stats_from_fisu(name):
    data = urllib.request.urlopen(fisu_url + name.lower())
    statistics_string = data.read().decode("utf-8")
    stats_pos_begin = statistics_string.find("OVERALL")
    stats_pos_end = statistics_string.find("BATTLE RANK", stats_pos_begin)
    statistics_string = statistics_string[stats_pos_begin:stats_pos_end]
    statistics_string = replace_html_tags(statistics_string, "|")
    statistics_string = remove_duplicate_separators(statistics_string, "|")
    statistics_string = statistics_string.lower()
    statistics_string = statistics_string.replace(" ", "_")
    statistics_string = statistics_string.replace("(", "")
    statistics_string = statistics_string.replace(")", "")
    statistics_string = statistics_string[8:]
    result = string_to_dict(statistics_string)
    result = dict_string_to_number(result)
    return result


def get_json_from_url(url):
    data = urllib.request.urlopen(url)
    json_data = json.loads(data.read().decode("utf-8"))
    return json_data


def format_float(number, decimal_places=2):
    number = str(number)
    dot_index = number.find(".")
    if dot_index != -1:
        number = number[:dot_index + decimal_places + 1]
    return float(number)


def create_header(metrics):
    header = ["Name"]
    for metric in metrics:
        header.append(metric.name)
    return header


def remove_duplicates(arr):
    result = []
    for elem in arr:
        if elem not in result:
            result.append(elem)
    return result


def sort_rows(data, begin, end):
    tmp = data[begin:end + 1]
    sorting = [elem[0].lower() for elem in tmp]
    sorting.sort()
    result = []
    for i in range(begin):
        result.append(data[i])
    for elem in sorting:
        for data_point in data:
            if elem == data_point[0].lower():
                result.append(data_point)
    for i in range(end+1, len(data)):
        result.append(data[i])
    return result


def get_outfit_members(outfit_tag):
    url = outfit_url_begin + outfit_tag.lower() + outfit_url_end
    data = get_json_from_url(url)
    members = []
    for data_point in data["outfit_list"][0]["members"]:
        members.append(data_point["name"]["first"])
    return members


import dryscrape


def get_month_data(name):
    data = urllib.request.urlopen(planetstats_url + name.lower()).read().decode("utf-8")
    # print(data)
    session = dryscrape.Session()
    session.visit(planetstats_url + name.lower())
    response = session.body()
    print(response)
