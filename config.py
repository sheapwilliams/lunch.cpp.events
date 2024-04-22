import os
from dotenv import load_dotenv
import json
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN') or 'http://127.0.0.1:5001'
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
            "date": "4/29/24",
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
                    "name": "Carne Asada Burrito",
                    "type": "B",
                    "desc": "Grilled Flank Steak, Tomatillo Salsa, Pico, French Fries, Shredded Lettuce and Guacamole"
                },
                {
                    "name": "Riviera",
                    "type": "V",
                    "desc": "Tomato, mozzarella, basil, organic spinach & vinaigrette dressing"
                },
                {
                    "name": "Preston",
                    "type": "P",
                    "desc": "Roast pork loin, sauteed onions, provolone & gravy"
                }
            ]
        },
        {
            "date": "4/30/24",
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
                },
                {
                    "name": "Pepperoni",
                    "type": "B",
                    "desc": "Pepperoni with roasted tomato sauce & mozzarella",
                },
                {
                    "name": "Margherita",
                    "type": "V",
                    "desc": "Roasted tomato sauce, fresh mozzarella, sliced tomatoes & sweet basil"
                }
            ]
        },
        {
            "date": "5/1/24",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Vegan Laksa Pak",
                    "type": "V",
                    "desc": "Steamed noodles in vegan yellow curry, mixed vegetables and fried onions."
                },
                {
                    "name": "Orange Chicken Bowl",
                    "type": "C",
                    "desc": "Lightly battered chicken nuggest prepared in homemade sauce featuring fresh oranges with house wild rice."
                },
                {
                    "name": "Beef Boat Bowl",
                    "type": "B",
                    "desc": "Traditional spicy thai beef noodle with bean sprouts and thai basil."
                },
                {
                    "name": "Pad Thai Pork ",
                    "type": "P",
                    "desc": "Most popular Thai noodle dish featuring stir-fried thin rice noodle with egg, bean sprouts, scallions and crunchy peanuts."
                },                
                {
                    "name": "Riviera",
                    "type": "V",
                    "desc": "Tomato, mozzarella, basil, organic spinach & vinaigrette dressing"
                },
                {
                    "name": "Preston",
                    "type": "P",
                    "desc": "Roast pork loin, sauteed onions, provolone & gravy"
                }
            ]
        },
        {
            "date": "5/2/24",
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
                },                
                {
                    "name": "Pepperoni",
                    "type": "B",
                    "desc": "Pepperoni with roasted tomato sauce & mozzarella",
                },
                {
                    "name": "Margherita",
                    "type": "V",
                    "desc": "Roasted tomato sauce, fresh mozzarella, sliced tomatoes & sweet basil"
                }
            ]
        },
        {
            "date": "5/3/24",
            "options": [
                {
                    "name": "None",
                    "type": "N",
                    "desc": "No Lunch Selected"
                },
                {
                    "name": "Basil Pesto",
                    "type": "V",
                    "desc": "Pesto, Roma Tomatoes, Olives, Goat Cheese & Pine Nuts."
                },
                {
                    "name": "Margherita",
                    "type": "V",
                    "desc": "Roasted Tomato Sauce, Fresh Mozzarella, Sliced Tomatoes & Sweet Basil."
                },
                {
                    "name": "Linguini with Chicken & Broccoli",
                    "type": "C",
                    "desc": "White wine garlic broth, chili flakes, capers."
                },
                {
                    "name": "The Italian Job",
                    "type": "P",
                    "desc": "Mortadella, nduja sausage, caciocavallo & mozzarella cheese, basil."
                },
                {
                    "name": "Mezz Burger",
                    "type": "B",
                    "desc": "Char-grilled beef burger with cheddar on fresh bun with chipotle aioli, lettuce, tomato & onion, served with french frizz."
                },
            ]
        }
    ]

