"""
Created on Sun Oct 24 15:55:12 2021
@author: Wolfgang Mitterbaur


"""

import mycsvfileoperation




    
def main():
    
    """
    main function to call other other functions and objects
    """
    
    
    file_operator = mycsvfileoperation.GuestDatabase("clientdatabase.csv")
    all_clients = file_operator.read_data()
    
    for i in range(0, len(all_clients)):
        
         
        a_client = all_clients[i]
        a_client.first_name
        a_client.first_name
        a_client.email_address
        a_client.phone_number
        a_client.checkin_date
        a_client.checkout_date
        a_client.number_guests
        a_client.number_rooms
        a_client.type_room
        a_client.reservation_number
       
        
    new_client = mycsvfileoperation.Client()
    
    new_client.first_name = "Franz"
    new_client.last_name = "Mitterbaur"
    new_client.email_address = "wolfgang@mitterbaur.at"
    new_client.phone_number = "06645831662"
    new_client.checkin_date = "01.01.2023"
    new_client.checkout_date = "31.12.2023"
    new_client.number_guests = "1"
    new_client.number_rooms = "1"
    new_client.type_room = "double"
    new_client.reservation_number = "123456"
  
    file_operator.add_new_client(new_client)
    
    
    
    # delete reservation
    new_client2 = mycsvfileoperation.Client()
    new_client2.reservation_number = "123456"
   
    done1 = file_operator.delete_reservation(new_client2)
    
    
    
    # add reservation to existing client
    new_client3 = mycsvfileoperation.Client()
    new_client3.first_name = "Franz"
    new_client3.last_name = "Mitterbaur"
    new_client3.email_address = "wolfgang@mitterbaur.at"
    new_client3.phone_number = "06645831662"
    new_client3.checkin_date = "01.01.2023"
    new_client3.checkout_date = "31.12.2023"
    new_client3.number_guests = "1"
    new_client3.number_rooms = "1"
    new_client3.type_room = "double"
    new_client3.reservation_number = "123456"
      
    done2 = file_operator.add_reservation(new_client3)
    
    
    
    file_operator2 = mycsvfileoperation.RoomDatabase("roomdatabase.csv")
    all_rooms = file_operator2.read_data()
    
    for i in range(0, len(all_rooms)):
         
        a_room = all_rooms[i]
        a_room.room_number
        a_room.type_room
        a_room.first_name
        a_room.last_name
        a_room.checkin_date
        a_room.checkout_date
        a_room.number_guests
        a_room.reservation_number

    
    
    # check room availability
    a_room1 = mycsvfileoperation.Room()
    
    #a_room1.room_number
    a_room1.type_room = "one"
    a_room1.first_name = "Wolfgang"
    a_room1.last_name = "Mitterbaur"
    a_room1.checkin_date = "1.1.2020"
    a_room1.checkout_date = "12.12.2040"
    a_room1.number_guests = "1"
    a_room1.reservation_number = "123456"
    
    done3 = file_operator2.check_one_room_avail(a_room1)
    
    
    
    # book a room
    a_room1 = mycsvfileoperation.Room()
    
    a_room1.room_number
    a_room1.type_room = "one"
    a_room1.first_name = "Wolfgang"
    a_room1.last_name = "Mitterbaur"
    a_room1.checkin_date = "1.1.2020"
    a_room1.checkout_date = "12.12.2040"
    a_room1.number_guests = "1"
    a_room1.reservation_number = "123456"
    
    done3 = file_operator2.book_one_room(a_room1)
    
    
    
    # delete room reservation
    a_room2 = mycsvfileoperation.Room()
    a_room2.room_number
    a_room2.type_room
    a_room2.first_name
    a_room2.last_name
    a_room2.checkin_date
    a_room2.checkout_date
    a_room2.number_guests
    a_room2.reservation_number = "123456"
    
    done4 = file_operator2.delete_room_reservation(a_room2)
    
    
    
    
    
    file_operator3 = mycsvfileoperation.RestaurantDatabase("restaurantdatabase.csv")
    all_tables = file_operator3.read_data()
    
    a_table =  mycsvfileoperation.Table()
   
    a_table.first_name = "Wolfgang"            # first name of client
    a_table.last_name = "Mitterbaur"             # last name of client
    a_table.reservation_date = "10.10.2022"      # reservation date
    a_table.reservation_time = "16:00"      # reservation time
        
    table = file_operator3.add_reservation(a_table)
       
    
    done = file_operator3.delete_reservation(a_table)
    
    
    
    
    
    
    
             
# Main program starts here

if __name__ == '__main__':

    main()

