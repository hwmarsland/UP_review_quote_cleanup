import pandas as pd
import re
import numpy as np
import sys

raw_data = pd.read_excel(sys.argv[1], index_col = 0)
edited_data = raw_data.copy()
edited_data

edited_data['temp'] = edited_data['CopyFiltered::Text']

edited_data = edited_data.reset_index()

edited_data['temp'] = edited_data['temp'].replace('â€™', '\'', regex=True)
edited_data['temp'] = edited_data['temp'].replace('###', '<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('##', '<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('#', '</i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€”', '--', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€“', '--', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€¦', ' . . . ', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€˜', '\'', regex=True)
edited_data['temp'] = edited_data['temp'].replace(' â€œ', ' \'', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€ ', '\' ', regex=True)
edited_data['temp'] = edited_data['temp'].replace('“', '"', regex=True)
edited_data['temp'] = edited_data['temp'].replace('.\'--<i>', '."--<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('.--<i>', '."--<i>', regex=True)
edited_data['temp'] = edited_data['temp'].replace('Ã¤', 'ä', regex=True)
edited_data['temp'] = edited_data['temp'].replace('Ã©', 'é', regex=True)
edited_data['temp'] = edited_data['temp'].replace('Ã', 'í', regex=True)

edited_data['temp'] = edited_data['temp'].replace('â€œ', '"', regex=True)
edited_data['temp'] = edited_data['temp'].replace('â€', '"', regex=True)


counter = 0
for i in edited_data['temp']:
    text = str(re.findall('"([^"]*)"', str(i)))
    text = text.replace('"', '\'')
    if '[]' not in text:
        text = text[2:-2]
    edited_data.at[counter, '<Text>'] = '"' + text + '"'
    counter = counter + 1

edited_data['<Text>'] = edited_data['<Text>'].replace('[[]]', '', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('  ', ' ', regex=True)
edited_data['<Text>'] = edited_data['<Text>'].replace('""', np.nan, regex=True)

counter = 0
for i in edited_data['temp']:
    temp = re.sub('"([^"]*)"', '', str(i))
    edited_data.at[counter, 'temp'] = str(temp)
    counter = counter + 1

counter = 0
for i in edited_data['temp']:
    source = re.findall('<i>([^>]*)</i>', str(i))
    edited_data.at[counter, '<TextSourceCorporate>'] = str(source) # if 'Author of' esque data in temp, no source
    counter = counter + 1

edited_data['<TextSourceCorporate>'] = edited_data['<TextSourceCorporate>'].replace('[[]]', np.nan, regex=True)
edited_data['<TextSourceCorporate>'] = edited_data['<TextSourceCorporate>'].replace('[[\']', '', regex=True)
edited_data['<TextSourceCorporate>'] = edited_data['<TextSourceCorporate>'].replace('[\']]', '', regex=True)
edited_data['<TextSourceCorporate>'] = edited_data['<TextSourceCorporate>'].replace('[]]', '', regex=True)
edited_data['<TextSourceCorporate>'] = edited_data['<TextSourceCorporate>'].replace('  ', ' ', regex=True)

counter = 0
for i in edited_data['temp']:
    if 'author of' in str(i):
        edited_data.at[counter, '<TextType>'] = 'Endorsement'
        counter = counter + 1
    else:
        temp = re.sub('<i>([^>]*)</i>', '', str(i))
        edited_data.at[counter, 'temp'] = str(temp)
        counter = counter + 1

edited_data['temp'] = edited_data['temp'].replace('--', '', regex=True)
edited_data['temp'] = edited_data['temp'].replace(', in ', '', regex=True)

counter = 0
for i in edited_data['temp']:
    if 'starred review' in str(i) or 'Starred Review' in str(i):
        counter = counter + 1
    else:
        edited_data.at[counter, '<TextAuthor>'] = str(i)
        counter = counter + 1

counter2 = 0
for i in edited_data['<TextAuthor>']:
    if str(i).endswith(', '):
        author = str(i)
        edited_data.at[counter2, '<TextAuthor>'] = author[:-2]
    elif str(i).startswith(' '):
        author = str(i)
        edited_data.at[counter2, '<TextAuthor>'] = author[1:]
    elif len(str(i)) < 5 or str(i) == '':
        edited_data.at[counter2, '<TextAuthor>'] = np.nan
    counter2 = counter2 + 1

counter = 0
for i in edited_data['<TextType>']:
    if edited_data.at[counter, 'CopyFiltered::Text'] is not np.nan:
        edited_data.at[counter, '<TextType>'] = 'Review Quote'
    counter = counter + 1

edited_data = edited_data.drop(columns=['temp'])
edited_data = edited_data.set_index(['Work Key'])
edited_data = edited_data.replace('--', '—', regex=True)

writer = pd.ExcelWriter(str(sys.argv[1])+' edited-data.xlsx', engine='xlsxwriter')
edited_data.to_excel(writer, sheet_name='Sheet1')
writer.save()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python review_text_cleanup_v2_0.py <filename>')
