
import subprocess
import pandas as pd
import re
import tqdm

input_data = pd.read_csv(
    "/Users/pritul/Downloads/combined_data_23_thru_27.csv")
issue23 = pd.read_csv("/Users/pritul/Downloads/issue23.csv")
issue24 = pd.read_csv("/Users/pritul/Downloads/issue24.csv")
issue25 = pd.read_csv("/Users/pritul/Downloads/issue25.csv")
issue26 = pd.read_csv("/Users/pritul/Downloads/issue26.csv")
issue27 = pd.read_csv("/Users/pritul/Downloads/issue27.csv")
issue_key_set23 = set(issue23['Issue key'])
issue_key_set24 = set(issue24['Issue key'])
issue_key_set25 = set(issue25['Issue key'])
issue_key_set26 = set(issue26['Issue key'])
issue_key_set27 = set(issue27['Issue key'])
bug = []
for i in tqdm.trange(len(input_data)):
    name_ = input_data['Class'][i].split('.')[-1]
    version = input_data['Class'][i].split('.')[2].split('-')[0]
    version = int(version)
    try:
        bug.append(0)
        output = subprocess.check_output(
            'git log -p --grep="{}" | grep PDFBOX'.format(name_), shell=True)
        output = output.decode('utf-8')
        output = output.split("\n")
        for issues in output:
            issues = issues.strip()
            pattern = r'\b(\w+-\d+)'
            match = re.search(pattern, issues)
            if match:
                x = match.group(1)
                if version == 23 and x in issue_key_set23:
                    bug[-1] = 1
                    break
                elif version == 24 and x in issue_key_set24:
                    bug[-1] = 1
                    break
                elif version == 25 and x in issue_key_set25:
                    bug[-1] = 1
                    break
                elif version == 26 and x in issue_key_set26:
                    bug[-1] = 1
                    break
                elif version == 27 and x in issue_key_set27:
                    bug[-1] = 1
                    break
            else:
                continue
    except:
        continue

input_data['bug'] = bug
input_data.to_csv("/Users/pritul/Downloads/final_dataset_se.csv")
