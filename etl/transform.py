import pandas as pd
import math
from sklearn.preprocessing import MultiLabelBinarizer

class Transformer:
    def __init__(self, base_location):
        self.base_location = base_location
        self.near_manda = [
            "United States", "Quezon City", "Caloocan", "Las Piñas", "Navotas",
            "Cavite", "Rizal", "Bulacan", "Laguna", "Muntinlupa", "Marikina",
            "Pampanga", "Batangas", "Parañaque", "Zambales", "Nueva Ecija",
            "Malabon", "Pasay", "San Pedro", "Baguio", "Filinvest"
        ]

    def haversine(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0
        return c * r

    def contains_any_keyword(self, address):
        return not any(keyword.lower() in address.lower() for keyword in self.near_manda)

    def process(self, raw_data):
        df = pd.DataFrame(raw_data)
        df = df[df['address'].apply(self.contains_any_keyword)]
        df['distance'] = df.apply(lambda x: self.haversine(self.base_location['latitude'], self.base_location['longitude'], x['latitude'], x['longitude']), axis=1)

        mlb = MultiLabelBinarizer()
        types_encoded = mlb.fit_transform(df['types'])
        types_df = pd.DataFrame(types_encoded, columns=mlb.classes_)
        exploded_final_df = df.join(types_df).drop('types', axis=1).drop_duplicates()

        grouped_df = exploded_final_df.groupby([
            'name', 'address', 'latitude', 'longitude', 
            'rating', 'user_ratings_total', 'business_status', 'distance'
        ]).max().reset_index()

        # Load additional data from Excel and join it with grouped_df
        fb_df = pd.read_excel("data/raw/fb_research.xlsx")
        # Merge DataFrames on the 'name' column or any other common column
        final_df = grouped_df.merge(fb_df, on='name', how='left')
        print(final_df)
        
        return final_df[final_df['distance'] < 3]
