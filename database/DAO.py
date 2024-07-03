from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT YEAR (s.`datetime`) as year
FROM sighting s 
        """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShape(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT s.shape 
FROM sighting s 
WHERE Year(s.`datetime`) = %s 
            """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
FROM state s 
                """

        cursor.execute(query, ())

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1 as s1, n.state2 as s2
FROM neighbor n 
WHERE n.state1 < n.state2  """

        cursor.execute(query, ())

        for row in cursor:
            result.append((idMap[row["s1"]], idMap[row["s2"]]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(n1,n2,anno,shape):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """SELECT count(*) as sum
FROM sighting s 
WHERE YEAR (s.`datetime`) = %s
and s.shape = %s
and (s.state = %s or s.state = %s  ) """

        cursor.execute(query, (anno,shape,n1.id,n2.id))

        for row in cursor:
            result = row["sum"]

        cursor.close()
        conn.close()
        return result