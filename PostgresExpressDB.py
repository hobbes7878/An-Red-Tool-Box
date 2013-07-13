class PostgresExpress:

    def __init__(self,database,user,password):
        import psycopg2
        connection="dbname="+database+" user="+user+" password="+password
        self.conn=psycopg2.connect(connection)
        self.cur=self.conn.cursor()




    def DictWriter(self, table, diction):
        SQL= 'SELECT * FROM \"'+table+'\";'
        
        #Check if table exists
        self.cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)",(table,))
        if self.cur.fetchone()[0] == False:
            response = raw_input("Table "+table+" does not exist in the database. Create this table? (Y/N): ")
            if response.upper() == "Y":
                SQL_Create = "CREATE TABLE " + table + " ();"
                self.cur.execute(SQL_Create)
            else:
                return


        self.cur.execute(SQL)
        col_names = [desc[0] for desc in self.cur.description]
        #Get column names from dict
        dict_keys=diction.keys()
        ### Create any new columns in database ###
        for dk in dict_keys:
            if dk in col_names:
                pass
            else:
                if len(dk.strip())>0:
                    SQL='ALTER TABLE \"'+table+'\" ADD \"'+str(dk)+'\" varchar;'
                    self.cur.execute(SQL)
                    self.conn.commit()
                else:
                    pass

        ### Write dict to database ###
        SQL='INSERT INTO \"'+table+'\" (' + str(diction.keys()).strip("[").strip("]").replace("'","\"") + ') VALUES ( ' +str(diction.values()).strip("[").strip("]") + ');' 
        self.cur.execute(SQL)
        self.conn.commit()
