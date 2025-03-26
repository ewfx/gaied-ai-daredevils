{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[{"file_id":"1Yqs9Z1UkrU09BY0lAECIrBRkrdQf9sTN","timestamp":1742835101783}],"authorship_tag":"ABX9TyMofEUTALA78d0+CxD4WtEO"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","source":["#!pip install datasets\n","\n","from transformers import pipeline\n","from datasets import load_dataset\n","from sklearn.ensemble import RandomForestClassifier\n","from sklearn.model_selection import train_test_split\n","from sklearn.feature_extraction.text import TfidfVectorizer\n","from datasets import Dataset\n","from sklearn.metrics import accuracy_score, classification_report\n","import pandas as pd\n","import numpy as np\n","\n","import os\n","import email\n","import re\n","import json\n","\n","\n","def fit_training_data_into_model(email_content):\n","\n","\n","  df_trainingdata2 = pd.read_csv(\"TrainingData2.csv\", header=0, encoding='latin-1')\n","  df_trainingdata3 = pd.read_csv(\"TrainingData3.csv\", header=0, encoding='latin-1')\n","\n","\n","  df = pd.concat([df_trainingdata2, df_trainingdata3])\n","  #df = pd.merge(df_trainingdata2, df_trainingdata3, left_index=True, right_index=True)\n","\n","  #print(df.head(40))\n","\n","  df2 = df.Email.to_frame()\n","\n","  ds_train = Dataset.from_pandas(df2)  # Creating training data\n","\n","  df3 = df.PrimaryAsk.to_frame()\n","\n","  ds_primask_test = Dataset.from_pandas(df3)  # Creating primary ask test data\n","\n","  df4 = df.SecondaryAsk.to_frame()\n","\n","  ds_secask_test = Dataset.from_pandas(df4)  # Creating secondary ask test data\n","\n","  # Loading dataset_sheet.csv\n","\n","  df5 = pd.read_csv(\"dataset_sheet.csv\", header=0)\n","\n","  df6 = df5.prompt.to_frame()\n","\n","  ds_train_datasetsheetcsv = Dataset.from_pandas(df6)  # Creating Training data\n","\n","  df7 = df5.label.to_frame()\n","\n","  ds_test_datasetsheetcsv = Dataset.from_pandas(df7)  # Creating Primary Ask test data\n","\n","  df8 = df5.label2.to_frame()\n","\n","  ds_test_datasetsheetcsv2 = Dataset.from_pandas(df8)  # Creating Secondary Ask test data\n","\n","  # Loading train.csv\n","\n","  df7 = pd.read_csv(\"train.csv\", header=0)\n","\n","  df8 = df7.Email.to_frame()\n","\n","  ds_train_traincsv = Dataset.from_pandas(df8)  # Creating train data\n","\n","  df9 = df7.Intent.to_frame()\n","\n","  ds_test_traincsv = Dataset.from_pandas(df9)  # Creating Primary Ask test data\n","\n","  df10 = df7.SecondaryIntent.to_frame()\n","\n","  ds_test_traincsv2 = Dataset.from_pandas(df10)  # Creating Secondary Ask test data\n","\n","  # Use a pipeline as a high-level helper\n","  pipe = pipeline(\"feature-extraction\", model=\"nicoladecao/msmarco-word2vec256000-distilbert-base-uncased\")\n","  # pipe = pipeline(\"text-classification\", model=\"keshavkmr076/email-intent-classification\")\n","  #pipe = pipeline(\"text-classification\", model=\"alex019/email_sentiment_classifier\")\n","\n","  #print(ds)\n","\n","  # Extract data from the 'E' (email) column\n","  emails = ds_train\n","  emails2 = ds_train_datasetsheetcsv\n","  emails3 = ds_train_traincsv\n","\n","  # Extract data from the 'L' (label) column\n","  labels = ds_primask_test\n","  labels2 = ds_secask_test\n","  labels3 = ds_test_datasetsheetcsv\n","  labels4 = ds_test_datasetsheetcsv2\n","  labels5 = ds_test_traincsv\n","  labels6 = ds_test_traincsv2\n","\n","\n","  # Example: Print the first 5 emails and their labels\n","  #for i in range(len(emails3)):\n","  #    print(f\"Email: {emails[i]}, Label: {labels5[i]}, Label2: {labels6[i]}\")\n","\n","  #for j in range(len(ds2['train'])):\n","  #    print(f\"Email: {emails2[i]}, Label: {labels2[i]}\")\n","\n","\n","  X_train, X_test, y_train, y_test = train_test_split(emails['Email'] + emails2['prompt'] + emails3['Email'], labels['PrimaryAsk'] + labels3['label'] + labels5['Intent'] , test_size=0.2, random_state=42)\n","  X_train2, X_test2, y_train2, y_test2 = train_test_split(emails['Email'] + emails2['prompt'] + emails3['Email'], labels2['SecondaryAsk'] + labels4['label2'] + labels6['SecondaryIntent'], test_size=0.2, random_state=42)\n","\n","\n","  # Feature extraction using TF-IDF\n","  vectorizer = TfidfVectorizer()\n","  X_train_vec = vectorizer.fit_transform(X_train)\n","  X_test_vec = vectorizer.transform(X_test)\n","\n","  # Feature extraction using TF-IDF for sub request type\n","  vectorizer1 = TfidfVectorizer()\n","  X_train_2_vec = vectorizer1.fit_transform(X_train2)\n","  X_test_2_vec = vectorizer.transform(X_test2)\n","\n","  # Train a Random Forest classifier\n","  rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)\n","  rf_classifier.fit(X_train_vec, y_train)\n","\n","  rf_classifier2 = RandomForestClassifier(n_estimators=100, random_state=42)\n","  rf_classifier2.fit(X_train_2_vec, y_train2)\n","\n","  # Make predictions on the test set\n","  y_pred = rf_classifier.predict(X_test_vec)\n","\n","  y_pred2 = rf_classifier2.predict(X_test_2_vec)\n","\n","  # Evaluate the model (e.g., using accuracy, precision, recall, F1-score)\n","  # ... (add your evaluation metrics here)\n","  accuracy = accuracy_score(y_test, y_pred)\n","  print(\"Accuracy:\", accuracy)\n","  #print(classification_report(y_test, y_pred))\n","\n","  # Evaluate the model for sub request type\n","  accuracy2 = accuracy_score(y_test2, y_pred2)\n","  print(\"Accuracy for sub request type:\", accuracy2)\n","  #print(classification_report(y_test2, y_pred2))\n","\n","  new_email = email_content\n","\n","  new_email_vec = vectorizer.transform([new_email])\n","  #new_features = pipe(new_email)[0][0]\n","  predicted_class = rf_classifier.predict(new_email_vec)[0]\n","  predicted_class2 = rf_classifier2.predict(new_email_vec)[0]\n","  print(f\"Predicted class for new email: {predicted_class}\")\n","  print(f\"Predicted secondary class for new email: {predicted_class2}\")\n","\n","  return predicted_class + '|' + predicted_class2\n","\n","\n","def extract_email_content(filepath):\n","    \"\"\"\n","    Extracts email content without greetings and salutations from a file.\n","\n","    Args:\n","        filepath (str): Path to the email file.\n","\n","    Returns:\n","        str: Extracted email content, or None if an error occurs.\n","    \"\"\"\n","    try:\n","        with open(filepath, 'r', encoding='utf-8') as f:\n","            msg = email.message_from_file(f)\n","\n","        if msg.is_multipart():\n","            for part in msg.walk():\n","                content_type = part.get_content_type()\n","                content_disposition = str(part.get('Content-Disposition'))\n","\n","                if content_type == 'text/plain' and 'attachment' not in content_disposition:\n","                    body = part.get_payload(decode=True).decode()\n","                    break #Take the first plain text part.\n","        else:\n","            body = msg.get_payload(decode=True).decode()\n","\n","\n","\n","        #\n","\n","        # Remove greetings and salutations using regular expressions. This is a basic approach and may need refinement.\n","        body = re.sub(r'^(Dear|Hello|Hi|Greetings|Good morning|Good afternoon|Good evening|Regards|& Regards|Best regards|Sincerely|Thanks|Thank you|Yours sincerely|Yours faithfully),?\\s*[\\w\\s,]*\\n?', '', body, flags=re.MULTILINE | re.IGNORECASE)\n","        body = re.sub(r'^(Dear|Hello|Hi|Greetings|Good morning|Good afternoon|Good evening|Regards|& Regards|Best regards|Sincerely|Thanks|Thank you|Yours sincerely|Yours faithfully),?\\s*[\\w\\s,]*$', '', body, flags=re.MULTILINE | re.IGNORECASE) #handles the edge case when the greeting is the only line.\n","\n","        #remove trailing blank lines.\n","        body = body.strip()\n","\n","        return body\n","\n","    except Exception as e:\n","        print(f\"Error processing {filepath}: {e}\")\n","        return None\n","\n","# Reading attachments\n","def read_email_attachment(email_file_path):\n","\n"," try:\n","  with open(email_file_path, 'rb') as fp:\n","    msg = email.message_from_binary_file(fp)\n","\n","  attachments = []\n","  for part in msg.walk():\n","    if part.get_content_maintype() == 'multipart':\n","      continue\n","    if part.get('Content-Disposition') is None:\n","      continue\n","\n","    filename = part.get_filename()\n","    if filename:\n","      att_data = part.get_payload(decode=True)\n","      attachments.append((filename, att_data))\n","\n","  return attachments\n","\n"," except Exception as e:\n","        print(f\"Error processing {email_file_path}: {e}\")\n","        return None\n","\n","#\n","\n","def process_email_folder(folder_path):\n","    \"\"\"\n","    Processes all email files in a folder and prints the extracted content.\n","\n","    Args:\n","        folder_path (str): Path to the folder containing email files.\n","    \"\"\"\n","\n","    subject_line_vec = []\n","    prediction_result_vec = []\n","    attachment_content = ''\n","\n","    for filename in os.listdir(folder_path):\n","        if filename.endswith((\".eml\", \".txt\")):  # Add or remove extensions as needed\n","            filepath = os.path.join(folder_path, filename)\n","            content = extract_email_content(filepath)\n","            attachments = read_email_attachment(filepath)\n","            subject_line = content.splitlines()[0]\n","            print(f\"Subject Line: {subject_line}\")\n","            if content and (subject_line not in subject_line_vec):\n","                #print(f\"Content from {filename}:\\n{content}\\n{'-'*40}\")\n","                prediction_output = fit_training_data_into_model(content.replace(\"\\n\", \" \"))\n","                print(f\"Prediction output: {prediction_output}\")\n","                prediction_result_vec.append({\n","                \"email_text\": subject_line,\n","                \"request_type\": prediction_output.split('|')[0],\n","                \"sub_request_type\": prediction_output.split('|')[1]\n","                })\n","                #for filename, content in attachments:\n","                #  print(f\"Attachment: {filename}\")\n","\n","                # You can process the content here, e.g., save it to a file:\n","                #  with open(filename, 'wb') as f:\n","                #    attachment_content = attachment_content + f.write(content)\n","\n","                # Passing the attachment content to the model\n","                #prediction_output_for_attachment = fit_training_data_into_model(attachment_content)\n","                #print(f\"Prediction output for attachment : {prediction_output_for_attachment}\")\n","\n","                print(\"\\n\")\n","                subject_line_vec.append(subject_line)\n","\n","\n","    with open('/content/Email_Classification_Results.json', 'w') as f:\n","      json.dump(prediction_result_vec, f, indent=4)\n","\n","    print(\"JSON file created successfully.\")\n","\n","\n","# Example usage:\n","folder_path = \"/content/Email_Folder\" #replace with your folder path.\n","process_email_folder(folder_path)\n","\n","\n","#fit_training_data_into_model(\"Loan has been disbursed. Account statement needs to be checked.\")\n","\n"],"metadata":{"colab":{"base_uri":"https://localhost:8080/"},"id":"X2B4-EG2D0XR","executionInfo":{"status":"ok","timestamp":1743001380193,"user_tz":-330,"elapsed":16026,"user":{"displayName":"Subhayan Roy","userId":"06587787499107266654"}},"outputId":"d8d3ed6a-972c-475a-cb24-12a3198f5b94"},"execution_count":120,"outputs":[{"output_type":"stream","name":"stdout","text":["Subject Line: Re : CANTOR FITZGERALD LP USD 425MM MAR22 / REVOLVER / CANTOR FIT00037\n"]},{"output_type":"stream","name":"stderr","text":["Device set to use cpu\n"]},{"output_type":"stream","name":"stdout","text":["Accuracy: 0.8341968911917098\n","Accuracy for sub request type: 0.8290155440414507\n","Predicted class for new email: Money Movement\n","Predicted secondary class for new email: Money Movement - Outbound\n","Prediction output: Money Movement|Money Movement - Outbound\n","\n","\n","Subject Line: Re : CANTOR FITZGERALD LP USD 425MM MAR22 / REVOLVER / CANTOR FIT00037\n","Subject Line: BORROWER:\n"]},{"output_type":"stream","name":"stderr","text":["Device set to use cpu\n"]},{"output_type":"stream","name":"stdout","text":["Accuracy: 0.8341968911917098\n","Accuracy for sub request type: 0.8290155440414507\n","Predicted class for new email: Money Movement\n","Predicted secondary class for new email: Money Movement - Inbound\n","Prediction output: Money Movement|Money Movement - Inbound\n","\n","\n","Subject Line: ---------- Forwarded message ---------\n"]},{"output_type":"stream","name":"stderr","text":["Device set to use cpu\n"]},{"output_type":"stream","name":"stdout","text":["Accuracy: 0.8341968911917098\n","Accuracy for sub request type: 0.8290155440414507\n","Predicted class for new email: Money Movement\n","Predicted secondary class for new email: Money Movement - Outbound\n","Prediction output: Money Movement|Money Movement - Outbound\n","\n","\n","Subject Line: Re : Citibank NA USD 425MM MAR22 / REVOLVER / CANTOR FIT00037\n"]},{"output_type":"stream","name":"stderr","text":["Device set to use cpu\n"]},{"output_type":"stream","name":"stdout","text":["Accuracy: 0.8341968911917098\n","Accuracy for sub request type: 0.8290155440414507\n","Predicted class for new email: Money Movement\n","Predicted secondary class for new email: Money Movement - Outbound\n","Prediction output: Money Movement|Money Movement - Outbound\n","\n","\n","JSON file created successfully.\n"]}]}]}