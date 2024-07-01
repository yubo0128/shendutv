import json

# Function to delete elements where the string contains 'YW'
def delete_elements_with_YW(data, key):
    # Identify the indices where the string contains 'YW'
    indices_to_delete = [i for i, s in enumerate(data[key][0]) if 'YW' in s]

    # Delete the identified indices from all three lists
    for index in sorted(indices_to_delete, reverse=True):
        del data[key][0][index]
        del data[key][1][index]
        del data[key][2][index]

    return data

def delete_elements_with_SS(data):
    keys = data.keys()
    for key in keys:
        # Identify the indices where the string contains 'YW'
        indices_to_delete = [i for i, s in enumerate(data[key][0]) if 'SS' in s]

        # Delete the identified indices from all three lists
        for index in sorted(indices_to_delete, reverse=True):
            del data[key][0][index]
            del data[key][1][index]
            del data[key][2][index]

    return data


# Read JSON data from a file
with open('modified_B_statis.json', 'r') as file:
    json_data = json.load(file)

# Modify the JSON data
modified_data = delete_elements_with_SS(json_data)

# Save the modified JSON data back to a file
with open('modified_B_statis.json', 'w') as file:
    json.dump(modified_data, file, indent=4)

print("Modified JSON data saved to 'modified_data.json'.")