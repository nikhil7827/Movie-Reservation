@reservation_bp.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_seat():
    data = request.json
    user = get_jwt_identity()

    showtime = Showtime.query.get(data['showtime_id'])
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    existing_reservation = Reservation.query.filter_by(showtime_id=data['showtime_id'],
                                                       seat_number=data['seat_number']).first()
    if existing_reservation:
        return jsonify({"message": "Seat already reserved"}), 400

    reservation = Reservation(user_id=user['id'], showtime_id=data['showtime_id'], seat_number=data['seat_number'])
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Seat reserved successfully"})
