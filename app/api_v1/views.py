from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)
from ..models import Model, Ride, RideRequest, UserRegister


class RideOffers(Resource):
    ''' getting all the ride offers '''

    @jwt_required
    def get(self):
        ride = Ride()
        ride_offers = ride.get_all_rides()
        return ride_offers, 200


class PostRide(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('from', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('to', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('depature', type=str, required=True,
                        help='This field cannot be left blank')

    ''' creating a ride offer '''
    @jwt_required
    def post(self):
        request_data = RideOffers.parser.parse_args()

        driver_name = get_jwt_identity()
        user = UserRegister()
        current_user = user.get_user_by_username(driver_name)

        if not current_user:
            return {}, 401
        _from = request_data['from']
        to = request_data['to']
        depature = request_data['depature']

        ride_offer = Ride(current_user, _from, to, depature)
        ride_offer.add_ride()
        return {'message': 'ride offer created succesfully'}, 201


class RideOffer(Resource):
    ''' getting a specific ride offer depending on the id passed '''

    @jwt_required
    def get(self, rideId):
        ride = Ride()
        ride_offer = ride.get_ride_by_id(rideId)
        if not ride_offer:
            return abort(404)
        return ride_offer.to_dict(), 200

    @jwt_required
    def delete(self, rideId):
        ride = Ride()
        ride_dl = ride.get_ride_by_id(rideId)
        ride_dl.delete_specific_ride(rideId)

        return {'message': 'ride offer deleted successfully'}, 200


class Request(Resource):

    '''Make a request to join aride'''
    @jwt_required
    def post(self, rideId):
        ride = Ride()
        ride_rq = ride.get_ride_by_id(rideId)
        passenger_name = get_jwt_identity()
        user = UserRegister()
        current_user = user.get_user_by_username(passenger_name)
        if not current_user:
            return {'message': 'unauthorized'}, 401

        ride_request = RideRequest(current_user, ride_rq)
        ride_request.add_ride_request()

        return {'message': 'ride offer request created succesfully'}, 201


class FetchedRideRequest(Resource):

    ''' fetch requests made for a specific ride '''
    @jwt_required
    def get(self, rideId):
        ride = Ride()
        ride_rq = ride.get_ride_by_id(rideId)

        if not ride_rq:
            return {'message': 'ride request does not exist'}, 404

        ride_rqst = RideRequest()
        fetched_ride_requests = ride_rqst.get_all_ride_request()

        return fetched_ride_requests
