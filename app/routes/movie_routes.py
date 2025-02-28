@movie_bp.route('/movies', methods=['POST'])
@jwt_required()
def add_movie():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    movie = Movie(title=data['title'], description=data['description'], genre=data['genre'], poster_url=data.get('poster_url'))
    db.session.add(movie)
    db.session.commit()
    return jsonify({"message": "Movie added successfully"})
