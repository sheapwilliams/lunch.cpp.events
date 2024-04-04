# Lunch Order System
A system to manage for attendee's to order lunches during the week to be handed out at the APC for C++ Now.

It would be nice to make this more generic in the future.  Its being generated initially for its primary use case of pre-ordering a weeks worth of lunches.  Its hacky -- I know :)  Its my first python app, be gentle.

## Requirements
- List of days which need lunch orders - done
- Each day a drop down of the menu items available. - done
    - None option if no lunch is wanted. - done
- Order button to complete order. - done
    - When order button clicked - total up $price per day by total days with items selected. - done
        - Ignore days which None is set. - done
- Confirmation Page - confirming order total cost and items per day (email as well). - done
    - Redirect to payment provider. - done
        - Account for fees. - done
- Order
    - Add order - done
        - user adds 2 days - done 
        - totalPaid set to 60 - done
    - Edit order - remove
        - Tries to remove one item
            - note - must email for refunds.
        - Tries to add item(s)
            - get new total
            - charge differences
                - on success
                    - update total paid
                - on failure - backout
    - Past date at 9am MST - disable.

    

## Design Notes
Header says it...
- Single app base json config file with cost and menu for days.
- Store orders in a sqlite db?
- Week long order set per day of the week.
    - Monday - Friday
    - Must pick one per day or have a line item for none.
    - Lock out orders so they cannot be updated past a certain time? 
- Multiple Restaurants per day.
    - May not need to worry about the restaurant in the order as much as the item being ordered.
    - Will use two restaurants per day due to order volume to help balance the load.
- Single form with a drop down to select one item to order each day.
- Cost per day is flat.

- Menu items have a type of
    - B - Beef
    - C - Chicken
    - F - Fish (never had before)
    - P - Pork
    - V - Vegetarian

Todo...
- Allow changes after order complete
- Don't over charge on changes
- What about refunds if they change a day to none?
- Perhaps use a FieldList instead? https://prettyprinted.com/tutorials/how-to-use-fieldlist-in-flask-wtf/

## Database

### Users
Track users and their login credentials.
| Field         |  Type         |
|---------------|---------------|
| id            | int           |
| username      | varchar(64)   |
| email         | varchar(256)  |
| password_hash | varchar(256)  |

### Orders Table
This table will maintain for each user their total weekly order set.  
| Field         |  Type         |
|---------------|---------------|
| id            | int           |
| status        | varchar(256)  |
| totalPaid     | int           |
| timestamp     | varchar(64)   |
| monday        | varchar(256)  |
| tuesday       | varchar(256)  |
| wednesday     | varchar(256)  |
| thursday      | varchar(256)  |
| friday        | varchar(256)  |
| user_id       | int           |

### Sessions Table - track order state/session.
This table will have one line per session - when completed data transfered to order on success and record will be cleaned after 24 hours.
| Field         |  Type         |
|---------------|---------------|
| id            | int           |
| user_id       | int           |
| ip            | varchar(64)   |
| timestamp     | varchar(64)   |
| monday        | varchar(256)  |
| tuesday       | varchar(256)  |
| wednesday     | varchar(256)  |
| thursday      | varchar(256)  |
| friday        | varchar(256)  |


### Notes
https://picocss.com/docs


### Email
#### Incoming Server Settings (IMAP)
mail.privateemail.com
993
support@cpp.events
SSL/TLS
Your account password

#### Outgoing Server Settings
These are in the .env file...
MAIL_SERVER=mail.privateemail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=support@cpp.events
MAIL_PASSWORD=<replace with pw>

