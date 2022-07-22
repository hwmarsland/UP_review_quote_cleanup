import pandas as pd
import re
import numpy as np
import sys

raw_data = pd.read_excel(sys.argv[1], index_col = 0)
edited_data = raw_data.copy()
edited_data

edited_data['temp'] = edited_data['Copy Filtered::Text']

edited_data = edited_data.reset_index()

edited_data['temp'] = edited_data['temp'].replace('<!--', '===', regex=True)
edited_data['temp'] = edited_data['temp'].replace('-->', '= =', regex=True)

edited_data['temp'] = edited_data['temp'].replace('###', '<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('##', '<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('#', '</i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('“', '"', regex=True)
edited_data['temp'] = edited_data['temp'].replace('”', '"', regex=True)
edited_data['temp'] = edited_data['temp'].replace('’', '\'', regex=True)
edited_data['temp'] = edited_data['temp'].replace('‘', '\'', regex=True)

counter = 0
for i in edited_data['temp']:
    text = str(re.findall('"([^"]*)"', str(i)))
    text = text.replace('"', '\'')
    edited_data.at[counter, '<Text>'] = '"' + text + '"'
    counter = counter + 1

edited_data['<Text>'] = edited_data['<Text>'].replace('  ', ' ', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('""', np.nan, regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('\n', '', regex=True)

counter = 0
for i in edited_data['temp']:
    temp = re.sub('"([^"]*)"', '', str(i))
    edited_data.at[counter, 'temp'] = str(temp)
    counter = counter + 1

edited_data['temp'] = edited_data['temp'].replace('—', '--', regex=True)
edited_data['temp'] = edited_data['temp'].replace('–', '--', regex=True)


counter = 0
for i in edited_data['temp']:
    source = edited_data.at[counter, 'temp']
    edited_data.at[counter, '<TextSource>'] = str(source)
    counter = counter + 1


edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('  ', ' ', regex=True)
edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('\n', '', regex=True)

counter = 0
for i in edited_data['<TextSource>']:
    if str(i).startswith('--') or str(i).startswith(' --') or str(i).startswith('===') or str(i) == '' or str(i).startswith('<i>') or str(i).startswith('-<i>'):
        pass
    elif str(i) == 'nan':
        edited_data.at[counter,'<TextSource>'] = ''
    else:
        edited_data.at[counter,'<Error>'] = 'MARKED AS ERROR'
    counter = counter + 1

edited_data['<TextSource>'] = edited_data['<TextSource>'].replace(' --', '', regex=True)
edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('--', '', regex=True)
edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('."', '', regex=True)
edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('-<i>', '<i>', regex=True)

edited_data['<Text>'] = edited_data['<Text>'].replace('\n', '', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('\xa0', '', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('.."', '."', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('.."', '."', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('"[[\']', '"', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('"\'', '"', regex=True)

counter = 0
for i in edited_data['<Text>']:
    if str(i) == '."':
        edited_data.at[counter,'<Text>'] = ''
    counter = counter + 1

edited_data = edited_data.drop(columns=['temp'])
edited_data = edited_data.replace('--', '—', regex=True)

edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('===', '<!--', regex=True)
edited_data['<TextSource>'] = edited_data['<TextSource>'].replace('= =', '-->', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('===', '<!--', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('= =', '-->', regex=True)

writer = pd.ExcelWriter(str(sys.argv[1])+' edited-data.xlsx', engine='xlsxwriter')
edited_data.to_excel(writer, sheet_name='Sheet1')
writer.save()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python blurb_cleanup_v1_0.py <filename>')
