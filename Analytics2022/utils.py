import pandas as pd
def encode(df, encoding_dictionary):
    if isinstance(df, pd.DataFrame):
        df = df.copy()
        for x in df:
            uns = df[x].dropna().unique()
            
            uns2 = '@'.join(sorted([str(x) for x in uns]))
            if uns2 in encoding_dictionary:
                tmp_encode = encoding_dictionary[uns2]
            else:
                continue
                if len(uns) > 10:
                    continue
                tmp_encode = {un : i for i, un in enumerate(uns) if un} 
            df[x] = df[x].apply(encode, args = [tmp_encode])
        return df
    if df in encoding_dictionary:
        df = encoding_dictionary[df]
    return df

def validEncodingCheck(encoding):
    encoding_split = [encoded.strip() for encoded in encoding.split(',')]
    if all(encoded.isnumeric() or encoded == 'nan' for encoded in encoding_split):
        return True
    is_valid = encoding.strip() in ['drop', 'none']
    if not is_valid:
        print("WARNING: Encoding -- {encoding} -- is not a valid encoding.")
        print("\tEncodings must be one of: 'drop', 'none', or numeric string ('nan' included)")
    return is_valid

def getEncodings(df, encodings = None):
    droppables = []
    if not encodings:
        encodings = {}
    for col in df:
        uns = df.loc[(~df[col].isna()), col].unique()
        if len(uns) <= 2:
            continue
        uns2 = '@'.join(sorted([str(x) for x in uns]))
        if uns2 in encodings:
            continue
        print("Create a comma seperate encoding (type 'none' to not encode or 'drop' top drop the column) for the following:")
        print(uns)
        encoding = ''
        isValidEncoding = False
        while not isValidEncoding:
            encoding = input()
            encoding = encoding.strip().replace('"', '').replace("'", '')
            isValidEncoding = validEncodingCheck(encoding)
        if encoding == 'drop':
            droppables.append(col)
            continue
        if encoding == 'none':
            continue
        encoding = [float(x.strip()) if x.strip() != 'nan' else np.nan for x in encoding.split(',')]
        encoding = {y : x for x, y in zip(encoding, uns)}
        encodings[uns2] = encoding
    return encodings, droppables

def getTypes(df):
    types_ref = {'d' : 'description', 'n' : 'number', 'a' : 'nan/drop', 'q' : 'quantitative', 'l' : 'qualitative'}
    types = []
    columns = {}
    for x in df:
        un = df[x].unique()
        print(x)
        print("number of uniques:", len(un))
        print("first 5 uniques", ', '.join([str(x) for x in un[:5]]))
        time.sleep(0.05)
        if len(un) <= 3:
            if len(un) == 1:
                columns[x] = types_ref['a']
                continue
            columns[x] = types_ref['q']
            continue
        a = 'test'
        while a not in types_ref:
            a = input()
        columns[x] = types_ref[a]
        print()
    return columns

def resize(text, length_limit = 50):
    text = text.split(' ')
    out = ['']
    for x in text:
        if (len(x) + len(out[-1]) + 1) >= length_limit:
            out.append('')
        if out[-1]:
            out[-1] += ' ' + x
        else:
            out[-1] = x
    out = '\n'.join(out)
    return out

def saveExcelSheetsToCsv(file, Savelocation):
    xls = pd.ExcelFile(file)
    file2 = file.split('.')[0]
    file2 = file2.split('\\')[1:]
    file2 = '.\\raw_csv\\' + '_'.join(file2)
    for sheetName in xls.sheet_names:
        sheet = pd.read_excel(file, sheetName)
        save_path = file2 + '_'  + sheetName + '.csv'
        save_path = save_path.replace(' ', '_')
        sheet.to_csv(save_path, sep = sep, index = False)