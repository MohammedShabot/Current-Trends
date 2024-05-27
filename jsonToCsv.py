#convert json to csv
import json
import csv

ctr = 1330

fieldnames = ['speaker', 'text', 'act', 'conv_id', 'topic', 'topic_ldaconv', 'topic_ldautt']

with open('TestSet.json', 'r') as json_file:
    with open('TestSet.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        act_dict = {}
        conv_id_dict = {}

        data = json.load(json_file)
        for i in range(ctr):
            row = data[i]['turns']
            conversation_id = data[i]['dialogue_id'] #conv_id
            print(conversation_id)
            topic = -1
            topic_ldaconv = -1
            topic_ldautt = -1

        
                #print(row)
            for turn in row:
                speaker_id = 0 #speaker
                speaker = turn['speaker']
                if speaker == 'SYSTEM': 
                    speaker_id = 1
                utterance = turn['utterance'] #text
                dialogue_act = turn['dialogue_act'] #act
                if dialogue_act not in act_dict:
                    act_dict[dialogue_act] = len(act_dict) + 1 
                    #print(act_dict[dialogue_act])
                if conversation_id not in conv_id_dict:
                    conv_id_dict[conversation_id] = len(conv_id_dict) + 1
                    #print(conv_id_dict[conversation_id])
                new_row = {'speaker': speaker_id, 'text': utterance, 'act': act_dict[dialogue_act], 'conv_id': conv_id_dict[conversation_id]
                            , 'topic': topic, 'topic_ldaconv': topic_ldaconv, 'topic_ldautt': topic_ldautt}
                writer.writerow(new_row)
        print(act_dict)
        print(conv_id_dict)

with open('TestSet.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)
    for row in data:
        print(row)

        # for row in data:
        #     act = row['act']
        #     if act not in act_dict:
        #         act_dict[act] = len(act_dict) + 1  # Assign new ID
        #         print(len(act_dict) + 1)
        #     row['act'] = act_dict[act]  # Update act in the row

        

    #new_row = {speaker}


# with open('TestSet.csv', 'w', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(data[0].keys())  # Write header
#     for item in data:
#         writer.writerow(item.values())

# with open('TestSet.csv', 'r') as csv_file:
#     # Create a CSV reader object
#     csv_reader = csv.reader(csv_file)

#     # Iterate over each row in the CSV file
#     for row in csv_reader:
#         # Split each row on the "," separator
#         conversation_id = row[0].split(',')
#         service= row[1].split(',')
#         conversation = row[2].split(',')
#         for utterance in conversation:
#             print(utterance)
#             index = utterance['index']
#             dialogue_act = utterance['dialogue_act']
#             utterance_text = utterance['utterance']

            # print("Speaker:", speaker)
            # print("Dialogue Act:", dialogue_act)
            # print("Utterance:", utterance_text)
            # print() 

def update_act_ids(input_file, output_file):
    act_dict = {}  # Dictionary to store act mappings

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        print(data)

        for row in data:
            act = row['act']
            if act not in act_dict:
                act_dict[act] = len(act_dict) + 1  # Assign new ID
                print(len(act_dict) + 1)
            row['act'] = act_dict[act]  # Update act in the row

    # Write updated data to a new CSV file
            with open(output_file, 'a', newline='') as csvwriter:
                fieldnames = ['speaker', 'text', 'act', 'conv_id', 'topic', 'topic_ldaconv', 'topic_ldautt;;']
                writer = csv.DictWriter(csvwriter, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(row)


# Example usage
input_file = 'TestSet.csv'
output_file = 'test.csv'
#update_act_ids(input_file, output_file)
print("Conversion completed. Output written to", output_file)