"""
Created on 29.10.2022
@author: Wolfgang Mitterbaur

classes to read and write client data
"""
import pandas as pd
import sys
import traceback

class MyCSVReader(object):
    '''
    base class for SQL with several standard methods
    ''' 
        
    def __init__(self):
        '''
        class constructor
        '''   
        
class Client(object):
    '''
    class for one client data
    '''
    # constructor of the class
    def __init__(self):
        self.first_name = ""            # first name
        self.last_name = ""             # last name
        self.email_address = ""         # email address
        self.phone_number = ""          # phone number
        self.checkin_date = ""          # check-in date
        self.checkout_date = ""         # check-out date
        self.number_guests = ""         # number of guests
        self.number_rooms = ""          # number of rooms
        self.type_room = ""             # type of the room
        self.reservation_number = ""    # reservation number
    
class Room(object):
    '''
    class for one room data
    '''
    # constructor of the class
    def __init__(self):
        self.room_number = ""           # room number
        self.type_room = ""             # room type
        self.first_name = ""            # first name of client
        self.last_name = ""             # last name of client
        self.checkin_date = ""          # check-in date of client
        self.checkout_date = ""         # check-out of client
        self.number_guests = ""         # number of guests
        self.reservation_number = ""    # reservation number     
        
class Table(object):
    '''
    class for one room data
    '''
    # constructor of the class
    def __init__(self):
        self.table_number = ""          # room number
        self.first_name = ""            # first name of client
        self.last_name = ""             # last name of client
        self.reservation_date = ""      # reservation date
        self.reservation_time = ""      # reservation time
        

