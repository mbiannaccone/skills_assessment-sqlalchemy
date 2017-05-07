"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

""" A Flask_SQLAlchemy object that holds the information to execute a SQL
    query in the database. """


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

""" An association table connects two tables that have a many-to-many
    relationship. It doesn't hold any real data that we wish to view, its sole
    purpose is to connect the two tables and create a relationship between them.
    It has a one-to-many relationship with each of the two tables."""


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.get('ram')

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter(Model.name == 'Corvette', Model.brand_id == 'che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued != None) | (Brand.founded < 1950)).all()

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id != "for").all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    # the below would run multiple queries in the db, everytime we ask for data
    # models = Model.query.filter(Model.year == year).all()

    models = db.session.query(Model.name,
                              Brand.name,
                              Brand.headquarters).join(Brand).filter(
                                                    Model.year == year).all()

    for model in models:
        print "MODEL #%s" % (models.index(model)+1)
        print "\tModel: %s\n\tBrand: %s\n\tHeadquarters: %s" % (model[0],
                                                                model[1],
                                                                model[2])


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    # the below would run multiple queries in the db ,everytime we ask for data
    # brands_summary = Brand.query.all()

    # the below would only have to run one query one time!
    brands_summary = db.session.query(Brand.name,
                                      Model.name,
                                      Model.year).join(Model).all()

    # and now we parse through the results, put into a dictionary with
    # {brand: [model1, model2, etc..]} so we can print nicely!
    brands_summary_dict = {}
    for brand in brands_summary:
        if brand[0] not in brands_summary_dict:
            brands_summary_dict[brand[0]] = []
        brands_summary_dict[brand[0]].append((brand[1], brand[2]))

    for brand, models in brands_summary_dict.items():
        print "BRAND: %s" % (brand)
        for model, year in models:
            print "\tModel: %s, %s" % (model, year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    brands = Brand.query.filter(Brand.name.like("%"+mystr+"%")).all()

    return brands


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models = Model.query.filter(Model.year >= start_year,
                                Model.year <= end_year).all()

    return models
