from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import db, User, Listing

main = Blueprint('main', __name__)

#-----------------------------------------------------------------------
# Get Users
#-----------------------------------------------------------------------
@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "telegram_id": l.telegram_id,
        "full_name": l.full_name,
        "username": l.username
    } for l in users])


#-----------------------------------------------------------------------
# Register User
#-----------------------------------------------------------------------
@main.route("/users", methods=["POST"])
def register_user():
    data = request.json
    user = User(
        telegram_id=data["telegram_id"],
        full_name=data["full_name"],
        username=data.get("username")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

#-----------------------------------------------------------------------
# List all active rentals
#-----------------------------------------------------------------------
@main.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.filter_by(status="active").all()
    return jsonify([{
         "id": listing.id,
        "title": listing.title,
        "price": listing.price,
        "region": listing.region,
        "city": listing.city,
        "bedrooms": listing.bedrooms,
        "description": listing.description,
        "image_urls": listing.image_urls,
        "contact": listing.contact,
        "status": listing.status,
        "created_at": listing.created_at
    } for listing in listings])

#-----------------------------------------------------------------------
# List all  rentals by user
#-----------------------------------------------------------------------

@main.route("/listings/user/<int:user_id>", methods=["GET"])
def get_listings_by_user(user_id):
    listings = Listing.query.filter_by(posted_by=user_id).all()
    return jsonify([{
        "id": l.id,
        "title": l.title,
        "price": l.price,
        "region": l.region,
        "city": l.city,
        "bedrooms": l.bedrooms,
        "status": l.status
    } for l in listings])


#-----------------------------------------------------------------------
# Get Listing by Id
#-----------------------------------------------------------------------

@main.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing_by_id(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return jsonify({
        "id": listing.id,
        "title": listing.title,
        "price": listing.price,
        "region": listing.region,
        "city": listing.city,
        "bedrooms": listing.bedrooms,
        "description": listing.description,
        "image_urls": listing.image_urls,
        "contact": listing.contact,
        "status": listing.status,
        "created_at": listing.created_at
    })


#-----------------------------------------------------------------------
# Search all active rentals by region,city and number of bedrooms 
#-----------------------------------------------------------------------
@main.route("/listings/search", methods=["GET"])
def search_listings():
    try:
        bedrooms = request.args.get("bedrooms", type=int)
        region = request.args.get("region", type=str)
        city = request.args.get("city", type=str)

        query = Listing.query.filter_by(status="active")
        
        if bedrooms:
            query = query.filter_by(bedrooms=bedrooms)
        if region:
            query = query.filter(Listing.region.ilike(f"%{region}%"))
        if city:
            query = query.filter(Listing.city.ilike(f"%{city}%"))

        listings = query.all()

        results = [{
            "title": l.title,
            "description":l.description,
            "price": l.price,
            "region": l.region,
            "city": l.city,
            "bedrooms": l.bedrooms,
            "image_urls" : l.image_urls,
            "contact" : l.contact
        } for l in listings]

        return jsonify(results)
    except Exception as e:        
        return jsonify({"error": "Search failed"}), 500


#-----------------------------------------------------------------------
# Add New Rental Property
#-----------------------------------------------------------------------
@main.route("/listings", methods=["POST"])
def add_listing():
    data = request.get_json()

    required_fields = ["title", "price", "bedrooms", "region", "city", "description", "image_urls", "contact"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field(s)"}), 400

    listing = Listing(
        title=data["title"],
        price=data["price"],
        bedrooms=data["bedrooms"],
        region=data["region"],
        city=data["city"],
        description=data["description"],
        image_urls=data["image_urls"],
        contact=data["contact"],
        posted_by=data.get("posted_by", "anonymous"),
        status="active",
        created_at=datetime.utcnow()
    )

    db.session.add(listing)
    db.session.commit()
    return jsonify({"message": "Listing added successfully"}), 201



#-----------------------------------------------------------------------
# Update Rental Property
#-----------------------------------------------------------------------

@main.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    data = request.get_json()

    for field in ["title", "price", "bedrooms", "region", "city", "description", "image_urls", "contact", "status"]:
        if field in data:
            setattr(listing, field, data[field])

    db.session.commit()
    return jsonify({"message": "Listing updated successfully"})


#-----------------------------------------------------------------------
# Delete Rental Property
#-----------------------------------------------------------------------

@main.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    db.session.delete(listing)
    db.session.commit()
    return jsonify({"message": "Listing deleted successfully"})
