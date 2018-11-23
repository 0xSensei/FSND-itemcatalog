from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Abdulaziz Guru", email="abdulaziz@juaythin.com",
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# catalog for Soccer
Catalog1 = Catalog(name="Soccer")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="shinguards",
    description="Equipped with hook-and-loop straps for a supportive fit that helps limit distractions during match play, the Nike Adult Mercurial Hard Shell Soccer Shin Guards maintain an anatomical, low-profile feel without compromising protection when challenging the opposition on the pitch.",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

CatalogItem2 = CatalogItem(user_id=1, name="jersey",
    description="Let your little showcase their unwavering fandom for their favorite soccer player with the Nike FC Barcelona Lionel Messi #10 Breathe Stadium Home Replica Jersey.",
    catalog=Catalog1)

session.add(CatalogItem2)
session.commit()

# catalog for Basketball
Catalog2 = Catalog(name="BasketBall")

session.add(Catalog2)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="Ball",
    description="you will feel like lebron james with this one :)",
    catalog=Catalog2)

session.add(CatalogItem1)
session.commit()

CatalogItem2 = CatalogItem(user_id=1, name="Shoes",
    description="Have you ever wondered how kobe bryant made his legacy," " you should check his thunder jammer, https://www.youtube.com/watch?v=zViZhFbMaL8",
    catalog=Catalog2)
session.add(CatalogItem2)
session.commit()

# catalog for Snowboarding
Catalog1 = Catalog(name="SnowBoarding")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="snowboard",
    description="the snowboard will make you feel you\'re in switzerland",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

CatalogItem2 = CatalogItem(user_id=1, name="googles",
    description="a googles that will protect you when you\'re in need.",
    catalog=Catalog1)

session.add(CatalogItem2)
session.commit()

# catalog for Baseball
Catalog1 = Catalog(name="Baseball")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="Bat",
    description="you will be hittin homeruns left and right whenever you wanted.",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

# catallog for Frisbee
Catalog1 = Catalog(name="Frisbee")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="Frisbee",
    description="your kid will thank you for making him skip overwatch season.",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

# catalog for Rock Climbing
Catalog1 = Catalog(name="Rock Climbing")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="chock ",
    description="metal wedge threaded on a wire and is used for protection by wedging it into a crack in the rock..",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

# catalog for FoseBall
Catalog1 = Catalog(name="Fooseball")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="ITSF B-Ball",
    description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

# catalog for Skating
Catalog1 = Catalog(name="Skating")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="Skating shoes",
    description="he tricot lined figure skate is comfortable, fits well and has an easy care durable PVC boot.",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

Catalog1 = Catalog(name="Hockey")

session.add(Catalog1)
session.commit()

CatalogItem1 = CatalogItem(user_id=1, name="Hockey Stick",
    description="DuraFlex Resin and specific weight reductions to provide the best Supreme stick to date.",
    catalog=Catalog1)

session.add(CatalogItem1)
session.commit()

print "added menu items!"
