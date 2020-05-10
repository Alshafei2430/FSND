#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json, datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable = False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),
      nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),
      nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues') # -----done
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.with_entities(Venue.city).all()
  cities = []
  data1= []
  i = 0
  for city in data:
    cities.append(city[i])
  cities_set = set(cities)
  for city in cities_set:
    data = Venue.query.filter(Venue.city == city).all()
    city_info = {"city": city, "state": data[i].state}
    venues = []
    for venue in data:
      venues.append({
        "id":venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id).count()
      })
    city_info['venues'] = venues
    data1.append(city_info)
  return render_template('pages/venues.html', areas=data1);

@app.route('/venues/search', methods=['POST']) #-----done
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(
    '%{}%'.format(search_term))).all()
  data = []
  for venue in venues:
    data.append({
      'id': venue.id,
      'name': venue.name,
      "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
    })
  response={
  "count": len(venues),
  "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>') # -----done
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()
  past_shows = []
  for show in shows:
    past_shows.append({
      'artist_id': show.artist_id,
      'artist_name': Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name).one_or_none()[0],
      "start_time": format_datetime(str(show.start_time))
    })
  shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
  upcoming_shows = []
  for show in shows:
    upcoming_shows.append({
      'artist_id': show.artist_id,
      'artist_name': Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name).one_or_none()[0],
      "start_time": format_datetime(str(show.start_time))
    })
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET']) 
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST']) # -----done
def create_venue_submissi():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  res = VenueForm(request.form)
  venue = Venue.query.filter(Venue.name == res.name.data, Venue.phone == res.phone.data).one_or_none()
  try:  
    if venue is None:
      venue = Venue(
        name = res.name.data,
        city = res.city.data,
        state = res.state.data,
        address = res.address.data,
        phone = res.phone.data,
        genres = res.genres.data,
        facebook_link = res.facebook_link.data)
      db.session.add(venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Venue ' + res.name.data + ' already exists')

  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + res.name.data + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE']) # -----done
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  shows = Show.query.filter(Show.venue_id == venue_id).all()
  for show in shows:
    try:
      db.session.delete(show)
      db.session.commit()

    except:
      db.session.rollback()
      return jsonify({
        "success": False
      })
    finally:
      db.session.close()
  
  try:  
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({
      "success": True
    })
  except:
    db.session.rollback()
    return jsonify({
      "success": False
    })
  finally:
    db.session.close()
  return jsonify({
    "message": "internal server error",
    "error": 500
  })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') # -----done
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST']) # -----done
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(
    '%{}%'.format(search_term))).all()
  data = []
  for venue in artists:
    data.append({
      'id': venue.id,
      'name': venue.name,
      "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
    })
  response={
  "count": len(artists),
  "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>') # -----done
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
  past_shows = []
  for show in shows:
    past_shows.append({
      'venue_id': show.venue_id,
      'venue_name': Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name).one_or_none()[0],
      "start_time": format_datetime(str(show.start_time))
    })
  shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
  upcoming_shows = []
  for show in shows:
    upcoming_shows.append({
      'venue_id': show.venue_id,
      'venue_name': Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name).one_or_none()[0],
      "start_time": format_datetime(str(show.start_time))
    })
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET']) # -----done
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST']) # -----done
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  updated_artist = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)
  try:
    artist = Artist.query.get(artist_id)
    artist.name = updated_artist.name.data
    artist.city = updated_artist.city.data
    artist.state = updated_artist.state.data
    artist.phone = updated_artist.phone.data
    artist.genres = updated_artist.genres.data
    artist.facebook_link = updated_artist.facebook_link.data
    db.session.commit()
    flash(f"Artist {artist.name} was successfully updated")
  except:
    db.session.rollback()
    flash("update failed")
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET']) # -----done
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST']) # -----done
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  updated_venue = VenueForm(request.form)
  try:
    venue = Venue.query.get(venue_id)
    venue.name = updated_venue.name.data
    venue.city = updated_venue.city.data
    venue.state = updated_venue.state.data
    venue.phone = updated_venue.phone.data
    venue.genres = updated_venue.genres.data
    venue.facebook_link = updated_venue.facebook_link.data
    db.session.commit()
    flash(f"Venue {venue.name} was updated successfully updated")
  except:
    db.session.rollback()
    flash("update failed")
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])    #----------done
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  res = ArtistForm(request.form)
  artist = Artist.query.filter(Artist.name == res.name.data, Artist.phone == res.phone.data).one_or_none()
  try:  
    if artist is None:
      artist = Artist(
        name = res.name.data,
        city = res.city.data,
        state = res.state.data,
        phone = res.phone.data,
        genres = res.genres.data,
        facebook_link = res.facebook_link.data)
      db.session.add(artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!') 
    else:
      flash('Artist ' + request.form['name'] + ' already exists')
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + res.name.data + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows') # -----done
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name)[0][0],
      "artist_id": show.artist_id,
      "artist_name":Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name)[0][0],
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create') # -----done
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST']) # -----done
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  res = ShowForm(request.form)
  show = Show.query.filter(Show.start_time == res.start_time.data).one_or_none()
  start_time = res.start_time.data
  venue_id = int(res.venue_id.data)
  artist_id = int(res.artist_id.data)
  try:
    if show is None:
      show = Show(
        start_time = start_time,
        venue_id = venue_id,
        artist_id = artist_id)

      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    else:
      flash('Another show was posted at that time.')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
