def DictWriterDB(table , diction):
    #Get column names from database
    SQL= 'SELECT * FROM \"'+table+'\";'
    cur.execute(SQL)
    col_names = [desc[0] for desc in cur.description]
    #Get column names from dict
    dict_keys=diction.keys()
    ### Create any new columns in database ###
    for dk in dict_keys:
        if dk in col_names:
            pass
        else:
            if len(dk.strip())>0:
                SQL='ALTER TABLE \"'+table+'\" ADD \"'+str(dk)+'\" varchar;'
                cur.execute(SQL)
                conn.commit()
            else:
                pass

    ### Write dict to database ###
    SQL='INSERT INTO \"'+table+'\" (' + str(diction.keys()).strip("[").strip("]").replace("'","\"") + ') VALUES ( ' +str(diction.values()).strip("[").strip("]") + ');' 
    cur.execute(SQL)
    conn.commit()