import json
import csv

# Define the fieldnames for the CSV file
fieldnames = ['speaker', 'text', 'act', 'conv_id', 'topic', 'topic_ldaconv', 'topic_ldautt']

# Initialize the act dictionary
act_dict = {}
conv_id_dict = {}

# Number of conversations to process
ctr = 1330

# Process the training set
with open('TrainSet.json', 'r') as json_file:
    with open('TrainSet.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        data = json.load(json_file)
        print(f"Number of conversations in training set: {len(data)}")
        for i in range(min(ctr, len(data))):  # Ensure ctr does not exceed the actual number of conversations
            row = data[i]['turns']
            conversation_id = data[i]['dialogue_id']  # conv_id
            topic = -1
            topic_ldaconv = -1
            topic_ldautt = -1

            for turn in row:
                speaker_id = 0  # speaker
                speaker = turn['speaker']
                if speaker == 'SYSTEM':
                    speaker_id = 1
                utterance = turn['utterance']  # text
                dialogue_act = turn['dialogue_act']  # act
                if dialogue_act not in act_dict:
                    act_dict[dialogue_act] = len(act_dict) + 1
                if conversation_id not in conv_id_dict:
                    conv_id_dict[conversation_id] = len(conv_id_dict) + 1
                new_row = {'speaker': speaker_id, 'text': utterance, 'act': act_dict[dialogue_act], 'conv_id': conv_id_dict[conversation_id],
                           'topic': topic, 'topic_ldaconv': topic_ldaconv, 'topic_ldautt': topic_ldautt}
                writer.writerow(new_row)

# Save the act_dict to a file for later use
with open('act_dict.json', 'w') as act_dict_file:
    json.dump(act_dict, act_dict_file)

print(f"Training set conversion completed. Output written to TrainSet.csv")

import json
import csv

# Load the act dictionary created during training set processing
with open('act_dict.json', 'r') as act_dict_file:
    act_dict = json.load(act_dict_file)

fieldnames = ['speaker', 'text', 'act', 'conv_id', 'topic', 'topic_ldaconv', 'topic_ldautt']

# Process the test set
with open('TestSet.json', 'r') as json_file:
    with open('TestSet.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        conv_id_dict = {}  # Reset the conversation ID dictionary for the test set
        data = json.load(json_file)
        print(f"Number of conversations in test set: {len(data)}")
        for i in range(len(data)):  # Process all conversations in the test set
            row = data[i]['turns']
            conversation_id = data[i]['dialogue_id']  # conv_id
            topic = -1
            topic_ldaconv = -1
            topic_ldautt = -1

            for turn in row:
                speaker_id = 0  # speaker
                speaker = turn['speaker']
                if speaker == 'SYSTEM':
                    speaker_id = 1
                utterance = turn['utterance']  # text
                dialogue_act = turn['dialogue_act']  # act
                if dialogue_act not in act_dict:
                    act_dict[dialogue_act] = len(act_dict) + 1  # This should rarely happen unless test set has unseen acts
                if conversation_id not in conv_id_dict:
                    conv_id_dict[conversation_id] = len(conv_id_dict) + 1
                new_row = {'speaker': speaker_id, 'text': utterance, 'act': act_dict[dialogue_act], 'conv_id': conv_id_dict[conversation_id],
                           'topic': topic, 'topic_ldaconv': topic_ldaconv, 'topic_ldautt': topic_ldautt}
                writer.writerow(new_row)

print(f"Test set conversion completed. Output written to TestSet.csv")