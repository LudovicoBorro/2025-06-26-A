from database.DB_connect import DBConnect
from model.circuito import Circuito
from model.position import Position


class DAO():

    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select c.circuitId, c.circuitRef, c.name, c.location, c.country, c.lat, c.lng, c.alt, c.url
                from circuits c
        """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuito(row["circuitId"], row["circuitRef"], row["name"], row["location"], row["country"], row["lat"], row["lng"],
                                row["alt"], row["url"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select s.year
                from seasons s 
        """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPlacementsByCircuitAndYear(circuitId, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select r2.driverId, r2.`position` 
                from races r, results r2 
                where r.raceId = r2.raceId and r.circuitId = %s and r.year = %s
        """
        cursor.execute(query, (circuitId, year))

        res = []
        for row in cursor:
            res.append(Position(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(yearMin, yearMax):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select t1.circuitid as circ1, t2.circuitid as circ2, (t1.numpiloti + t2.numpiloti) as peso
                from 
                (
                    select r.circuitId, count(*) as numPiloti
                    from races r, results r2 
                    where r.raceId = r2.raceId and r.`year` >= %s and r.`year` <= %s and r2.`position` is not null
                    group by r.circuitId 
                ) as t1,
                (
                    select r.circuitId, count(*) as numPiloti
                    from races r, results r2 
                    where r.raceId = r2.raceId and r.`year` >= %s and r.`year` <= %s and r2.`position` is not null
                    group by r.circuitId 
                ) as t2
                where t1.circuitid < t2.circuitid
        """
        cursor.execute(query, (yearMin, yearMax, yearMin, yearMax))

        res = []
        for row in cursor:
            res.append((row["circ1"], row["circ2"], row["peso"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNumCorsePerCircuito(yearMin, yearMax):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select r.circuitId, count(*) as numCorse
                from races r
                where r.`year` >= %s and r.`year` <= %s
                group by r.circuitId 
        """
        cursor.execute(query, (yearMin, yearMax))

        res = []
        for row in cursor:
            res.append((row["circuitId"], row["numCorse"]))

        cursor.close()
        cnx.close()
        return res