class GuestDatabase(MyCSVReader):
    '''
    class for the guests database
    ''' 
    # constructor of the class
    def __init__(self, filename):
        super().__init__();
        self.filename = filename   
        
    def read_data(self):
        '''
        public method to read all user data from file
        '''
        all_clients = []
         
        try:
            df_client_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_client_data.loc[:,'first_name'].size):
            
                new_client = Client()
                new_client.first_name = (df_client_data.loc[i,'first_name'])
                new_client.last_name =  (df_client_data.loc[i,'last_name'])
                new_client.email_address = (df_client_data.loc[i,'email_address'])
                new_client.phone_number = (df_client_data.loc[i,'phone_number'])
                new_client.checkin_date = (df_client_data.loc[i,'checkin_date'])
                new_client.checkout_date = (df_client_data.loc[i,'checkout_date'])
                new_client.number_guests = (df_client_data.loc[i,'number_guests'])
                new_client.number_rooms = (df_client_data.loc[i,'number_rooms'])
                new_client.type_room = (df_client_data.loc[i,'type_room'])
                new_client.reservation_number = (df_client_data.loc[i,'reservation_number'])
                
                all_clients.append(new_client)
            
        except:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
            print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                  .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
            
        return all_clients  
    
    def add_new_client(self, new_client):
        '''
        public method to write a user data to file
        new_client: the new client to be added to the client database
        '''
        try:
            df_client_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            no_data = df_client_data.loc[:,'first_name'].size
                 
            df_client_data.loc[no_data,'first_name'] = new_client.first_name
            df_client_data.loc[no_data,'last_name'] = new_client.last_name
            df_client_data.loc[no_data,'email_address'] = new_client.email_address
            df_client_data.loc[no_data,'phone_number'] = new_client.phone_number
            df_client_data.loc[no_data,'checkin_date'] = new_client.checkin_date
            df_client_data.loc[no_data,'checkout_date'] = new_client.checkout_date
            df_client_data.loc[no_data,'number_guests'] = new_client.number_guests
            df_client_data.loc[no_data,'number_rooms'] = new_client.number_rooms
            df_client_data.loc[no_data,'type_room'] = new_client.type_room
            df_client_data.loc[no_data,'reservation_number'] = new_client.reservation_number
            
            clients = pd.DataFrame(df_client_data, columns=['first_name', 'last_name', 'email_address', 
                                                            'phone_number', 'checkin_date', 'checkout_date', 
                                                            'number_guests', 'number_rooms', 'type_room', 'reservation_number'  ])
            clients.to_csv(self.filename)
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
       
    def delete_reservation(self, a_client):
        '''
        public method to delete user data from file
        a_client: the data of the client to be deleted from the client database
        '''
        retval = False
        
        try:
            df_client_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_client_data.loc[:,'first_name'].size):
            
                if (int(a_client.reservation_number) == int(df_client_data.loc[i,'reservation_number'])):
                    
                    df_client_data.loc[i,'checkin_date'] = "none"
                    df_client_data.loc[i,'checkout_date'] = "none"
                    df_client_data.loc[i,'number_guests'] = "none"
                    df_client_data.loc[i,'number_rooms'] = "none"
                    df_client_data.loc[i,'type_room'] = "none"
                    df_client_data.loc[i,'reservation_number'] = "0"
                
                    clients = pd.DataFrame(df_client_data, columns=['first_name', 'last_name', 'email_address', 
                                                                    'phone_number', 'checkin_date', 'checkout_date', 
                                                                    'number_guests', 'number_rooms', 'type_room', 'reservation_number'  ])
                    clients.to_csv(self.filename)
                    
                    retval =  True
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return retval
                
    def add_reservation(self, a_client):
        '''
        public method to add a reservation
        a_client: the data of a client with reservation data
        '''
        retval = False
        
        
        try:
            df_client_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_client_data.loc[:,'first_name'].size):
                
            
                if (a_client.first_name == df_client_data.loc[i,'first_name'] and 
                    a_client.last_name == df_client_data.loc[i,'last_name'] and
                    a_client.email_address == df_client_data.loc[i,'email_address']):
                    
                    df_client_data.loc[i,'checkin_date'] = a_client.checkin_date
                    df_client_data.loc[i,'checkout_date'] = a_client.checkout_date 
                    df_client_data.loc[i,'number_guests'] = a_client.number_guests
                    df_client_data.loc[i,'number_rooms'] = a_client.number_rooms
                    df_client_data.loc[i,'type_room'] = a_client.type_room
                    df_client_data.loc[i,'reservation_number'] = a_client.reservation_number
            
                    clients = pd.DataFrame(df_client_data, columns=['first_name', 'last_name', 'email_address', 
                                                            'phone_number', 'checkin_date', 'checkout_date', 
                                                            'number_guests','number_rooms', 'type_room', 'reservation_number'  ])
                    
                    clients.to_csv(self.filename)
                    
                    retval = True
           
                    break
            
            # could´t find the guest in the database: create new guest entry    
            if not retval:
                no_data = df_client_data.loc[:,'first_name'].size
                 
                df_client_data.loc[no_data,'first_name'] = a_client.first_name
                df_client_data.loc[no_data,'last_name'] = a_client.last_name
                df_client_data.loc[no_data,'email_address'] = a_client.email_address
                df_client_data.loc[no_data,'phone_number'] = a_client.phone_number
                df_client_data.loc[no_data,'checkin_date'] = a_client.checkin_date
                df_client_data.loc[no_data,'checkout_date'] = a_client.checkout_date
                df_client_data.loc[no_data,'number_guests'] = a_client.number_guests
                df_client_data.loc[no_data,'number_rooms'] = a_client.number_rooms
                df_client_data.loc[no_data,'type_room'] = a_client.type_room
                df_client_data.loc[no_data,'reservation_number'] = a_client.reservation_number
                
                clients = pd.DataFrame(df_client_data, columns=['first_name', 'last_name', 'email_address', 
                                                                'phone_number', 'checkin_date', 'checkout_date', 
                                                                'number_guests', 'number_rooms', 'type_room', 'reservation_number'  ])
                clients.to_csv(self.filename)
                
                retval = True
             
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return retval
   

