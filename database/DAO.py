from database.DB_connect import DBConnect
from model.location import Location


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_providers():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct Provider from nyc_wifi_hotspot_locations nwhl order by Provider """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["Provider"])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_locations(provider):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select nwhl.Location , nwhl.Latitude , nwhl.Longitude 
                    from nyc_wifi_hotspot_locations nwhl 
                    where Provider = %s
                    group by nwhl.Location 
                    order by  nwhl.Location"""
        cursor.execute(query, (provider,))
        result = []
        for row in cursor:
            result.append(Location(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_edges(provider):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select n1.Location n1loc, n2.Location n2loc, avg(n1.Latitude) n1Lat, avg(n1.Longitude) n1Long, 
        avg(n2.Latitude) n2Lat, avg(n2.Longitude) n2Long
        from nyc_wifi_hotspot_locations n1 , nyc_wifi_hotspot_locations n2 
        where n1.Provider = n2.Provider and n1.Location < n2.Location and n1.Provider = %s
        group by n1.Location , n2.Location"""
        cursor.execute(query, (provider, ))
        result = []
        for row in cursor:
            loc1 = Location(row["n1loc"], row["n1Lat"], row["n1Long"])
            loc2 = Location(row["n2loc"], row["n2Lat"], row["n2Long"])
            result.append((loc1, loc2))
        cursor.close()
        cnx.close()
        return result
