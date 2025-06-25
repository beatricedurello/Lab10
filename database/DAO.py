from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllStati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM country"""

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodi(anno, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.CCode
                    FROM country c, contiguity co
                    WHERE (c.CCode = co.state1no OR c.CCode = co.state2no) 
                    AND co.year <= %s
                    GROUP BY c.CCode
                    ORDER BY c.StateNme ASC"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(idMap[row["CCode"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT co.state1no, co.state2no
                    FROM contiguity co
                    WHERE co.year <= %s
                    AND co.conttype = 1"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append((idMap[row["state1no"]], idMap[row["state2no"]]))

        cursor.close()
        conn.close()
        return result