class RoomDatabase(MyCSVReader):
    '''
    class for the rooms database
    ''' 
    # constructor of the class
    def __init__(self, filename):
        super().__init__();
        self.filename = filename   
        
    def read_data(self):
        '''
        public method to read all user data from file
        '''
        all_rooms = []
         
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                new_room = Room()
                new_room.room_number = (df_room_data.loc[i,'room_number'])
                new_room.type_room = (df_room_data.loc[i,'type_room'])
                new_room.first_name = (df_room_data.loc[i,'first_name'])
                new_room.last_name =  (df_room_data.loc[i,'last_name'])
                new_room.checkin_date = (df_room_data.loc[i,'checkin_date'])
                new_room.checkout_date = (df_room_data.loc[i,'checkout_date'])
                new_room.number_guests = (df_room_data.loc[i,'number_guests'])
                new_room.reservation_number = (df_room_data.loc[i,'reservation_number'])
                
                all_rooms.append(new_room)
            
        except:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
            print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                  .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return all_rooms  
    
    
    def read_all_avail_rooms(self):
        '''
        public method to read available rooms
        '''
        no_room_one = 0
        no_room_two = 0
        no_room_double = 0
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                                        
                    
                    if df_room_data.loc[i,'type_room'] == "one":
                                            
                         no_room_one = no_room_one + 1
                         
                    elif df_room_data.loc[i,'type_room'] == "two":
                    
                        no_room_two = no_room_two + 1    
                    
                    elif df_room_data.loc[i,'type_room'] == "double":
                    
                        no_room_double = no_room_double + 1    
  
            
        except:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
            print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                  .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return no_room_one, no_room_two, no_room_double
       
    def delete_room_reservation(self, a_room):
        '''
        public method to delete user data from file
        a_room: the room to delete an existing reservation
        '''
        retval = False
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (int(a_room.reservation_number) == int(df_room_data.loc[i,'reservation_number'])):
                    
                    df_room_data.loc[i,'first_name'] = "none"
                    df_room_data.loc[i,'last_name'] = "none"
                    df_room_data.loc[i,'checkin_date'] = "none"
                    df_room_data.loc[i,'checkout_date'] = "none"
                    df_room_data.loc[i,'number_guests'] = "0"
                    df_room_data.loc[i,'reservation_number'] = "0"
                
                    rooms = pd.DataFrame(df_room_data, columns=['room_number', 'type_room', 'first_name', 
                                                                    'last_name', 'checkin_date', 'checkout_date', 
                                                                    'number_guests', 'reservation_number'])
                    rooms.to_csv(self.filename)
                    
                    retval =  True
                    
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return retval
    
    def check_one_room_avail(self, a_room):
        '''
        public method to delete user data from file
        a_room: data to search a available room
        '''
        room_number = 0
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                                        
                    room_number = int( df_room_data.loc[i,'room_number'])
                    
                    break                   
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return room_number
    
    def check_two_room_avail(self, a_room):
        '''
        public method to delete user data from file
        a_room: data to search the first available room        
        '''
        room_number1 = 0
        room_number2 = 0
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (room_number1 == 0 and
                    a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                                        
                    room_number1 = int( df_room_data.loc[i,'room_number'])
                    
                elif (room_number2 == 0 and
                    a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                                        
                    room_number2 = int( df_room_data.loc[i,'room_number'])   
                    
                    break                   
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return room_number1, room_number2
    
    def book_one_room(self, a_room):
        '''
        public method to delete user data from file
        a_room: dato of a room for booking
        '''
        room_number = 0
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                    
                    df_room_data.loc[i,'first_name'] = a_room.first_name
                    df_room_data.loc[i,'last_name'] = a_room.last_name
                    df_room_data.loc[i,'checkin_date'] = a_room.checkin_date
                    df_room_data.loc[i,'checkout_date'] = a_room.checkout_date
                    df_room_data.loc[i,'number_guests'] = a_room.number_guests
                    df_room_data.loc[i,'reservation_number'] = a_room.reservation_number
                                    
                    rooms = pd.DataFrame(df_room_data, columns=['room_number', 'type_room', 'first_name', 
                                                                    'last_name', 'checkin_date', 'checkout_date', 
                                                                    'number_guests', 'reservation_number'])
                    rooms.to_csv(self.filename)
                                        
                    room_number = int( df_room_data.loc[i,'room_number'])
                    
                    break                   
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return room_number
    
    
    def book_two_rooms(self, a_room):
        '''
        public method to delete user data from file
        a_room: dato of a room for booking
        '''
        room_number1 = 0
        room_number2 = 0
        
        try:
            df_room_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_room_data.loc[:,'room_number'].size):
            
                if (room_number1 == 0 and 
                    a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                    
                    df_room_data.loc[i,'first_name'] = a_room.first_name
                    df_room_data.loc[i,'last_name'] = a_room.last_name
                    df_room_data.loc[i,'checkin_date'] = a_room.checkin_date
                    df_room_data.loc[i,'checkout_date'] = a_room.checkout_date
                    df_room_data.loc[i,'number_guests'] = a_room.number_guests
                    df_room_data.loc[i,'reservation_number'] = a_room.reservation_number
                                    
                    rooms = pd.DataFrame(df_room_data, columns=['room_number', 'type_room', 'first_name', 
                                                                    'last_name', 'checkin_date', 'checkout_date', 
                                                                    'number_guests', 'reservation_number'])
                    rooms.to_csv(self.filename)
                                        
                    room_number1 = int( df_room_data.loc[i,'room_number'])
               
                elif (room_number2 == 0 and
                    a_room.type_room == (df_room_data.loc[i,'type_room']) and                        
                    df_room_data.loc[i,'checkin_date'] == "none" and 
                    df_room_data.loc[i,'checkout_date'] == "none"): 
                    
                    df_room_data.loc[i,'first_name'] = a_room.first_name
                    df_room_data.loc[i,'last_name'] = a_room.last_name
                    df_room_data.loc[i,'checkin_date'] = a_room.checkin_date
                    df_room_data.loc[i,'checkout_date'] = a_room.checkout_date
                    df_room_data.loc[i,'number_guests'] = a_room.number_guests
                    df_room_data.loc[i,'reservation_number'] = a_room.reservation_number
                                    
                    rooms = pd.DataFrame(df_room_data, columns=['room_number', 'type_room', 'first_name', 
                                                                    'last_name', 'checkin_date', 'checkout_date', 
                                                                    'number_guests', 'reservation_number'])
                    rooms.to_csv(self.filename)
                                        
                    room_number2 = int( df_room_data.loc[i,'room_number'])
                    
                    break                   
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return room_number1, room_number2


class RestaurantDatabase(MyCSVReader):
    '''
    class of guest database
    ''' 
    # constructor of the class
    def __init__(self, filename):
        super().__init__();
        self.filename = filename   
        
    def read_data(self):
        '''
        public method to read all tables data from file
        '''
        all_tables = []
         
        try:
            df_table_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_table_data.loc[:,'table_number'].size):
            
                new_tablet = Table()
                new_tablet.table_number = (df_table_data.loc[i,'table_number'])
                new_tablet.first_name = (df_table_data.loc[i,'first_name'])
                new_tablet.last_name =  (df_table_data.loc[i,'last_name'])
                new_tablet.reservation_date = (df_table_data.loc[i,'reservation_date'])
                new_tablet.reservation_time = (df_table_data.loc[i,'reservatoin_time'])
                                
                all_tables.append(new_tablet)
            
        except:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
            print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                  .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
            
        return all_tables  
    
    
    def add_reservation(self, a_table):
        '''
        public method to delete user data from file
        a_table: the data of a client with reservation data
        '''
        
        table_no = 0
        
        try:
            df_table_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_table_data.loc[:,'table_number'].size):
            
            
                if (df_table_data.loc[i,'first_name']== "none" and
                    df_table_data.loc[i,'last_name'] == "none"):
                    
                    df_table_data.loc[i,'first_name'] = a_table.first_name
                    df_table_data.loc[i,'last_name'] = a_table.last_name
                    df_table_data.loc[i,'reservation_date'] = a_table.reservation_date
                    df_table_data.loc[i,'reservatoin_time'] = a_table.reservation_time
                                        
                    table_no = df_table_data.loc[i,'table_number'] 
            
                    tables = pd.DataFrame(df_table_data, columns=['table_number', 'first_name', 'last_name',
                                                            'reservation_date', 'reservatoin_time', 'number_guests' ])
                    
                    tables.to_csv(self.filename)
           
                    break
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
                
        return table_no
    
    
    def delete_reservation(self, a_table):
        '''
        public method to delete table reservation
        a_table: the data of the client to be deleted from the client database
        '''
        retval = False
        
        try:
            df_table_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            for i in range(0, df_table_data.loc[:,'table_number'].size):
            
                if ((a_table.first_name == df_table_data.loc[i,'first_name']) and
                    (a_table.last_name == df_table_data.loc[i,'last_name'])
                    
                ):
                    
                    df_table_data.loc[i,'first_name'] = "none"
                    df_table_data.loc[i,'last_name'] = "none"
                    df_table_data.loc[i,'reservation_date'] = "none"
                    df_table_data.loc[i,'reservatoin_time'] = "none"
                    df_table_data.loc[i,'number_guests'] = "0"
                
                    tables = pd.DataFrame(df_table_data, columns=['table_number', 'first_name', 'last_name',
                                                            'reservation_date', 'reservatoin_time', 'number_guests' ])
                    
                    tables.to_csv(self.filename)
                    
                    retval =  True
              
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
        
        return retval
                
class MessageDatabase(MyCSVReader):
    '''
    class for client messages
    ''' 
    # constructor of the class
    def __init__(self, filename):
        super().__init__();
        self.filename = filename   
        
    
    def add_message(self, a_message):
        '''
        public method to add a message
        a_message: the message to be added
        '''
        
        try:
            df_message_data = pd.read_csv(filepath_or_buffer = self.filename)
            
            no_data = df_message_data.loc[:,'message'].size
                 
            df_message_data.loc[no_data,'message'] = a_message
            
            messages = pd.DataFrame(df_message_data, columns=['message'])
            messages.to_csv(self.filename)
            
        except:
           exception_type, exception_value, exception_traceback = sys.exc_info()
           print("Exception Type: {}\nExcpetion Value: {}"
                  .format(exception_type, exception_value))
           file_name, line_number, procedure_name, line_code = traceback.extract_tb(
                exception_traceback)[-1]
           print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}"
                   .format(file_name, line_number, procedure_name, line_code))
        finally:
            pass
   