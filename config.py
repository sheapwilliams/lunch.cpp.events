import os
from dotenv import load_dotenv
import json
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN') or 'http://192.168.0.20:5001'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SavingAspenLunchesIn2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'lunch.db')
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'mail.privateemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'support@cpp.events'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    ADMINS = ['support@cpp.events']

    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or ''
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY') or ''
    
    # -------- app lunch config -------
    ORDER_PRICE = 30
    ORDER_OPTIONS = [
        {
            "date": "4/29/24 - Monday",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Kale & Quinoa Bowl",
                    "type": "V",
                    "desc": "Chopped Kale, Roasted Peppers, Toasted Sunflower and Hemp Seeds, Tossed in sweet garlic balsamic vinaigrette"
                },
                {
                    "name": "Grilled Chicken Tacos",
                    "type": "C",
                    "desc": "Grilled Chicken with Tomatillo Salsa, Pico and Fresh Cilantro"
                },
                {
                    "name": "Philly Cheese Steak",
                    "type": "B",
                    "desc": "Classic Hoagie Bun, Shaved Sirloin Steak, Onions, Melted American Cheese and Spicy Mayo"
                },
                {
                    "name": "Carne Asada Burrito",
                    "type": "B",
                    "desc": "Grilled Flank Steak, Tomatillo Salsa, Pico, French Fries, Shredded Lettuce and Guacamole"
                }
            ]
        },
        {
            "date": "4/30/24 - Tuesday",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Riviera",
                    "type": "V",
                    "desc": "Tomato, mozzarella, basil, organic spinach & vinaigrette dressing"
                },
                {
                    "name": "Gigi",
                    "type": "C",
                    "desc": "Sauteed apple & roasted walnut chicken salad, organic romaine and tomato"
                },
                {
                    "name": "Troy",
                    "type": "B",
                    "desc": "Roast beef, provolone, sauteed onions, organic romaine, tomato and horseradish spread."
                },
                {
                    "name": "Preston",
                    "type": "P",
                    "desc": "Roast pork loin, sauteed onions, provolone & gravy"
                }
            ]
        },
        {
            "date": "5/1/24 - Wednesday",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Black Bean Burger",
                    "type": "V",
                    "desc": "Zesty blend of black beans, brown rice, onions, peppers, corn, lettuce tomato & pickle, Fries and Coleslaw"
                },
                {
                    "name": "Grilled Chicken Breast Sandwich",
                    "type": "C",
                    "desc": "8oz Chicken Breast topped with BBQ Sauce, Fries and Coleslaw"
                },
                {
                    "name": "Smoked Beef Brisket",
                    "type": "B",
                    "desc": "Beef brisket, fries, cole slaw and garlic toast."
                },
                {
                    "name": "Smoked pulled Pork ",
                    "type": "P",
                    "desc": "Pulled pork, fries, cole slaw and garlic toast."
                }
            ]
        },
        {
            "date": "5/2/24 - Thursday",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Black Bean Burger",
                    "type": "V",
                    "desc": "Zesty blend of black beans, brown rice, onions, peppers, corn, lettuce tomato & pickle, Fries and Coleslaw"
                },
                {
                    "name": "Grilled Chicken Breast Sandwich",
                    "type": "C",
                    "desc": "8oz Chicken Breast topped with BBQ Sauce, Fries and Coleslaw"
                },
                {
                    "name": "Smoked Beef Brisket",
                    "type": "B",
                    "desc": "Beef brisket, fries, cole slaw and garlic toast."
                },
                {
                    "name": "Smoked pulled Pork ",
                    "type": "P",
                    "desc": "Pulled pork, fries, cole slaw and garlic toast."
                }
            ]
        },
        {
            "date": "5/3/24 - Friday",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Black Bean Burger",
                    "type": "V",
                    "desc": "Zesty blend of black beans, brown rice, onions, peppers, corn, lettuce tomato & pickle, Fries and Coleslaw"
                },
                {
                    "name": "Grilled Chicken Breast Sandwich",
                    "type": "C",
                    "desc": "8oz Chicken Breast topped with BBQ Sauce, Fries and Coleslaw"
                },
                {
                    "name": "Smoked Beef Brisket",
                    "type": "B",
                    "desc": "Beef brisket, fries, cole slaw and garlic toast."
                },
                {
                    "name": "Smoked pulled Pork ",
                    "type": "P",
                    "desc": "Pulled pork, fries, cole slaw and garlic toast."
                }
            ]
        }
    ]

