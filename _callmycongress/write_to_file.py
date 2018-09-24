def python_to_json(pyData, outFilename):
    with open(outFilename, 'w', encoding='utf-8') as f:
        f.write(pyData)    
