import googlemaps
import logging
import time

class Extractor:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)
        self.keywords = [
            "vet clinics"] #, "veterinary services", "animal hospitals", "pet care providers",
            #"veterinary clinics", "veterinarians", "emergency vet services", "pet grooming",
            #"pet boarding", "pet shops", "pet supplies", "pet food stores", "dog grooming",
            #"cat grooming", "pet vaccination", "pet dental care", "animal clinic",
            #"exotic pet care", "pet adoption", "pet training", "pet accessories",
            #"mobile vet services", "24-hour vet clinic", "affordable vet services",
            #"holistic pet care", "pet behaviorist", "pet microchipping"]

    def fetch_places(self, query, location, radius, next_page_token=None):
        try:
            if next_page_token:
                return self.gmaps.places(query=query, location=location, radius=radius, page_token=next_page_token)
            return self.gmaps.places(query=query, location=location, radius=radius)
        except Exception as e:
            logging.error(f"Error fetching places: {e}")
            return None



    def get_all_results(self, places_result, search_query, location, radius):
        all_results = places_result['results']
        while 'next_page_token' in places_result:
            time.sleep(2)
            places_result = self.fetch_places(search_query, location, radius, places_result['next_page_token'])
            if places_result and places_result['status'] == 'OK':
                all_results.extend(places_result['results'])

        # Ensure consistent keys
        standardized_results = []
        for data in all_results:
            standardized_results.append({
                'name': data.get('name', None),
                'address': data.get('formatted_address', None),
                'latitude': data['geometry']['location'].get('lat', None),
                'longitude': data['geometry']['location'].get('lng', None),
                'rating': data.get('rating', None),
                'user_ratings_total': data.get('user_ratings_total', None),
                'weighted_ratings': data.get('rating', None)*data.get('user_ratings_total', None),
                'business_status': data.get('business_status', None),
                'types': data.get('types', [])
            })

        return standardized_results

    def fetch_all_places(self, location, radius):
        all_results = []
        for keyword in self.keywords:
            logging.info(f"Fetching places for keyword: {keyword}")
            places_result = self.fetch_places(keyword, location, radius)
            if places_result and places_result['status'] == 'OK':
                all_results.extend(self.get_all_results(places_result, keyword, location, radius))
        return all_results